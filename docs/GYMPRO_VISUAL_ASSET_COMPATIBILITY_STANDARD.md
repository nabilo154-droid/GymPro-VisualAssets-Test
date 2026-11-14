# GymPro Visual Asset Compatibility Standard

**Purpose:** assets discovered from external design and component sources (including 21st.dev) must be adapted and verified before being published in GymPro Visual Lab or offered to GymPro Enterprise.

## Source and intake

21st.dev is a discovery and UI-component source, not a direct trusted GymPro animation feed. The authenticated MCP/CLI connection is used by the agent/operator to search and retrieve selected source material; the static public website never stores an API key or calls authenticated MCP from visitor browsers. Retrieved React/TSX/CSS code is untrusted source material. No downloaded source is copied into the public catalogue as-is and no external JavaScript, HTML, arbitrary CSS, remote iframe, or dependency bundle is executed by GymPro.

For each candidate, record:
- Source URL and source component/asset identity
- Original author/creator
- License identifier, license URL, and attribution obligations
- Intake date and adaptation notes
- Target GymPro renderer and minimum app version

Candidates without verifiable licensing/provenance or compatible terms are rejected. Public catalogue entries must declare `compatibilityStatus: "verified"`, `sourcePlatform`, `sourceUrl` (HTTPS), and `verifiedAt` (YYYY-MM-DD); the validator rejects missing provenance or any non-verified status.

## Required compatibility review

### Runtime and security
- Convert candidates into supported data-only package formats: `canvas_shader`, `svg_vector`, or `css_micro`.
- No eval/dynamic code execution, arbitrary HTML/JS, external iframe, or unreviewed remote resource dependency.
- Validate schema, renderer allowlist, package byte size, SHA-256, and minimum app version.
- Fail closed: any missing or failed required validation blocks publication.

### Performance
- Respect a documented CPU/frame budget; avoid unbounded loops, expensive per-frame work, excessive particles, and unnecessary redraws.
- Use request/render lifecycle appropriately and pause when off-screen or inactive where the renderer supports it.
- Use high-DPI-aware dimensions and scaling when relevant without uncontrolled backing-buffer growth.
- Preserve intended appearance while optimizing implementation.

### Accessibility and user control
- Support `prefers-reduced-motion` or GymPro reduced-motion controls; provide a reduced/static state when applicable.
- Motion must not flash dangerously or create disorienting rapid transitions.
- Preview and installation are separate user actions; downloading must never auto-apply an asset.

### Theme and layout
- Adapt colors, contrast, and surface styling to GymPro Base Theme and Integrated Studio Canvas Tone.
- Frosted-glass surfaces must respond to the current theme/tone rather than remain hard-coded black or white.
- Test light/dark themes, relevant canvas tones, layout resizing, and supported display densities.

## Publication pipeline

1. **Discover** — search 21st.dev or other documented sources.
2. **Intake** — preserve source metadata and licensing.
3. **Adapt** — rewrite into the supported GymPro data-only renderer/package format.
4. **Validate** — run schema, renderer, integrity, licensing, accessibility, performance, theme and compatibility checks.
5. **Preview** — inspect in a representative GymPro-compatible preview, including reduced motion and theme variants.
6. **Publish** — add immutable versioned package and catalogue metadata only after all required checks pass.
7. **Maintain** — revalidate when renderer, standards, source license, or package is changed.

## Catalogue entry minimums

A verified catalogue record should include unique ID, title (and Arabic title where available), category, version, author, descriptive text, preview type, exact package byte size, SHA-256, download URL, license ID/URL, attribution, and minimum GymPro app version.

## Acceptance gate

A candidate is listed in the public website as **verified** only when:
- Source and license are documented and compatible.
- It uses an allowed data-only renderer and schema.
- Integrity values match the final exact package bytes.
- Reduced-motion, performance, high-DPI (where relevant), theme and layout checks are complete.
- The visual result is reviewed and does not materially regress the intended source appearance.

This standard governs the GymPro Visual Lab catalogue. Discovery from 21st.dev does not imply automatic approval or direct live ingestion.
