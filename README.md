# Privacy-Preserving Browser Agent

A Chrome extension that lets an LLM agent help with web tasks while raw page content and PII never leave the browser.
Only placeholders such as `[EMAIL_1]` and a redacted screenshot are sent to the server.

**Status:** Phase 1 (setup and contracts) complete.

## Layout
- `extension/` Chrome MV3 extension (TypeScript, built with esbuild)
- `server/` FastAPI server
- `shared/` JSON schemas and example fixtures (the contract)
- `test-pages/` mock pages with fake PII
- `docs/` protocol and diagrams
- `eval/` evaluation code (Phase 6)

## Run it
**Server**
```
cd server
python -m venv .venv
.venv\Scripts\activate          # Windows   (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
**Extension**
```
cd extension
npm install
npm run build
```
Then open `chrome://extensions`, enable Developer mode, click Load unpacked, and choose `extension/dist`.

**Test pages**
```
cd test-pages
python -m http.server 5500
```
Open `http://localhost:5500/signup.html`, click the extension icon to open the side panel, and press the two buttons.

## Tests
```
python shared/validate_fixtures.py     # fixtures match schemas
cd server && pytest                    # server tests
cd extension && npm run typecheck
```
