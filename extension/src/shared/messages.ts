// Messages sent from the side panel to the service worker.
export type PanelToWorker =
  | { type: "PING_PAGE" }
  | { type: "CALL_SERVER"; payload: unknown };

// Messages sent from the service worker to the content script.
export type WorkerToContent = { type: "PING" };

export type PingReply = {
  ok: true;
  title: string;
  url: string; // origin + path only (never query strings)
  elementCount: number;
};
