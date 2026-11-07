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
            sha = hashlib.sha1(b"blob " + str(len(payload)).encode() + bytes([0]) + payload).hexdigest()
            self.assertEqual(sha, expected, name)
        # The dated archive is immutable and independently checked against Git blob SHAs.
        # The current active app can legitimately evolve beyond that historical bank.
        self.assertTrue((ACTIVE / "run_test.py").is_file())

if __name__ == "__main__":
    unittest.main()
