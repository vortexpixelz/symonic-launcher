#!/usr/bin/env python3
"""Render the Symonic SPLAT Reporting Design Guide.

Canonicalized from the original internal generator:
/mnt/data/create_symonic_design_guide.py
bytes: 37682
sha256: 3fef63f07bbb488570a849b497bc00fa957586cfeb3a1605e01069f4055ab6a5

Run:
    uv run --with reportlab python tools/create_symonic_design_guide.py \
      --out docs/generated/symonic_splat_design_guide_v0_2.pdf
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle

W, H = letter
M = 48
PAPER, INK, MUTED, LINE = (HexColor(v) for v in ("#F5F3ED", "#171817", "#6E706D", "#C9C6BB"))
FIELD, PROOF, CUT = (HexColor(v) for v in ("#005AAE", "#006B44", "#B52B27"))
PURPLE, PURPLE_DARK, GRAPHITE, PALE_YELLOW = (HexColor(v) for v in ("#7650B7", "#4D327E", "#393A3E", "#F2E7A8"))
LIGHTS = {FIELD: HexColor("#E4EFFB"), PROOF: HexColor("#E0F1E8"), CUT: HexColor("#F7E4E2")}

STYLES = {
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.2, leading=13, textColor=INK),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=7.7, leading=10, textColor=MUTED),
    "head": ParagraphStyle("head", fontName="Times-Roman", fontSize=28, leading=32, textColor=INK),
    "quote": ParagraphStyle("quote", fontName="Times-Roman", fontSize=14.5, leading=19, textColor=INK),
    "table": ParagraphStyle("table", fontName="Helvetica", fontSize=7.2, leading=9.4, textColor=INK),
    "table_head": ParagraphStyle("table_head", fontName="Helvetica-Bold", fontSize=7, leading=9, textColor=INK),
}


def paragraph(text: str, style: str = "body") -> Paragraph:
    return Paragraph(text, STYLES[style])


def draw_text(c: canvas.Canvas, text: str, x: float, y: float, width: float, style: str = "body") -> float:
    item = paragraph(text, style)
    height = item.wrap(width, 1000)[1]
    item.drawOn(c, x, y - height)
    return y - height


def draw_table(c: canvas.Canvas, rows: list[list[str]], y: float, widths: list[float]) -> float:
    cells = [[paragraph(str(cell), "table_head" if i == 0 else "table") for cell in row] for i, row in enumerate(rows)]
    block = Table(cells, colWidths=widths, repeatRows=1)
    block.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), .35, LINE), ("BACKGROUND", (0, 0), (-1, 0), HexColor("#E9E7DF")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    _, height = block.wrapOn(c, sum(widths), 600)
    block.drawOn(c, M, y - height)
    return y - height


def splat(c: canvas.Canvas, cx: float, cy: float, radius: float) -> None:
    c.setFillColor(PURPLE)
    points = []
    for i in range(30):
        angle = 2 * math.pi * i / 30
        wobble = 1 + .16 * math.sin(i * 2.8) + .09 * math.cos(i * 5.1)
        points.append((cx + radius * wobble * math.cos(angle), cy + radius * wobble * math.sin(angle)))
    path = c.beginPath(); path.moveTo(*points[0])
    for point in points[1:]: path.lineTo(*point)
    path.close(); c.drawPath(path, stroke=0, fill=1)
    for angle, scale in ((.2, .12), (1.82, .1), (3.74, .08), (5.05, .06)):
        c.circle(cx + radius * 1.42 * math.cos(angle), cy + radius * 1.42 * math.sin(angle), radius * scale, stroke=0, fill=1)


def chrome(c: canvas.Canvas, page: int, section: str) -> None:
    c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 6.8)
    c.drawString(M, H - 30, "SYMONIC SPLAT DESIGN GUIDE")
    c.drawRightString(W - M, H - 30, section)
    c.setStrokeColor(LINE); c.line(M, H - 36, W - M, H - 36); c.line(M, 28, W - M, 28)
    c.setFont("Helvetica", 6.5)
    c.drawString(M, 16, f"SYMONIC SPLAT REPORTING / DESIGN GUIDE / v0.2 / {section}")
    c.drawRightString(W - M, 16, f"PAGE {page:02d}")


def title(c: canvas.Canvas, page: int, section: str, name: str, subtitle: str, color: HexColor = INK) -> float:
    chrome(c, page, section)
    c.setFillColor(color); c.setFont("Helvetica-Bold", 7); c.drawString(M, H - 64, section)
    y = draw_text(c, name, M, H - 96, 485, "head")
    y = draw_text(c, subtitle, M, y - 5, 480)
    c.setStrokeColor(color); c.setLineWidth(1.1); c.line(M, 92, W - M, 92)
    return y


def bullet_page(c: canvas.Canvas, page: int, section: str, name: str, subtitle: str, rows: list[tuple[str, str, HexColor]]) -> None:
    y = title(c, page, section, name, subtitle, PURPLE if section == "INTERNAL" else INK) - 26
    for heading, text, color in rows:
        c.setFillColor(color); c.setFont("Helvetica-Bold", 8); c.drawString(M, y, heading.upper())
        y = draw_text(c, text, M, y - 13, 485) - 16
    c.showPage()


def build(out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out), pagesize=letter, pageCompression=1)
    c.setTitle("Symonic SPLAT Reporting Design Guide v0.2")
    c.setAuthor("Symonic LLC")
    c.setSubject("SPLAT reporting, document templates, and internal-to-private staging")

    # Cover
    c.setFillColor(GRAPHITE); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(PALE_YELLOW); c.setFont("Helvetica-Bold", 7.5)
    c.drawString(M, H - 48, "SYMONIC SPLAT REPORTING / DESIGN GUIDE / v0.2")
    c.setStrokeColor(HexColor("#57585C")); c.line(M, H - 57, W - M, H - 57)
    splat(c, W - 135, H - 205, 102)
    c.setFillColor(PALE_YELLOW); c.setFont("Times-Bold", 39); c.drawString(M, H - 188, "SPLAT")
    c.setFont("Times-Roman", 31); c.drawString(M, H - 224, "Reporting Design Guide")
    c.setFont("Times-Roman", 17); c.drawString(M, H - 258, "Internal staging for private work")
    c.setFillColor(HexColor("#D9D8D0")); c.setFont("Helvetica", 10)
    c.drawString(M, H - 300, "Signal · Proof · Limit · Action · Trace")
    c.setFont("Helvetica", 8); c.drawString(M, 54, "PURPLE + PALE YELLOW: edition syntax. BLUE / GREEN / RED: operating semantics.")
    c.showPage()

    # Contents
    chrome(c, 2, "INTERNAL")
    y = draw_text(c, "Contents", M, H - 88, 485, "head") - 18
    contents = [
        ("01", "Operating premise", "SPLAT is a traceable decision artifact."),
        ("02", "Three handling zones", "Public, Private, Internal."),
        ("03", "Deck keys", "FIELD, PROOF, CUT, JACK, JOKER."),
        ("04", "SPLAT grammar", "Signal, Proof, Limit, Action, Trace."),
        ("05", "Perspective modes", "Seven report lenses."),
        ("06", "Template kit", "Title, memo, outline, metadata."),
        ("07", "Release gates", "Internal → Private staging."),
        ("A", "Glossary + source note", "Vocabulary and scope."),
    ]
    for key, heading, desc in contents:
        c.setFillColor(PURPLE); c.setFont("Courier", 8); c.drawString(M, y, key)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 9); c.drawString(M + 42, y, heading)
        c.setFillColor(MUTED); c.setFont("Helvetica", 8); c.drawString(M + 205, y, desc); y -= 34
    c.showPage()

    bullet_page(c, 3, "INTERNAL", "The operating premise", "A SPLAT Report is not merely a report wearing a loud hat. It is a traceable decision artifact.", [
        ("Signal", "State what changed, matters, or needs attention. The signal is a proposition, not a folder title.", FIELD),
        ("Proof", "Show the receipt, observation, method, reproducible result, or bounded source that supports the signal.", PROOF),
        ("Limit", "Name uncertainty, exclusions, contradictory evidence, invalid states, and unresolved ambiguity.", CUT),
        ("Action + Trace", "Specify the next move, owner, and horizon, then leave an auditable route to sources, versions, and receipts.", PURPLE),
    ])

    chrome(c, 4, "INTERNAL")
    y = draw_text(c, "Three handling zones", M, H - 88, 485, "head") - 12
    y = draw_table(c, [
        ["Zone", "Primary job", "Required posture", "Default audience"],
        ["PUBLIC", "State the external promise", "Bounded claims; no internal operating context", "Open reader"],
        ["PRIVATE", "Enable a named decision", "Context-rich but recipient-safe", "Named recipient / group"],
        ["INTERNAL", "Make work survivable", "Receipts, counterexamples, drafts, cuts, alternatives", "Working system"],
    ], y, [80, 130, 175, 100]) - 26
    draw_text(c, "<b>Current priority:</b> Internal is the staging forge for Private. Public rules exist to prevent leakage and future drift, not because public polish is the next move.", M, y, 485, "quote")
    c.showPage()

    chrome(c, 5, "INTERNAL")
    y = draw_text(c, "Deck keys", M, H - 88, 485, "head") - 18
    for label, color, meaning in [
        ("FIELD / BLUE", FIELD, "Inputs, source context, orientation, and the visible field."),
        ("PROOF / GREEN", PROOF, "Structured result state, reproducible support, and successful validation."),
        ("CUT / RED", CUT, "Limits, invalidity, constraints, counterexamples, and decisions."),
    ]:
        c.setFillColor(LIGHTS[color]); c.roundRect(M, y - 31, 485, 31, 4, stroke=0, fill=1)
        c.setFillColor(color); c.circle(M + 16, y - 15, 5.3, stroke=0, fill=1)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 8); c.drawString(M + 30, y - 18, label)
        c.setFont("Helvetica", 7.7); c.drawString(M + 180, y - 18, meaning); y -= 42
    y -= 10
    draw_text(c, "<b>JACK</b> renders raw material into a stable artifact. <b>JOKER</b> changes the format when the normal one hides the important thing. Neither may erase receipts, versions, or limits.", M, y, 485, "quote")
    c.showPage()

    chrome(c, 6, "INTERNAL")
    y = draw_text(c, "Color system", M, H - 88, 485, "head") - 12
    y = draw_table(c, [
        ["Token", "Hex", "Use", "Never use it for"],
        ["FIELD", "#005AAE", "Input, context, navigation", "A claim tier"],
        ["PROOF", "#006B44", "Validated structured output", "A blanket truth claim"],
        ["CUT", "#B52B27", "Limit, overflow, constraint", "Aesthetic alarmism"],
        ["PURPLE", "#7650B7", "Edition, staging, cover syntax", "Evidence status"],
        ["PALE YELLOW", "#F2E7A8", "Navigation and callout field", "Warning or success"],
    ], y, [93, 82, 165, 145]) - 22
    draw_text(c, "Color never works alone. Every channel keeps a text label, structural placement, and readable contrast. The palette is a guide rail, not a truth machine.", M, y, 485, "quote")
    c.showPage()

    chrome(c, 7, "INTERNAL")
    y = draw_text(c, "SPLAT grammar", M, H - 88, 485, "head") - 20
    for key, name, prompt, color in [
        ("S", "Signal", "What changed, matters, or needs attention?", FIELD),
        ("P", "Proof", "What supports the signal, and where is the receipt?", PROOF),
        ("L", "Limit", "What does this not establish, include, or resolve?", CUT),
        ("A", "Action", "What happens next, owned by whom, by which horizon?", PURPLE),
        ("T", "Trace", "How does a reader return to source, version, and context?", PURPLE_DARK),
    ]:
        c.setFillColor(color); c.circle(M + 16, y - 12, 10, stroke=0, fill=1)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 8); c.drawCentredString(M + 16, y - 15, key)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 9); c.drawString(M + 38, y - 9, name.upper())
        y = draw_text(c, prompt, M + 38, y - 17, 445, "small") - 15
    c.showPage()

    chrome(c, 8, "INTERNAL")
    y = draw_text(c, "Perspective modes", M, H - 88, 485, "head") - 12
    draw_table(c, [
        ["Mode", "Primary job", "Use when"],
        ["Horizon", "Orient a field", "The reader needs landscape before a decision"],
        ["Vanishing Point", "Converge a decision", "Many inputs must answer one question"],
        ["Orthogonal", "Show the path of proof", "A claim needs source-to-claim visibility"],
        ["Transversal", "Hold a cross-section", "Versions, cohorts, or workstreams require matched rows"],
        ["Depth", "Separate near and far", "Context, stakes, and details are blending together"],
        ["Atmospheric", "Calibrate visibility", "The signal is early, weak, or distance-sensitive"],
        ["Value", "Stress the form", "A plan needs highlights, shadows, and consequences drawn"],
    ], y, [110, 145, 230])
    c.showPage()

    bullet_page(c, 9, "INTERNAL", "Default SPLAT composition", "Choose one primary viewing mode. Add a second only when it makes the decision clearer.", [
        ("1. Horizon", "State the field, watch window, and meaningful change since the last scan.", FIELD),
        ("2. Vanishing Point", "Write one decision question. A report may have a dozen inputs; its reader needs one convergence point.", PURPLE),
        ("3. Orthogonal", "Attach evidence lines where the decision must survive inspection. Keep the receipt path visible.", PROOF),
        ("4. Value", "Before release, name the highlight, midtone, core shadow, and cast shadow of the recommended action.", CUT),
    ])

    chrome(c, 10, "PRIVATE")
    y = draw_text(c, "Template: title page", M, H - 88, 485, "head") - 12
    c.setStrokeColor(INK); c.rect(M, y - 350, 485, 350, stroke=1, fill=0)
    c.setFillColor(PURPLE); c.rect(M, y - 8, 485, 8, stroke=0, fill=1)
    c.setFillColor(MUTED); c.setFont("Helvetica-Bold", 7); c.drawString(M + 22, y - 32, "PRIVATE / SPLAT MODE / STATUS / VERSION")
    c.setFillColor(INK); c.setFont("Times-Roman", 28); c.drawString(M + 22, y - 82, "Specific noun phrase")
    c.setFont("Times-Roman", 16); c.drawString(M + 22, y - 111, "One-sentence decision thesis")
    c.setStrokeColor(LINE); c.line(M + 22, y - 145, W - M - 22, y - 145)
    c.setFillColor(MUTED); c.setFont("Courier", 7)
    for index, line in enumerate(("artifact_id: SYM-PRV-YYYY-NN", "handling: PRIVATE", "status: review-ready", "owner: [name]", "decision_horizon: [ISO date]", "receipt_manifest: [path]")):
        c.drawString(M + 22, y - 170 - index * 22, line)
    c.showPage()

    chrome(c, 11, "PRIVATE")
    y = draw_text(c, "Template: memo page", M, H - 88, 485, "head") - 18
    draw_table(c, [
        ["Slot", "Required content"],
        ["Signal", "The thing that changed or needs attention, in a sentence."],
        ["Decision", "The exact choice, threshold, or next move requested."],
        ["Proof", "Three to five receipts or a compact method/result line."],
        ["Limit", "Strongest counterpoint, exclusion, and what is not proven."],
        ["Action", "Owner + next step + decision horizon."],
        ["Trace", "Version, commit/ledger/source path, and handling class."],
    ], y, [105, 380])
    c.showPage()

    chrome(c, 12, "INTERNAL")
    y = draw_text(c, "Template: internal staging note", M, H - 88, 485, "head") - 18
    for index, step in enumerate((
        "Artifact target + intended private reader", "Raw inputs / source list / receipts", "Working thesis and open questions",
        "Evidence ledger and claim tiers", "CUT: contradictions, limits, required revisions", "SPLAT mode selection and template choice",
        "Metadata check + release decision: hold / revise / private-ready",
    ), 1):
        c.setFillColor(CUT); c.circle(M + 14, y - 4, 5.4, stroke=0, fill=1)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 6); c.drawCentredString(M + 14, y - 6.3, str(index))
        c.setFillColor(INK); c.setFont("Helvetica", 8.6); c.drawString(M + 30, y - 7, step); y -= 37
    c.showPage()

    chrome(c, 13, "INTERNAL")
    y = draw_text(c, "Metadata passport", M, H - 88, 485, "head") - 16
    draw_table(c, [
        ["Field", "Example", "Why"],
        ["artifact_id", "SYM-PRV-AI7-2026-01", "Stable identity"],
        ["handling", "PUBLIC | PRIVATE | INTERNAL", "Sharing boundary"],
        ["status", "stage | review-ready | sent | released | retired", "Lifecycle"],
        ["splat_mode", "horizon | value | ...", "Primary report lens"],
        ["claim_tier", "established | plausible | conjectural | ornamental", "Epistemic label"],
        ["receipt_manifest", "path / URL / commit / ledger", "Evidence route"],
        ["next_action", "verb + owner + date", "Prevents document drift"],
    ], y, [118, 188, 179])
    c.showPage()

    bullet_page(c, 14, "INTERNAL", "Internal → Private release gates", "Private is not a smaller Internal document. It is a chosen route through an inspected working record.", [
        ("Receipt gate", "Every material proposition points to a source, commit, dataset, email, screenshot, or reproducible result.", PROOF),
        ("CUT gate", "The strongest limitation and salient alternative appear in the private-facing narrative.", CUT),
        ("Reader gate", "Decision, recipient, handling boundary, and next action are clear without internal archaeology.", FIELD),
        ("Trace gate", "Artifact ID, version, metadata, and receipt route survive detachment from the folder or chat.", PURPLE),
    ])

    chrome(c, 15, "APPENDIX")
    y = draw_text(c, "Glossary + source note", M, H - 88, 485, "head") - 12
    y = draw_table(c, [
        ["Term", "Working definition"],
        ["SPLAT Report", "Traceable report with Signal, Proof, Limit, Action, and Trace."],
        ["FIELD", "Context, inputs, and reader orientation."],
        ["PROOF", "Receipt-linked result state, not a universal truth claim."],
        ["CUT", "Limits, invalidity, constraints, and necessary decisions."],
        ["JACK", "Rendering operator for reusable artifact forms."],
        ["JOKER", "Format exception that preserves provenance and limits."],
        ["Value SPLAT", "Pressure test using highlight, midtone, core shadow, and cast shadow."],
    ], y, [135, 350]) - 20
    draw_text(c, "<b>Source note.</b> Perspective vocabulary is adapted as a reporting taxonomy. It does not claim research literally obeys a visual-perspective model. It provides reusable ways to organize context, convergence, evidence, comparison, distance, uncertainty, and pressure.", M, y, 485, "quote")
    c.showPage(); c.save(); return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the Symonic SPLAT Reporting Design Guide.")
    parser.add_argument("--out", type=Path, default=Path("docs/generated/symonic_splat_design_guide_v0_2.pdf"))
    args = parser.parse_args(); print(build(args.out)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
