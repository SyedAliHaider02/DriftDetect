
import json
from pathlib import Path

from backend.analyzer import compare_environments


dev_path = Path("examples/development.json")
prod_path = Path("examples/production.json")

with dev_path.open(encoding="utf-8") as file:
    development = json.load(file)

with prod_path.open(encoding="utf-8") as file:
    production = json.load(file)

findings = compare_environments(development, production)

if not findings:
    print("No differences found in the collected fields.")
else:
    print(f"Found {len(findings)} difference(s):\n")

    for finding in findings:
        print(
            f"[{finding['severity'].upper()}] "
            f"{finding['category']} - {finding['item']}"
        )
        print(f"  Development: {finding['development_value']}")
        print(f"  Production:  {finding['production_value']}")
        print(f"  Explanation: {finding['message']}")
        print()
