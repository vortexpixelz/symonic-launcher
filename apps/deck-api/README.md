# Symonic Deck control panel

A small, document-like interface for MCORE-1 API responses.

The core design rule is deliberately strict:

> **Color renders an explicit operation state. It does not decide whether a claim is true.**

`FIELD`, `PROOF`, and `CUT` are returned as typed segments with labels, raw data, and a provenance note. The client may color them blue, green, and red, but the semantic and accessibility path remains textual.

## Architecture

```text
TypeScript document surface  ──POST──>  FastAPI Deck adapter  ──direct──>  mcore-py
      apps/deck-web                         apps/deck-api                    mcore-1
            │                                      │
            └── colors, labels, raw JSON            └── /api/v1/openapi.json
                                                     └── /lab (Gradio)
```

The TypeScript application is the polished surface. Gradio is the fast research workbench, mounted by default at `/lab`; it makes the same underlying validation function easy to test and later portable to a Hugging Face Space.

The publishing counterpart lives under `tools/`: the SPLAT design-guide generator, report template, JSON Schema, example report, validator, and a GitHub Actions renderer. Start with `tools/README.md`.

## Local run

MCORE-1 is currently a private source dependency. From sibling clones of `symonic-launcher` and `mcore-1`:

```bash
cd ../mcore-1
uv sync --extra dev

cd ../symonic-launcher/apps/deck-api
uv venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload --port 8000
```

In a second terminal:

```bash
cd apps/deck-web
npm install
npm run dev
```

Open the Vite URL. The dev server proxies `/api` to port `8000`.

Useful endpoints:

```text
GET  /api/v1/health
POST /api/v1/mcore/validate-pattern
GET  /api/v1/openapi.json
GET  /api/v1/docs
GET  /lab
```

## First contract

```json
{
  "operation": "mcore_validate_metrical_pattern",
  "status": "valid | invalid | overflow",
  "valid": true,
  "segments": [
    {
      "kind": "field | proof | cut",
      "label": "PROOF · VALID",
      "text": "Conserved at S3.",
      "semantic": "result",
      "provenance": {
        "adapter": "mcore-py direct adapter",
        "operation": "mcore_validate_metrical_pattern",
        "note": "mcore_py.checker.check_tree result"
      }
    }
  ],
  "data": {}
}
```

## Boundaries

- No claim-tier promotion happens here. That belongs to the receipt ledger and review layer.
- The Deck renderer does not infer facts from prose. It renders structured states emitted by a known adapter.
- The first release is Python + TypeScript because the working MCORE implementation is Python. Rust/WASM can later own a fast renderer or local analysis engine without prematurely splitting the proof path.
