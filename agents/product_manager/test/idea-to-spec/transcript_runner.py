#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


RESERVED_CLEANUP_PATHS = (
    "with_skill",
    "without_skill",
    "comparison.auto.md",
    "comparison.md",
)

DEFAULT_TIMEOUT_SECONDS = 180


class TranscriptRunError(RuntimeError):
    def __init__(self, message: str, status: dict):
        super().__init__(message)
        self.status = status


def load_metadata(path: Path) -> dict:
    return json.loads(path.read_text())


def remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def prepare_execution_workspace(
    eval_root: Path,
    execution_root: Path,
    cleanup_paths: list[str] | None = None,
) -> None:
    if execution_root.exists():
        shutil.rmtree(execution_root)

    shutil.copytree(eval_root, execution_root)

    for rel in RESERVED_CLEANUP_PATHS:
        remove_path(execution_root / rel)

    for rel in cleanup_paths or []:
        remove_path(execution_root / rel)


def extract_result_text(stdout: str) -> str:
    if not stdout.strip():
        raise ValueError("Claude returned empty stdout")

    payload = json.loads(stdout)
    if payload.get("is_error"):
        raise ValueError(payload.get("result") or "Claude returned an error payload")

    result = payload.get("result")
    if not isinstance(result, str) or not result.strip():
        raise ValueError("Claude JSON payload does not contain a non-empty result")

    return result


def iter_output_paths(outputs: list) -> list[str]:
    paths = []
    for item in outputs:
        if isinstance(item, str):
            paths.append(item)
            continue
        if isinstance(item, list):
            paths.extend(iter_output_paths(item))
            continue
        raise TypeError(f"Unsupported output spec: {item!r}")
    return paths


def copy_path(source: Path, destination: Path) -> None:
    if source.is_dir():
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def sync_declared_outputs(execution_root: Path, eval_root: Path, outputs: list) -> None:
    for rel in iter_output_paths(outputs):
        source = execution_root / rel
        if not source.exists():
            continue
        copy_path(source, eval_root / rel)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def build_claude_command(
    prompt: str,
    *,
    with_skill: bool,
    entry_command: str = "/idea-to-spec",
    plugin_dir: str = "agents/product_manager",
) -> list[str]:
    command = [
        "claude",
        "-p",
        "--no-session-persistence",
        "--permission-mode",
        "bypassPermissions",
        "--output-format",
        "json",
    ]

    if with_skill:
        plugin_root = Path(plugin_dir)
        if not plugin_root.is_absolute():
            plugin_root = repo_root() / plugin_root

        normalized_entry = entry_command.strip()
        if not normalized_entry.startswith("/"):
            normalized_entry = f"/{normalized_entry}"

        command.extend(["--plugin-dir", str(plugin_root)])
        command.append(f"{normalized_entry} {prompt}")
        return command

    command.append(prompt)
    return command


def run_claude(command: list[str], cwd: Path, timeout_seconds: int) -> tuple[str, dict]:
    started = time.time()
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        status = {
            "command": command,
            "cwd": str(cwd),
            "timeout": True,
            "returncode": None,
            "stdout_length": len(exc.stdout or ""),
            "stderr": exc.stderr or "",
            "duration_ms": int((time.time() - started) * 1000),
        }
        raise TranscriptRunError("Claude command timed out", status) from exc

    status = {
        "command": command,
        "cwd": str(cwd),
        "timeout": False,
        "returncode": completed.returncode,
        "stdout_length": len(completed.stdout),
        "stderr": completed.stderr,
        "duration_ms": int((time.time() - started) * 1000),
    }

    if completed.returncode != 0:
        raise TranscriptRunError("Claude command failed", status)

    try:
        result_text = extract_result_text(completed.stdout)
    except Exception as exc:  # noqa: BLE001
        raise TranscriptRunError(str(exc), status) from exc

    status["result_length"] = len(result_text)
    return result_text, status


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def write_status(path: Path, status: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n")


def generate_eval_outputs(
    metadata_path: Path,
    *,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> list[dict]:
    metadata_path = metadata_path.resolve()
    eval_root = metadata_path.parent
    meta = load_metadata(metadata_path)
    cleanup_paths = meta.get("execution_cleanup", [])
    statuses = []

    with tempfile.TemporaryDirectory(prefix="idea-to-spec-eval-") as temp_dir:
        execution_root = Path(temp_dir) / "workspace"
        prepare_execution_workspace(eval_root, execution_root, cleanup_paths=cleanup_paths)

        runs = [
            ("with_skill", meta.get("with_skill_outputs", []), True),
            ("without_skill", meta.get("without_skill_outputs", []), False),
        ]

        for label, outputs, with_skill in runs:
            command = build_claude_command(
                meta["prompt"],
                with_skill=with_skill,
                entry_command=meta.get("entry_command", "/idea-to-spec"),
                plugin_dir=meta.get("plugin_dir", "agents/product_manager"),
            )
            transcript_path = execution_root / label / "outputs/transcript.md"
            status_path = execution_root / label / "outputs/run_status.json"

            try:
                transcript, status = run_claude(
                    command,
                    execution_root,
                    timeout_seconds,
                )
            except TranscriptRunError as exc:
                status = exc.status
            else:
                write_text(transcript_path, transcript)

            write_status(status_path, status)
            sync_declared_outputs(execution_root, eval_root, outputs)
            copy_path(status_path, eval_root / label / "outputs/run_status.json")
            statuses.append({"label": label, **status})

    return statuses
