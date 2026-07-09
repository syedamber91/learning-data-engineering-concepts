"""Typer CLI for the persona wiki: bootstrap / update / query."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional

import typer

from .bootstrap import bootstrap as run_bootstrap
from .bootstrap import parse_persona_sections
from .config import persona_root, resolve_vault_dir
from .learn import concept_order, learn as run_learn, load_topic_concepts
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


@app.command()
def learn(
    learner: str = typer.Option("alex", "--learner"),
    source: str = typer.Option("vutr", "--from"),
    topic: str = typer.Option("spark", "--topic"),
    vault_dir: Optional[str] = typer.Option(None, "--vault-dir"),
    max_retries: int = typer.Option(2, "--max-retries"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    """Have a learner persona learn a topic from a source persona's wiki."""
    vault = resolve_vault_dir(vault_dir)
    vutr_root = persona_root(vault, source)
    learn_root = persona_root(vault, learner) / topic
    if dry_run:
        order = concept_order(load_topic_concepts(vutr_root, topic))
        typer.echo(f"{learner} would learn {len(order)} '{topic}' concepts from {source}:")
        for i, slug in enumerate(order, 1):
            typer.echo(f"  {i}. {slug}")
        return
    result = run_learn(learn_root, vutr_root, topic, default_llm, date.today().isoformat(),
                       max_retries=max_retries)
    typer.echo(f"{learner} mastered {result['mastered']}/{result['total']} "
               f"({result['pct']}%); failed={result['failed']}")


@app.command()
def ingest(
    persona: str = typer.Option("vutr", "--persona"),
    topic: str = typer.Option(..., "--topic"),
    posts_dir: str = typer.Option(..., "--posts-dir"),
    include: Optional[str] = typer.Option(None, "--include"),
    propose: Optional[str] = typer.Option(None, "--propose", help="comma keywords; print candidates and exit"),
    vault_dir: Optional[str] = typer.Option(None, "--vault-dir"),
) -> None:
    """Copy captured posts into the persona's raw/<topic>/ layer."""
    from .ingest import ingest as run_ingest, load_include, propose_include
    root = _root(vault_dir, persona)
    posts = Path(posts_dir).expanduser()
    if propose:
        for name in propose_include(posts, [k.strip() for k in propose.split(",")]):
            typer.echo(name)
        raise typer.Exit(0)
    if not include:
        typer.echo("either --propose or --include is required", err=True)
        raise typer.Exit(2)
    stamp = date.today().isoformat()
    res = run_ingest(posts, root, topic, load_include(Path(include)), stamp)
    typer.echo(f"copied {len(res.copied)}, skipped {len(res.skipped)} -> {res.manifest.parent}")


@app.command()
def synthesize(
    persona: str = typer.Option("vutr", "--persona"),
    topic: str = typer.Option(..., "--topic"),
    vault_dir: Optional[str] = typer.Option(None, "--vault-dir"),
) -> None:
    """Synthesize mechanism-depth concept notes from raw/<topic>/."""
    from .synthesize import synthesize as run_synthesize
    root = _root(vault_dir, persona)
    stamp = date.today().isoformat()
    res = run_synthesize(root, topic, default_llm, stamp)
    typer.echo(f"written={len(res.written)} skipped={len(res.skipped)} "
               f"quarantined={len(res.quarantined)} gaps={sum(len(v) for v in res.source_gaps.values())}")


@app.command()
def status(
    persona: str = typer.Option("vutr", "--persona"),
    learner: str = typer.Option("alex", "--learner"),
    topic: str = typer.Option(..., "--topic"),
    vault_dir: Optional[str] = typer.Option(None, "--vault-dir"),
) -> None:
    """Report current/stale/missing per pipeline stage (for stage-skip)."""
    from .status import stage_status
    root = _root(vault_dir, persona)
    learner_root = _root(vault_dir, learner)
    for stage, val in stage_status(root, learner_root, topic).items():
        typer.echo(f"{stage}: {val}")
