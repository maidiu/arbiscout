"""CI guard: the 54-source treatment inventory and dashboard remain synchronized."""
from pathlib import Path
import subprocess
import sys
import unittest

REPO = Path(__file__).resolve().parents[1]
VALIDATOR = REPO / "CONTROL_ROOM/RETAILER_EXPANSION/20261117_R1/scripts/validate_and_render.py"

class RetailerTreatmentWorkroomTest(unittest.TestCase):
    def test_all_54_sources_have_coherent_ledger_and_dashboard(self):
        self.assertTrue(VALIDATOR.is_file())
        completed = subprocess.run(
            [sys.executable, str(VALIDATOR), "--check"], cwd=str(REPO),
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("54 treatment files", completed.stdout)

if __name__ == "__main__":
    unittest.main()
