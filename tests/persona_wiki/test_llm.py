from persona_wiki.llm import (
    build_bootstrap_prompt,
    build_derive_prompt,
    build_qc_prompt,
)


def test_derive_prompt_includes_source_and_json_contract():
    p = build_derive_prompt("vutr", "kafka", "Kafka is optimized for writing.")
    assert "vutr" in p and "kafka" in p
    assert "Kafka is optimized for writing." in p
    assert "entities" in p and "synthesis" in p and "JSON" in p


def test_derive_prompt_includes_existing_note_when_revising():
    p = build_derive_prompt("vutr", "kafka", "new source text", existing_note="OLD NOTE BODY")
    assert "OLD NOTE BODY" in p
    assert "revise" in p.lower()


def test_bootstrap_prompt_carries_section_text():
    p = build_bootstrap_prompt("vutr", "kafka", "### Apache Kafka\n- built by LinkedIn")
    assert "built by LinkedIn" in p and "JSON" in p


def test_qc_prompt_asks_for_verdict():
    p = build_qc_prompt("NOTE", "SOURCE")
    assert "NOTE" in p and "SOURCE" in p
    assert "passed" in p and "reason" in p
