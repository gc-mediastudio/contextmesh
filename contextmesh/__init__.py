"""
ContextMesh Core: High-Horizon Multi-Agent Orchestration Engine
Developed by GC (Generative Creative) Media Studio
"""

__version__ = "0.1.0"
__author__ = ""

from .core import ContextMesh, AgentMessage, ExecutionResult
from .evaluators.anthropic_claude import ClaudeEvaluator
from .evaluators.openai_auditor import OpenAIAuditor

__all__ = [
    "ContextMesh",
    "AgentMessage",
    "ExecutionResult",
    "ClaudeEvaluator",
    "OpenAIAuditor",
]
