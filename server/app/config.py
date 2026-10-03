import os

PROTOCOL_VERSION = "1.0"
# Origins allowed to call the server: the extension and local test pages.
CORS_ORIGIN_REGEX = r"^(chrome-extension://.*|http://localhost(:\d+)?|http://127\.0\.0\.1(:\d+)?)$"
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "")
LLM_MODEL = os.getenv("LLM_MODEL", "")
