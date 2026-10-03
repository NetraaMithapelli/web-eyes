from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import CORS_ORIGIN_REGEX, PROTOCOL_VERSION
from .models import Action, ActionPlan, SanitizedContext

app = FastAPI(title="Privacy Agent Server", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=CORS_ORIGIN_REGEX,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "protocol_version": PROTOCOL_VERSION}


@app.post("/plan", response_model=ActionPlan)
def plan(ctx: SanitizedContext) -> ActionPlan:
    """Phase 1 stub: no LLM yet. Click the first button if there is one, else scroll down.
    In Phase 3 this becomes: build prompt -> call LLM -> validate -> return plan."""
    button = next((e for e in ctx.elements if e.tag == "button"), None)
    if button:
        action = Action(type="click", target=button.id)
        thought = f"[stub] Clicking the first button ({button.id})."
    else:
        action = Action(type="scroll", direction="down", amount=400)
        thought = "[stub] No button found, scrolling down."
    return ActionPlan(snapshot_id=ctx.snapshot_id, thought=thought, actions=[action])
