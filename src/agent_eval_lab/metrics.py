from __future__ import annotations

from .models import AgentResponse, EvalCase, MetricResult

METRIC_NAMES = ("answer_term_support", "route_accuracy", "citation_f1", "safe_abstention", "expected_tool_success")
_METHOD = "deterministic lexical check; not semantic truth"


def _unscored(name: str, reason: str) -> MetricResult:
    return MetricResult(name=name, value=None, status="unscored", details={"reason": reason, "method": _METHOD})


def _scored(name: str, value: float, **details: str) -> MetricResult:
    return MetricResult(name=name, value=value, status="scored", details={**details, "method": _METHOD})


def score_trial(case: EvalCase, response: AgentResponse | None) -> list[MetricResult]:
    results: list[MetricResult] = []
    if case.expected_answer_terms:
        if response is None:
            results.append(_scored("answer_term_support", 0.0, reason="trial failed"))
        else:
            answer = " ".join(response.answer.casefold().split())
            terms = [" ".join(term.casefold().split()) for term in case.expected_answer_terms]
            results.append(_scored("answer_term_support", sum(term in answer for term in terms) / len(terms)))
    else:
        results.append(_unscored("answer_term_support", "no expected answer terms"))
    if case.expected_route is not None:
        actual = response.route.casefold().strip() if response and response.route else ""
        results.append(_scored("route_accuracy", float(actual == case.expected_route.casefold().strip())) if response
                       else _scored("route_accuracy", 0.0, reason="trial failed"))
    else:
        results.append(_unscored("route_accuracy", "no expected route"))
    if case.required_source_ids:
        if response is None:
            results.append(_scored("citation_f1", 0.0, reason="trial failed"))
        else:
            required, cited = set(case.required_source_ids), set(response.citation_ids)
            tp = len(required & cited)
            denom = 2 * tp + len(cited - required) + len(required - cited)
            results.append(_scored("citation_f1", 2 * tp / denom if denom else 0.0))
    else:
        results.append(_unscored("citation_f1", "no required source IDs"))
    if case.should_abstain:
        if response is None:
            results.append(_scored("safe_abstention", 0.0, reason="trial failed"))
        else:
            results.append(_scored("safe_abstention", float(response.abstained)))
    else:
        results.append(_unscored("safe_abstention", "case does not require abstention"))
    if case.expected_tool_names:
        if response is None:
            results.append(_scored("expected_tool_success", 0.0, reason="trial failed"))
        else:
            successes = {call.name for call in response.tool_calls if call.succeeded}
            expected = set(case.expected_tool_names)
            results.append(_scored("expected_tool_success", len(expected & successes) / len(expected)))
    else:
        results.append(_unscored("expected_tool_success", "no expected tools"))
    return results
