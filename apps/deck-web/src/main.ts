import "./styles.css";

type DeckKind = "field" | "proof" | "cut";
type RunStatus = "valid" | "invalid" | "overflow";

type Provenance = {
  adapter: string;
  operation: string;
  note: string;
};

type DeckSegment = {
  kind: DeckKind;
  label: string;
  text: string;
  semantic: "context" | "result" | "constraint";
  provenance: Provenance;
};

type McoreResponse = {
  operation: string;
  status: RunStatus;
  valid: boolean;
  segments: DeckSegment[];
  data: Record<string, unknown>;
};

const escapeHtml = (value: string): string =>
  value.replace(/[&<>'"]/g, (character) => {
    const entities: Record<string, string> = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      "'": "&#039;",
      '"': "&quot;",
    };
    return entities[character];
  });

const responseCard = (response: McoreResponse): string => {
  const segments = response.segments
    .map(
      (segment) => `
        <section class="segment segment--${segment.kind}" data-deck-kind="${segment.kind}">
          <div class="segment__topline">
            <span class="segment__kind" aria-label="${segment.kind} channel">${escapeHtml(segment.label)}</span>
            <span class="segment__semantic">${escapeHtml(segment.semantic)}</span>
          </div>
          <p>${escapeHtml(segment.text)}</p>
          <small>${escapeHtml(segment.provenance.adapter)} · ${escapeHtml(segment.provenance.note)}</small>
        </section>`,
    )
    .join("");

  return `
    <article class="response-card" aria-live="polite">
      <header class="response-card__header">
        <div>
          <p class="eyebrow">${escapeHtml(response.operation)}</p>
          <h2>${escapeHtml(response.status.toUpperCase())}</h2>
        </div>
        <span class="status status--${response.valid ? "valid" : "constraint"}">
          ${response.valid ? "VALID" : "CONSTRAINT"}
        </span>
      </header>
      <div class="segments">${segments}</div>
      <details class="raw-data">
        <summary>Structured response</summary>
        <pre>${escapeHtml(JSON.stringify(response.data, null, 2))}</pre>
      </details>
    </article>`;
};

const mount = document.querySelector<HTMLElement>("#app");
if (!mount) throw new Error("Application mount not found.");

mount.innerHTML = `
  <div class="shell">
    <aside class="rail" aria-label="Deck channels">
      <a class="wordmark" href="#top">SYMONIC<br />DECK</a>
      <nav>
        <a href="#control">CONTROL</a>
        <a href="#response">RESPONSE</a>
        <a href="#contract">CONTRACT</a>
      </nav>
      <div class="rail__legend">
        <p><span class="dot dot--field"></span> FIELD / blue</p>
        <p><span class="dot dot--proof"></span> PROOF / green</p>
        <p><span class="dot dot--cut"></span> CUT / red</p>
      </div>
    </aside>

    <main class="document" id="top">
      <header class="masthead">
        <p class="eyebrow">JACK · RENDERING SURFACE · 0.1.0</p>
        <h1>Make the response<br /><em>legible.</em></h1>
        <p class="dek">A small control panel for rendering MCORE-1 output as an evidence-bearing document rather than an anonymous JSON puddle.</p>
      </header>

      <section class="control-card" id="control" aria-labelledby="control-title">
        <div>
          <p class="eyebrow">MCORE-1 / DIRECT ADAPTER</p>
          <h2 id="control-title">Validate a metrical pattern</h2>
        </div>
        <form id="run-form">
          <label for="pattern">Pattern</label>
          <div class="input-row">
            <input id="pattern" name="pattern" value="01" autocomplete="off" spellcheck="false" />
            <button type="submit">Run</button>
          </div>
          <div class="sample-row" aria-label="Sample patterns">
            <button type="button" data-sample="01">valid: 01</button>
            <button type="button" data-sample="22">overflow: 22</button>
          </div>
        </form>
      </section>

      <section class="response-section" id="response" aria-labelledby="response-title">
        <div class="section-heading">
          <p class="eyebrow">RESPONSE CARD</p>
          <h2 id="response-title">Awaiting a run.</h2>
        </div>
        <div id="response-root" class="response-root">
          <p class="empty-state">The color channels will appear beside explicit labels, source notes, and raw structured output.</p>
        </div>
      </section>

      <section class="contract" id="contract">
        <p class="eyebrow">OPENAPI / RECEIPT</p>
        <p><code>POST /api/v1/mcore/validate-pattern</code> returns typed display segments. Color is a rendering convention, never a claim classifier.</p>
        <a href="/api/v1/docs" target="_blank" rel="noreferrer">Open API documentation ↗</a>
        <a href="/lab" target="_blank" rel="noreferrer">Open Gradio lab ↗</a>
      </section>
    </main>
  </div>`;

const form = document.querySelector<HTMLFormElement>("#run-form");
const patternInput = document.querySelector<HTMLInputElement>("#pattern");
const responseRoot = document.querySelector<HTMLElement>("#response-root");
const responseTitle = document.querySelector<HTMLElement>("#response-title");

if (!form || !patternInput || !responseRoot || !responseTitle) {
  throw new Error("Control panel elements are missing.");
}

async function runPattern(pattern: string): Promise<void> {
  responseRoot.innerHTML = '<p class="empty-state">Running MCORE-1 validation…</p>';
  responseTitle.textContent = "Rendering the result.";

  try {
    const request = await fetch("/api/v1/mcore/validate-pattern", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ pattern }),
    });
    if (!request.ok) throw new Error(`API returned ${request.status}`);

    const response = (await request.json()) as McoreResponse;
    responseTitle.textContent = response.valid ? "Conservation holds." : "A boundary appeared.";
    responseRoot.innerHTML = responseCard(response);
  } catch (error) {
    responseTitle.textContent = "The adapter is unavailable.";
    responseRoot.innerHTML = `<p class="error-state">${escapeHtml(error instanceof Error ? error.message : "Unknown request failure")}</p>`;
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const pattern = patternInput.value.trim();
  if (pattern) void runPattern(pattern);
});

document.querySelectorAll<HTMLButtonElement>("[data-sample]").forEach((button) => {
  button.addEventListener("click", () => {
    const sample = button.dataset.sample;
    if (!sample) return;
    patternInput.value = sample;
    void runPattern(sample);
  });
});
