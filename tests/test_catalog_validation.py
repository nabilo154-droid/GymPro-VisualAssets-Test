import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_catalog.py"


class CatalogValidatorTests(unittest.TestCase):
    def run_validator(self, root: Path) -> subprocess.CompletedProcess:
        (root / "scripts").mkdir(exist_ok=True)
        target = root / "scripts" / "validate_catalog.py"
        target.write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")
        return subprocess.run([sys.executable, str(target)], capture_output=True, text=True)

    def seed(self, root: Path):
        (root / "assets").mkdir(exist_ok=True)
        package = {
            "id": "sample_motion", "title": "Sample Motion", "category": "background",
            "version": "1.0.0", "author": "GymPro", "previewType": "canvas_shader",
            "safeVectorData": {"colors": ["#123456"], "fps": 30}
        }
        raw = json.dumps(package, separators=(",", ":")).encode()
        (root / "assets" / "sample.v1.json").write_bytes(raw)
        catalog = {
            "schemaVersion": 1, "catalogVersion": "1.0.0",
            "generatedAt": "2026-01-01T00:00:00Z",
            "assets": [{
                **package, "description": "Test asset", "license": "CC0-1.0",
                "licenseUrl": "https://creativecommons.org/publicdomain/zero/1.0/",
                "attribution": "Original", "minAppVersion": "2.5.0",
                "sizeBytes": len(raw), "sizeKb": 1,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "downloadUrl": "assets/sample.v1.json"
            }]
        }
        (root / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

    def test_valid_catalog_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.seed(root)
            result = self.run_validator(root)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_hash_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.seed(root)
            catalog = json.loads((root / "catalog.json").read_text())
            catalog["assets"][0]["sha256"] = "0" * 64
            (root / "catalog.json").write_text(json.dumps(catalog))
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("sha256 mismatch", result.stderr)

    def test_path_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.seed(root)
            catalog = json.loads((root / "catalog.json").read_text())
            catalog["assets"][0]["downloadUrl"] = "../catalog.json"
            (root / "catalog.json").write_text(json.dumps(catalog))
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("inside assets", result.stderr)


if __name__ == "__main__":
    unittest.main()
