# LicenseLens - License Compliance Scanner

<div align="center">

**Automated detection of open-source license conflicts in Python projects**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-green)

</div>

---

## 📋 Problem Statement

Open-source projects often use third-party dependencies without checking license compatibility, creating significant legal and compliance risks. For example:
- Combining GPL-licensed libraries with proprietary code
- Using incompatible licenses in the same project (e.g., GPL-3.0 + Apache-2.0)
- Not tracking the licenses of transitive dependencies

**LicenseLens solves this** by automatically scanning your Python project's dependencies, identifying each library's license, detecting incompatible combinations, and generating a comprehensive Software Bill of Materials (SBOM).

---

## 🎯 Objectives

- ✅ Automatically scan Python project dependencies (from `requirements.txt` / `pyproject.toml`)
- ✅ Query the **PyPI API** to fetch license information
- ✅ Match licenses against the **SPDX standard** license list
- ✅ Detect **license conflicts** and incompatibilities
- ✅ Generate **SBOM** in CycloneDX and SPDX JSON formats
- ✅ Provide a user-friendly **Streamlit dashboard** for visualization
- ✅ Demonstrate **containerization** with Docker & Docker Compose
- ✅ Show proper **Git workflow** and collaboration

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    LicenseLens System                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────┐         ┌──────────────────────┐   │
│  │  STREAMLIT          │         │  FASTAPI BACKEND     │   │
│  │  DASHBOARD          │◄────────┤  (Port 8000)         │   │
│  │  (Port 8501)        │         │                      │   │
│  │                     │         │  ✅ /scan            │   │
│  │  ✅ File Upload     │         │  ✅ /results/{id}    │   │
│  │  ✅ Visualization   │         │  ✅ /sbom/{id}       │   │
│  │  ✅ Conflict View   │         │  ✅ /projects        │   │
│  │  ✅ SBOM Download   │         │  ✅ /stats           │   │
│  └─────────────────────┘         └──────────────────────┘   │
│          │                                      │             │
│          │                                      │             │
│          └──────────────────┬───────────────────┘             │
│                             │                                 │
│              ┌──────────────▼─────────────┐                  │
│              │   MOCK DATA / SCANNER      │                  │
│              │  (Will integrate with      │                  │
│              │   Person A's service)      │                  │
│              └────────────────────────────┘                  │
│                             │                                 │
│              ┌──────────────▼─────────────┐                  │
│              │     PYPI API                │                  │
│              │  (License lookup)           │                  │
│              └────────────────────────────┘                  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Services (Docker Compose)

1. **Backend Service** (FastAPI)
   - Exposes REST API endpoints
   - Processes scan requests
   - Generates SBOM
   - Manages results storage

2. **Dashboard Service** (Streamlit)
   - Interactive UI for file upload
   - Real-time visualization
   - Conflict highlighting
   - SBOM export

### Data Flow

```
[User Upload] → [Backend /scan] → [Mock Scanner] → [License Lookup] 
    ↓                                                      ↓
[Results Stored] ← [Conflict Detection] ← [SPDX Matching]
    ↓
[Dashboard Display] + [SBOM Generation]
```

---

## 🚀 Quick Start

### Prerequisites

- **Docker** & **Docker Compose** (recommended)
  - Or: Python 3.11+, pip

### Option 1: Run with Docker Compose (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd licenselens

# Start all services
docker-compose up

# Access:
# - Dashboard: http://localhost:8501
# - API Docs: http://localhost:8000/docs
```

### Option 2: Run Locally (Without Docker)

#### Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
# API runs on http://localhost:8000
```

#### Dashboard (in a new terminal)

```bash
cd dashboard
pip install -r requirements.txt
streamlit run streamlit_app.py
# Dashboard runs on http://localhost:8501
```

---

## 📚 API Reference

### Backend Endpoints

#### 1. Health Check
```http
GET /health
```
Returns service status.

**Response:**
```json
{
  "status": "healthy",
  "service": "licenselens-backend",
  "timestamp": "2024-09-28T12:00:00"
}
```

---

#### 2. Scan Project
```http
POST /scan
Content-Type: multipart/form-data

[File: requirements.txt]
```
Uploads and scans a project file.

**Response:**
```json
{
  "project_id": "proj_a1b2c3d4",
  "project_name": "my-project",
  "timestamp": "2024-09-28T12:00:00",
  "packages": [
    {
      "name": "Django",
      "version": "4.2.0",
      "license": "BSD-3-Clause",
      "source": "pypi"
    }
  ],
  "conflicts": [
    {
      "package1": "Django",
      "license1": "BSD-3-Clause",
      "package2": "requests",
      "license2": "Apache-2.0",
      "severity": "low",
      "reason": "No known incompatibility"
    }
  ],
  "compliance_status": "compliant"
}
```

---

#### 3. Get Scan Results
```http
GET /results/{project_id}
```
Retrieves previously scanned project results.

---

#### 4. Download SBOM
```http
GET /sbom/{project_id}?format=json
```
Generates SBOM in specified format (json, spdx).

---

#### 5. List Projects
```http
GET /projects
```
Lists all scanned projects.

---

#### 6. Statistics
```http
GET /stats
```
Overall statistics across all scans.

---

## 📊 Dashboard Features

### 📤 New Scan
- Upload `requirements.txt` or `pyproject.toml`
- Real-time scan processing
- View scanned packages
- Visual conflict highlighting
- Download SBOM

### 📊 Project History
- View all previous scans
- Click to view details
- Track compliance status

### 📈 Statistics
- Total scans performed
- License distribution chart
- Conflict trends

---

## 🔧 Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Requests** - HTTP library for PyPI API

### Frontend
- **Streamlit** - Python UI framework
- **Pandas** - Data manipulation
- **JSON** - Data format

### Deployment
- **Docker** - Containerization
- **Docker Compose** - Orchestration

---

## 🏃 Development Workflow

### Team Members
- **Person A**: Backend Scanner & License Resolver
  - Builds the actual scanner that reads requirements.txt
  - Integrates PyPI API for real license lookup
  - Creates compatibility rules table

- **Person B**: Frontend Dashboard & SBOM Export
  - Builds FastAPI backend API
  - Creates Streamlit dashboard UI
  - Implements SBOM generation

### Git Branching Strategy

```
main (protected)
├── feature/scanner-license-resolver (Person A)
└── feature/dashboard-backend (Person B)
```

**Workflow:**
1. Each person works on their feature branch
2. Regular commits with clear messages
3. Once ready, create PR to merge into main
4. Code review before merging

### Commit Message Format

```
type(scope): description

[optional body]
[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code reorganization
- `test`: Tests
- `docker`: Docker/deployment

**Examples:**
```
feat(backend): add /scan endpoint
feat(dashboard): implement file upload
docs(readme): add setup instructions
docker: create docker-compose.yml
```

---

## 📋 License Compatibility Rules

### Critical Conflicts (🔴 CRITICAL)
- GPL-3.0-only + Apache-2.0
- AGPL-3.0-only + Apache-2.0
- GPL-2.0-only + Apache-2.0

### High Conflicts (🟠 HIGH)
- GPL-2.0-only + MIT

### Medium/Low
- Most other combinations

---

## 📝 Project Structure

```
licenselens/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Pydantic models
│   ├── sbom_generator.py       # SBOM generation logic
│   ├── mock_data.py            # Mock scanner data
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile.backend      # Backend container
│
├── dashboard/
│   ├── streamlit_app.py        # Streamlit application
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile.dashboard    # Dashboard container
│
├── docker-compose.yml          # Service orchestration
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
```

---

## 🧪 Testing

### Test with Mock Data

The system includes mock data for testing without Person A's scanner.

**Mock Projects Available:**
- `django-project` - Django + Apache 2.0 + BSD mix
- `flask-app` - Flask + multiple license types
- `data-science` - Data science stack
- `gpl-project` - GPL conflict examples

### Testing Steps

1. Start the services:
   ```bash
   docker-compose up
   ```

2. Open dashboard: http://localhost:8501

3. Upload a test file (or use the provided mock projects)

4. Verify:
   - ✅ Files are scanned
   - ✅ Packages are listed
   - ✅ Conflicts are detected
   - ✅ SBOM can be downloaded

---

## 🔄 Integration with Person A's Scanner

When Person A completes the scanner service, integrate it as follows:

1. **Define API Contract:**
   ```python
   # Person A's /scan endpoint returns:
   {
     "packages": [{"name": "...", "version": "...", "license": "..."}],
     "conflicts": [...]
   }
   ```

2. **Update Backend:**
   In `backend/main.py`, replace mock calls with real API calls:
   ```python
   # Replace this:
   scan_data = get_mock_scan_results(project_name)
   
   # With this:
   response = requests.post("http://scanner:5000/scan", files=files)
   scan_data = response.json()
   ```

3. **Update Docker Compose:**
   Add Person A's service to `docker-compose.yml`

4. **Test Integration:**
   Run `docker-compose up` and verify end-to-end flow

---

## 🎓 Learning Outcomes

This project demonstrates:

- ✅ **Container Technology**: Docker & Docker Compose
- ✅ **REST API Design**: FastAPI endpoints
- ✅ **Web UI Development**: Streamlit
- ✅ **Git Workflow**: Branching, commits, collaboration
- ✅ **SBOM Standards**: CycloneDX, SPDX
- ✅ **License Compliance**: Understanding open-source licenses
- ✅ **API Integration**: PyPI API, external services
- ✅ **Data Processing**: JSON, license matching

---

## 📖 References

- **SPDX License List**: https://spdx.org/licenses/
- **CycloneDX**: https://cyclonedx.org/
- **PyPI API**: https://warehouse.pypa.io/api-reference/json.html
- **FastAPI**: https://fastapi.tiangolo.com/
- **Streamlit**: https://streamlit.io/
- **Docker**: https://www.docker.com/

---

## 🤝 Team Information

| Role | Responsibility | Status |
|------|---|---|
| **Person A** | Scanner + License Resolver | 🔄 In Progress |
| **Person B** | Dashboard + API + SBOM Export | ✅ Complete |

---

## 📅 Important Dates

- **CA3 (First Review)**: 28 Sept - 1 Oct 2026
  - Problem statement
  - Architecture design
  - Working MVP demo
  
- **CA4 (Final Submission)**: 5-9 Oct 2026
  - Complete end-to-end system
  - Integration of both services
  - Final presentation

---

## 📧 Support

For issues or questions:
1. Check the logs: `docker-compose logs backend` / `docker-compose logs dashboard`
2. Review API docs: http://localhost:8000/docs
3. Check error messages in Streamlit dashboard

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

<div align="center">

**Built for OST Course - Open Source Tools for Data Science**

Made with ❤️ by Person A & Person B

</div>

 # #   S t a t u s 
 B a c k e n d   a n d   D a s h b o a r d   i m p l e m e n t e d   w i t h   m o c k   d a t a   ( r e a d y   f o r   P e r s o n   A   i n t e g r a t i o n ) . 
  
 