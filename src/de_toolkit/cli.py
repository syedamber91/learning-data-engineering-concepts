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
from . import teach as teach_mod
from . import vault as vault_mod
from .models import Area, Catalog, Concept, Topic

app = typer.Typer(
    add_completion=False,
    help="Turn data-engineering study notes into a linked Obsidian vault.",
)
console = Console()


def _sample_catalog() -> Catalog:
    """A fuller starter syllabus spanning software- and data-engineering.

    Each concept carries a short explanation, a few key points and a reference
    link. ``de-toolkit teach`` expands any concept into a full beginner lesson.
    """
    now = datetime.now(timezone.utc)

    def c(title, body, points, url=None):
        return Concept(
            title=title, body_text=body, key_points=points,
            source_url=url, updated_at=now,
        )

    return Catalog(
        title="Data & Software Engineering Concepts",
        areas=[
            Area(
                title="Software Engineering Foundations",
                topics=[
                    Topic(
                        title="Working with Code",
                        concepts=[
                            c(
                                "Version Control with Git",
                                "Git records snapshots of your code over time so "
                                "many people can change it safely and you can undo "
                                "mistakes.",
                                ["Commits are saved snapshots",
                                 "Branches isolate work in progress",
                                 "Merging combines branches"],
                                "https://git-scm.com/about",
                            ),
                            c(
                                "Code Review & Pull Requests",
                                "A pull request proposes changes so teammates can "
                                "read, comment on and approve them before they join "
                                "the main code.",
                                ["Catches bugs before release",
                                 "Spreads knowledge across the team",
                                 "Keeps a discussion trail"],
                            ),
                        ],
                    ),
                    Topic(
                        title="Code Quality",
                        concepts=[
                            c(
                                "Automated Testing",
                                "Tests are extra code that checks your real code "
                                "still behaves correctly, run automatically on every "
                                "change.",
                                ["Unit tests check small pieces",
                                 "Tests catch regressions early",
                                 "Green tests build confidence to change code"],
                            ),
                            c(
                                "Clean Code & Refactoring",
                                "Refactoring improves the shape of code (names, "
                                "structure) without changing what it does, keeping "
                                "it easy to read and extend.",
                                ["Clear names beat clever tricks",
                                 "Small functions are easier to test",
                                 "Refactor under green tests"],
                            ),
                        ],
                    ),
                ],
            ),
            Area(
                title="Computer Science Basics",
                topics=[
                    Topic(
                        title="Data Structures",
                        concepts=[
                            c(
                                "Arrays & Hash Maps",
                                "An array stores items in a numbered row; a hash map "
                                "stores items by a key so you can fetch them almost "
                                "instantly.",
                                ["Arrays: fast by position",
                                 "Hash maps: fast by key",
                                 "Choice depends on how you look data up"],
                            ),
                            c(
                                "Big-O / Time Complexity",
                                "Big-O describes how the work a piece of code does "
                                "grows as the input gets bigger, ignoring constant "
                                "details.",
                                ["O(1) constant, O(n) linear, O(n^2) quadratic",
                                 "Predicts behaviour at scale",
                                 "Guides which approach to pick"],
                                "https://en.wikipedia.org/wiki/Big_O_notation",
                            ),
                        ],
                    ),
                ],
            ),
            Area(
                title="Databases",
                topics=[
                    Topic(
                        title="Relational Databases",
                        concepts=[
                            c(
                                "Tables, Keys & SQL Basics",
                                "Relational databases store data in tables of rows "
                                "and columns; keys link tables and SQL is the "
                                "language used to ask questions of the data.",
                                ["Primary key uniquely identifies a row",
                                 "Foreign key references another table",
                                 "SELECT/INSERT/UPDATE/DELETE are core SQL"],
                            ),
                            c(
                                "Indexing",
                                "An index is a sorted lookup structure that lets the "
                                "database find rows without scanning the whole table.",
                                ["Speeds up reads, slows down writes",
                                 "Works like a book's index",
                                 "Pick columns you filter/join on"],
                                "https://use-the-index-luke.com/",
                            ),
                            c(
                                "Transactions & ACID",
                                "A transaction groups several changes so they all "
                                "succeed or all fail together; ACID names the "
                                "guarantees that keep data correct.",
                                ["Atomic: all-or-nothing",
                                 "Consistent, Isolated, Durable",
                                 "Prevents half-finished updates"],
                                "https://en.wikipedia.org/wiki/ACID",
                            ),
                        ],
                    ),
                ],
            ),
            Area(
                title="Data Modeling",
                topics=[
                    Topic(
                        title="Warehouse Modeling",
                        concepts=[
                            c(
                                "Star Schema",
                                "A star schema models data as a central fact table "
                                "of measurements surrounded by dimension tables that "
                                "describe them, optimised for analytics.",
                                ["Fact table holds measures and foreign keys",
                                 "Dimensions hold descriptive attributes",
                                 "Denormalised for fast reads"],
                                "https://en.wikipedia.org/wiki/Star_schema",
                            ),
                            c(
                                "Slowly Changing Dimensions",
                                "SCD techniques decide how to handle a dimension "
                                "attribute that changes over time (overwrite, keep "
                                "history, or store the previous value).",
                                ["Type 1 overwrites, keeps no history",
                                 "Type 2 adds a new row per change",
                                 "Type 3 keeps a previous-value column"],
                            ),
                            c(
                                "Normalization vs Denormalization",
                                "Normalization splits data to avoid duplication; "
                                "denormalization deliberately duplicates it to make "
                                "reads faster.",
                                ["Normalize for clean writes",
                                 "Denormalize for fast reads",
                                 "Warehouses often denormalize"],
                            ),
                        ],
                    ),
                ],
            ),
            Area(
                title="Data Pipelines",
                topics=[
                    Topic(
                        title="Processing Paradigms",
                        concepts=[
                            c(
                                "Batch vs Streaming",
                                "Batch processing handles a bounded chunk of data on "
                                "a schedule; streaming processes never-ending data "
                                "continuously with low latency.",
                                ["Batch favours throughput",
                                 "Streaming favours latency",
                                 "Many systems use both (lambda/kappa)"],
                            ),
                            c(
                                "Idempotency",
                                "An idempotent step produces the same result no "
                                "matter how many times it runs, so retries and "
                                "backfills are safe.",
                                ["Use deterministic keys and upserts",
                                 "Critical for exactly-once semantics",
                                 "Makes failures recoverable"],
                            ),
                        ],
                    ),
                    Topic(
                        title="Orchestration",
                        concepts=[
                            c(
                                "DAGs & Schedulers",
                                "A DAG (directed acyclic graph) describes tasks and "
                                "their order; a scheduler like Airflow runs them on "
                                "time and in the right sequence.",
                                ["Nodes are tasks, edges are dependencies",
                                 "Acyclic = no loops",
                                 "Schedulers handle retries and timing"],
                                "https://airflow.apache.org/",
                            ),
                            c(
                                "Data Quality & Validation",
                                "Data quality checks verify incoming data is "
                                "complete, valid and reasonable before it is trusted "
                                "downstream.",
                                ["Check nulls, ranges, uniqueness",
                                 "Fail fast on bad data",
                                 "Freshness matters as much as correctness"],
                            ),
                        ],
                    ),
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
def teach(
    vault_path: Optional[str] = typer.Option(
        None, "--vault-path",
        help="Where to write lessons (default: ./learning-vault).",
    ),
    area: Optional[str] = typer.Option(None, "--area", help="Only this area."),
    topic: Optional[str] = typer.Option(None, "--topic", help="Only this topic."),
    concept: Optional[str] = typer.Option(
        None, "--concept", help="Only this concept (exact title)."
    ),
    model: Optional[str] = typer.Option(
        None, "--model", help="Model to pass to the claude CLI."
    ),
    roadmap: bool = typer.Option(
        False, "--roadmap", help="Also generate the Home/roadmap note."
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run",
        help="Print the assembled prompt(s) instead of calling claude.",
    ),
) -> None:
    """Generate beginner lessons from the vault using your Claude Code subscription.

    Reads data/content.json, builds the teaching prompt per concept and asks the
    local `claude` CLI to write a lesson into the learning vault.
    """
    if not config.CONTENT_PATH.exists():
        console.print(
            f"[red]Error:[/red] no catalog at {config.CONTENT_PATH}. "
            "Run `de-toolkit init` first."
        )
        raise typer.Exit(code=1)
    raw = json.loads(config.CONTENT_PATH.read_text(encoding="utf-8"))
    catalog = Catalog.model_validate(raw)
    try:
        teach_mod.teach(
            catalog, vault_path=vault_path, area=area, topic=topic,
            concept=concept, model=model, roadmap=roadmap, dry_run=dry_run,
            console=console,
        )
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
