import type { WorkerToContent, PingReply } from "../shared/messages";

console.log("[PrivacyAgent] content script loaded on", location.origin + location.pathname);

chrome.runtime.onMessage.addListener((msg: WorkerToContent, _sender, sendResponse) => {
  if (msg.type === "PING") {
    const reply: PingReply = {
      ok: true,
      title: document.title,
      url: location.origin + location.pathname,
      elementCount: document.querySelectorAll("input, button, a, select, textarea").length,
    };
    sendResponse(reply);
  }
  return false; // synchronous reply
});
