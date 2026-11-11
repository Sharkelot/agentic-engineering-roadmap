import os
import subprocess
import sys

import pytest


def test_import_is_safe_without_httpx():
    script = """import sys
sys.modules['httpx'] = None
import agent_eval_lab.http_adapter as adapter
try:
    adapter.OpenAICompatibleAdapter('http://localhost:8000/v1', 'model')
except ImportError as exc:
    assert 'local-http' in str(exc)
else:
    raise AssertionError('adapter unexpectedly initialized without httpx')
"""
    env = os.environ.copy()
    env.pop("VIRTUAL_ENV", None)
    env["PYTHONPATH"] = "src"
    result = subprocess.run(
        [sys.executable, "-c", script],
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_loopback_and_mocked_completion():
    httpx = pytest.importorskip("httpx")
    import json

    from agent_eval_lab.http_adapter import OpenAICompatibleAdapter

    payload = {
        "answer": "ok",
        "route": "support",
        "citation_ids": [],
        "tool_calls": [],
        "abstained": False,
    }

    def handler(request):
        assert request.url.path == "/v1/chat/completions"
        assert "authorization" not in request.headers
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": json.dumps(payload)}}]},
        )

    transport = httpx.MockTransport(handler)
    adapter = OpenAICompatibleAdapter(
        "http://localhost:8000/v1", "model", transport=transport
    )
    from agent_eval_lab.models import EvalCase

    case = EvalCase(
        case_id="x",
        prompt="help",
        evidence=[],
        required_source_ids=[],
        expected_route=None,
        expected_answer_terms=[],
        expected_tool_names=[],
        should_abstain=False,
        dataset_version="1",
    )
    result = __import__("asyncio").run(adapter.run(case))
    assert result.answer == "ok" and result.error is None and result.latency_ms >= 0


def test_non_loopback_rejected():
    pytest.importorskip("httpx")
    from agent_eval_lab.http_adapter import OpenAICompatibleAdapter

    with pytest.raises(ValueError, match="loopback"):
        OpenAICompatibleAdapter("https://example.com", "model")


@pytest.mark.parametrize("url", [
    "HTTP://LOCALHOST:8000/v1", "http://127.0.0.1:8000", "https://[::1]/v1",
])
def test_accepts_normalized_loopback_urls(url):
    pytest.importorskip("httpx")
    from agent_eval_lab.http_adapter import OpenAICompatibleAdapter
    OpenAICompatibleAdapter(url, "model")


@pytest.mark.parametrize("url", [
    "ftp://localhost/path", "http://user:pass@localhost/v1",
    "http://localhost/v1?x=1", "http://localhost/v1#frag", "http:///v1",
    "http://example.com/v1",
])
def test_rejects_invalid_url_forms(url):
    pytest.importorskip("httpx")
    from agent_eval_lab.http_adapter import OpenAICompatibleAdapter
    with pytest.raises(ValueError):
        OpenAICompatibleAdapter(url, "model")


def _case():
    from agent_eval_lab.models import EvalCase
    return EvalCase(case_id="x", prompt="secret prompt", evidence=[], required_source_ids=[],
        expected_route=None, expected_answer_terms=[], expected_tool_names=[],
        should_abstain=False, dataset_version="1")


@pytest.mark.parametrize("content", ["not json", "[]", '{"answer":"secret response"}'])
def test_malformed_payload_raises_sanitized_value_error(content):
    httpx = pytest.importorskip("httpx")
    from agent_eval_lab.http_adapter import OpenAICompatibleAdapter
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={
        "choices": [{"message": {"content": content}}]}))
    adapter = OpenAICompatibleAdapter("http://localhost/v1", "model", transport=transport)
    with pytest.raises(ValueError, match="^Invalid OpenAI-compatible response payload$") as exc:
        __import__("asyncio").run(adapter.run(_case()))
    assert "secret" not in str(exc.value)


@pytest.mark.parametrize("error", [
    pytest.param("connect", id="connection"), pytest.param("timeout", id="timeout"),
    pytest.param("status", id="status"),
])
def test_httpx_exceptions_propagate(error):
    httpx = pytest.importorskip("httpx")
    from agent_eval_lab.http_adapter import OpenAICompatibleAdapter
    def handler(request):
        if error == "connect": raise httpx.ConnectError("offline", request=request)
        if error == "timeout": raise httpx.ReadTimeout("late", request=request)
        return httpx.Response(503, request=request)
    adapter = OpenAICompatibleAdapter("http://localhost/v1", "model", transport=httpx.MockTransport(handler))
    expected = httpx.ConnectError if error == "connect" else httpx.ReadTimeout if error == "timeout" else httpx.HTTPStatusError
    with pytest.raises(expected):
        __import__("asyncio").run(adapter.run(_case()))


def test_trust_env_disabled_and_no_authorization_header():
    httpx = pytest.importorskip("httpx")
    from agent_eval_lab.http_adapter import OpenAICompatibleAdapter
    def handler(request):
        assert "authorization" not in request.headers
        return httpx.Response(200, json={"choices":[{"message":{"content":'{}'}}]})
    # Invalid content is sufficient to make the request and inspect safety properties.
    adapter=OpenAICompatibleAdapter("http://localhost/v1", "model", transport=httpx.MockTransport(handler))
    assert adapter._client_options["trust_env"] is False
    with pytest.raises(ValueError):
        __import__("asyncio").run(adapter.run(_case()))
