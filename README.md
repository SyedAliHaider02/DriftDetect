# DriftDetect 🔍

**Find the differences. Understand the drift. Fix the environment.**

DriftDetect is a lightweight environment comparison tool designed to help developers troubleshoot one of software development's most common problems: *"It works on my machine, but not in production."*

It collects software environment metadata into JSON reports and compares development and production environments to identify potential causes of inconsistencies, compatibility issues, and deployment failures.

Built with Python and FastAPI, DriftDetect provides a simple web interface for uploading environment reports and reviewing differences without manually inspecting configuration files.

## 🚀 Features

- **Environment Comparison:** Compare development and production environment reports side by side.
- **Python Version Detection:** Identify differences in Python versions and implementations.
- **Package Analysis:** Detect differences in installed Python packages and their versions.
- **Configuration Checks:** Compare whether selected environment variables are present without collecting their actual values.
- **Severity-Based Findings:** Organize detected differences by severity to help prioritize investigation.
- **JSON Report Upload:** Upload environment reports through a simple web interface.
- **Environment Collector:** Generate environment reports using a standalone Python script.
- **REST API:** Access comparison functionality through FastAPI endpoints.
- **Interactive API Documentation:** Explore and test API endpoints through Swagger UI.
- **Lightweight Deployment:** Deploy the application on Render with a GitHub-connected workflow.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application and environment collection |
| FastAPI | Backend API and request handling |
| Uvicorn | ASGI server |
| HTML | Web interface structure |
| CSS | User interface styling |
| JavaScript | Frontend interactions |
| JSON | Environment report format |
| Packaging | Python version and package version comparison |
| Pytest | Automated testing |
| Render | Cloud deployment |
| Git & GitHub | Version control and source hosting |

## 🏗️ Project Structure

```text
DriftDetector/
├── backend/
│   ├── __init__.py
│   ├── analyzer.py
│   └── main.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── examples/
│   ├── development.json
│   ├── production.json
│   └── production-test.json
├── driftdetect.py
├── requirements.txt
├── test_comparison.py
├── .gitignore
└── README.md
```

## ⚙️ Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.10 or later
- Git
- A code editor such as Visual Studio Code

### 1. Clone the repository

```bash
git clone https://github.com/SyedAliHaider02/DriftDetect.git
cd DriftDetect
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, you can activate the environment from Command Prompt instead:

```cmd
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the application

From the project root directory, run:

```bash
python -m uvicorn backend.main:app --reload --app-dir .
```

Open the following URLs in your browser:

- **Web Interface:** http://127.0.0.1:8000/
- **API Documentation:** http://127.0.0.1:8000/docs
- **Health Check:** http://127.0.0.1:8000/health

## 📊 Generating Environment Reports

DriftDetect includes a standalone collector script that records environment metadata and writes it to a JSON file.

Generate a development report:

```bash
python driftdetect.py --name development --output examples/development.json
```

Generate another report from a different environment:

```bash
python driftdetect.py --name production --output examples/production.json
```

**Important:** Run the collector separately in each environment you want to compare. Generating both reports on the same machine will not reveal genuine differences between development and production.

The collector records information such as:

- Python version and implementation
- Operating system and architecture
- Installed Python packages and versions
- Presence or absence of selected environment variables

For configuration privacy, the collector records whether selected variables are present, not their actual values.

## 🔎 Comparing Environments

1. Start the DriftDetect application.
2. Open the web interface.
3. Upload the development environment JSON report.
4. Upload the production environment JSON report.
5. Run the comparison.
6. Review the findings, including detected differences, severity levels, and explanatory messages.

Findings can help identify potential issues such as incompatible Python versions, missing dependencies, package version differences, or missing configuration variables.

A detected difference is a diagnostic clue, not automatic proof of the root cause.

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serves the web interface |
| GET | `/health` | Checks whether the API is running |
| POST | `/compare` | Compares two uploaded environment reports |
| GET | `/docs` | Opens interactive API documentation |

The comparison endpoint accepts two multipart file uploads:

- `development_file`
- `production_file`

Example using Python:

```python
import requests

url = "http://127.0.0.1:8000/compare"

with open("examples/development.json", "rb") as dev_file, \
     open("examples/production.json", "rb") as prod_file:

    response = requests.post(
        url,
        files={
            "development_file": dev_file,
            "production_file": prod_file,
        },
        timeout=30,
    )

response.raise_for_status()
print(response.json())
```

## 🧪 Running Tests

Run the comparison test script:

```bash
python test_comparison.py
```

If the project has pytest-compatible automated tests, run:

```bash
python -m pytest -v
```

## ☁️ Deployment on Render

DriftDetect can be deployed as a Python web service on [Render](https://render.com/).

### Deployment configuration

| Setting | Value |
|---|---|
| Runtime | Python 3 |
| Branch | `main` |
| Root Directory | Leave blank |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn backend.main:app --host 0.0.0.0 --port $PORT` |

Connect the GitHub repository to Render and create a Web Service using these settings.

With automatic deployment enabled, new commits pushed to the configured branch can trigger deployments automatically.

**Free-tier note:** Render free web services may spin down after inactivity, so the first request after a period of inactivity can take longer.

## 🔐 Security and Limitations

- Environment reports may reveal system details and installed dependency versions. Share them only with trusted recipients.
- The collector checks the presence of selected environment variables but should never be used to collect secrets.
- Uploaded JSON files are validated for required fields and size limits before comparison.
- DriftDetect identifies differences that may contribute to failures. It does not reproduce the target environment or guarantee a definitive root-cause diagnosis.
- A local report labelled `production` is not a substitute for a report collected from the actual production environment.
- Avoid uploading credentials, access tokens, private keys, or other sensitive information.

## 🗺️ Roadmap

Potential future improvements include:

- Dependency compatibility analysis
- More detailed OS and runtime comparisons
- Exportable comparison reports
- Historical environment snapshots
- Container image and deployment metadata comparison
- Improved diagnostic recommendations
- CI/CD integration for automated drift checks

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes and add tests where appropriate.
4. Submit a pull request describing the improvement.

## 📄 License

Choose a license before distributing the project publicly. If you intend to make the source code open source, consider adding an appropriate license file to the repository.

---

**DriftDetect**  
*Because "it works on my machine" is not a deployment strategy.*
