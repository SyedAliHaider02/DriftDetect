import argparse
import json
import platform
import sys

from datetime import datetime, timezone
from importlib.metadata import distributions
from pathlib import Path


def collect_environment(environment_name):
    """Collect basic information about the current Python environment."""

    # Collect installed package names and versions.
    packages = {}

    for package in distributions():
        name = package.metadata.get("Name")

        if name:
            packages[name.lower()] = package.version

    # Check selected configuration variables without reading their values.
    selected_variables = [
        "DATABASE_URL",
        "GROQ_API_KEY",
        "API_BASE_URL",
    ]

    configuration_presence = {
        name: name in __import__("os").environ
        for name in selected_variables
    }

    # Create the environment report.
    report = {
        "environment_name": environment_name,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "packages": dict(sorted(packages.items())),
        "configuration_presence": configuration_presence,
    }

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Collect environment information for DriftDetect."
    )

    parser.add_argument(
        "--output",
        default="environment.json",
        help="Path where the JSON report will be saved.",
    )

    parser.add_argument(
        "--name",
        default="unspecified",
        help="Environment label, such as development or production.",
    )

    args = parser.parse_args()

    report = collect_environment(args.name)

    output_path = Path(args.output)

    # Do not accidentally overwrite an existing report.
    if output_path.exists():
        parser.error(
            f"{output_path} already exists. Choose a different filename."
        )

    # Create the output directory if necessary.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the report as readable JSON.
    with output_path.open("x", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("Environment report created successfully.")
    print(f"Environment: {args.name}")
    print(f"Python version: {report['python_version']}")
    print(f"Installed packages: {len(report['packages'])}")
    print(f"Saved to: {output_path.resolve()}")


if __name__ == "__main__":
    main()
