import argparse

from app.analytics.exceptions import DatasetError
from app.analytics.features import calculate_features
from app.analytics.graph_builder import build_graph
from app.analytics.loader import load_dataset
from app.analytics.models import HACKATHON_EXPECTATIONS
from app.analytics.roles import assign_roles
from app.analytics.validator import validate_dataset


def main() -> int:
    parser = argparse.ArgumentParser(description="Assign and inspect MoneyGraph roles")
    parser.add_argument("--data-dir", required=True)
    args = parser.parse_args()

    try:
        dataset = load_dataset(args.data_dir)
        validate_dataset(dataset, HACKATHON_EXPECTATIONS)
        features = calculate_features(build_graph(dataset))
        roles = assign_roles(features)
    except DatasetError as exc:
        print(f"Role assignment: FAILED\n{exc}")
        return 1

    print("MoneyGraph role assignment")
    print(f"[OK] classified nodes: {len(roles)}")
    for role, count in roles["role"].value_counts().sort_index().items():
        print(f"[OK] {role}: {count}")
    print("Role assignment: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
