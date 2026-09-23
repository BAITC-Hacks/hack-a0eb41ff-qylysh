import argparse

from app.analytics.exceptions import DatasetError
from app.analytics.features import calculate_features
from app.analytics.graph_builder import build_graph
from app.analytics.loader import load_dataset
from app.analytics.models import HACKATHON_EXPECTATIONS
from app.analytics.validator import validate_dataset


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build and check MoneyGraph node features"
    )
    parser.add_argument("--data-dir", required=True)
    args = parser.parse_args()

    try:
        dataset = load_dataset(args.data_dir)
        validate_dataset(dataset, HACKATHON_EXPECTATIONS)
        graph = build_graph(dataset)
        features = calculate_features(graph)
    except DatasetError as exc:
        print(f"Feature engineering: FAILED\n{exc}")
        return 1

    percentiles = features.filter(like="_percentile")
    print("MoneyGraph feature table")
    print(f"[OK] rows: {len(features)}")
    print(f"[OK] unique gids: {features['gid'].nunique()}")
    print(f"[OK] columns: {len(features.columns)}")
    print(
        "[OK] percentile range: "
        f"{percentiles.min().min():.6f}..{percentiles.max().max():.6f}"
    )
    print(
        "[OK] truncated depth-4 nodes: "
        f"{int(features['truncated_by_depth'].sum())}"
    )
    print("Feature engineering: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
