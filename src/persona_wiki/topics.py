"""Minimal, deterministic topic matcher for the vutr persona.

Local to this package: the spec referenced media_core's ``match_topics``, which
lives in a different repo. This is a small whole-word vocabulary matcher — no
LLM — so change-detection stays cheap and repeatable.
"""

from __future__ import annotations

import re
from typing import Dict, List

VUTR_TOPICS: Dict[str, List[str]] = {
    "kafka": ["kafka"],
    "spark": ["spark", "apache spark"],
    "airflow": ["airflow"],
    "dbt": ["dbt", "data build tool"],
    "iceberg": ["iceberg", "apache iceberg"],
    "parquet": ["parquet"],
    "flink": ["flink"],
}

_COMPILED = {
    slug: [re.compile(rf"\b{re.escape(alias)}\b", re.IGNORECASE) for alias in aliases]
    for slug, aliases in VUTR_TOPICS.items()
}


def match_topics(text: str) -> List[str]:
    """Return sorted unique topic slugs whose vocabulary appears in ``text``."""
    hits = {
        slug
        for slug, patterns in _COMPILED.items()
        if any(p.search(text) for p in patterns)
    }
    return sorted(hits)
