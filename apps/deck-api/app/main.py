"""Symonic Deck API: typed MCORE-1 responses rendered as document segments.

Color is a display convention, never the evidence model. The API returns explicit
labels, raw data, and provenance for every displayed segment.
"""

from __future__ import annotations

import os
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from mcore_py.algebra import OVERFLOW, trit_add_seq
from mcore_py.checker import check_tree as check_constituent_tree
from mcore_py.cli import parse_pattern, trits_to_str
from mcore_py.model import Constituent, Level, ProsodicUnit


DeckKind = Literal["field", "proof", "cut"]
RunStatus = Literal["valid", "invalid", "overflow"]


class Provenance(BaseModel):
    adapter: str
    operation: str
    note: str


class DeckSegment(BaseModel):
    """A response fragment that the client can render with a deck channel."""

    kind: DeckKind
    label: str
    text: str
    semantic: Literal["context", "result", "constraint"]
    provenance: Provenance


class ValidatePatternRequest(BaseModel):
    pattern: str = Field(
        min_length=1,
        examples=["01", "22"],
        description="MCORE shorthand such as 01, -u-, or Unicode morae.",
    )


class McoreResponse(BaseModel):
    operation: str
    status: RunStatus
    valid: bool
    segments: list[DeckSegment]
    data: dict[str, object]


APP_TITLE = "Symonic Deck API"
app = FastAPI(
    title=APP_TITLE,
    summary="Typed MCORE-1 responses for the Symonic Deck control panel.",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)


def receipt(operation: str, note: str) -> Provenance:
    return Provenance(
        adapter="mcore-py direct adapter",
        operation=operation,
        note=note,
    )


def validate_metrical_pattern(pattern: str) -> McoreResponse:
    """Mirror the core MCORE validation path while returning Deck-ready segments."""

    operation = "mcore_validate_metrical_pattern"
    try:
        trits = parse_pattern(pattern)
    except Exception as exc:  # MCORE parser preserves the useful error message.
        return McoreResponse(
            operation=operation,
            status="invalid",
            valid=False,
            segments=[
                DeckSegment(
                    kind="field",
                    label="FIELD · INPUT",
                    text=f"pattern: {pattern}",
                    semantic="context",
                    provenance=receipt(operation, "request payload"),
                ),
                DeckSegment(
                    kind="cut",
                    label="CUT · PARSE",
                    text=str(exc),
                    semantic="constraint",
                    provenance=receipt(operation, "MCORE parser rejected the input"),
                ),
            ],
            data={"pattern": pattern, "error": str(exc)},
        )

    pooled = trit_add_seq(trits)
    input_segment = DeckSegment(
        kind="field",
        label="FIELD · INPUT",
        text=f"{pattern} → {trits_to_str(trits)}",
        semantic="context",
        provenance=receipt(operation, "parsed MCORE trit sequence"),
    )

    if pooled is OVERFLOW:
        return McoreResponse(
            operation=operation,
            status="overflow",
            valid=False,
            segments=[
                input_segment,
                DeckSegment(
                    kind="cut",
                    label="CUT · OVERFLOW",
                    text="The sequence exceeds the available ternary budget.",
                    semantic="constraint",
                    provenance=receipt(operation, "trit_add_seq returned OVERFLOW"),
                ),
            ],
            data={"pattern": pattern, "result": "OVERFLOW"},
        )

    children = [ProsodicUnit(weight=trit) for trit in trits]
    parent = ProsodicUnit(weight=pooled, level=Level.L2_GANA)
    result = check_constituent_tree(Constituent(parent=parent, children=children))
    errors = [{"kind": error.kind.name, "message": error.message} for error in result.errors]
    valid = result.valid

    output_segment = DeckSegment(
        kind="proof" if valid else "cut",
        label="PROOF · VALID" if valid else "CUT · INVALID",
        text=(
            f"Conserved at {pooled.name}."
            if valid
            else "The constructed constituent did not conserve its stated weight."
        ),
        semantic="result" if valid else "constraint",
        provenance=receipt(operation, "mcore_py.checker.check_tree result"),
    )

    return McoreResponse(
        operation=operation,
        status="valid" if valid else "invalid",
        valid=valid,
        segments=[input_segment, output_segment],
        data={
            "pattern": pattern,
            "pattern_classical": trits_to_str(trits),
            "total_weight": pooled.name,
            "errors": errors,
        },
    )


@app.get("/api/v1/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": APP_TITLE}


@app.post(
    "/api/v1/mcore/validate-pattern",
    response_model=McoreResponse,
    tags=["mcore"],
    summary="Validate a metrical pattern and return Deck-renderable segments.",
)
def validate_pattern(payload: ValidatePatternRequest) -> McoreResponse:
    return validate_metrical_pattern(payload.pattern)


def _build_gradio_lab():
    """A deliberately small lab surface. The TypeScript client is the primary UI."""

    import gradio as gr

    def run(pattern: str) -> str:
        response = validate_metrical_pattern(pattern)
        lines = [f"## {response.status.upper()}"]
        lines.extend(f"**{segment.label}**  \n{segment.text}" for segment in response.segments)
        return "\n\n".join(lines)

    with gr.Blocks(title="Symonic Deck Lab") as lab:
        gr.Markdown("# Symonic Deck Lab\nA rapid MCORE-1 response renderer.")
        pattern = gr.Textbox(label="MCORE pattern", value="01")
        output = gr.Markdown(label="Deck response")
        gr.Button("Run validation").click(run, inputs=pattern, outputs=output)
    return lab


if os.getenv("DECK_ENABLE_GRADIO", "1") == "1":
    import gradio as gr

    app = gr.mount_gradio_app(app, _build_gradio_lab(), path="/lab")
