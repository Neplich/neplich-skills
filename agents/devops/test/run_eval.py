#!/usr/bin/env python3

import json
import sys
from pathlib import Path


def load_metadata(path: Path) -> dict:
    return json.loads(path.read_text())


def check_outputs(root: Path, outputs: list) -> list[tuple[str, bool]]:
    results = []
    for item in outputs:
        if isinstance(item, str):
            target = root / item
            ok = target.exists() and (target.is_dir() or target.stat().st_size > 0)
            results.append((item, ok))
            continue

        if isinstance(item, list):
            checks = []
            for rel in item:
                target = root / rel
                ok = target.exists() and (target.is_dir() or target.stat().st_size > 0)
                checks.append((rel, ok))
            label = " OR ".join(rel for rel, _ in checks)
            results.append((label, any(ok for _, ok in checks)))
            continue

        raise TypeError(f"Unsupported output spec: {item!r}")
    return results


def read_target(root: Path, target_spec) -> str:
    if isinstance(target_spec, str):
        path = root / target_spec
        if not path.exists() or path.is_dir():
            return ""
        return path.read_text()

    if isinstance(target_spec, list):
        return "\n\n".join(
            chunk for chunk in (read_target(root, item) for item in target_spec) if chunk
        )

    raise TypeError(f"Unsupported target spec: {target_spec!r}")


def evaluate_assertion(root: Path, assertion: dict) -> dict:
    target = assertion.get("target", "with_skill/outputs/transcript.md")
    text = read_target(root, target)

    failures = []

    for item in assertion.get("all_of", []):
        if item not in text:
            failures.append(f"Missing required text: {item}")

    any_of = assertion.get("any_of", [])
    if any_of and not any(item in text for item in any_of):
        failures.append(f"Missing any-of text: {any_of}")

    for item in assertion.get("none_of", []):
        if item in text:
            failures.append(f"Found forbidden text: {item}")

    for item in assertion.get("count_at_least", []):
        actual = text.count(item["text"])
        if actual < item["count"]:
            failures.append(
                f"'{item['text']}' count {actual} < required {item['count']}"
            )

    return {
        "id": assertion["id"],
        "description": assertion["description"],
        "status": "PASS" if not failures else "FAIL",
        "details": "; ".join(failures) if failures else "All checks passed",
    }


def render_report(meta: dict, with_results, without_results, assertion_results) -> str:
    lines = [
        f"# Eval {meta['eval_id']}: {meta['eval_name']}",
        "",
        "## Prompt",
        "",
        meta["prompt"],
        "",
        "## Output Presence Check",
        "",
        "### With Skill",
        "",
    ]

    for rel, ok in with_results:
        lines.append(f"- [{'PASS' if ok else 'FAIL'}] `{rel}`")

    lines.extend(["", "### Without Skill", ""])

    for rel, ok in without_results:
        lines.append(f"- [{'PASS' if ok else 'FAIL'}] `{rel}`")

    lines.extend(["", "## Assertion Checks", ""])

    for result in assertion_results:
        lines.append(
            f"- [{result['status']}] `{result['id']}`: {result['description']}"
        )
        lines.append(f"  - {result['details']}")

    lines.extend(["", "## Notes", "", "- Fill in qualitative comparison if needed."])
    return "\n".join(lines) + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: run_eval.py <path-to-eval_metadata.json>")
        return 2

    metadata_path = Path(sys.argv[1]).resolve()
    root = metadata_path.parent
    meta = load_metadata(metadata_path)

    with_results = check_outputs(root, meta.get("with_skill_outputs", []))
    without_results = check_outputs(root, meta.get("without_skill_outputs", []))
    assertion_results = [
        evaluate_assertion(root, assertion) for assertion in meta.get("assertions", [])
    ]

    report_path = root / "comparison.auto.md"
    report_path.write_text(
        render_report(meta, with_results, without_results, assertion_results)
    )

    failed = any(not ok for _, ok in with_results + without_results) or any(
        result["status"] == "FAIL" for result in assertion_results
    )
    print(report_path)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
