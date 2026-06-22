"""Command-line interface for de_toolkit.

Typical flow::

    de-toolkit init            # scaffold a sample data/content.json
    de-toolkit build-vault     # write the Obsidian vault under ./vault
    de-toolkit build-vault --vault-path ~/Obsidian/MyVault   # or your real vault
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Optional

import typer
from rich.console import Console

from . import config
from . import vault as vault_mod
from .models import Area, Catalog, Concept, Topic

app = typer.Typer(
    add_completion=False,
    help="Turn data-engineering study notes into a linked Obsidian vault.",
)
console = Console()


def _sample_catalog() -> Catalog:
    """A tiny starter catalog so `build-vault` works out of the box."""
    now = datetime.now(timezone.utc)
    return Catalog(
        title="Data Engineering Concepts",
        areas=[
            Area(
                title="Data Modeling",
                topics=[
                    Topic(
                        title="Warehouse Modeling",
                        concepts=[
                            Concept(
                                title="Star Schema",
                                body_text=(
                                    "A star schema models data as a central fact "
                                    "table referencing surrounding dimension "
                                    "tables, optimising analytical queries."
                                ),
                                key_points=[
                                    "Fact table holds measures and foreign keys",
                                    "Dimensions hold descriptive attributes",
                                    "Denormalised for fast reads",
                                ],
                                source_url="https://en.wikipedia.org/wiki/Star_schema",
                                updated_at=now,
                            ),
                            Concept(
                                title="Slowly Changing Dimensions",
                                body_text=(
                                    "SCD techniques track how dimension attributes "
                                    "change over time (Type 1 overwrite, Type 2 "
                                    "history rows, Type 3 previous-value column)."
                                ),
                                key_points=[
                                    "Type 1 overwrites and keeps no history",
                                    "Type 2 adds a new row per change",
                                ],
                                updated_at=now,
                            ),
                        ],
                    )
                ],
            ),
            Area(
                title="Pipelines",
                topics=[
                    Topic(
                        title="Processing Paradigms",
                        concepts=[
                            Concept(
                                title="Batch vs Streaming",
                                body_text=(
                                    "Batch processing handles bounded datasets on a "
                                    "schedule; streaming processes unbounded data "
                                    "continuously with low latency."
                                ),
                                key_points=[
                                    "Batch favours throughput",
                                    "Streaming favours latency",
                                ],
                                updated_at=now,
                            ),
                            Concept(
                                title="Idempotency",
                                body_text=(
                                    "An idempotent pipeline produces the same result "
                                    "when re-run, making retries and backfills safe."
                                ),
                                key_points=[
                                    "Use deterministic keys and upserts",
                                    "Critical for exactly-once semantics",
                                ],
                                updated_at=now,
                            ),
                        ],
                    )
                ],
            ),
        ],
    )


@app.command()
def init(
    force: bool = typer.Option(
        False, "--force", help="Overwrite an existing data/content.json."
    ),
) -> None:
    """Scaffold a sample ``data/content.json`` catalog to build from."""
    config.ensure_dirs()
    if config.CONTENT_PATH.exists() and not force:
        console.print(
            f"[yellow]{config.CONTENT_PATH} already exists[/yellow] "
            "(use --force to overwrite)."
        )
        raise typer.Exit(code=0)
    catalog = _sample_catalog()
    config.CONTENT_PATH.write_text(
        catalog.model_dump_json(indent=2), encoding="utf-8"
    )
    console.print(f"[green]✓[/green] Wrote sample catalog to {config.CONTENT_PATH}")


@app.command(name="build-vault")
def build_vault(
    vault_path: Optional[str] = typer.Option(
        None,
        "--vault-path",
        help="Write notes straight into this Obsidian vault folder. "
        "Defaults to ./vault (or $DE_VAULT_PATH).",
    ),
) -> None:
    """Build an Obsidian vault with one linked note per concept."""
    try:
        vault_mod.build_vault_from_disk(vault_path=vault_path)
    except RuntimeError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1)


@app.command()
def status() -> None:
    """Show where the catalog and the target vault are."""
    exists = config.CONTENT_PATH.exists()
    console.print(f"Catalog:     {config.CONTENT_PATH} "
                  f"({'found' if exists else 'missing'})")
    console.print(f"Vault path:  {config.resolve_vault_dir()}")
    if exists:
        raw = json.loads(config.CONTENT_PATH.read_text(encoding="utf-8"))
        catalog = Catalog.model_validate(raw)
        n_concepts = sum(
            len(t.concepts) for a in catalog.areas for t in a.topics
        )
        console.print(f"Concepts:    {n_concepts} across {len(catalog.areas)} areas")


if __name__ == "__main__":
    app()
