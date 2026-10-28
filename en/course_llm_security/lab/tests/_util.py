"""Shared helpers for the lab self-tests. The tests ALWAYS use the mock model."""
import os
import unittest

os.environ["LLM_BASE_URL"] = "mock"   # never hit a real model from the self-tests

from lab import paths, servers, setup_lab  # noqa: E402

# Base URLs (ports follow LAB_*_PORT if you moved them; the default is 8765/8766/8760).
WEB = f"http://127.0.0.1:{paths.WEB_PORT}"
ATK = f"http://127.0.0.1:{paths.ATTACKER_PORT}"
UI_HOST = f"127.0.0.1:{paths.UI_PORT}"


class LabTest(unittest.TestCase):
    """Fresh lab before every test; web + attacker servers running."""

    @classmethod
    def setUpClass(cls):
        servers.ensure_running()

    def setUp(self):
        self.secrets = setup_lab.setup()

    def plant_page(self, name: str, body: str) -> str:
        setup_lab.plant({f"web/{name}": body})
        return f"{WEB}/{name}"
