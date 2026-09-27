"""
Mock data generator for testing.
Replace this with real Person A's scanner API calls later.
"""

# License compatibility matrix
LICENSE_CONFLICTS = {
    ("GPL-3.0-only", "Apache-2.0"): {"severity": "critical", "reason": "GPL-3.0 is incompatible with Apache-2.0"},
    ("GPL-3.0-only", "MIT"): {"severity": "critical", "reason": "GPL-3.0 restricts proprietary modifications, MIT doesn't"},
    ("AGPL-3.0-only", "Apache-2.0"): {"severity": "critical", "reason": "AGPL network clause conflicts"},
    ("GPL-2.0-only", "Apache-2.0"): {"severity": "high", "reason": "GPL-2.0 is incompatible with Apache-2.0"},
    ("GPL-2.0-only", "MIT"): {"severity": "medium", "reason": "GPL-2.0 stricter than MIT"},
}

MOCK_PACKAGES = {
    "django-project": [
        {"name": "Django", "version": "4.2.0", "license": "BSD-3-Clause"},
        {"name": "requests", "version": "2.31.0", "license": "Apache-2.0"},
        {"name": "celery", "version": "5.3.0", "license": "BSD-3-Clause"},
        {"name": "sqlalchemy", "version": "2.0.0", "license": "MIT"},
        {"name": "pandas", "version": "2.0.0", "license": "BSD-3-Clause"},
    ],
    "flask-app": [
        {"name": "Flask", "version": "2.3.0", "license": "BSD-3-Clause"},
        {"name": "requests", "version": "2.31.0", "license": "Apache-2.0"},
        {"name": "python-dotenv", "version": "1.0.0", "license": "BSD-3-Clause"},
        {"name": "cryptography", "version": "41.0.0", "license": "Apache-2.0"},
    ],
    "data-science": [
        {"name": "numpy", "version": "1.24.0", "license": "BSD-3-Clause"},
        {"name": "pandas", "version": "2.0.0", "license": "BSD-3-Clause"},
        {"name": "scikit-learn", "version": "1.3.0", "license": "BSD-3-Clause"},
        {"name": "matplotlib", "version": "3.7.0", "license": "PSF"},
        {"name": "pytorch", "version": "2.0.0", "license": "BSD"},
        {"name": "tensorflow", "version": "2.13.0", "license": "Apache-2.0"},
    ],
    "gpl-project": [
        {"name": "Django", "version": "4.2.0", "license": "BSD-3-Clause"},
        {"name": "some-gpl-lib", "version": "1.0.0", "license": "GPL-3.0-only"},
        {"name": "requests", "version": "2.31.0", "license": "Apache-2.0"},
    ]
}


def get_mock_scan_results(project_name: str):
    """
    Get mock scan results based on project name.
    This simulates Person A's scanner output.
    """
    
    # Select packages based on project name
    if "gpl" in project_name.lower():
        packages_list = MOCK_PACKAGES["gpl-project"]
    elif "flask" in project_name.lower():
        packages_list = MOCK_PACKAGES["flask-app"]
    elif "data" in project_name.lower():
        packages_list = MOCK_PACKAGES["data-science"]
    else:
        packages_list = MOCK_PACKAGES["django-project"]  # default
    
    # Convert to proper format
    packages = [
        {
            "name": pkg["name"],
            "version": pkg["version"],
            "license": pkg["license"],
            "source": "pypi"
        }
        for pkg in packages_list
    ]
    
    # Detect conflicts
    conflicts = detect_conflicts(packages)
    
    # Determine compliance status
    if any(c["severity"] == "critical" for c in conflicts):
        compliance_status = "critical"
    elif any(c["severity"] == "high" for c in conflicts):
        compliance_status = "warnings"
    else:
        compliance_status = "compliant"
    
    return {
        "packages": packages,
        "conflicts": conflicts,
        "compliance_status": compliance_status
    }


def detect_conflicts(packages):
    """
    Detect license conflicts between packages.
    """
    conflicts = []
    
    # Check all pairs
    for i, pkg1 in enumerate(packages):
        for pkg2 in packages[i+1:]:
            license1 = pkg1["license"]
            license2 = pkg2["license"]
            
            # Check both directions
            key1 = (license1, license2)
            key2 = (license2, license1)
            
            if key1 in LICENSE_CONFLICTS:
                conflict_info = LICENSE_CONFLICTS[key1]
                conflicts.append({
                    "package1": pkg1["name"],
                    "license1": license1,
                    "package2": pkg2["name"],
                    "license2": license2,
                    "severity": conflict_info["severity"],
                    "reason": conflict_info["reason"]
                })
            elif key2 in LICENSE_CONFLICTS:
                conflict_info = LICENSE_CONFLICTS[key2]
                conflicts.append({
                    "package1": pkg1["name"],
                    "license1": license1,
                    "package2": pkg2["name"],
                    "license2": license2,
                    "severity": conflict_info["severity"],
                    "reason": conflict_info["reason"]
                })
    
    return conflicts
