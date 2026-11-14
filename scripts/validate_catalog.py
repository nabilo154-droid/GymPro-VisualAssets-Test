#!/usr/bin/env python3
"""Fail-closed validation for the GymPro Visual Lab static catalogue.

This checks manifest/package integrity and the data-only package envelope. The
GymPro Enterprise installer remains the authoritative runtime schema validator.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.json"
ALLOWED_RENDERERS = {"canvas_shader", "svg_vector", "css_micro"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_PACKAGE_FIELDS = {
    "id", "title", "category", "version", "author", "previewType", "safeVectorData"
}
FORBIDDEN_KEYS = {"html", "javascript", "script", "sourcecode", "executable"}


class ValidationError(Exception):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def require_string(obj: dict, key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(f"{label}: required non-empty string '{key}'")
    return value


def validate_catalog() -> int:
    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"Cannot read catalog.json as UTF-8 JSON: {exc}")

    if not isinstance(catalog, dict) or catalog.get("schemaVersion") != 1:
        fail("catalog.json: schemaVersion must be 1")
    require_string(catalog, "catalogVersion", "catalog")
    require_string(catalog, "generatedAt", "catalog")
    assets = catalog.get("assets")
    if not isinstance(assets, list) or not assets:
        fail("catalog.json: assets must be a non-empty array")

    seen_ids: set[str] = set()
    for index, item in enumerate(assets):
        label = f"assets[{index}]"
        if not isinstance(item, dict):
            fail(f"{label}: expected object")
        asset_id = require_string(item, "id", label)
        if asset_id in seen_ids:
            fail(f"{label}: duplicate asset id '{asset_id}'")
        seen_ids.add(asset_id)

        for field in ("title", "category", "version", "author", "description",
                      "previewType", "downloadUrl", "license", "licenseUrl",
                      "attribution", "minAppVersion", "compatibilityStatus",
                      "sourcePlatform", "sourceUrl", "verifiedAt"):
            require_string(item, field, label)

        if item["compatibilityStatus"] != "verified":
            fail(f"{label}: only compatibilityStatus='verified' assets may enter the public catalogue")
        if not ISO_DATE.fullmatch(item["verifiedAt"]):
            fail(f"{label}: verifiedAt must use YYYY-MM-DD")
        source_url = urlparse(item["sourceUrl"])
        if source_url.scheme != "https" or not source_url.netloc:
            fail(f"{label}: sourceUrl must be an HTTPS URL")

        renderer = item["previewType"]
        if renderer not in ALLOWED_RENDERERS:
            fail(f"{label}: unsupported previewType '{renderer}'")
        if not SEMVER.fullmatch(item["version"]) or not SEMVER.fullmatch(item["minAppVersion"]):
            fail(f"{label}: version/minAppVersion must use semver")

        license_url = urlparse(item["licenseUrl"])
        if license_url.scheme != "https" or not license_url.netloc:
            fail(f"{label}: licenseUrl must be an HTTPS URL")

        digest = item.get("sha256")
        if not isinstance(digest, str) or not SHA256.fullmatch(digest):
            fail(f"{label}: sha256 must be 64 lowercase hex characters")
        size = item.get("sizeBytes")
        if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
            fail(f"{label}: sizeBytes must be a positive integer")

        package_url = item["downloadUrl"]
        parsed = urlparse(package_url)
        if parsed.scheme or parsed.netloc or package_url.startswith(("/", "\\\\")):
            fail(f"{label}: downloadUrl must be a repository-relative path")
        if parsed.query or parsed.fragment:
            fail(f"{label}: downloadUrl must not include query or fragment")
        package_path = (ROOT / package_url).resolve()
        assets_root = (ROOT / "assets").resolve()
        if not package_path.is_relative_to(assets_root):
            fail(f"{label}: package path must remain inside assets/")
        if not package_path.is_file():
            fail(f"{label}: package not found: {package_url}")

        raw = package_path.read_bytes()
        actual_size = len(raw)
        actual_digest = hashlib.sha256(raw).hexdigest()
        if actual_size != size:
            fail(f"{label}: sizeBytes mismatch (manifest {size}, actual {actual_size})")
        if actual_digest != digest:
            fail(f"{label}: sha256 mismatch (manifest {digest}, actual {actual_digest})")

        try:
            package = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            fail(f"{label}: package must be UTF-8 JSON: {exc}")
        if not isinstance(package, dict):
            fail(f"{label}: package root must be an object")
        missing = REQUIRED_PACKAGE_FIELDS - package.keys()
        if missing:
            fail(f"{label}: package missing required fields: {', '.join(sorted(missing))}")
        if package["previewType"] not in ALLOWED_RENDERERS:
            fail(f"{label}: package uses unsupported renderer")
        for key in package:
            if key.lower().replace("_", "") in FORBIDDEN_KEYS:
                fail(f"{label}: forbidden executable/source field '{key}'")
        if package["id"] != asset_id:
            fail(f"{label}: manifest/package id mismatch")
        for field in ("title", "category", "version", "author", "previewType"):
            if package[field] != item[field]:
                fail(f"{label}: manifest/package '{field}' mismatch")
        if package["safeVectorData"] is None or not isinstance(package["safeVectorData"], dict):
            fail(f"{label}: safeVectorData must be an object")

        declared_kb = item.get("sizeKb")
        if declared_kb is not None and (
            not isinstance(declared_kb, (int, float)) or declared_kb < actual_size / 1024
        ):
            fail(f"{label}: sizeKb understates actual package size")

    print(f"GymPro Visual Lab catalogue validation passed: {len(assets)} verified asset(s).")
    return len(assets)


if __name__ == "__main__":
    try:
        validate_catalog()
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
