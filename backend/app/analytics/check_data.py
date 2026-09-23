import argparse

from app.analytics.exceptions import DatasetError
from app.analytics.loader import load_dataset
from app.analytics.models import HACKATHON_EXPECTATIONS
from app.analytics.validator import validate_dataset


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the MoneyGraph hackathon parquet dataset")
    parser.add_argument("--data-dir", required=True, help="Directory containing the three parquet files")
    args = parser.parse_args()

    print("MoneyGraph dataset validation")
    try:
        dataset = load_dataset(args.data_dir)
        validate_dataset(dataset, HACKATHON_EXPECTATIONS)
    except DatasetError as exc:
        print(f"Dataset validation: FAILED\n{exc}")
        return 1

    print(f"[OK] nodes loaded: {len(dataset.nodes)}")
    print(f"[OK] edges loaded: {len(dataset.edges)}")
    print(f"[OK] transactions loaded: {len(dataset.transactions)}")
    print(f"[OK] seed nodes: {int(dataset.nodes['is_seed'].sum())}")
    print("[OK] schema validation passed")
    print("[OK] cross-table validation passed")
    print("Dataset validation: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
