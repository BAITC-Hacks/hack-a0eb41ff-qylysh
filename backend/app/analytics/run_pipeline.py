import argparse
from pathlib import Path

from app.analytics.exceptions import DatasetError
from app.analytics.pipeline import run_analysis
from app.db.snapshot import write_snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the MoneyGraph analytical snapshot")
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--database", default="analysis.db")
    parser.add_argument("--out-dir", default="out")
    args = parser.parse_args()
    try:
        snapshot = run_analysis(args.data_dir)
        write_snapshot(snapshot, Path(args.database), Path(args.out_dir))
    except (DatasetError, OSError) as exc:
        print(f"Analysis pipeline: FAILED\n{exc}")
        return 1
    print(f"[OK] nodes: {len(snapshot.nodes)}")
    print(f"[OK] edges: {len(snapshot.dataset.edges)}")
    print(f"[OK] clusters: {len(snapshot.clusters)}")
    print(f"[OK] ranked nodes: {len(snapshot.ranking)}")
    print("Analysis pipeline: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
