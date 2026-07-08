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
