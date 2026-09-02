"""Build portable, metadata-only indexes for the Klyp agency graph and mentor RAG."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "knowledge-federation"


def load_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unreadable JSON: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"Expected a JSON object: {path}")
    return payload


def graph_summary(agency_root: Path) -> dict:
    graph_path = agency_root / "graphify-out" / "graph.json"
    report_path = agency_root / "graphify-out" / "GRAPH_REPORT.md"
    graph = load_json(graph_path)
    nodes = graph.get("nodes", [])
    links = graph.get("links", [])
    communities = {node.get("community") for node in nodes if node.get("community") is not None}
    # Derive hubs from graph structure, rather than parsing Markdown bullets in
    # the report (which also contains unrelated statistics and conclusions).
    degree: Counter[str] = Counter()
    for link in links:
        source = link.get("source", link.get("from"))
        target = link.get("target", link.get("to"))
        if source is not None:
            degree[str(source)] += 1
        if target is not None:
            degree[str(target)] += 1
    labels = {
        str(node.get("id")): str(node.get("label") or node.get("title") or node.get("id"))
        for node in nodes
        if node.get("id") is not None
    }
    hubs = [
        {"label": labels.get(node_id, node_id), "degree": node_degree}
        for node_id, node_degree in degree.most_common(10)
    ]
    return {
        "canonical_repository": "ProgramadorAlpha/Klyp-Agencia_marketing-IA",
        "source_root_env": "KLYP_AGENCY_ROOT",
        "graph_relative_path": "graphify-out/graph.json",
        "report_relative_path": "graphify-out/GRAPH_REPORT.md",
        "snapshot": {
            "nodes": len(nodes),
            "links": len(links),
            "communities": len(communities),
            "top_hubs": hubs[:10],
        },
        "routing": {
            "use_for": ["services", "clients", "campaigns", "funnels", "offers", "marketing operations"],
            "do_not_use_for": ["mentor evidence", "Jarvis implementation details", "secrets"],
        },
    }


def mentor_catalog(mentor_root: Path, vector_chunks: int | None) -> dict:
    people: dict[str, dict] = {}
    source_counts: Counter[str] = Counter()
    language_counts: Counter[str] = Counter()
    missing_vector_evidence = 0
    metadata_files = sorted(mentor_root.rglob("metadata.json"))
    for metadata_path in metadata_files:
        data = load_json(metadata_path)
        mentor = str(data.get("mentor") or metadata_path.relative_to(mentor_root).parts[0]).strip()
        entry = people.setdefault(
            mentor,
            {"mentor": mentor, "videos": 0, "books": 0, "languages": Counter(), "channels": Counter()},
        )
        source = str(data.get("fuente") or ("libro" if "libro_id" in data else "video"))
        source_counts[source] += 1
        if source == "libro":
            entry["books"] += 1
        else:
            entry["videos"] += 1
        language = data.get("idioma")
        if language:
            entry["languages"][str(language)] += 1
            language_counts[str(language)] += 1
        channel = data.get("canal")
        if channel:
            entry["channels"][str(channel)] += 1
        if "NO entra todavia al indice vectorial" in str(data.get("nota_procedencia", "")):
            missing_vector_evidence += 1

    mentors = []
    for mentor, entry in sorted(people.items()):
        mentors.append(
            {
                "mentor": mentor,
                "videos": entry["videos"],
                "books": entry["books"],
                "languages": dict(sorted(entry["languages"].items())),
                "channels": [channel for channel, _ in entry["channels"].most_common(3)],
            }
        )

    catalog = {
        "source_root_env": "MENTOR_RAG_ROOT",
        "query_contract": {
            "tool": "herramientas/consultar.py",
            "requires_citation": ["mentor", "title", "url", "time_or_page"],
            "metadata_is_not_evidence": True,
        },
        "coverage": {
            "mentor_folders": len([p for p in mentor_root.iterdir() if p.is_dir()]),
            "metadata_records": len(metadata_files),
            "transcripts": sum(1 for _ in mentor_root.rglob("transcripcion.md")),
            "books": sum(1 for _ in mentor_root.rglob("texto.md")),
            "sources": dict(sorted(source_counts.items())),
            "languages": dict(sorted(language_counts.items())),
            "vector_chunks": vector_chunks,
            "manual_only_records": missing_vector_evidence,
        },
        "mentors": mentors,
        "routing": {
            "use_for": ["evidence retrieval", "strategy references", "playbook research"],
            "do_not_use_for": ["uncited claims", "raw transcript syncing", "production secrets"],
        },
    }
    return catalog


def executive_map() -> dict:
    return {
        "schema_version": 1,
        "nodes": [
            {"id": "jarvis_predator", "label": "Jarvis Predator", "kind": "local_control"},
            {"id": "klyp_agency", "label": "Klyp Agencia", "kind": "marketing_operation"},
            {"id": "mentor_rag", "label": "Mentor RAG", "kind": "evidence_retrieval"},
            {"id": "cortana_hermes", "label": "Cortana / Hermes", "kind": "vps_execution"},
            {"id": "social_execution", "label": "Social marketing execution", "kind": "planned_workflow"},
        ],
        "links": [
            {"source": "jarvis_predator", "target": "cortana_hermes", "relation": "coordinates", "state": "active"},
            {"source": "klyp_agency", "target": "mentor_rag", "relation": "uses_evidence_from", "state": "active"},
            {"source": "klyp_agency", "target": "social_execution", "relation": "defines_strategy_for", "state": "planned"},
            {"source": "cortana_hermes", "target": "social_execution", "relation": "will_execute", "state": "planned"},
            {"source": "jarvis_predator", "target": "klyp_agency", "relation": "provides_local_observability_for", "state": "planned"},
        ],
        "interpretation": "Active describes currently available knowledge/control surfaces. Planned requires implementation evidence before it can be treated as production capability.",
    }


def write_json(name: str, payload: dict, generated_at: str) -> None:
    payload = {"generated_at": generated_at, **payload}
    (OUTPUT / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agency-root", type=Path, required=True)
    parser.add_argument("--mentor-root", type=Path, required=True)
    parser.add_argument("--vector-chunks", type=int)
    args = parser.parse_args()

    if not (args.agency_root / "graphify-out" / "graph.json").is_file():
        raise SystemExit("The Klyp agency graph is missing.")
    if not args.mentor_root.is_dir():
        raise SystemExit("The mentor source root is missing.")

    OUTPUT.mkdir(exist_ok=True)
    generated_at = datetime.now(timezone.utc).isoformat()
    write_json("klyp-agency-index.json", graph_summary(args.agency_root), generated_at)
    write_json("mentor-rag-catalog.json", mentor_catalog(args.mentor_root, args.vector_chunks), generated_at)
    write_json("executive-map.json", executive_map(), generated_at)
    print("federation indexes written to knowledge-federation/")


if __name__ == "__main__":
    main()
