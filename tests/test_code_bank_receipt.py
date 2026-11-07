"""Standard-library check that the ArbiScout source bank is present and byte-identical."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "ENGINEERING" / "SOURCE_BANK_20261107_R1"
ACTIVE = ROOT / "ENGINEERING" / "arbiscout_app"

class SourceBankReceiptTest(unittest.TestCase):
    def test_manifest_and_source_capital(self):
        manifest = json.loads((ROOT / "CONTROL_ROOM" / "PROGRAMMA" / "09_SOURCE_BANK_MANIFEST_20261107_R1.json").read_text())
        paths = [p for p in BANK.rglob("*") if p.is_file()]
        self.assertEqual(len(paths), manifest["bank_source_file_count"])
        for name, expected in manifest["reference_git_blobs"].items():
            payload = (BANK / name).read_bytes()
            sha = hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\\0" + payload).hexdigest()
            self.assertEqual(sha, expected, name)
        for name in ("arbiscout.py", "ebay_comparison.py", "run_compare.py", "README.md", "requirements.txt"):
            self.assertEqual((BANK / "active" / name).read_bytes(), (ACTIVE / name).read_bytes(), name)

if __name__ == "__main__":
    unittest.main()
