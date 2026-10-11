const form = document.getElementById("compare-form");
const developmentInput = document.getElementById("development-file");
const productionInput = document.getElementById("production-file");

const developmentFilename = document.getElementById("development-filename");
const productionFilename = document.getElementById("production-filename");

const compareButton = document.getElementById("compare-button");
const buttonLabel = document.getElementById("button-label");
const errorMessage = document.getElementById("error-message");

const resultsSection = document.getElementById("results-section");
const findingsList = document.getElementById("findings-list");

let latestReport = null;

function updateFilePicker(input, filenameElement) {
    const file = input.files[0];

    filenameElement.textContent = file?.name || "Choose JSON file";
    input.closest(".upload-card").classList.toggle("is-filled", Boolean(file));
}

developmentInput.addEventListener("change", () => {
    updateFilePicker(developmentInput, developmentFilename);
});

productionInput.addEventListener("change", () => {
    updateFilePicker(productionInput, productionFilename);
});

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.hidden = false;
}

function clearError() {
    errorMessage.textContent = "";
    errorMessage.hidden = true;
}

function displayValue(value) {
    if (value === null || value === undefined) {
        return "Not present";
    }

    if (typeof value === "object") {
        return JSON.stringify(value, null, 2);
    }

    return String(value);
}

function createValueBox(label, value) {
    const box = document.createElement("div");
    box.className = "value-box";

    const heading = document.createElement("span");
    heading.className = "value-label";
    heading.textContent = label;

    const content = document.createElement("div");
    content.className = "value-text";
    content.textContent = displayValue(value);

    box.append(heading, content);
    return box;
}

function renderFindings(report) {
    const findings = report.findings || [];

    document.getElementById("total-count").textContent = findings.length;

    for (const severity of ["high", "medium", "low"]) {
        const count = findings.filter(
            (finding) => String(finding.severity).toLowerCase() === severity
        ).length;

        document.getElementById(`${severity}-count`).textContent = count;
    }

    document.getElementById("results-summary").textContent =
        `${report.development_environment} → ${report.production_environment}`;

    findingsList.replaceChildren();

    if (findings.length === 0) {
        const empty = document.createElement("div");
        empty.className = "empty-state";
        empty.textContent =
            "No differences were found in the fields collected. This does not guarantee the environments are identical.";
        findingsList.appendChild(empty);
    }

    for (const finding of findings) {
        const card = document.createElement("article");
        card.className = "finding";

        const top = document.createElement("div");
        top.className = "finding-top";

        const severity = document.createElement("span");
        const severityName = String(finding.severity || "unknown").toLowerCase();
        severity.className = `severity severity-${severityName}`;
        severity.textContent = severityName;

        const title = document.createElement("h3");
        title.textContent = `${finding.category}: ${finding.item}`;

        top.append(severity, title);

        const message = document.createElement("p");
        message.className = "finding-message";
        message.textContent = finding.message || "Difference detected.";

        const values = document.createElement("div");
        values.className = "value-grid";
        values.append(
            createValueBox("Development", finding.development_value),
            createValueBox("Production", finding.production_value)
        );

        card.append(top, message, values);
        findingsList.appendChild(card);
    }

    resultsSection.hidden = false;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearError();

    const developmentFile = developmentInput.files[0];
    const productionFile = productionInput.files[0];

    if (!developmentFile || !productionFile) {
        showError("Choose both the development and production JSON reports.");
        return;
    }

    if (
        !developmentFile.name.toLowerCase().endsWith(".json") ||
        !productionFile.name.toLowerCase().endsWith(".json")
    ) {
        showError("Both files must have a .json extension.");
        return;
    }

    const formData = new FormData();
    formData.append("development_file", developmentFile);
    formData.append("production_file", productionFile);

    compareButton.disabled = true;
    buttonLabel.textContent = "Analyzing...";

    try {
        const response = await fetch("/compare", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();

        if (!response.ok) {
            const detail = result.detail;
            const message =
                typeof detail === "string"
                    ? detail
                    : detail?.message || JSON.stringify(detail);

            throw new Error(message || `Request failed (${response.status}).`);
        }

        latestReport = result;
        renderFindings(result);
        resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
        showError(
            error instanceof TypeError
                ? "Could not connect to DriftDetect. Check that the API is running."
                : error.message
        );
    } finally {
        compareButton.disabled = false;
        buttonLabel.textContent = "Analyze differences";
    }
});

document.getElementById("reset-button").addEventListener("click", () => {
    latestReport = null;
    findingsList.replaceChildren();
    resultsSection.hidden = true;
    clearError();
    form.reset();

    updateFilePicker(developmentInput, developmentFilename);
    updateFilePicker(productionInput, productionFilename);
});

document.getElementById("download-button").addEventListener("click", () => {
    if (!latestReport) {
        showError("Run a comparison before downloading a report.");
        return;
    }

    const blob = new Blob(
        [JSON.stringify(latestReport, null, 2)],
        { type: "application/json" }
    );

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "driftdetect-analysis.json";
    link.click();

    URL.revokeObjectURL(url);
});