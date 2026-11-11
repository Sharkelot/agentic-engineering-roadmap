import json
import time
from typing import TYPE_CHECKING
from urllib.parse import urlsplit

if TYPE_CHECKING:
    import httpx
else:
    try:
        import httpx
    except ImportError:
        httpx = None

from .models import AgentResponse, EvalCase


class OpenAICompatibleAdapter:
    def __init__(
        self,
        base_url: str,
        model: str,
        timeout_seconds: float = 10.0,
        transport: "httpx.AsyncBaseTransport | None" = None,
    ) -> None:
        self._httpx = httpx
        if self._httpx is None:
            raise ImportError("Install the local-http extra to use OpenAICompatibleAdapter")
        parsed = urlsplit(base_url)
        is_loopback = (parsed.hostname or "").lower() in {"localhost", "127.0.0.1", "::1"}
        has_credentials = parsed.username is not None or parsed.password is not None
        if (
            parsed.scheme.lower() not in {"http", "https"}
            or not parsed.netloc
            or has_credentials
            or parsed.query
            or parsed.fragment
            or not is_loopback
        ):
            raise ValueError("base_url must be an absolute HTTP(S) loopback URL without credentials, query, or fragment")
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.transport = transport
        self._client_options = {"trust_env": False}

    async def run(self, case: EvalCase) -> AgentResponse:
        request_content = {
            "prompt": case.prompt,
            "evidence": [item.model_dump() for item in case.evidence],
        }
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": json.dumps(request_content)}],
        }
        start = time.perf_counter()
        async with self._httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout_seconds,
            trust_env=False,
            transport=self.transport,
        ) as client:
            response = await client.post("/chat/completions", json=body)
            response.raise_for_status()
            try:
                result = json.loads(response.json()["choices"][0]["message"]["content"])
                if not isinstance(result, dict):
                    raise TypeError
                result.update(latency_ms=(time.perf_counter() - start) * 1000, error=None)
                return AgentResponse.model_validate(result)
            except (ValueError, TypeError, KeyError, IndexError, AttributeError):
                raise ValueError("Invalid OpenAI-compatible response payload") from None
