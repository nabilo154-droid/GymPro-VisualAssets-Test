# GymPro Visual Lab

This repository hosts the public, static visual-asset catalogue used by GymPro's optional Online Animation Library.

- Website: https://nabilo154-droid.github.io/GymPro-VisualAssets-Test/
- Manifest: https://nabilo154-droid.github.io/GymPro-VisualAssets-Test/catalog.json
- Packages are versioned JSON data only; no downloaded JavaScript, HTML or arbitrary CSS is executed.
- GymPro verifies HTTPS origin, declared byte size, SHA-256, package schema, licence metadata and minimum app version before installing locally.
- Installed packages are stored locally and remain available offline.

## First-time Pages setup

After merging the website PR, open **Settings → Pages** and set **Build and deployment → Source** to **GitHub Actions** once. The workflow then deploys the site on pushes to `main`. This is a one-time repository setting; the workflow uses the standard `GITHUB_TOKEN` permissions and does not need a personal access token.

## Publishing a new asset

Update `catalog.json` and add the referenced immutable package under `assets/`. Calculate `sizeBytes` and SHA-256 from the exact final package bytes before publishing the manifest.
