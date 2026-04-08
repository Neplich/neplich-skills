#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


def find_eval_metadata(root: Path) -> list[Path]:
    return sorted(root.rglob("eval_metadata.json"))


def main() -> int:
    test_root = Path(__file__).resolve().parent
    targets = [Path(arg).resolve() for arg in sys.argv[1:]] or find_eval_metadata(test_root)

    if not targets:
        print("No eval_metadata.json files found under agents/designer/test")
        return 2

    run_eval = test_root / "run_eval.py"
    failures = []

    for metadata_path in targets:
        print(
            f"==> Running {metadata_path.relative_to(test_root.parent.parent.parent)}",
            flush=True,
        )
        result = subprocess.run([sys.executable, str(run_eval), str(metadata_path)])
        if result.returncode != 0:
            failures.append(metadata_path)

    print("")
    print(f"Ran {len(targets)} eval(s)")

    if failures:
        print(f"Failures: {len(failures)}")
        for path in failures:
            print(f"- {path.relative_to(test_root.parent.parent.parent)}")
        return 1

    print("All designer evals passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
