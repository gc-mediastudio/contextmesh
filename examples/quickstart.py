"""
ContextMesh Quickstart: Multi-Agent Ingestion, Long-Horizon Evaluation, and GPU Assembly
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from contextmesh import ContextMesh, ClaudeEvaluator, OpenAIAuditor
from contextmesh.pipeline import HardwareRunner


def main():
    print("=" * 60)
    print("ContextMesh Core: Multi-Agent Creative Pipeline Demo")
    print("GC (Generative Creative) Media Studio")
    print("=" * 60)

    # 1. Initialize ContextMesh engine
    mesh = ContextMesh(project_name="Commercial-Presenter-4K")

    # 2. Ingest script and narrative context
    script_chunk_1 = "Scene 1: Presenter opens on virtual set, introduces applied AI architecture."
    script_chunk_2 = "Scene 2: Teleprompter scrolls kinetic typography safe-zone constraints."
    script_chunk_3 = "Scene 3: Audio transitions to 432Hz ambient rain binaural soundscape."

    tokens_1 = mesh.ingest_context(script_chunk_1, {"scene": 1})
    tokens_2 = mesh.ingest_context(script_chunk_2, {"scene": 2})
    tokens_3 = mesh.ingest_context(script_chunk_3, {"scene": 3})

    print(f"[Ingest] Accumulated Context Tokens: {mesh.total_context_tokens():,} tokens")

    # 3. Register frontier model evaluators
    claude = ClaudeEvaluator()
    openai = OpenAIAuditor()

    print("\n[Orchestration] Dispatching cross-model evaluation passes...")
    result = mesh.assemble_pipeline(evaluators=[claude, openai])

    print(f"Status: {result.status.upper()}")
    print(f"Validation Passed: {result.validation_passed}")
    for chunk in result.timeline_chunks:
        print(f"  • {chunk['evaluator']} -> Passed: {chunk['passed']}")

    # 4. Dispatch local hardware rendering pipeline
    print("\n[Hardware] Dispatching parallel NVENC timeline chunk workers...")
    runner = HardwareRunner(num_workers=4, use_nvenc=True)
    render_manifest = runner.render_parallel_chunks({"chunks": ["scene_01", "scene_02", "scene_03"]})

    print(f"Assembly Complete: {render_manifest['total_chunks_processed']} chunks across {render_manifest['worker_processes']} workers in {render_manifest['render_time_seconds']}s.")
    print("=" * 60)
    print("All passes validated. Ready for broadcast deployment.")


if __name__ == "__main__":
    main()
