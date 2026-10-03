import type { PanelToWorker } from "../shared/messages";
// Single source of truth: reuse the same fixture file the server tests use.
import sample from "../../../shared/schemas/fixtures/sanitized_context.example.json";

const out = document.getElementById("out") as HTMLPreElement;
const show = (x: unknown) => (out.textContent = JSON.stringify(x, null, 2));

async function send(msg: PanelToWorker) {
  try {
    show(await chrome.runtime.sendMessage(msg));
  } catch (e) {
    show({ ok: false, error: String(e) });
  }
}

document.getElementById("ping")!.addEventListener("click", () => send({ type: "PING_PAGE" }));
document.getElementById("server")!.addEventListener("click", () =>
  send({ type: "CALL_SERVER", payload: sample })
);
