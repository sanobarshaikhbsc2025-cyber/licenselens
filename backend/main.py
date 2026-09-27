from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import uuid
from datetime import datetime
from sbom_generator import generate_sbom
from mock_data import get_mock_scan_results

app = FastAPI(
    title="LicenseLens Backend API",
    description="License Compliance Scanner API",
    version="1.0.0"
)

# Enable CORS for Streamlit dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (replace with DB later)
scan_results_store = {}


# ============= MODELS =============
class Package(BaseModel):
    name: str
    version: str
    license: str
    source: str = "pypi"


class LicenseConflict(BaseModel):
    package1: str
    package2: str
    severity: str  # "critical", "high", "medium", "low"
    reason: str


class ScanResult(BaseModel):
    project_id: str
    project_name: str
    timestamp: str
    packages: List[Package]
    conflicts: List[LicenseConflict]
    compliance_status: str  # "compliant", "warnings", "critical"


# ============= ENDPOINTS =============

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "licenselens-backend",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/scan")
async def scan_project(file: UploadFile = File(...)):
    """
    Scan a project file for license compliance.
    
    Accepts: requirements.txt or pyproject.toml
    Returns: Scan results with license breakdown and conflicts
    """
    try:
        # Read uploaded file
        contents = await file.read()
        file_content = contents.decode('utf-8')
        
        # Generate unique project ID
        project_id = f"proj_{str(uuid.uuid4())[:8]}"
        project_name = file.filename.replace('.txt', '')
        
        # Get mock scan results (or call Person A's scanner later)
        scan_data = get_mock_scan_results(project_name)
        
        # Create result object
        result = ScanResult(
            project_id=project_id,
            project_name=project_name,
            timestamp=datetime.now().isoformat(),
            packages=scan_data["packages"],
            conflicts=scan_data["conflicts"],
            compliance_status=scan_data["compliance_status"]
        )
        
        # Store in memory
        scan_results_store[project_id] = result.dict()
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error scanning file: {str(e)}")


@app.get("/results/{project_id}")
def get_scan_results(project_id: str):
    """
    Retrieve previously scanned project results
    """
    if project_id not in scan_results_store:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return scan_results_store[project_id]


@app.get("/sbom/{project_id}")
def get_sbom(project_id: str, format: str = "json"):
    """
    Generate and return SBOM for a scanned project
    
    Formats: json, spdx
    """
    if project_id not in scan_results_store:
        raise HTTPException(status_code=404, detail="Project not found")
    
    scan_data = scan_results_store[project_id]
    
    if format == "json":
        sbom = generate_sbom(scan_data, format="cyclonedx")
        return JSONResponse(content=sbom)
    elif format == "spdx":
        sbom = generate_sbom(scan_data, format="spdx")
        return JSONResponse(content=sbom)
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")


@app.get("/projects")
def list_projects():
    """
    List all scanned projects
    """
    projects = []
    for project_id, data in scan_results_store.items():
        projects.append({
            "project_id": project_id,
            "project_name": data.get("project_name"),
            "timestamp": data.get("timestamp"),
            "package_count": len(data.get("packages", [])),
            "conflict_count": len(data.get("conflicts", []))
        })
    return {"projects": projects}


@app.get("/conflicts")
def get_all_conflicts():
    """
    Get all flagged conflicts across all scans
    """
    all_conflicts = []
    for project_id, data in scan_results_store.items():
        for conflict in data.get("conflicts", []):
            conflict["project_id"] = project_id
            conflict["project_name"] = data.get("project_name")
            all_conflicts.append(conflict)
    
    return {"total_conflicts": len(all_conflicts), "conflicts": all_conflicts}


@app.get("/stats")
def get_statistics():
    """
    Get overall statistics
    """
    total_scans = len(scan_results_store)
    total_packages = sum(len(data.get("packages", [])) for data in scan_results_store.values())
    total_conflicts = sum(len(data.get("conflicts", [])) for data in scan_results_store.values())
    
    # License distribution
    license_count = {}
    for data in scan_results_store.values():
        for pkg in data.get("packages", []):
            license = pkg.get("license", "Unknown")
            license_count[license] = license_count.get(license, 0) + 1
    
    return {
        "total_scans": total_scans,
        "total_packages_scanned": total_packages,
        "total_conflicts": total_conflicts,
        "license_distribution": license_count
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
