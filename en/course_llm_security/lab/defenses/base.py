"""The defence interface. Every defence in the course is a subclass of Defense.

Sieve calls the hooks at five points of every session:

    on_memory(note, ctx)               each memory entry, before it enters the system prompt
    on_user(text, ctx)                 the user's message, before the model sees it
    on_tool_call(name, args, ctx)      a tool call the model asked for, before it runs
    on_tool_result(name, result, ctx)  a tool's result, before the model sees it
    on_output(text, ctx)               the final answer, before the user (and the UI) sees it

Each hook returns a Verdict:
    Verdict()                                 allow, unchanged
    Verdict("block", reason="...")            stop this item
    Verdict("rewrite", text="...", reason=..) replace it (for on_tool_call: text = new args as JSON)

Keep per-session state in ctx.state (a dict), not on self: one Defense instance
is reused across sessions and repetitions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

ACTIONS = ("allow", "block", "rewrite")


@dataclass
class Verdict:
    action: str = "allow"
    text: Optional[str] = None
    reason: str = ""

    def __post_init__(self):
        if self.action not in ACTIONS:
            raise ValueError(f"Verdict.action must be one of {ACTIONS}, got {self.action!r}")
        if self.action == "rewrite" and self.text is None:
            raise ValueError("a 'rewrite' verdict needs text=")


ALLOW = Verdict()


@dataclass
class Context:
    """What a defence can see. `tainted` becomes True as soon as untrusted content
    (fetch_url or search_docs results, or memory written by the agent) has entered
    the conversation, and never goes back to False within a session."""
    trace: Any                       # the Trace being built (lab.target.Trace)
    secrets: dict                    # {"SYSTEM_CANARY": ..., "FILE_CANARY": ..., "MEMORY_CANARY": ...}
    tainted: bool = False
    tools: frozenset = frozenset()   # the tools enabled for this session
    state: dict = field(default_factory=dict)  # scratch space for defences


class Defense:
    """Base class: allows everything. Override only the hooks you need."""

    @property
    def name(self) -> str:
        return type(self).__name__

    def on_memory(self, note: str, ctx: Context) -> Verdict:
        return ALLOW

    def on_user(self, text: str, ctx: Context) -> Verdict:
        return ALLOW

    def on_tool_call(self, name: str, args: dict, ctx: Context) -> Verdict:
        return ALLOW

    def on_tool_result(self, name: str, result: str, ctx: Context) -> Verdict:
        return ALLOW

    def on_output(self, text: str, ctx: Context) -> Verdict:
        return ALLOW
