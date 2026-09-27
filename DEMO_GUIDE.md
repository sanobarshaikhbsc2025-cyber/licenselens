# LicenseLens - Demo Guide for CA3 Review

This guide provides a step-by-step walkthrough for demonstrating your project to the reviewers on 28 Sept.

---

## ⏱️ Pre-Demo Checklist (Before Review Date)

- [ ] All code committed to `feature/dashboard-backend` branch
- [ ] GitHub repo is public
- [ ] All services build without errors
- [ ] Docker Compose starts successfully
- [ ] Dashboard is accessible at http://localhost:8501
- [ ] API docs are accessible at http://localhost:8000/docs
- [ ] Mock data loads correctly
- [ ] SBOM export works
- [ ] Practiced the demo flow

---

## 🚀 Starting the Demo (5 minutes before)

### Step 1: Start Services (2 mins)
```bash
cd licenselens
docker-compose up

# Expected output:
# licenselens-backend | Uvicorn running on http://0.0.0.0:8000
# licenselens-dashboard | You can now view your Streamlit app in your browser.
# licenselens-dashboard | Local URL: http://localhost:8501
```

### Step 2: Verify Services (1 min)
```bash
# In another terminal:
curl http://localhost:8000/health
# Expected: {"status":"healthy","service":"licenselens-backend",...}

# Visit http://localhost:8501 in browser
# Should see: LicenseLens dashboard loaded
```

### Step 3: Have demo files ready
```bash
# Sample requirements.txt files:

# 1. Safe project
cat > django_safe.txt << EOF
Django==4.2
requests==2.31
sqlalchemy==2.0
EOF

# 2. Project with conflicts
cat > gpl_conflict.txt << EOF
some-gpl-lib==1.0
requests==2.31
EOF
```

---

## 📊 Demo Flow (10 minutes)

### Demo Segment 1: Architecture Overview (2 mins)
**Show on screen: Docker Compose output**
```
Point out:
✅ Backend service running (port 8000)
✅ Dashboard service running (port 8501)
✅ Both connected via Docker network
```

**Talk points:**
- "We have two main services: FastAPI backend and Streamlit dashboard"
- "They communicate via HTTP API"
- "Both containerized and orchestrated with Docker Compose"
- "Easy to scale or swap components"

---

### Demo Segment 2: API Documentation (1 min)
**Show on screen: http://localhost:8000/docs**
```
Click on different endpoints to show:
- POST /scan
- GET /results/{project_id}
- GET /sbom/{project_id}
- GET /stats
- GET /health
```

**Talk points:**
- "API is fully documented with Swagger UI"
- "Can test endpoints directly from browser"
- "Clear request/response schemas"

---

### Demo Segment 3: Dashboard Overview (1 min)
**Show on screen: http://localhost:8501**
```
Show the navigation:
- 📤 New Scan (current)
- 📊 Project History
- 📈 Statistics
- ℹ️ About
```

**Talk points:**
- "Clean, intuitive interface"
- "Multiple sections for different workflows"
- "Real-time processing with Streamlit"

---

### Demo Segment 4: File Upload & Scan (3 mins)
**Live demo:**

1. **Upload file:**
   - Click "Choose a file"
   - Select `django_safe.txt`
   - Click "🔍 Start Scan"

2. **Show results loading:**
   - "Connecting to backend API..."
   - "Processing dependencies..."
   - Results appear with:
     - Compliance status (✅ COMPLIANT)
     - Package count
     - Conflict count
     - License distribution

3. **Show packages table:**
   - Django (BSD-3-Clause)
   - requests (Apache-2.0)
   - sqlalchemy (MIT)
   - "All licenses compatible"

**Talk points:**
- "System scans dependencies in real-time"
- "Each package is identified with its license"
- "Licenses matched against SPDX standard"
- "Compatibility checked automatically"

---

### Demo Segment 5: Conflict Detection (2 mins)
**Upload file with conflicts:**

1. **Upload `gpl_conflict.txt`**
   - Shows some-gpl-lib + requests

2. **Point out:**
   - "⚠️ WARNINGS - There are license conflicts"
   - Red highlight on conflicts
   - Detailed explanation of why they conflict
   - Severity level (CRITICAL, HIGH, MEDIUM, LOW)

3. **Explain rules:**
   - "GPL-3.0 is incompatible with Apache-2.0"
   - "Our system detects this automatically"
   - "Prevents distribution issues later"

**Talk points:**
- "Conflict detection is the core value"
- "Rules based on SPDX guidelines"
- "Severity helps prioritize fixes"

---

### Demo Segment 6: SBOM Export (1 min)
**Back to first (safe) scan:**

1. **Scroll to SBOM section**
2. **Click "📥 Download SBOM (JSON)"**
3. **Show JSON output:**
   ```json
   {
     "bomFormat": "CycloneDX",
     "specVersion": "1.4",
     "components": [
       {
         "type": "library",
         "name": "Django",
         "version": "4.2.0",
         "licenses": [...]
       }
     ]
   }
   ```

4. **Download button:**
   - Click "⬇️ Download as JSON"
   - File downloads to computer

**Talk points:**
- "SBOM is industry standard (CycloneDX)"
- "Can be used for compliance reporting"
- "Also supports SPDX format"
- "Ready for supply chain security tools"

---

### Demo Segment 7: History & Stats (1 min)
**Navigate to 📊 Project History**
```
Show:
- List of previous scans
- Projects with package counts
- Conflict indicators
```

**Then show 📈 Statistics:**
```
Show:
- Total scans
- Total packages analyzed
- License distribution chart
- Most common licenses
```

**Talk points:**
- "System keeps history of all scans"
- "Can run reports across projects"
- "Metrics help track compliance trends"

---

## 🎤 Q&A Preparation

### Expected Questions & Answers

**Q: Why did you use FastAPI for the backend?**
```
A: "FastAPI is modern, fast, and has automatic API documentation
via Swagger. Plus it's lightweight - perfect for a microservice.
Also integrates well with Streamlit."
```

**Q: How does the license detection work?**
```
A: "Currently using mock data that represents what Person A's
scanner will provide. The scanner reads requirements.txt, queries
PyPI API for each package's license, and returns the data.
Our backend then processes it and checks compatibility rules."
```

**Q: What's the purpose of Docker Compose?**
```
A: "Allows us to define all services in one file. Makes it easy
to start/stop everything together. Also ensures it runs the same
on any machine - important for reproducibility and testing."
```

**Q: How do you detect conflicts?**
```
A: "We have a compatibility matrix that defines which license
combinations are problematic. For example, GPL-3.0 conflicts with
Apache-2.0. We check all pairs of licenses in the project against
this matrix and flag incompatibilities."
```

**Q: Can this integrate with Person A's scanner?**
```
A: "Yes! Once Person A finishes the scanner, we'll call their API
instead of using mock data. The interface is the same, so it's a
drop-in replacement. The frontend code won't need to change."
```

**Q: What if a project has no conflicts?**
```
A: "The system shows 'COMPLIANT' status in green. Users can still
export the SBOM for documentation and audit purposes. Zero conflicts
is the goal!"
```

**Q: How do you handle errors?**
```
A: "We have error handling throughout - file upload errors, API
connection errors, etc. User gets clear error messages on the
dashboard. Backend logs full errors for debugging."
```

**Q: Why use Streamlit for the dashboard?**
```
A: "Streamlit lets us build interactive dashboards quickly with pure
Python. No need for JavaScript/React. Perfect for data visualization
and rapid prototyping. Makes it easy to add features."
```

---

## 📝 Presenting Your Code

### Repository Tour (5 minutes)

**In GitHub or terminal:**

```bash
# Show the structure
tree -L 2 licenselens/

# Show Git history
git log --oneline --graph

# Explain branching
git branch -a
```

**Talking points:**
- "15+ commits on feature/dashboard-backend"
- "Each commit is focused on one feature"
- "Clear commit messages explain what changed"
- "Demonstrates proper Git discipline"
- "Ready to merge to main via PR"

---

### Code Walkthrough (5 minutes)

**Show key files:**

1. **docker-compose.yml**
   ```yaml
   services:
     backend:
       build: ./backend
       ports: [8000:8000]
     dashboard:
       build: ./dashboard
       ports: [8501:8501]
   ```
   "Shows our multi-service architecture"

2. **backend/main.py (just /scan endpoint)**
   ```python
   @app.post("/scan")
   async def scan_project(file: UploadFile = File(...)):
       # Process file
       # Call mock scanner
       # Return results
   ```
   "Core endpoint for scanning"

3. **backend/sbom_generator.py**
   ```python
   def generate_cyclonedx_sbom(scan_data):
       # Build SBOM in industry standard format
   ```
   "Handles compliance report generation"

4. **dashboard/streamlit_app.py**
   ```python
   uploaded_file = st.file_uploader(...)
   response = requests.post(f"{API_URL}/scan", ...)
   st.write(results)
   ```
   "Clean, simple UI code"

---

## 🎬 Demo Script (Print This)

Use this script during your presentation:

```
=== DEMO SCRIPT ===

Intro (30 seconds):
"LicenseLens scans Python projects for license compliance issues.
It's a two-service application: FastAPI backend and Streamlit
dashboard, orchestrated with Docker Compose."

Architecture (1 minute):
"Here's docker-compose.yml. You can see we have two services:
the backend runs on port 8000, dashboard on 8501, connected via
a Docker network. Both are containerized, so they run consistently
anywhere."

API (30 seconds):
"The backend exposes a REST API. Here's the Swagger docs showing
all endpoints. The main one is POST /scan which processes a
requirements.txt file."

Dashboard Demo (3 minutes):
"Let me upload a project file..." [upload]
"Here are the scanned packages, each with its license identified."
[show table]
"No conflicts here, so we see ✅ COMPLIANT."
[scroll to conflicts section]
"Let me upload a conflicting project..." [upload]
"Here's an example of GPL + Apache-2.0. Our system flags this as
CRITICAL because it's a known incompatibility. Users get clear
guidance on what needs to be fixed."

SBOM Export (1 minute):
"We can export the results as a Software Bill of Materials in
industry-standard CycloneDX format. This is useful for compliance
and supply chain security."

Results (1 minute):
"We keep history of all scans and show statistics. This helps
track compliance across multiple projects over time."

Questions:
"Any questions about the architecture, code, or approach?"
```

---

## ✅ Demo Checklist

Before starting demo:
- [ ] Services are running and healthy
- [ ] Terminal shows no errors
- [ ] Dashboard loads in browser
- [ ] API docs are accessible
- [ ] Test files are ready
- [ ] GitHub repo is up to date
- [ ] Have this guide printed/available

During demo:
- [ ] Speak clearly and confidently
- [ ] Point to things on screen
- [ ] Pause for questions
- [ ] Don't rush through features
- [ ] Show both success and edge cases
- [ ] Explain what reviewers are seeing

After demo:
- [ ] Answer all questions
- [ ] Thank reviewers
- [ ] Be ready for follow-up questions

---

## 🎯 What Reviewers Are Looking For

✅ **Problem Statement**: Clear problem, why it matters
✅ **Architecture**: Sound design, containerization explained
✅ **Working Code**: Runs without errors, does what it claims
✅ **Git History**: Quality commits, collaboration evident
✅ **Documentation**: README is clear, setup works
✅ **Explanation**: You can explain design choices confidently

---

## 🚨 Troubleshooting During Demo

**Issue: Services don't start**
```
Solution: Pre-test on morning of demo!
docker-compose up
# Let it run for 30 seconds to ensure all services healthy
```

**Issue: File upload fails**
```
Solution: Check backend logs
docker-compose logs backend
# Look for error messages
```

**Issue: Dashboard can't reach backend**
```
Solution: Check network connectivity
curl http://localhost:8000/health
# Should get JSON response
```

**Issue: Browser won't load**
```
Solution: Try different browser, clear cache, check ports
lsof -i :8501  # Check if port is in use
```

---

## 📸 Screenshot Tips

Take screenshots during demo for your CA4 submission:
- Dashboard homepage
- File upload in progress
- Scan results with packages
- Conflict detection highlight
- SBOM export preview
- API Swagger docs
- GitHub repository view
- Git log showing commits

---

## 🎓 Learning Points to Emphasize

During Q&A, mention these to show understanding:

- "We used Docker to ensure reproducibility"
- "FastAPI auto-generates API documentation"
- "Mock data lets us build independently while Person A works"
- "SBOM is an industry standard for compliance"
- "Git branching lets us collaborate without conflicts"
- "Streamlit simplifies UI development"
- "License compatibility is complex but critical"

---

## 💡 Pro Tips

1. **Rehearse the demo** - Practice 2-3 times before 28 Sept
2. **Have a backup** - Prepare a recorded demo video just in case
3. **Know your numbers** - Be ready to say how many commits, files, etc.
4. **Explain decisions** - Why Docker? Why Streamlit? Why this architecture?
5. **Show confidence** - You built this! You should be proud.

---

## 📞 If Something Goes Wrong

**Plan B: Explain Anyway**
Even if demo fails, you can:
1. Show the code
2. Show the GitHub history
3. Walk through the architecture on paper
4. Explain the mock data and how it works
5. Describe what would happen if you ran it

Reviewers value understanding over perfect execution!

---

Good luck with your demo! 🎉

You've got this! ✨
