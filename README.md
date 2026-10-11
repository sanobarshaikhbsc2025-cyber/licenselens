# 🔍 LicenseLens — License Compliance Scanner

> **Automated detection of open-source license conflicts and compliance risks in Python projects.**

![Version](https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.11+-green?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

---

## 📌 Problem Statement

Open-source projects often use third-party dependencies without checking license compatibility, creating significant legal and compliance risks:
- Combining GPL-licensed libraries with proprietary code.
- Using incompatible licenses in the same project (e.g., GPL-3.0 + Apache-2.0).
- Lack of visibility into transitive dependencies' licenses.

**LicenseLens** solves this by automatically scanning Python dependency trees, flagging illegal/risky license combinations, and generating a Software Bill of Materials (SBOM).

---

## ✨ Key Features

- 🎯 **Automated Dependency Scanning:** Scans `requirements.txt` and `pyproject.toml` files instantly.
- 🌐 **PyPI API Integration:** Live fetch for accurate, real-time license metadata.
- ⚠️ **Conflict Detection:** Identifies GPL, Apache, MIT, and permissive vs. copyleft license clashes.
- 📄 **SBOM Generation:** Export clear compliance reports for audit-ready builds.
- 🐳 **Dockerized Setup:** Ready to run in isolated environments with Docker Compose.

---

## 🛠️ Tech Stack

- **Core Engine:** Python 3.11+
- **Containerization:** Docker, Docker Compose
- **APIs:** PyPI Metadata API

---
2. Run with Docker Compose
   
   docker-compose up --build

4. Repository Structure
   
├── backend/          # Scanner engine & logic
├── dashboard/        # UI/Analytics frontend
├── docker-compose.yml # Container orchestration
└── README.md


## 🚀 Quick Setup & Usage

###  Clone the repository
```bash
git clone [https://github.com/sanobarshaikhbsc2025-cyber/licensens.git](https://github.com/sanobarshaikhbsc2025-cyber/licensens.git)
cd licensens

