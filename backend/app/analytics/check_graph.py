import argparse

import networkx as nx

from app.analytics.exceptions import DatasetError
from app.analytics.graph_builder import build_graph
from app.analytics.loader import load_dataset
from app.analytics.models import HACKATHON_EXPECTATIONS
from app.analytics.validator import validate_dataset


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate MoneyGraph data and build the canonical directed graph"
    )
    parser.add_argument("--data-dir", required=True)
    args = parser.parse_args()

    try:
        dataset = load_dataset(args.data_dir)
        validate_dataset(dataset, HACKATHON_EXPECTATIONS)
        graph = build_graph(dataset)
    except DatasetError as exc:
        print(f"Graph construction: FAILED\n{exc}")
        return 1

    seed_count = sum(
        bool(attributes["is_seed"]) for _, attributes in graph.nodes(data=True)
    )
    print("MoneyGraph directed graph")
    print(f"[OK] nodes: {graph.number_of_nodes()}")
    print(f"[OK] edges: {graph.number_of_edges()}")
    print(f"[OK] seed nodes: {seed_count}")
    print(f"[OK] isolated nodes retained: {len(list(nx.isolates(graph)))}")
    print("Graph construction: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
