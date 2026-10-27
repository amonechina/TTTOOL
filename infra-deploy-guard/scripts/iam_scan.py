#!/usr/bin/env python3
"""iam_scan.py — static least-privilege / wildcard / secret scanner.

Scans Terraform (.tf), CloudFormation (JSON/YAML), and standalone IAM policy
JSON for high-risk patterns:

  R1  IAM Allow statements with wildcard Action
  R2  IAM Allow statements with wildcard Resource
  R3  Trust policies with Principal "*" lacking a Condition block
  R4  Public ingress: 0.0.0.0/0 or ::/0 on admin ports (22, 3389)
  R5  Public-read storage (public-read ACL / public-access blocks disabled
      without restriction)
  R6  Hardcoded secrets: AWS access keys, private key blocks, password=
      literals

This is a static heuristic scanner — a clean result is not a security
certification. Findings are starting points for review.

Usage:
    python iam_scan.py <file-or-directory> [--format text|json] [--fail-on high]

Exit codes: 0 = no findings at or above threshold, 1 = findings found,
            2 = usage/IO error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ADMIN_PORTS = {"22", "3389"}
SECRET_PATTERNS = [
    ("R6", r"AKIA[0-9A-Z]{16}", "AWS access key id", "high"),
    ("R6", r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----", "private key block", "high"),
    ("R6", r"(?i)\b(?:password|passwd|secret|token)\s*[=:]\s*[\"'][^\"']{6,}[\"']", "hardcoded password/secret literal", "high"),
    ("R6", r"(?i)\baws_secret_access_key\s*[=:]\s*[\"'][0-9a-zA-Z/+]{40}[\"']", "AWS secret access key", "high"),
]
TF_ACTION_WILDCARD = re.compile(r"^\s*actions?\s*=\s*\[[^\]]*\"(\*|[\w-]+:\*)", re.M)
INGRESS_CIDR = re.compile(
    r"\"\s*(?:C|c)idr(?:_ip|_blocks|)\"\s*:\s*[\"'\[]?\s*[\"\[]?(0\.0\.0\.0/0|::/0)",
)
TF_INGRESS_CIDR = re.compile(r"cidr_blocks\s*=\s*\"(0\.0\.0\.0/0|::/0)\"")
PORT = re.compile(r"(?:from_port|to_port)\s*=\s*(\d+)|\"\s*(?:F|f)rom(?:_port|Port)\"\s*:\s*\"?(\d+)")
PUBLIC_READ = re.compile(r"(?i)acl\s*=\s*\"public-read\"|\"\s*(?:A|a)cl\"\s*:\s*\"public-read\"")


def file_score(text: str) -> list[dict]:
    findings: list[dict] = []

    # R1/R2: wildcards in statements (crude statement segmentation)
    for stmt_m in re.finditer(r"\{[^{}]*?\"Effect\"\s*:\s*\"Allow\"[^{}]*?\}", text, re.S):
        stmt = stmt_m.group(0)
        if re.search(r"\"Action\"\s*:\s*\[[^\]]*\"(\*|[\w-]+:\*)\"", stmt, re.S):
            findings.append(("R1", "high", "Allow statement with wildcard Action"))
        if re.search(r"\"Resource\"\s*:\s*\"\*\"", stmt) and "GetCallerIdentity" not in stmt:
            findings.append(("R2", "high", "Allow statement with wildcard Resource"))
        if "\"Principal\": \"*\"" in stmt and "Condition" not in stmt:
            findings.append(("R3", "high", 'Principal "*" without Condition block'))

    # HCL / jsonencode variants (Action = "*", Effect = "Allow")
    for stmt_m in re.finditer(r"\{[^{}]*?Effect\s*=\s*\"Allow\"[^{}]*?\}", text, re.S):
        stmt = stmt_m.group(0)
        if re.search(r"Action\s*=\s*\"(\*|[\w-]+:\*)\"", stmt):
            findings.append(("R1", "high", "HCL Allow statement with wildcard Action"))
        if re.search(r"Resource\s*=\s*\"\*\"", stmt) and "GetCallerIdentity" not in stmt:
            findings.append(("R2", "high", "HCL Allow statement with wildcard Resource"))

    # Terraform data-block variants
    if TF_ACTION_WILDCARD.search(text):
        findings.append(("R1", "high", "Terraform policy actions contain wildcard"))
    if re.search(r"resources\s*=\s*\[\"\*\"\]", text):
        findings.append(("R2", "high", "Terraform policy resource is \"*\""))

    # R4: open admin ports (pair CIDR with nearby from_port)
    for cidr in list(INGRESS_CIDR.finditer(text)) + list(TF_INGRESS_CIDR.finditer(text)):
        window = text[max(0, cidr.start() - 400): cidr.end() + 400]
        ports = {a or b for a, b in PORT.findall(window)}
        if ports & ADMIN_PORTS:
            findings.append(("R4", "high", f"admin port open to 0.0.0.0/0 ({cidr.group(1)})"))
        elif ports:
            findings.append(("R4", "medium", f"service port open to 0.0.0.0/0 ({cidr.group(1)})"))

    # R5: public-read storage
    if PUBLIC_READ.search(text):
        findings.append(("R5", "high", "public-read ACL on storage"))

    # R6: secrets
    for rule, pattern, label, sev in SECRET_PATTERNS:
        for m in re.finditer(pattern, text):
            snippet = m.group(0)
            if len(snippet) > 48:
                snippet = snippet[:24] + "…[redacted]…" + snippet[-8:]
            findings.append((rule, sev, f"{label}: {snippet}"))

    # R6b: Terraform variable blocks named like secrets with a literal default
    for var_m in re.finditer(
        r"variable\s+\"([^\"]*)\"\s*\{([^{}]*)\}", text
    ):
        name, body = var_m.group(1), var_m.group(2)
        if re.search(r"(?i)password|passwd|secret|token|api[_-]?key", name):
            if re.search(r"(?i)\bdefault\s*=\s*\"[^\"]{4,}\"", body):
                findings.append(("R6", "high", f"Terraform variable '{name}' has a hardcoded default value"))

    return findings


SCAN_EXTENSIONS = {".tf", ".json", ".yaml", ".yml"}


def main() -> int:
    global _  # noqa
    ap = argparse.ArgumentParser(description="Static least-privilege/secrets scanner for IaC")
    ap.add_argument("target", help="file or directory to scan")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--fail-on", choices=["high", "medium", "any"], default="high")
    args = ap.parse_args()

    root = Path(args.target)
    if not root.exists():
        print(f"error: not found: {root}")
        return 2
    files = [root] if root.is_file() else sorted(
        p for p in root.rglob("*") if p.suffix.lower() in SCAN_EXTENSIONS and p.is_file()
    )
    if not files:
        print("no scannable files (.tf/.json/.yaml/.yml)")
        return 0

    results = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"error reading {f}: {exc}")
            return 2
        for rule, sev, msg in file_score(text):
            results.append({"file": str(f), "rule": rule, "severity": sev, "message": msg})

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        if not results:
            print("✅ no findings")
        for r in results:
            print(f"[{r['severity'].upper():6}] {r['rule']}  {r['file']}\n        {r['message']}")
        print(f"\n{len(results)} finding(s). A clean scan is not a certification — review before apply.")

    threshold = {"any": 0, "medium": 1, "high": 2}[args.fail_on]
    return 1 if any({"any": 0, "medium": 1, "high": 2}[s] >= threshold for r in results for s in [r["severity"]]) else 0


if __name__ == "__main__":
    sys.exit(main())
