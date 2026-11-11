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
