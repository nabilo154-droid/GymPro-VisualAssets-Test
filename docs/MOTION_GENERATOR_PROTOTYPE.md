# GymPro Motion Generator Prototype

## Purpose

The first prototype adds a constrained local workspace at `generator.html`. It accepts either a short text description or pasted React/TSX/CSS source and creates a candidate package using the existing Aurora-style `canvas_shader` package envelope.

## Safety model

- Pasted source is treated strictly as text and scanned with bounded regular expressions for color tokens and a small set of visual hints.
- No source code is evaluated, imported, rendered, uploaded, or sent to a remote service.
- The output contains only the approved package fields and `safeVectorData.colors` / `safeVectorData.fps`.
- The fixed template and renderer cannot be changed by the pasted source.
- The public catalogue and `catalog.json` are not modified by generating a candidate.
- Downloaded candidate JSON is not automatically verified or publishable.

## Current limitations

This is a deterministic prototype, not an AI/LLM conversion service. It does not semantically understand arbitrary React components, preserve arbitrary animation behavior, or convert unsupported effects. It extracts a small palette and reports recognizable CSS hints, then maps the result into the fixed Aurora template. The preview is a Lab-side approximation and is not evidence of identical output in GymPro Enterprise.

The existing GymPro Enterprise repository currently contains only its controlled-handoff README and does not expose the production renderer implementation or authoritative package schema. Therefore the prototype deliberately exports only the fields already present in the checked-in Aurora package (`previewType`, `safeVectorData.colors`, and `safeVectorData.fps`) and does not invent new runtime parameters such as exported animation speed.

## Next required integration work

1. Obtain the actual GymPro Enterprise renderer source and authoritative package schema.
2. Verify the generated package against that implementation and add shared conformance fixtures.
3. Add source provenance and licence intake fields to a separate review record; never infer a licence from pasted code.
4. Add additional fixed templates only after each renderer contract is verified.
5. If AI-assisted conversion is introduced, keep it behind a trusted server/agent boundary; never expose API credentials in the public static website and never execute generated source.
6. Run reduced-motion, high-DPI, off-screen pause, performance, theme/tone, and layout-resize acceptance checks against the real renderer before marking a candidate verified.

## Manual prototype checks

- Open `generator.html` from the Visual Lab site.
- Generate from a text prompt with no source.
- Paste CSS/TSX containing a few hex colors and animation declarations; verify only color tokens and hint labels are extracted.
- Paste code containing script tags or expressions; verify no code is executed and no network request is made.
- Change preview speed and FPS; verify preview responds while the JSON exports only palette and FPS.
- Download the candidate and confirm it is JSON with the existing Aurora package envelope.
- Confirm the catalogue remains unchanged until a separately reviewed package is published.
