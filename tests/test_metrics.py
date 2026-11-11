from agent_eval_lab.metrics import score_trial
from agent_eval_lab.models import AgentResponse, EvalCase, EvidenceRef


def make_case(**changes: object) -> EvalCase:
    values: dict[str, object] = {
        "case_id": "c1", "prompt": "help", "evidence": [EvidenceRef(source_id="s1", excerpt="proof")],
        "required_source_ids": ["s1"], "expected_route": "billing", "expected_answer_terms": ["Refund", "  tracking   number "],
        "expected_tool_names": ["lookup"], "should_abstain": True, "dataset_version": "d1",
    }
    values.update(changes)
    return EvalCase(**values)  # type: ignore[arg-type]


def response(**changes: object) -> AgentResponse:
    values: dict[str, object] = {
        "answer": "A REFUND is pending; your tracking number is ready.", "route": "BILLING ",
        "citation_ids": ["s1", "unknown"], "tool_calls": [], "abstained": True,
        "latency_ms": 1, "error": None,
    }
    values.update(changes)
    return AgentResponse(**values)  # type: ignore[arg-type]


def test_scores_lexical_terms_route_citations_abstention_and_tools() -> None:
    results = {item.name: item for item in score_trial(make_case(), response())}
    assert results["answer_term_support"].value == 1.0
    assert results["route_accuracy"].value == 1.0
    assert results["citation_f1"].value == 2 / 3
    assert results["safe_abstention"].value == 1.0
    assert results["expected_tool_success"].value == 0.0
    assert all("deterministic lexical" in item.details["method"] for item in results.values())


def test_missing_required_citation_and_wrong_route_score_zero() -> None:
    results = {item.name: item for item in score_trial(make_case(), response(route="sales", citation_ids=[]))}
    assert results["route_accuracy"].value == 0.0
    assert results["citation_f1"].value == 0.0


def test_nonapplicable_metrics_are_unscored() -> None:
    case = make_case(required_source_ids=[], expected_route=None, expected_answer_terms=[], expected_tool_names=[], should_abstain=False)
    results = score_trial(case, response())
    assert {item.name: item.status for item in results} == {"answer_term_support": "unscored", "route_accuracy": "unscored", "citation_f1": "unscored", "safe_abstention": "scored", "expected_tool_success": "unscored"}


def test_failed_trial_scores_zero_for_applicable_and_unscored_otherwise() -> None:
    results = {item.name: item for item in score_trial(make_case(), None)}
    assert all((item.value == 0.0 if item.status == "scored" else item.value is None) for item in results.values())
    case = make_case(required_source_ids=[], expected_route=None, expected_answer_terms=[], expected_tool_names=[], should_abstain=False)
    results = {item.name: item for item in score_trial(case, None)}
    assert results["safe_abstention"].status == "scored" and results["safe_abstention"].value == 0.0
    assert all(item.status == "unscored" for name, item in results.items() if name != "safe_abstention")


def test_safe_abstention_is_exact_boolean_match_for_all_cases() -> None:
    case = make_case(should_abstain=False)
    assert {m.name:m for m in score_trial(case, response(abstained=True))}["safe_abstention"].value == 0.0
    assert {m.name:m for m in score_trial(case, response(abstained=False))}["safe_abstention"].value == 1.0

def test_expected_tool_metric_is_set_f1() -> None:
    from agent_eval_lab.models import ToolCallRecord
    case=make_case(expected_tool_names=["a", "b"])
    result={m.name:m for m in score_trial(case,response(tool_calls=[ToolCallRecord(name="a", succeeded=True, error=None),ToolCallRecord(name="extra", succeeded=True, error=None)]))}["expected_tool_success"]
    assert result.value == 0.5
