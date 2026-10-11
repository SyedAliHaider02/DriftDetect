
import json
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.analyzer import compare_environments


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB per report

app = FastAPI(
    title="DriftDetect API",
    description="Compare software environments and identify configuration drift.",
    version="0.1.0",
)

app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static",
)


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/download/collector")
def download_collector():
    collector_path = BASE_DIR / "driftdetect.py"

    if not collector_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Collector script not found.",
        )

    return FileResponse(
        path=collector_path,
        media_type="text/x-python",
        filename="driftdetect.py",
    )

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "DriftDetect API",
    }


async def read_environment_report(file: UploadFile) -> dict:
    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"{file.filename} exceeds the 2 MB limit.",
        )

    try:
        report = json.loads(content)
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(
            status_code=400,
            detail=f"{file.filename} is not valid JSON.",
        )

    if not isinstance(report, dict):
        raise HTTPException(
            status_code=400,
            detail=f"{file.filename} must contain a JSON object.",
        )

    required_fields = {
        "environment_name",
        "python_version",
        "os",
        "packages",
        "configuration_presence",
    }

    missing_fields = required_fields - report.keys()

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail={
                "message": f"{file.filename} is missing required fields.",
                "missing_fields": sorted(missing_fields),
            },
        )

    if not isinstance(report["packages"], dict):
        raise HTTPException(
            status_code=400,
            detail=f"{file.filename}: packages must be a JSON object.",
        )

    if not isinstance(report["configuration_presence"], dict):
        raise HTTPException(
            status_code=400,
            detail=(
                f"{file.filename}: "
                "configuration_presence must be a JSON object."
            ),
        )

    return report


@app.post("/compare")
async def compare_reports(
    development_file: UploadFile = File(...),
    production_file: UploadFile = File(...),
):
    development = await read_environment_report(development_file)
    production = await read_environment_report(production_file)

    findings = compare_environments(development, production)

    return JSONResponse(
        content={
            "development_environment": development["environment_name"],
            "production_environment": production["environment_name"],
            "total_findings": len(findings),
            "findings": findings,
        }
    )
