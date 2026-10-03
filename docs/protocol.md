# Redaction Placeholder Protocol v1.0

Contract between the extension (trusted) and the server (untrusted).
Machine-readable versions live in `shared/schemas/`. Examples live in `shared/schemas/fixtures/`.

## Message types
| Message | Direction | Schema | Contains raw PII? |
|---|---|---|---|
| PageSnapshot | content script -> service worker (local only) | `page_snapshot.schema.json` | YES, never sent |
| SanitizedContext | extension -> server | `sanitized_context.schema.json` | NO |
| ActionPlan | server -> extension | `action_plan.schema.json` | NO (placeholders only) |

## Placeholder format
`[TYPE_N]` where TYPE is capital letters and N a counter, e.g. `[EMAIL_1]`, `[PERSON_2]`.
Regex: `\[([A-Z]+)_(\d+)\]`

## Entity types
PERSON, EMAIL, PHONE, ADDRESS, CARD, CVV, OTP, PASSWORD, AADHAAR, PAN, DOB, SECRET, FACE, IMAGE.

| Type | Rehydrated into a `type` action? |
|---|---|
| PERSON, EMAIL, PHONE, ADDRESS, DOB | Yes |
| CARD, AADHAAR, PAN | Only after explicit user confirmation |
| CVV, OTP, PASSWORD, SECRET | Never. The user types these. |

## Rules
1. Same normalized value -> same placeholder within a session.
2. Counters are per type and reset when a new task starts.
3. Placeholders carry no hints (no last-4 digits, no domain).
4. URLs are trimmed to origin + path. Query strings and fragments are dropped.
5. Element IDs (`el_N`) are valid only for the `snapshot_id` they came from.
6. The placeholder -> value mapping (the Vault) never leaves the browser.
7. Fail closed: if the Privacy Gate cannot confirm a payload is clean, nothing is sent.
8. Submitting, paying, or typing CARD/AADHAAR/PAN requires explicit user confirmation.

## Action types
`click`, `type`, `select`, `scroll`, `wait`, `ask_user`, `answer`. See `action_plan.schema.json` for fields and limits.

## Outbound invariants (become leak tests in Phase 6)
- I1: no Vault value appears anywhere in the outbound request.
- I2: no PII regex match appears in the outbound body.
- I3: the screenshot has no unredacted pixels inside any recorded redaction box.
- I4: only the service worker calls the server.
- I5: a blocked request is logged and the user is notified.
