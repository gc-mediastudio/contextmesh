"""
ContextMesh Core State Machine and Agent Coordinator
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import time


@dataclass
class AgentMessage:
    role: str
    content: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionResult:
    status: str
    timeline_chunks: List[Dict[str, Any]]
    total_tokens_evaluated: int
    validation_passed: bool
    summary: str


class ContextMesh:
    """
    Orchestrates sequential and parallel evaluations across Anthropic Claude
    and OpenAI models for long-horizon narrative and media timelines.
    """

    def __init__(self, project_name: str = "GC-Media-Production"):
        self.project_name = project_name
        self.history: List[AgentMessage] = []
        self.manifest: Dict[str, Any] = {}

    def ingest_context(self, text_payload: str, metadata: Optional[Dict[str, Any]] = None) -> int:
        """
        Ingests high-volume narrative payload or transcript chunks.
        Returns estimated token horizon.
        """
        meta = metadata or {}
        # Rough token approximation (1 token ~= 4 chars)
        token_estimate = max(1, len(text_payload) // 4)
        msg = AgentMessage(
            role="ingest",
            content=text_payload,
            metadata={"token_estimate": token_estimate, **meta}
        )
        self.history.append(msg)
        return token_estimate

    def total_context_tokens(self) -> int:
        return sum(m.metadata.get("token_estimate", 0) for m in self.history)

    def assemble_pipeline(self, evaluators: List[Any]) -> ExecutionResult:
        """
        Dispatches multi-agent verification passes across registered evaluators.
        """
        total_tokens = self.total_context_tokens()
        results = []
        all_passed = True

        for evaluator in evaluators:
            res = evaluator.evaluate(self.history)
            results.append(res)
            if not res.get("passed", True):
                all_passed = False

        return ExecutionResult(
            status="completed" if all_passed else "flagged",
            timeline_chunks=results,
            total_tokens_evaluated=total_tokens,
            validation_passed=all_passed,
            summary=f"ContextMesh evaluated {len(evaluators)} passes across {total_tokens:,} tokens."
        )
