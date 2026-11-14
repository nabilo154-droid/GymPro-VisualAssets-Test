# GymPro Visual Lab

This repository hosts the public, static visual-asset catalogue used by GymPro's optional Online Animation Library.

- Website: https://nabilo154-droid.github.io/GymPro-VisualAssets-Test/
- Manifest: https://nabilo154-droid.github.io/GymPro-VisualAssets-Test/catalog.json
- Packages are versioned JSON data only; no downloaded JavaScript, HTML or arbitrary CSS is executed.
- GymPro verifies HTTPS origin, declared byte size, SHA-256, package schema, licence metadata and minimum app version before installing locally.
- Installed packages are stored locally and remain available offline.

The Pages workflow deploys the website and the same manifest/package files from the repository root. Update `catalog.json` and add the referenced immutable package under `assets/` when publishing a new asset.
