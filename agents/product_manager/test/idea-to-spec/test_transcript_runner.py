import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


RUNNER_PATH = (
    Path(__file__).resolve().parent / "transcript_runner.py"
)


def load_runner_module():
    spec = importlib.util.spec_from_file_location(
        "idea_to_spec_transcript_runner",
        RUNNER_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TranscriptRunnerTests(unittest.TestCase):
    def test_build_claude_command_supports_custom_entry_command(self):
        runner = load_runner_module()

        command = runner.build_claude_command(
            "我想做一个 AI 对话助手",
            with_skill=True,
            entry_command="/pm-agent",
            plugin_dir="agents/product_manager",
        )

        self.assertIn("--plugin-dir", command)
        self.assertEqual(command[-1], "/pm-agent 我想做一个 AI 对话助手")

    def test_prepare_execution_workspace_removes_reserved_and_custom_outputs(self):
        runner = load_runner_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            eval_root = Path(temp_dir) / "eval"
            exec_root = Path(temp_dir) / "exec"

            (eval_root / "with_skill/outputs").mkdir(parents=True)
            (eval_root / "without_skill/outputs").mkdir(parents=True)
            (eval_root / "docs/input").mkdir(parents=True)
            (eval_root / "with_skill/outputs/transcript.md").write_text("old")
            (eval_root / "without_skill/outputs/transcript.md").write_text("old")
            (eval_root / "comparison.auto.md").write_text("stale")
            (eval_root / "PRD.md").write_text("stale-prd")
            (eval_root / "docs/input/fixture.md").write_text("fixture")
            (eval_root / "README.md").write_text("readme")

            runner.prepare_execution_workspace(
                eval_root,
                exec_root,
                cleanup_paths=["PRD.md"],
            )

            self.assertTrue((exec_root / "README.md").exists())
            self.assertTrue((exec_root / "docs/input/fixture.md").exists())
            self.assertFalse((exec_root / "with_skill").exists())
            self.assertFalse((exec_root / "without_skill").exists())
            self.assertFalse((exec_root / "comparison.auto.md").exists())
            self.assertFalse((exec_root / "PRD.md").exists())

    def test_extract_result_text_reads_json_payload(self):
        runner = load_runner_module()

        payload = json.dumps(
            {
                "type": "result",
                "subtype": "success",
                "result": "structured transcript",
            },
            ensure_ascii=False,
        )

        self.assertEqual(
            runner.extract_result_text(payload),
            "structured transcript",
        )

    def test_sync_declared_outputs_copies_existing_candidates(self):
        runner = load_runner_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            exec_root = Path(temp_dir) / "exec"
            eval_root = Path(temp_dir) / "eval"

            (exec_root / "with_skill/outputs").mkdir(parents=True)
            (exec_root / "docs/pm/feature").mkdir(parents=True)
            (eval_root / "with_skill/outputs").mkdir(parents=True)
            (eval_root / "docs/pm/feature").mkdir(parents=True)

            (exec_root / "with_skill/outputs/transcript.md").write_text("fresh")
            (exec_root / "docs/pm/feature/PRD.md").write_text("prd")

            runner.sync_declared_outputs(
                exec_root,
                eval_root,
                [
                    "with_skill/outputs/transcript.md",
                    ["docs/pm/feature/design.md", "docs/pm/feature/PRD.md"],
                ],
            )

            self.assertEqual(
                (eval_root / "with_skill/outputs/transcript.md").read_text(),
                "fresh",
            )
            self.assertEqual(
                (eval_root / "docs/pm/feature/PRD.md").read_text(),
                "prd",
            )
            self.assertFalse((eval_root / "docs/pm/feature/design.md").exists())


if __name__ == "__main__":
    unittest.main()
