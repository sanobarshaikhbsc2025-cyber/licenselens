"""
SBOM (Software Bill of Materials) Generator
Generates SBOMs in CycloneDX and SPDX formats
"""

import json
from datetime import datetime
import uuid


def generate_sbom(scan_data, format="cyclonedx"):
    """
    Generate SBOM in specified format.
    
    Args:
        scan_data: Dictionary with scan results
        format: "cyclonedx" or "spdx"
    
    Returns:
        Dictionary representing the SBOM
    """
    
    if format == "cyclonedx":
        return generate_cyclonedx_sbom(scan_data)
    elif format == "spdx":
        return generate_spdx_sbom(scan_data)
    else:
        raise ValueError(f"Unsupported format: {format}")


def generate_cyclonedx_sbom(scan_data):
    """
    Generate SBOM in CycloneDX JSON format (v1.4 spec).
    """
    
    project_id = scan_data.get("project_id", "unknown")
    project_name = scan_data.get("project_name", "Unknown Project")
    packages = scan_data.get("packages", [])
    conflicts = scan_data.get("conflicts", [])
    
    # Generate component list
    components = []
    for pkg in packages:
        component = {
            "type": "library",
            "name": pkg.get("name", ""),
            "version": pkg.get("version", ""),
            "licenses": [
                {
                    "license": {
                        "name": pkg.get("license", "Unknown")
                    }
                }
            ],
            "purl": f"pkg:pypi/{pkg.get('name').lower()}@{pkg.get('version')}",
            "scope": "required"
        }
        components.append(component)
    
    # Generate dependencies
    dependencies = []
    for pkg in packages:
        dependencies.append({
            "ref": f"pkg:pypi/{pkg.get('name').lower()}@{pkg.get('version')}",
            "dependsOn": []
        })
    
    # Build SBOM
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "serialNumber": f"urn:uuid:{str(uuid.uuid4())}",
        "version": 1,
        "metadata": {
            "timestamp": datetime.now().isoformat() + "Z",
            "tools": [
                {
                    "vendor": "LicenseLens",
                    "name": "licenselens-backend",
                    "version": "1.0.0"
                }
            ],
            "component": {
                "type": "application",
                "name": project_name,
                "version": "1.0.0",
                "description": f"License compliance scan for {project_name}"
            }
        },
        "components": components,
        "dependencies": dependencies
    }
    
    # Add vulnerabilities/conflicts as external references
    if conflicts:
        sbom["vulnerabilities"] = []
        for conflict in conflicts:
            vuln = {
                "ref": f"pkg:pypi/{conflict.get('package1', '').lower()}",
                "id": str(uuid.uuid4()),
                "severity": map_severity(conflict.get("severity", "medium")),
                "description": conflict.get("reason", "License compatibility issue"),
                "details": f"Conflict with {conflict.get('package2')}: {conflict.get('reason')}"
            }
            sbom["vulnerabilities"].append(vuln)
    
    return sbom


def generate_spdx_sbom(scan_data):
    """
    Generate SBOM in SPDX JSON format.
    """
    
    project_id = scan_data.get("project_id", "unknown")
    project_name = scan_data.get("project_name", "Unknown Project")
    packages = scan_data.get("packages", [])
    conflicts = scan_data.get("conflicts", [])
    
    # Generate package list
    spdx_packages = [
        {
            "SPDXID": f"SPDXRef-Package-{i}",
            "name": pkg.get("name", ""),
            "versionInfo": pkg.get("version", ""),
            "downloadLocation": f"https://pypi.org/project/{pkg.get('name')}/",
            "filesAnalyzed": False,
            "licenseConcluded": pkg.get("license", "NOASSERTION"),
            "licenseDeclared": pkg.get("license", "NOASSERTION"),
            "copyrightText": "NOASSERTION",
            "externalRefs": [
                {
                    "referenceCategory": "PACKAGE-MANAGER",
                    "referenceType": "purl",
                    "referenceLocator": f"pkg:pypi/{pkg.get('name').lower()}@{pkg.get('version')}"
                }
            ]
        }
        for i, pkg in enumerate(packages)
    ]
    
    # Generate relationships
    relationships = [
        {
            "spdxElementId": "SPDXRef-DOCUMENT",
            "relationshipType": "DESCRIBES",
            "relatedSpdxElement": "SPDXRef-Project"
        }
    ]
    
    for i in range(len(packages)):
        relationships.append({
            "spdxElementId": "SPDXRef-Project",
            "relationshipType": "DEPENDS_ON",
            "relatedSpdxElement": f"SPDXRef-Package-{i}"
        })
    
    # Build SPDX document
    spdx = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": f"License Scan: {project_name}",
        "documentNamespace": f"https://licenselens.example.com/{project_id}/{str(uuid.uuid4())}",
        "creationInfo": {
            "created": datetime.now().isoformat() + "Z",
            "creators": ["Tool: licenselens-backend-1.0.0"],
            "licenseListVersion": "3.19"
        },
        "packages": spdx_packages,
        "relationships": relationships
    }
    
    # Add conflict information as annotations
    if conflicts:
        spdx["annotations"] = []
        for conflict in conflicts:
            annotation = {
                "spdxId": f"SPDXRef-Package-0",
                "annotationType": "REVIEW",
                "annotationDate": datetime.now().isoformat() + "Z",
                "annotationComment": f"License conflict detected: {conflict.get('package1')} ({conflict.get('license1')}) vs {conflict.get('package2')} ({conflict.get('license2')}). Reason: {conflict.get('reason')}",
                "annotationSPDXID": "Tool: licenselens"
            }
            spdx["annotations"].append(annotation)
    
    return spdx


def map_severity(severity_str):
    """
    Map our severity levels to CVSS severity scale.
    """
    severity_map = {
        "critical": "critical",
        "high": "high",
        "medium": "medium",
        "low": "low"
    }
    return severity_map.get(severity_str.lower(), "medium")
