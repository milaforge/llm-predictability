# Goal

Turn an unpredictable LLM into an API with a predictable contract.

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

## Utility: Classifier

I'll build a support-ticket classifier.

Input:

```json
{ "text": "The login button does not work" }
```

Expected output:

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
