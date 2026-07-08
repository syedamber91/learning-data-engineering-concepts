"""The persona wiki's ``index.yaml`` — the catalog an agent reads first."""

from __future__ import annotations

from pathlib import Path

import yaml

from .models import AtomicEntry, TopicEntry, WikiIndex

INDEX_NAME = "index.yaml"


def load_index(root: Path) -> WikiIndex:
    path = root / INDEX_NAME
    if not path.exists():
        return WikiIndex()
    return WikiIndex.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")) or {})


def save_index(root: Path, index: WikiIndex) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    path = root / INDEX_NAME
    path.write_text(
        yaml.safe_dump(index.model_dump(), sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return path


def register_topic(index: WikiIndex, slug: str, sources_count: int, stamp: str) -> None:
    index.topics[slug] = TopicEntry(
        file=f"topics/{slug}.md", sources=sources_count, last_updated=stamp
    )


def register_atomic(index: WikiIndex, kind: str, slug: str, topic: str, stamp: str) -> None:
    bucket = index.entities if kind == "entity" else index.concepts
    entry = bucket.get(slug)
    if entry is None:
        entry = AtomicEntry(file=f"{kind}s/{slug}.md", topics=[], last_updated=stamp)
        bucket[slug] = entry
    if topic and topic not in entry.topics:
        entry.topics.append(topic)
    entry.last_updated = stamp


def has_topic(index: WikiIndex, slug: str) -> bool:
    return slug in index.topics


def has_atomic(index: WikiIndex, kind: str, slug: str) -> bool:
    bucket = index.entities if kind == "entity" else index.concepts
    return slug in bucket
