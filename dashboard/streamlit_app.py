import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="LicenseLens - License Compliance Scanner",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
    }
    .conflict-critical {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .conflict-high {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .conflict-medium {
        background-color: #fce4ec;
        border-left: 4px solid #e91e63;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .compliance-compliant {
        color: #4caf50;
        font-weight: bold;
        font-size: 18px;
    }
    .compliance-warnings {
        color: #ff9800;
        font-weight: bold;
        font-size: 18px;
    }
    .compliance-critical {
        color: #f44336;
        font-weight: bold;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# API Base URL
API_URL = "http://localhost:8000"

# Session state initialization
if 'current_project_id' not in st.session_state:
    st.session_state.current_project_id = None
if 'current_scan_data' not in st.session_state:
    st.session_state.current_scan_data = None
if 'projects_list' not in st.session_state:
    st.session_state.projects_list = []


def check_api_health():
    """Check if backend API is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def upload_and_scan(uploaded_file):
    """Upload file and trigger scan"""
    try:
        with st.spinner("🔍 Scanning project..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(f"{API_URL}/scan", files=files, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: {response.status_code}")
                return None
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return None


def fetch_scan_results(project_id):
    """Fetch results for a specific project"""
    try:
        response = requests.get(f"{API_URL}/results/{project_id}", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Could not fetch results")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


def fetch_all_projects():
    """Fetch list of all scanned projects"""
    try:
        response = requests.get(f"{API_URL}/projects", timeout=5)
        if response.status_code == 200:
            return response.json().get("projects", [])
        else:
            return []
    except:
        return []


def fetch_statistics():
    """Fetch overall statistics"""
    try:
        response = requests.get(f"{API_URL}/stats", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None


def download_sbom_json(project_id):
    """Download SBOM in JSON format"""
    try:
        response = requests.get(f"{API_URL}/sbom/{project_id}?format=json", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Could not generate SBOM")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


def render_conflict(conflict):
    """Render a single conflict with styling"""
    severity = conflict.get("severity", "medium").lower()
    
    icon_map = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢"
    }
    
    icon = icon_map.get(severity, "⚪")
    
    html_class = f"conflict-{severity}"
    
    conflict_html = f"""
    <div class="{html_class}">
        <strong>{icon} {severity.upper()} - License Conflict</strong><br>
        <b>{conflict.get('package1', 'Unknown')}</b> ({conflict.get('license1', 'Unknown')}) 
        ↔️ 
        <b>{conflict.get('package2', 'Unknown')}</b> ({conflict.get('license2', 'Unknown')})<br>
        <small>Reason: {conflict.get('reason', 'No details')}</small>
    </div>
    """
    st.markdown(conflict_html, unsafe_allow_html=True)


# ============= MAIN APP =============

st.title("📋 LicenseLens - License Compliance Scanner")
st.markdown("Automated detection of open-source license conflicts and compliance reporting")

# Check API health
if not check_api_health():
    st.error("""
    ❌ **Backend API is not running!**
    
    Make sure to start the backend service:
    ```bash
    docker-compose up
    ```
    or
    ```bash
    cd backend && python main.py
    ```
    """)
    st.stop()

st.success("✅ Backend API is running")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["📤 New Scan", "📊 Project History", "📈 Statistics", "ℹ️ About"])

# ============= PAGE: NEW SCAN =============
if page == "📤 New Scan":
    st.header("Start a New License Scan")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload Project Dependencies")
        uploaded_file = st.file_uploader(
            "Choose a requirements.txt or pyproject.toml file",
            type=["txt", "toml"],
            help="Upload your Python project's dependency file"
        )
        
        if uploaded_file is not None:
            st.info(f"📄 File selected: **{uploaded_file.name}**")
            
            if st.button("🔍 Start Scan", use_container_width=True, type="primary"):
                result = upload_and_scan(uploaded_file)
                
                if result:
                    st.session_state.current_project_id = result.get("project_id")
                    st.session_state.current_scan_data = result
                    st.success("✅ Scan completed successfully!")
                    time.sleep(1)
                    st.rerun()
    
    with col2:
        st.subheader("Sample Files")
        st.markdown("**Django Project**")
        st.code("Django==4.2\nrequests==2.31\ncelery==5.3", language="text")
    
    # Display current scan results
    if st.session_state.current_scan_data:
        st.divider()
        scan_data = st.session_state.current_scan_data
        
        st.subheader("📊 Scan Results")
        
        # Compliance status
        compliance = scan_data.get("compliance_status", "unknown").upper()
        if compliance == "COMPLIANT":
            st.markdown('<p class="compliance-compliant">✅ COMPLIANT</p>', unsafe_allow_html=True)
        elif compliance == "WARNINGS":
            st.markdown('<p class="compliance-warnings">⚠️ WARNINGS</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="compliance-critical">❌ CRITICAL ISSUES</p>', unsafe_allow_html=True)
        
        # Metrics
        packages = scan_data.get("packages", [])
        conflicts = scan_data.get("conflicts", [])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Packages", len(packages))
        with col2:
            st.metric("Unique Licenses", len(set(p.get("license") for p in packages)))
        with col3:
            st.metric("Conflicts Found", len(conflicts))
        with col4:
            severity_counts = {}
            for c in conflicts:
                sev = c.get("severity", "low")
                severity_counts[sev] = severity_counts.get(sev, 0) + 1
            critical = severity_counts.get("critical", 0)
            st.metric("Critical Issues", critical)
        
        st.divider()
        
        # Packages Table
        st.subheader("📦 Scanned Packages")
        df_packages = pd.DataFrame(packages)
        st.dataframe(df_packages, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Conflicts
        st.subheader("⚠️ License Conflicts")
        if conflicts:
            for conflict in conflicts:
                render_conflict(conflict)
        else:
            st.success("No license conflicts detected! ✅")
        
        st.divider()
        
        # SBOM Export
        st.subheader("📋 Software Bill of Materials (SBOM)")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Download SBOM (JSON)", use_container_width=True):
                sbom = download_sbom_json(scan_data.get("project_id"))
                if sbom:
                    st.json(sbom)
                    st.download_button(
                        "⬇️ Download as JSON",
                        json.dumps(sbom, indent=2),
                        file_name=f"sbom-{scan_data.get('project_name')}.json",
                        mime="application/json"
                    )
        
        with col2:
            st.info("ℹ️ SBOM in CycloneDX format\nIndustry standard for supply chain security")


# ============= PAGE: PROJECT HISTORY =============
elif page == "📊 Project History":
    st.header("Project Scan History")
    
    projects = fetch_all_projects()
    
    if not projects:
        st.info("No previous scans found. Upload a file to get started!")
    else:
        st.subheader(f"Total Projects Scanned: {len(projects)}")
        
        # Display projects as cards
        for project in projects:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{project.get('project_name')}**")
                st.caption(f"ID: {project.get('project_id')}")
            with col2:
                st.metric("Packages", project.get("package_count", 0))
            with col3:
                st.metric("Conflicts", project.get("conflict_count", 0))
            
            if st.button(f"View Details", key=f"btn_{project.get('project_id')}"):
                st.session_state.current_project_id = project.get('project_id')
                result = fetch_scan_results(project.get('project_id'))
                st.session_state.current_scan_data = result
                st.rerun()
            
            st.divider()


# ============= PAGE: STATISTICS =============
elif page == "📈 Statistics":
    st.header("Overall Statistics")
    
    stats = fetch_statistics()
    
    if stats:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Scans", stats.get("total_scans", 0))
        with col2:
            st.metric("Total Packages", stats.get("total_packages_scanned", 0))
        with col3:
            st.metric("Total Conflicts", stats.get("total_conflicts", 0))
        
        st.divider()
        
        # License Distribution
        st.subheader("License Distribution")
        license_dist = stats.get("license_distribution", {})
        
        if license_dist:
            df_licenses = pd.DataFrame(list(license_dist.items()), columns=["License", "Count"])
            df_licenses = df_licenses.sort_values("Count", ascending=False)
            
            st.bar_chart(df_licenses.set_index("License"))
            st.dataframe(df_licenses, use_container_width=True, hide_index=True)
        else:
            st.info("No license data available yet.")
    else:
        st.warning("Could not fetch statistics")


# ============= PAGE: ABOUT =============
elif page == "ℹ️ About":
    st.header("About LicenseLens")
    
    st.markdown("""
    ### 🎯 What is LicenseLens?
    
    LicenseLens is an automated tool for detecting open-source license conflicts in Python projects.
    
    **Key Features:**
    - 📤 Automatic dependency scanning
    - 🔍 License identification via PyPI API
    - ⚠️ Conflict detection & severity classification
    - 📋 SBOM (Software Bill of Materials) generation
    - 📊 Compliance reporting
    
    ### 🔧 Technology Stack
    
    **Backend:**
    - FastAPI (Python web framework)
    - PyPI API integration
    - SPDX License standards
    
    **Frontend:**
    - Streamlit (Python UI framework)
    - Real-time visualization
    
    **Deployment:**
    - Docker containerization
    - Docker Compose orchestration
    
    ### 📚 License Compatibility
    
    Some common incompatibilities:
    - ❌ GPL-3.0 + Apache-2.0 (CRITICAL)
    - ❌ AGPL-3.0 + Apache-2.0 (CRITICAL)
    - ⚠️ GPL-2.0 + Apache-2.0 (HIGH)
    
    ### 👥 Team
    - **Person A:** Backend Scanner & License Resolver
    - **Person B:** Frontend Dashboard & SBOM Export
    
    ### 📖 Documentation
    See README.md for setup and usage instructions.
    """)
    
    st.divider()
    st.markdown("**LicenseLens v1.0.0** - Built for OST Course")
