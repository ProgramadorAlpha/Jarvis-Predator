"""Fail fast when the shared Graphify snapshot is malformed or incomplete."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "graphify-out" / "graph.json"
REPORT = ROOT / "graphify-out" / "GRAPH_REPORT.md"
MANIFEST = ROOT / "graphify-out" / "manifest.json"


def fail(message: str) -> None:
    print(f"graph validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


for artifact in (GRAPH, REPORT, MANIFEST):
    if not artifact.is_file():
        fail(f"missing required artifact: {artifact.relative_to(ROOT)}")

try:
    payload = json.loads(GRAPH.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as exc:
    fail(f"graph.json is unreadable: {exc}")

nodes = payload.get("nodes")
links = payload.get("links")
if not isinstance(nodes, list) or not nodes:
    fail("graph.json has no nodes")
if not isinstance(links, list) or not links:
    fail("graph.json has no links")

node_ids = {node.get("id") for node in nodes if node.get("id")}
if len(node_ids) != len(nodes):
    fail("node IDs are missing or duplicated")

for index, link in enumerate(links):
    if link.get("source") not in node_ids or link.get("target") not in node_ids:
        fail(f"dangling link at index {index}")
    if not link.get("relation") or not link.get("source_file"):
        fail(f"link at index {index} lacks relation or provenance")

print(f"graph validation passed: {len(nodes)} nodes, {len(links)} links")
