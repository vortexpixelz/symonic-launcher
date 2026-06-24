# Launcher tools

## SPLAT design guide

`create_symonic_design_guide.py` is the maintained source for the **Symonic SPLAT Reporting Design Guide v0.2**.

It was canonicalized from the original internal generator captured at:

```text
/mnt/data/create_symonic_design_guide.py
bytes: 37682
sha256: 3fef63f07bbb488570a849b497bc00fa957586cfeb3a1605e01069f4055ab6a5
```

The committed version removes the original hard-coded output path and accepts an explicit output destination.

### Render locally

```bash
uv run --with reportlab python tools/create_symonic_design_guide.py \
  --out docs/generated/symonic_splat_design_guide_v0_2.pdf
```

For a plain virtual environment:

```bash
python -m pip install reportlab
python tools/create_symonic_design_guide.py \
  --out docs/generated/symonic_splat_design_guide_v0_2.pdf
```

### Verify the result

```bash
python /home/oai/skills/pdfs/scripts/render_pdf.py \
  docs/generated/symonic_splat_design_guide_v0_2.pdf \
  --out_dir /tmp/splat-guide-render \
  --dpi 200
```

Inspect at least the cover, one table page, and the title-page template before sharing a newly generated PDF.

## Related artifacts

- `templates/splat-report.md` - human-facing report scaffold with YAML metadata.
- `schemas/splat-report-0.1.schema.json` - JSON Schema Draft 2020-12 contract for structured SPLAT reports.
- `.github/workflows/render-splat-guide.yml` - renders the guide as a GitHub Actions artifact whenever this toolchain changes.

## Operating boundary

Purple and pale yellow are edition and staging syntax. Blue, green, and red retain the deck’s explicit operational meanings:

```text
FIELD / blue  - context, input, orientation
PROOF / green - structured result state
CUT / red     - limit, invalidity, constraint
```

No color alone can convey a claim tier or evidence state. Templates and schema fields carry that meaning explicitly.
