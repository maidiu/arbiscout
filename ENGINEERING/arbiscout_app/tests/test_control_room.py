import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import control_room


class ControlRoomTests(unittest.TestCase):
    def test_env_roundtrip_and_clear(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / ".env"
            path.write_text("A=1\nB=2\n", encoding="utf-8")
            control_room.write_env({"A": "3", "C": "4"}, ["B"], path=path)
            values = control_room.read_env(path)
            self.assertEqual(values, {"A": "3", "C": "4"})
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_job_commands_exist(self):
        for job in ("bestbuy", "dell", "lego", "meh", "woot", "kroger", "catalog"):
            command = control_room.command_for(job)
            self.assertIsInstance(command, list)
            self.assertGreater(len(command), 1)

    def test_kroger_command_uses_per_run_zip(self):
        command = control_room.command_for("kroger", "29072")
        self.assertIn("--zip", command)
        self.assertIn("29072", command)
        self.assertNotIn("--zip", control_room.command_for("kroger"))


if __name__ == "__main__":
    unittest.main()
