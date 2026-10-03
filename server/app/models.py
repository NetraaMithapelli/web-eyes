"""Pydantic models that mirror shared/schemas/*.schema.json (protocol v1.0)."""
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class Strict(BaseModel):
    # Reject unknown fields, same as additionalProperties=false in the JSON schemas.
    model_config = ConfigDict(extra="forbid")


class Viewport(Strict):
    w: int
    h: int


class Scroll(Strict):
    y: int
    max_y: int


class Page(Strict):
    origin: str
    path: str
    title: str = ""
    viewport: Viewport
    scroll: Scroll


class Element(Strict):
    id: str = Field(pattern=r"^el_\d+$")
    tag: str
    type: Optional[str] = None
    label: Optional[str] = None
    text: Optional[str] = None
    value: Optional[str] = None
    required: bool = False


class TextBlock(Strict):
    id: str
    text: str


class Redaction(Strict):
    type: str
    placeholder: str = Field(pattern=r"^\[[A-Z]+_\d+\]$")
    box: list[int] = Field(min_length=4, max_length=4)


class Screenshot(Strict):
    mime: Literal["image/jpeg", "image/webp", "image/png"]
    b64: str
    redactions: list[Redaction] = []


class SanitizedContext(Strict):
    protocol_version: Literal["1.0"]
    session_id: str
    snapshot_id: str = Field(pattern=r"^snap_\d+$")
    step: int = Field(ge=1)
    goal: str
    page: Page
    elements: list[Element]
    text_blocks: list[TextBlock] = []
    screenshot: Optional[Screenshot] = None
    redaction_summary: dict[str, int] = {}
    vault_fields_available: list[str] = []


class Action(Strict):
    type: Literal["click", "type", "select", "scroll", "wait", "ask_user", "answer"]
    target: Optional[str] = Field(default=None, pattern=r"^el_\d+$")
    value: Optional[str] = None
    direction: Optional[Literal["up", "down"]] = None
    amount: Optional[int] = Field(default=None, ge=1, le=2000)
    ms: Optional[int] = Field(default=None, ge=1, le=3000)
    question: Optional[str] = None
    text: Optional[str] = None


class ActionPlan(Strict):
    protocol_version: Literal["1.0"] = "1.0"
    snapshot_id: str
    thought: str = ""
    actions: list[Action]
    needs_user_confirmation: bool = False
    done: bool = False
    answer: Optional[str] = None
