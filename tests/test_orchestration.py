import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from contextmesh import ContextMesh, ClaudeEvaluator, OpenAIAuditor
from contextmesh.pipeline import HardwareRunner


class TestContextMesh(unittest.TestCase):
    def setUp(self):
        self.mesh = ContextMesh("Test-Project")

    def test_ingest_and_token_count(self):
        t1 = self.mesh.ingest_context("Testing ingestion chunk one.")
        t2 = self.mesh.ingest_context("Testing ingestion chunk two.")
        self.assertGreater(self.mesh.total_context_tokens(), 0)

    def test_multi_agent_evaluation(self):
        self.mesh.ingest_context("Sample media narrative script.")
        claude = ClaudeEvaluator()
        openai = OpenAIAuditor()
        result = self.mesh.assemble_pipeline([claude, openai])
        self.assertTrue(result.validation_passed)
        self.assertEqual(result.status, "completed")
        self.assertEqual(len(result.timeline_chunks), 2)

    def test_hardware_runner(self):
        runner = HardwareRunner(num_workers=2, use_nvenc=True)
        manifest = runner.render_parallel_chunks({"chunks": ["c1", "c2"]})
        self.assertEqual(manifest["total_chunks_processed"], 2)
        self.assertTrue(manifest["lossless_assembly"])


if __name__ == "__main__":
    unittest.main()
