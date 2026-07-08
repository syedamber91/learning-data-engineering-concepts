"""Typer CLI for the persona wiki: bootstrap / update / query."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional

import typer

from .bootstrap import bootstrap as run_bootstrap
from .bootstrap import parse_persona_sections
from .config import persona_root, resolve_vault_dir
from .llm import default_llm
from .pipeline import Source, update as run_update
from .query import query as run_query

app = typer.Typer(help="Incremental research-memory wiki for a persona.")


def _root(vault_dir: Optional[str], persona: str) -> Path:
    return persona_root(resolve_vault_dir(vault_dir), persona)


@app.command()
def bootstrap(
    persona: str = typer.Option("vutr", "--persona"),
    vault_dir: Optional[str] = typer.Option(None, "--vault-dir"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    """Split the persona snapshot (data/personas/<persona>.md) into atomic notes."""
    vault = resolve_vault_dir(vault_dir)
    snapshot = vault / "data" / "personas" / f"{persona}.md"
    md = snapshot.read_text(encoding="utf-8")
    if dry_run:
        for title, _ in parse_persona_sections(md):
            typer.echo(f"would process section: {title}")
        return
    result = run_bootstrap(_root(vault_dir, persona), persona, md, default_llm, date.today().isoformat())
    typer.echo(f"bootstrapped {result['topics']} topic(s); logged={result['logged']}")


@app.command()
def update(
    persona: str = typer.Option("vutr", "--persona"),
    vault_dir: Optional[str] = typer.Option(None, "--vault-dir"),
) -> None:
    """(POC) update from stdin: one 'id<TAB>text' source per line."""
    sources = []
    for line in typer.get_text_stream("stdin"):
        line = line.rstrip("\n")
        if not line:
            continue
        sid, _, text = line.partition("\t")
        sources.append(Source(id=sid, text=text))
    result = run_update(_root(vault_dir, persona), persona, sources, default_llm, date.today().isoformat())
    typer.echo(f"written={result['written']} failed={result['failed']} logged={result['logged']}")


@app.command()
def query(
    question: str,
    persona: str = typer.Option("vutr", "--persona"),
    vault_dir: Optional[str] = typer.Option(None, "--vault-dir"),
) -> None:
    """Route a question to the relevant persona-wiki notes."""
    typer.echo(run_query(_root(vault_dir, persona), question))
