"""Minimal, deterministic topic matcher for the vutr persona.

Local to this package: the spec referenced media_core's ``match_topics``, which
lives in a different repo. This is a small whole-word vocabulary matcher — no
LLM — so change-detection stays cheap and repeatable.
"""

from __future__ import annotations

import re
from typing import Dict, List

# Slug -> alias phrases. The slug is the topic note's filename, so each key must
# match an existing `topics/<slug>.md`. Aliases are the distinctive terms that
# appear in a source about that topic; `update` routes a new source to every
# topic whose aliases it contains. Keep aliases specific — generic words (e.g.
# "data", "log", bare "sql") over-match and route everything everywhere.
VUTR_TOPICS: Dict[str, List[str]] = {
    "kafka": ["kafka"],
    "spark": ["spark", "apache spark"],
    "airflow": ["airflow"],
    "dbt": ["dbt", "data build tool"],
    "iceberg": ["iceberg", "apache iceberg", "delta lake", "apache hudi",
                "open table format", "open table formats"],
    "parquet": ["parquet"],
    "flink": ["flink", "apache flink"],
    "amazon-s3-gfs-hdfs-and-distributed-file-systems": [
        "amazon s3", "s3", "gfs", "hdfs", "distributed file system", "object storage"],
    "apache-arrow": ["apache arrow", "arrow flight", "arrow ipc", "record batch"],
    "apache-pinot-druid-and-real-time-olap": [
        "pinot", "apache pinot", "druid", "apache druid", "real-time olap",
        "real time olap", "star-tree", "star tree"],
    "big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter": [
        "case study", "case studies"],
    "change-data-capture-cdc-and-data-sourcing": [
        "change data capture", "cdc", "debezium", "data sourcing"],
    "data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa": [
        "lakehouse", "data lake", "data mesh", "data warehouse",
        "lambda architecture", "kappa architecture", "medallion"],
    "data-engineering-career-roadmap-and-learning-philosophy": [
        "career", "roadmap", "learning philosophy"],
    "data-pipeline-design-framework": [
        "data pipeline", "pipeline design", "idempotency", "idempotent",
        "dead letter queue", "backfill"],
    "history-of-data-engineering": ["history of data engineering", "history of data"],
    "llms-ai-agents-and-vector-databases": [
        "llm", "large language model", "vector database", "vector db",
        "embedding", "embeddings", "rag", "ai agent", "text-to-sql", "text to sql"],
    "lsm-tree-storage-engines": [
        "lsm-tree", "lsm tree", "sstable", "memtable", "write-ahead log", "wal",
        "bloom filter"],
    "olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks": [
        "olap", "bigquery", "snowflake", "clickhouse", "redshift", "databricks",
        "photon", "vectorized"],
    "single-node-engines-duckdb-polars-vs-distributed-systems": [
        "duckdb", "polars", "single-node", "single node"],
    "sql-fundamentals-and-execution-model": [
        "relational model", "sql execution", "execution order", "execution model",
        "join strategy", "nested loop join", "hash join", "sort-merge join"],
    "storage-models-nsm-dsm-pax-and-column-store": [
        "nsm", "dsm", "pax", "column store", "column-store", "row store",
        "storage model"],
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
