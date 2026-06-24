# CARRY CASCADE

## An algorithmic philosophy for the Symonic SPLAT cover

> **Form is part of the proof.**

Carry Cascade is not a logo generator. It is a browser-native instrument for producing deterministic SPLAT report covers: each seeded cover records a propagation event, from a localized and coherent onset through asymmetric downstream debasement to a visible limit.

## Operating claim

A splat is a **propagation event**. One signal originates at a clean point, travels through a resisting field, sheds coherence downstream, and is cut at the limit. The image is a visual argument for how a claim can begin cleanly and decay as it travels.

## Visual grammar

| Element | Rendered behavior | SPLAT meaning |
| --- | --- | --- |
| Origin / body | Dense, localized mass with a crisp onset | Traceable source or lesion site |
| Downstream fingers | Viscous tendrils biased along one seeded axis | Propagation rather than radial decoration |
| Debasement | Fingers thin, wander, fragment, and shed droplets with distance | Loss of confidence, fidelity, or provenance |
| Ternary tone | Shadow / mid / highlight assigned as discrete tonal families | Quiet `{−1, 0, +1}` structure rather than a flat fill |
| Satellites / spray | Scattered droplets concentrated downstream | Downstream scatter and secondary contamination |
| Cut hairline | Type-color draughtsman's line with ticks | The explicit limit of a report or claim |
| Optional lattice | Perspective lines converging to a vanishing point | An optional reporting lens, never required ritual |
| Grain | Fine print tooth over the completed artifact | Objecthood, handling, and the printed-report contract |

## Determinism contract

- `seed` drives p5 random and noise state at every render.
- The spread helper uses a local, seed-stable sum-of-uniforms implementation rather than `randomGaussian()`, whose hidden state can produce cross-render drift.
- A seed therefore represents an **edition**: the same incident under the same physics.
- Canvas output is 1280 × 1600 at `pixelDensity(2)`, producing a high-resolution 4:5 PNG export.

## Palette firewall

The cover surface is an **edition plane**, not an evidence rail. Its available preset family intentionally excludes blue, green, and red semantic-evidence palettes.

| Edition | Ground | Splat | Type / cut |
| --- | --- | --- | --- |
| Cover | `#1e1c1a` | `#6e4aa6` | `#e9dfa3` |
| Amber | `#111009` | `#c97e08` | `#f2e4c4` |
| Receipt | `#1a1917` | `#9a9890` | `#e7e4da` |

That separation is intentional: visual evidence semantics belong in a different rendering rail and must not leak into title-page edition language.

## Controls

- **Seed:** reproducible edition number, with previous, next, and random navigation.
- **Spread / body mass:** scale and density of the onset field.
- **Finger count / reach:** quantity and length of propagation channels.
- **Turbulence / cascade:** directional instability and rate of downstream debasement.
- **Satellite scatter / grain:** secondary droplets and print tooth.
- **Furniture toggles:** full cover, clean splat-only export, cut line, and optional perspective lattice.

## Module boundary

- **Runtime entry point:** `index.html`
- **External dependency:** p5.js 1.7.0 through CDN
- **Fonts:** Syne, IBM Plex Mono, and Lora through Google Fonts
- **No build step:** open in a browser or mount in a future launcher webview.

The algorithm is the plate. The seed is the pull.
