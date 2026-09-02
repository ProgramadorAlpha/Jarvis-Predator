"""Validate portable knowledge-federation metadata without requiring source corpora."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
FEDERATION = ROOT / "knowledge-federation"
REQUIRED = ("klyp-agency-index.json", "mentor-rag-catalog.json", "executive-map.json")


def fail(message: str) -> None:
    print(f"federation validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(name: str) -> dict:
    path = FEDERATION / name
    if not path.is_file():
        fail(f"missing {name}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid {name}: {exc}")


agency, mentors, executive = (load(name) for name in REQUIRED)
if agency.get("canonical_repository") != "ProgramadorAlpha/Klyp-Agencia_marketing-IA":
    fail("Klyp canonical repository is missing or changed")
if agency.get("snapshot", {}).get("nodes", 0) < 1:
    fail("Klyp snapshot has no nodes")
if mentors.get("coverage", {}).get("metadata_records", 0) < 1:
    fail("mentor catalogue has no metadata")
if mentors.get("query_contract", {}).get("metadata_is_not_evidence") is not True:
    fail("mentor evidence contract is missing")
node_ids = {node.get("id") for node in executive.get("nodes", [])}
for link in executive.get("links", []):
    if link.get("source") not in node_ids or link.get("target") not in node_ids:
        fail("executive map has a dangling link")
    if link.get("state") not in {"active", "planned"}:
        fail("executive map link has no declared state")

print(f"federation validation passed: {len(node_ids)} domains, {len(executive.get('links', []))} links")
