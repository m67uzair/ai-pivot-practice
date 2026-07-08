"""Run the same PDF through three hosted document-parsing services and
save each result, so we can compare output quality side-by-side.

  - LlamaParse (LlamaCloud) -> Markdown
  - Marker (Datalab)        -> Markdown
  - unstructured            -> typed elements, flattened to Markdown-ish text

We test on two inputs derived from the same paper:
  - paper_6p.pdf   : born-digital (real text layer)  -> tests layout/reading order
  - scanned_6p.pdf : rasterized images (no text)     -> forces OCR

Run:  uv run document-parsing/compare.py
      uv run document-parsing/compare.py llamaparse marker      # subset
"""

import sys
import time
from pathlib import Path

import httpx
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """The three hosted-parser keys, loaded from the repo-root .env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llama_parse_api_key: str
    marker_api_key: str  # Datalab (Marker) API
    unstructured_api_key: str
    # Shared SaaS default; override in .env with your per-workspace URL if needed.
    unstructured_api_url: str = "https://api.unstructuredapp.io/general/v0/general"


settings = Settings()

HERE = Path(__file__).parent
PDFS = HERE / "pdfs"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

INPUTS = ["paper_6p.pdf", "scanned_6p.pdf"]
POLL_TIMEOUT = 240  # seconds to wait for async jobs
POLL_EVERY = 3


def _read(name: str) -> bytes:
    return (PDFS / name).read_bytes()


# ── LlamaParse (LlamaCloud): upload -> poll job -> fetch markdown ────────────
def parse_llamaparse(name: str) -> str:
    base = "https://api.cloud.llamaindex.ai/api/v1/parsing"
    auth = {"Authorization": f"Bearer {settings.llama_parse_api_key}"}
    with httpx.Client(timeout=120) as c:
        up = c.post(
            f"{base}/upload",
            headers={**auth, "Accept": "application/json"},
            files={"file": (name, _read(name), "application/pdf")},
            data={"result_type": "markdown"},
        )
        up.raise_for_status()
        job_id = up.json()["id"]

        deadline = time.monotonic() + POLL_TIMEOUT
        while True:
            job = c.get(f"{base}/job/{job_id}", headers=auth).json()
            status = job.get("status")
            if status == "SUCCESS":
                break
            if status in ("ERROR", "CANCELED") or time.monotonic() > deadline:
                raise RuntimeError(f"llamaparse job {status}: {job}")
            time.sleep(POLL_EVERY)

        res = c.get(f"{base}/job/{job_id}/result/markdown", headers=auth)
        res.raise_for_status()
        return res.json()["markdown"]


# ── Marker (Datalab): submit -> poll check_url -> markdown ───────────────────
def parse_marker(name: str) -> str:
    key = {"X-Api-Key": settings.marker_api_key}
    with httpx.Client(timeout=120) as c:
        sub = c.post(
            "https://www.datalab.to/api/v1/marker",
            headers=key,
            files={"file": (name, _read(name), "application/pdf")},
            data={"output_format": "markdown"},
        )
        sub.raise_for_status()
        body = sub.json()
        if not body.get("success", True):
            raise RuntimeError(f"marker submit failed: {body}")
        check_url = body["request_check_url"]

        deadline = time.monotonic() + POLL_TIMEOUT
        while True:
            job = c.get(check_url, headers=key).json()
            if job.get("status") == "complete":
                if not job.get("success", True):
                    raise RuntimeError(f"marker job failed: {job.get('error')}")
                return job["markdown"]
            if time.monotonic() > deadline:
                raise RuntimeError("marker job timed out")
            time.sleep(POLL_EVERY)


# ── unstructured: partition -> typed elements -> flatten to markdown-ish ─────
def parse_unstructured(name: str) -> str:
    with httpx.Client(timeout=240) as c:
        r = c.post(
            settings.unstructured_api_url,
            headers={"unstructured-api-key": settings.unstructured_api_key, "accept": "application/json"},
            files={"files": (name, _read(name), "application/pdf")},
            data={"strategy": "hi_res"},  # layout model + OCR
        )
        r.raise_for_status()
        elements = r.json()

    lines = []
    for el in elements:
        text = (el.get("text") or "").strip()
        if not text:
            continue
        t = el.get("type")
        if t == "Title":
            lines.append(f"# {text}")
        elif t == "ListItem":
            lines.append(f"- {text}")
        else:
            lines.append(text)
    return "\n\n".join(lines)


PARSERS = {
    "llamaparse": parse_llamaparse,
    "marker": parse_marker,
    "unstructured": parse_unstructured,
}


def main() -> None:
    which = [a for a in sys.argv[1:] if a in PARSERS] or list(PARSERS)
    rows = []
    for name in INPUTS:
        if not (PDFS / name).exists():
            print(f"! missing {name}, skipping")
            continue
        for parser in which:
            label = f"{parser:12} {name:16}"
            t0 = time.monotonic()
            try:
                text = PARSERS[parser](name)
                dt = time.monotonic() - t0
                out_path = OUT / f"{parser}__{Path(name).stem}.md"
                out_path.write_text(text)
                rows.append((parser, name, f"{dt:6.1f}s", f"{len(text):>7} ch", "ok"))
                print(f"✓ {label} {dt:6.1f}s  {len(text):>7} chars -> {out_path.name}")
            except Exception as e:
                dt = time.monotonic() - t0
                rows.append((parser, name, f"{dt:6.1f}s", "-", f"ERR {e}"))
                print(f"✗ {label} {dt:6.1f}s  {type(e).__name__}: {str(e)[:200]}")

    print("\n=== summary ===")
    for r in rows:
        print("  " + "  ".join(str(x) for x in r))


if __name__ == "__main__":
    main()
