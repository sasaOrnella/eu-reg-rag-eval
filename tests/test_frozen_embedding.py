import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

from src import run_retrieval_eval as runner
from src.dense import describe_snapshot, file_sha256


def test_snapshot_records_revision_and_detects_tokenizer_changes(tmp_path):
    snapshot = tmp_path / "snapshots" / ("a" * 40)
    snapshot.mkdir(parents=True)
    blob = tmp_path / "blob"
    blob.write_bytes(b"weights")
    (snapshot / "model.safetensors").symlink_to(blob)
    tokenizer = snapshot / "tokenizer.json"
    tokenizer.write_text("first")
    original = describe_snapshot(snapshot)
    assert original["revision"] == "a" * 40
    assert original["file_sha256"]["model.safetensors"] == file_sha256(blob)
    tokenizer.write_text("second")
    assert describe_snapshot(snapshot)["snapshot_sha256"] != original["snapshot_sha256"]


def test_dev_runner_writes_verified_local_embedding_metadata(tmp_path, monkeypatch):
    snapshot = tmp_path / "model"
    snapshot.mkdir()
    (snapshot / "config.json").write_text("{}")
    digest = describe_snapshot(snapshot)["snapshot_sha256"]
    out = tmp_path / "result.csv"
    local_loads = []
    def load_snapshot(path, *, local_files_only):
        local_loads.append((path, local_files_only))
        return SimpleNamespace(model_name=path, max_seq_length=512, library_version="test")
    monkeypatch.setattr(runner, "load_sentence_transformer", load_snapshot)
    monkeypatch.setattr(runner, "load_units", lambda *paths: [])
    monkeypatch.setattr(runner, "load_questions", lambda *args: [])
    monkeypatch.setattr(runner, "run_chunking", lambda *args: [
        dict(budget_policy="strict", budget_chars=budget, chunk_size=400, method="dense", recall=0)
        for budget in runner.BUDGETS
    ])
    argv = ["eval", "--split", "dev", "--methods", "dense", "--out", str(out),
            "--embedding-snapshot", str(snapshot), "--embedding-sha256"]
    monkeypatch.setattr(sys, "argv", [*argv, "0" * 64])
    with pytest.raises(SystemExit) as rejected:
        runner.main()
    assert rejected.value.code == 2
    assert not local_loads and not out.exists()
    monkeypatch.setattr(sys, "argv", [*argv, digest])
    runner.main()
    assert local_loads == [(str(snapshot.resolve()), True)]
    metadata = json.loads(Path(str(out) + ".metadata.json").read_text())
    assert metadata["split"] == "dev"
    assert metadata["results_sha256"] == file_sha256(out)
    assert metadata["embedding_model"]["snapshot_sha256"] == digest
