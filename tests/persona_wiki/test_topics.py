from persona_wiki.topics import match_topics


def test_matches_single_topic_whole_word():
    assert match_topics("Kafka partitions and the commit log") == ["kafka"]


def test_matches_multiple_and_dedupes_sorted():
    text = "Spark shuffle vs Kafka, and more Spark AQE"
    assert match_topics(text) == ["kafka", "spark"]


def test_no_false_positive_substring():
    # "sparkling" must not match "spark"
    assert match_topics("sparkling water") == []


def test_unknown_text_returns_empty():
    assert match_topics("gardening tips") == []


def test_expanded_vocab_routes_new_topics_to_existing_slugs():
    # each maps to a real topics/<slug>.md that the wiki already has
    assert "olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks" \
        in match_topics("A deep dive into Snowflake and ClickHouse internals")
    assert "single-node-engines-duckdb-polars-vs-distributed-systems" \
        in match_topics("DuckDB vs Polars on a single node")
    assert "iceberg" in match_topics("Comparing Delta Lake and Apache Hudi table formats")
    assert "llms-ai-agents-and-vector-databases" in match_topics("RAG over a vector database")
    assert "storage-models-nsm-dsm-pax-and-column-store" in match_topics("PAX vs DSM layouts")


def test_new_topic_can_match_multiple_when_genuinely_shared():
    # DuckDB is both an OLAP engine and a single-node engine — route to both
    hits = match_topics("DuckDB is an embedded OLAP engine")
    assert "single-node-engines-duckdb-polars-vs-distributed-systems" in hits
    assert "olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks" in hits


def test_every_vocab_slug_is_lowercase_hyphenated():
    from persona_wiki.topics import VUTR_TOPICS
    import re
    assert all(re.fullmatch(r"[a-z0-9-]+", s) for s in VUTR_TOPICS)
