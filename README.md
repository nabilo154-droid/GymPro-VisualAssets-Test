# GymPro Visual Lab

This repository hosts the public, static visual-asset catalogue used by GymPro's optional Online Animation Library.

- Website: https://nabilo154-droid.github.io/GymPro-VisualAssets-Test/
- Manifest: https://nabilo154-droid.github.io/GymPro-VisualAssets-Test/catalog.json
- Packages are versioned JSON data only; no downloaded JavaScript, HTML or arbitrary CSS is executed.
- GymPro verifies HTTPS origin, declared byte size, SHA-256, package schema, licence metadata and minimum app version before installing locally.
- Installed packages are stored locally and remain available offline.

## External component intake (including 21st.dev)

21st.dev is used as a discovery and component-source library, not as a direct trusted animation feed. Retrieved React/TSX/CSS is untrusted source material. A candidate must be manually adapted into a supported GymPro data-only package (`canvas_shader`, `svg_vector`, or `css_micro`) and reviewed for provenance/licensing, reduced motion, performance, high-DPI behavior where relevant, off-screen pausing, theme/tone compatibility, and visual fidelity.

The intake path is:

`Discover → Record source & licence → Adapt → Preview/review → Validate → Publish`

There is no automatic ingestion of raw 21st.dev code and no runtime execution of downloaded source.

## Automated publication gates

Run locally from the repository root:

```sh
python3 scripts/validate_catalog.py
python3 -m unittest discover -s tests -v
```

The validator checks manifest structure, unique asset IDs, allowed renderer IDs, version formats, HTTPS licence URLs, package path containment, exact package byte size and SHA-256, UTF-8 JSON/data-only package envelope, and manifest/package identity consistency. Regression tests exercise the valid package path, hash mismatch refusal, and path traversal refusal.

GitHub Actions runs these checks on pull requests and pushes to `main`. GitHub Pages deployment also runs both checks before assembling or deploying the site. This static validation is a publication gate; GymPro Enterprise remains the final authoritative runtime package-schema validator.

## First-time Pages setup

After merging the website PR, open **Settings → Pages** and set **Build and deployment → Source** to **GitHub Actions** once. The workflow then deploys the site on pushes to `main`. This is a one-time repository setting; the workflow uses the standard `GITHUB_TOKEN` permissions and does not need a personal access token.

## Publishing a new asset

Add the immutable package under `assets/`, update `catalog.json` with its metadata and source/licence attribution, and calculate `sizeBytes` and SHA-256 from the exact final package bytes. Open a pull request; the validator and regression checks must pass before the catalogue is merged and published.
