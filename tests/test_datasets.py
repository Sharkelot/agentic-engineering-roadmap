import pytest

from agent_eval_lab.datasets import load_cases

VALID = '{"case_id":"c1","prompt":"p","evidence":[],"required_source_ids":[],"expected_route":null,"expected_answer_terms":[],"expected_tool_names":[],"should_abstain":false,"dataset_version":"v1"}\n'


def test_load_jsonl_and_reject_invalid_rows(tmp_path) -> None:
    path = tmp_path / "cases.jsonl"
    path.write_text(VALID)
    assert [case.case_id for case in load_cases(path)] == ["c1"]
    path.write_text(VALID + VALID)
    with pytest.raises(ValueError, match="line 2"):
        load_cases(path)
    for content in ("\n", "{bad}\n", "{}\n", VALID.replace("}\n", ",\"extra\":1}\n")):
        path.write_text(content)
        with pytest.raises(ValueError, match="line 1"):
            load_cases(path)
