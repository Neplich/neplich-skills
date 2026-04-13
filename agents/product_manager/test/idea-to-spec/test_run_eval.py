import importlib.util
import tempfile
import unittest
from pathlib import Path


RUN_EVAL_PATH = Path(__file__).resolve().parent / "run_eval.py"


def load_run_eval_module():
    import sys

    run_eval_dir = str(RUN_EVAL_PATH.parent)
    if run_eval_dir not in sys.path:
        sys.path.insert(0, run_eval_dir)

    spec = importlib.util.spec_from_file_location(
        "idea_to_spec_run_eval",
        RUN_EVAL_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RunEvalTests(unittest.TestCase):
    def test_evaluate_assertion_supports_all_of_any_groups(self):
        run_eval = load_run_eval_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            transcript = root / "with_skill/outputs/transcript.md"
            transcript.parent.mkdir(parents=True)
            transcript.write_text(
                "\n".join(
                    [
                        "项目上下文摘要",
                        "- **状态**: empty workspace",
                        "- **建议车道**: `greenfield-discovery`",
                    ]
                )
            )

            result = run_eval.evaluate_assertion(
                root,
                {
                    "id": "pm_first_lane",
                    "description": "Allows localized PM-first lane labels",
                    "all_of_any": [
                        ["Project context:", "项目上下文摘要"],
                        ["Suggested lane", "建议车道"],
                        ["greenfield-bootstrap", "greenfield-discovery"],
                    ],
                },
            )

            self.assertEqual(result["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
