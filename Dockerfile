FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY synthetic-data ./synthetic-data
RUN python -m pip install --no-cache-dir . && useradd --create-home --uid 10001 appuser && mkdir /output && chown appuser:appuser /output
USER 10001:10001
ENTRYPOINT ["agent-eval"]
CMD ["run", "--cases", "/app/synthetic-data/support_cases.jsonl", "--out", "/output/run"]
