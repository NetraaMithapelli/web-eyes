import { SERVER_URL } from "../shared/constants";
import type { PanelToWorker, WorkerToContent } from "../shared/messages";

// Open the side panel when the toolbar icon is clicked.
chrome.sidePanel
  .setPanelBehavior({ openPanelOnActionClick: true })
  .catch((e) => console.error("sidePanel behavior error", e));

chrome.runtime.onMessage.addListener((msg: PanelToWorker, _sender, sendResponse) => {
  handle(msg)
    .then(sendResponse)
    .catch((e) => sendResponse({ ok: false, error: String(e) }));
  return true; // keep the channel open for the async response
});

async function activeTabId(): Promise<number> {
  const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
  if (!tab?.id) throw new Error("No active tab found");
  return tab.id;
}

async function handle(msg: PanelToWorker) {
  switch (msg.type) {
    case "PING_PAGE": {
      const tabId = await activeTabId();
      const out: WorkerToContent = { type: "PING" };
      return await chrome.tabs.sendMessage(tabId, out);
    }
    case "CALL_SERVER": {
      // In later phases this becomes api-client.ts: the ONLY place that calls the server.
      const res = await fetch(`${SERVER_URL}/plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(msg.payload),
      });
      if (!res.ok) throw new Error(`Server returned ${res.status}: ${await res.text()}`);
      return { ok: true, data: await res.json() };
    }
  }
}
