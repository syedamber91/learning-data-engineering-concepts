from persona_wiki.qc import qc_check


def _grounded_llm(prompt):
    return '{"passed": true, "reason": "all claims supported"}'


def _overreach_llm(prompt):
    return '{"passed": false, "reason": "absolute claim from conditional source"}'


def _garbage_llm(prompt):
    return "I think it is fine"


def test_grounded_note_passes():
    passed, reason = qc_check("NOTE", "SOURCE", _grounded_llm)
    assert passed is True and "supported" in reason


def test_overreach_note_fails():
    passed, reason = qc_check("NOTE", "SOURCE", _overreach_llm)
    assert passed is False and "conditional" in reason


def test_unparseable_verdict_fails_closed():
    passed, reason = qc_check("NOTE", "SOURCE", _garbage_llm)
    assert passed is False
