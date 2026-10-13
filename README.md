# Predictability

Predictable API contracts around nondeterministic models.

```mermaid

%%{init: {"theme": "base", "themeVariables": {"fontFamily": "monospace"}, "flowchart": {"rankSpacing": 55, "htmlLabels": true, "markdownAutoWrap": false, "wrappingWidth": 500}}}%%

flowchart TB
    A["<b>HTTP Request</b><br/><small>Validate input with Pydantic</small>"]
    B["<b>LLM (Ollama)</b><br/><small>Generate schema-constrained JSON</small>"]
    C["<b>Pydantic</b><br/><small>Validate output or reject it</small>"]
    D("<b>Valid JSON response or HTTP error</b>")

    A --> B
    B --> C
    C --> D

    classDef plain fill:transparent,stroke:transparent,color:#222
    classDef result fill:#f4f4f4,stroke:#d5d5d5,color:#222

    class A,B,C plain
    class D result

    linkStyle default stroke:#666,stroke-width:1px

```

## Stack

- Python / FastAPI
- Pydantic
- Ollama
- uv / pytest

## Run

```bash
uv sync
ollama pull qwen3:4b
uv run uvicorn main:app --reload
```

Requires a running Ollama server.

## API

Input:

```json
{ "text": "The login button does not work" }
```

Output:

```json
{ "category": "bug" }
```

Send a request:

```sh
curl -s localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text":"Please add dark mode"}'
```

Expected output:

```json
{ "category": "feature" }
```

Allowed categories: bug, feature, question, other.

## Contracts

- Input: nonempty text, maximum 2000 characters
- Output: strictly validated JSON schema
- Invalid input: HTTP 422
- Invalid model output: HTTP 502

## Tests

```bash
uv run pytest -v
```

Tests mock Ollama to verify API behavior independently
of model availability.

## Limitations

- Schema validity does not guarantee semantic correctness.
- Temperature 0 does not guarantee determinism.
- Whitespace-only input is currently accepted.
- Ollama transport errors and timeouts are not yet handled.
