"""Check that each example JSON file matches its schema.  Run:  python shared/validate_fixtures.py"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).parent / "schemas"
PAIRS = [
    ("page_snapshot.schema.json", "fixtures/page_snapshot.example.json"),
    ("sanitized_context.schema.json", "fixtures/sanitized_context.example.json"),
    ("action_plan.schema.json", "fixtures/action_plan.example.json"),
]

failed = False
for schema_file, fixture_file in PAIRS:
    schema = json.loads((ROOT / schema_file).read_text(encoding="utf-8"))
    data = json.loads((ROOT / fixture_file).read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(data))
    if errors:
        failed = True
        print(f"FAIL  {fixture_file}")
        for e in errors:
            print("   -", "/".join(map(str, e.path)) or "(root)", ":", e.message)
    else:
        print(f"OK    {fixture_file}")

sys.exit(1 if failed else 0)
