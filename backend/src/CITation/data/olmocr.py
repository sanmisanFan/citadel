"""
olmocr integration via CLI subprocess.

By default invokes `python -m olmocr.pipeline <workspace> --pdfs <pdf>` and
reads the JSONL output written to `<workspace>/results/`. Override the
command with the OLMOCR_CMD env var (space-separated argv prefix); set
OLMOCR_TIMEOUT to change the per-PDF timeout (seconds).
"""

import os
import json
import shlex
import shutil
import subprocess
import tempfile
from pathlib import Path

OLMOCR_CMD = os.getenv("OLMOCR_CMD", "python -m olmocr.pipeline")
OLMOCR_TIMEOUT = int(os.getenv("OLMOCR_TIMEOUT", "900"))


def _cmd_argv() -> list[str]:
    return shlex.split(OLMOCR_CMD)


def is_olmocr_available() -> bool:
    """Probe whether the configured olmocr command can be launched.

    Checks the launcher binary is on PATH and, for the default
    `python -m olmocr.pipeline` invocation, that the `olmocr` package is
    importable. For custom commands we trust the binary check.
    """
    argv = _cmd_argv()
    if not argv or shutil.which(argv[0]) is None:
        return False

    if argv[:3] == ["python", "-m", "olmocr.pipeline"] or argv[:3] == [
        "python3",
        "-m",
        "olmocr.pipeline",
    ]:
        try:
            subprocess.run(
                [argv[0], "-c", "import olmocr"],
                check=True,
                timeout=10,
                capture_output=True,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return False
    return True


def pdf_to_md_str_olmocr(pdf_content: bytes) -> str:
    """Convert PDF bytes to markdown by shelling out to olmocr.

    Emits ``<!-- olmocr-page: N -->`` HTML-comment markers at each page
    boundary using the ``attributes.pdf_page_numbers`` spans from olmocr's
    Dolma JSONL output. Downstream parsers (group_references_by_number)
    attribute each cited line to its source page using these markers.

    Raises subprocess.CalledProcessError / TimeoutExpired on failure so the
    caller can decide whether to fall back.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        pdf_path = tmp_path / "input.pdf"
        pdf_path.write_bytes(pdf_content)
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        subprocess.run(
            [*_cmd_argv(), str(workspace), "--pdfs", str(pdf_path)],
            check=True,
            timeout=OLMOCR_TIMEOUT,
            capture_output=True,
        )

        chunks: list[str] = []
        results_dir = workspace / "results"
        for jsonl_file in sorted(results_dir.glob("output_*.jsonl")):
            for line in jsonl_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                text = record.get("text") or record.get("content") or ""
                if not text:
                    continue
                spans = (record.get("attributes") or {}).get("pdf_page_numbers") or []
                if spans:
                    for start, end, page_num in spans:
                        chunks.append(
                            f"<!-- olmocr-page: {page_num} -->\n\n{text[start:end]}"
                        )
                else:
                    chunks.append(text)

        return "\n\n".join(chunks)
