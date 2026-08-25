"""Resumable driver so synthesize() can run with the Agent tool as LLM transport.

Round-based: a cache miss records the prompt and returns "" (which synthesize()
already handles gracefully), so one pass collects a whole phase of prompts.
Answer each pending prompt by writing <hash>.answer.txt next to its
<hash>.prompt.txt, then re-run. When nothing is pending, the final run writes
the real notes.

  python scripts/sj_synthesize.py <hub> <cache_dir> <topic> [--final]
"""

import hashlib
import shutil
import sys
import tempfile
from pathlib import Path

from persona_wiki.synthesize import synthesize


class CacheLLM:
    def __init__(self, cache_dir: Path):
        self.dir = cache_dir
        self.dir.mkdir(parents=True, exist_ok=True)
        self.pending = []

    def __call__(self, prompt: str) -> str:
        h = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
        answer = self.dir / f"{h}.answer.txt"
        if answer.exists():
            return answer.read_text(encoding="utf-8")
        (self.dir / f"{h}.prompt.txt").write_text(prompt, encoding="utf-8")
        self.pending.append(h)
        return ""


def main(hub: Path, cache_dir: Path, topic: str, final: bool) -> int:
    real_root = hub / "wiki" / "personas" / "sj"
    llm = CacheLLM(cache_dir / topic)

    if final:
        root = real_root
    else:                       # warm-up: never write into the real vault
        tmp = Path(tempfile.mkdtemp(prefix=f"sj-{topic}-"))
        (tmp / "raw").symlink_to(real_root / "raw")
        root = tmp

    try:
        res = synthesize(root, topic, llm, "2026-08-23")
    except Exception as exc:    # warm-up rounds legitimately blow up on empty answers
        if final:
            raise
        res = None
        print(f"[warm-up] {topic}: {type(exc).__name__}: {exc}")

    if llm.pending:
        print(f"PENDING {len(llm.pending)} prompt(s) in {llm.dir}")
        for h in llm.pending:
            print(f"  {h}")
        return 1

    if res is not None:
        print(f"{topic}: written={len(res.written)} skipped={len(res.skipped)} "
              f"quarantined={len(res.quarantined)} "
              f"gaps={sum(len(v) for v in res.source_gaps.values())}")
    if not final:
        shutil.rmtree(root, ignore_errors=True)
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--final"]
    sys.exit(main(Path(args[0]), Path(args[1]), args[2], "--final" in sys.argv))
