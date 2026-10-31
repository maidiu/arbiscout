import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_programma import check_registry


class TestProgramma(unittest.TestCase):
    def test_graph_and_source_registry(self):
        self.assertEqual(check_registry(), [])

    def test_hq_read_first_exists(self):
        self.assertTrue((ROOT / "CONTROL_ROOM" / "00_READ_ME_FIRST.md").is_file())

    def test_programma_exists(self):
        self.assertTrue((ROOT / "CONTROL_ROOM" / "PROGRAMMA" / "00_PROGRAMMA_ARBISCOUT.md").is_file())


if __name__ == "__main__":
    unittest.main()
