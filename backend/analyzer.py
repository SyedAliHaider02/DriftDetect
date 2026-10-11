
from packaging.version import InvalidVersion, Version


def compare_environments(development, production):
    """Compare two environment reports and return structured findings."""

    findings = []

    def add_finding(category, item, dev_value, prod_value,
                    severity, message):
        findings.append({
            "category": category,
            "item": item,
            "development_value": dev_value,
            "production_value": prod_value,
            "severity": severity,
            "message": message,
        })

    # 1. Compare Python versions.
    dev_python = development.get("python_version")
    prod_python = production.get("python_version")

    if dev_python != prod_python:
        add_finding(
            "runtime",
            "python_version",
            dev_python,
            prod_python,
            "medium",
            "Python versions differ. Check runtime compatibility."
        )

    # 2. Compare operating systems.
    dev_os = development.get("os")
    prod_os = production.get("os")

    if dev_os != prod_os:
        add_finding(
            "operating_system",
            "os",
            dev_os,
            prod_os,
            "medium",
            "Operating systems differ. Check platform-specific behavior."
        )

    # 3. Compare installed packages.
    dev_packages = development.get("packages", {})
    prod_packages = production.get("packages", {})

    all_packages = sorted(set(dev_packages) | set(prod_packages))

    for package in all_packages:
        dev_version = dev_packages.get(package)
        prod_version = prod_packages.get(package)

        if dev_version is None:
            add_finding(
                "dependency",
                package,
                None,
                prod_version,
                "medium",
                "Package is installed only in production."
            )

        elif prod_version is None:
            add_finding(
                "dependency",
                package,
                dev_version,
                None,
                "medium",
                "Package is missing from production."
            )

        elif dev_version != prod_version:
            severity = "medium"
            message = "Package versions differ. Check compatibility."

            # Identify version downgrades when versions are comparable.
            try:
                if Version(prod_version) < Version(dev_version):
                    message = (
                        "Production has an older package version. "
                        "Check whether required functionality is available."
                    )
            except (InvalidVersion, TypeError):
                message = (
                    "Package versions differ and could not be safely "
                    "ordered. Review the version values."
                )

            add_finding(
                "dependency",
                package,
                dev_version,
                prod_version,
                severity,
                message
            )

    # 4. Compare selected configuration-variable presence.
    dev_config = development.get("configuration_presence", {})
    prod_config = production.get("configuration_presence", {})

    all_variables = sorted(set(dev_config) | set(prod_config))

    for variable in all_variables:
        dev_present = dev_config.get(variable)
        prod_present = prod_config.get(variable)

        if dev_present is True and prod_present is False:
            add_finding(
                "configuration",
                variable,
                "present",
                "missing",
                "high",
                "Configuration variable is missing in production."
            )

        elif dev_present is False and prod_present is True:
            add_finding(
                "configuration",
                variable,
                "missing",
                "present",
                "medium",
                "Configuration variable is missing in development."
            )

    return findings
