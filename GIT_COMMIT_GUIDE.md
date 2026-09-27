# Git Commit Guide for Person B (Frontend/Dashboard)

This guide provides recommended commit messages to demonstrate proper Git workflow and commit discipline for the CA3 review.

## Getting Started

### 1. Initialize Repository
```bash
# Only do this ONCE for the entire project
git init
git remote add origin <your-github-url>

# Create and switch to your feature branch
git checkout -b feature/dashboard-backend
```

### 2. First Commit - Project Setup
```bash
git add .gitignore README.md
git commit -m "docs: initialize project with README and gitignore"
```

---

## Recommended Commit Sequence (In Order)

Copy-paste each commit message as you complete the corresponding work.

### Commit 1: Project Structure
```bash
git add backend/main.py backend/models.py
git commit -m "feat(backend): scaffold FastAPI application structure"
```

### Commit 2: Mock Data Module
```bash
git add backend/mock_data.py
git commit -m "feat(backend): add mock data generator for testing

- Includes 4 mock project types
- License conflict detection logic
- Compliance status determination"
```

### Commit 3: SBOM Generator
```bash
git add backend/sbom_generator.py
git commit -m "feat(backend): implement SBOM generation

- CycloneDX JSON format support
- SPDX JSON format support
- Severity mapping for conflicts"
```

### Commit 4: Backend Requirements
```bash
git add backend/requirements.txt
git commit -m "build(backend): add Python dependencies

- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- pydantic==2.4.2
- requests==2.31.0"
```

### Commit 5: Backend Docker Setup
```bash
git add backend/Dockerfile.backend
git commit -m "docker(backend): create Dockerfile for FastAPI service

- Python 3.11 slim base image
- Installs dependencies
- Exposes port 8000
- Runs uvicorn server"
```

### Commit 6: Core API Endpoints
```bash
git add backend/main.py  # (with updated version)
git commit -m "feat(backend): implement REST API endpoints

- POST /scan - file upload and scan
- GET /results/{project_id} - fetch results
- GET /sbom/{project_id} - export SBOM
- GET /projects - list all projects
- GET /stats - overall statistics
- GET /health - health check"
```

### Commit 7: Dashboard UI Setup
```bash
git add dashboard/streamlit_app.py
git commit -m "feat(dashboard): build Streamlit UI with core features

- Page: New Scan (upload and process)
- Page: Project History (previous scans)
- Page: Statistics (overall metrics)
- Page: About (project info)
- Custom CSS styling
- API integration"
```

### Commit 8: Dashboard Requirements
```bash
git add dashboard/requirements.txt
git commit -m "build(dashboard): add Streamlit dependencies

- streamlit==1.28.1
- requests==2.31.0
- pandas==2.1.1"
```

### Commit 9: Dashboard Docker Setup
```bash
git add dashboard/Dockerfile.dashboard
git commit -m "docker(dashboard): create Dockerfile for Streamlit service

- Python 3.11 slim base image
- Installs dependencies
- Exposes port 8501
- Runs Streamlit app"
```

### Commit 10: Docker Compose Configuration
```bash
git add docker-compose.yml
git commit -m "docker: add docker-compose for service orchestration

- Defines backend (FastAPI) service
- Defines dashboard (Streamlit) service
- Network bridge connection
- Health checks
- Port mappings"
```

### Commit 11: Documentation Updates
```bash
git add README.md
git commit -m "docs: complete project documentation

- Problem statement
- Architecture overview
- Quick start guide
- API reference
- Technology stack
- Team roles and workflow"
```

### Commit 12: SBOM Export Feature
```bash
git add backend/sbom_generator.py dashboard/streamlit_app.py
git commit -m "feat: add SBOM export functionality

- Download as CycloneDX JSON
- Download as SPDX format
- Include in project results
- User-friendly naming"
```

### Commit 13: Conflict Visualization
```bash
git add dashboard/streamlit_app.py
git commit -m "feat(dashboard): enhance conflict visualization

- Color-coded severity levels
- Detailed conflict cards
- License compatibility info
- Severity distribution metrics"
```

### Commit 14: Session State Management
```bash
git add dashboard/streamlit_app.py
git commit -m "fix(dashboard): improve session state handling

- Persist scan results across pages
- Navigate between projects
- Maintain user selections"
```

### Commit 15: Error Handling and Logging
```bash
git add backend/main.py dashboard/streamlit_app.py
git commit -m "refactor: add comprehensive error handling

- API error responses
- Connection error handling
- User-friendly error messages
- Health check validation"
```

---

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc)
- `refactor`: Code refactoring
- `test`: Adding tests
- `docker`: Docker/deployment changes
- `build`: Build system or dependencies
- `perf`: Performance improvements
- `chore`: Maintenance tasks

### Scopes
- `backend`: FastAPI backend code
- `dashboard`: Streamlit dashboard code
- `docker`: Docker configuration
- `docs`: Documentation

### Subject
- Use imperative mood ("add" not "added")
- Don't capitalize first letter
- No period at the end
- Max 50 characters

### Body (Optional)
- Explain what and why, not how
- Wrap at 72 characters
- Separate from subject by blank line

### Example
```
feat(backend): add CORS middleware

Allow requests from dashboard service running on different port.
Necessary for development and production deployment.
```

---

## Pushing to GitHub

### First time pushing to remote
```bash
git push -u origin feature/dashboard-backend
```

### Subsequent pushes
```bash
git push origin feature/dashboard-backend
```

### View your commits
```bash
git log --oneline
# or
git log --graph --oneline --all
```

---

## Creating a Pull Request

1. Push your feature branch to GitHub
2. Go to repository on GitHub
3. Click "New Pull Request"
4. Select `feature/dashboard-backend` → `main`
5. Add PR title and description
6. Submit for review

### PR Template
```markdown
## Description
Brief description of changes

## Related Issues
Fixes #(issue number)

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Infrastructure

## Testing
Tested with mock data:
- [ ] File upload works
- [ ] API endpoints respond
- [ ] Conflicts are detected
- [ ] SBOM generates

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for clarity
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
```

---

## Useful Git Commands

### Check status
```bash
git status
```

### View commits
```bash
git log --oneline -10
git log --graph --oneline --all
```

### Undo changes
```bash
# Unstage a file
git reset HEAD filename

# Discard changes
git checkout -- filename

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

### Stash changes
```bash
git stash
git stash pop
```

### Merge main into feature (if needed)
```bash
git fetch origin
git merge origin/main
```

---

## Tips for CA3 Review

✅ **DO:**
- Make commits as you complete features
- Use meaningful commit messages
- Keep commits focused (one feature per commit)
- Push to GitHub regularly
- Reference issues in commits if applicable

❌ **DON'T:**
- Make giant commits with 10 features
- Use vague messages like "fixed stuff"
- Commit directly to main branch
- Force push unless absolutely necessary
- Commit large binary files

---

## Example Output for Reviewer

When you run `git log --oneline` on CA3 review date:

```
abc1234 refactor: add comprehensive error handling
def5678 fix(dashboard): improve session state handling
ghi9012 feat(dashboard): enhance conflict visualization
jkl3456 feat: add SBOM export functionality
mno7890 docs: complete project documentation
pqr1234 docker: add docker-compose for orchestration
stu5678 docker(dashboard): create Dockerfile for Streamlit
vwx9012 build(dashboard): add Streamlit dependencies
yza3456 feat(dashboard): build Streamlit UI
bcd7890 docker(backend): create Dockerfile for FastAPI
efg1234 build(backend): add Python dependencies
hij5678 feat(backend): implement REST API endpoints
klm9012 docker(backend): scaffold FastAPI structure
nop3456 feat(backend): implement SBOM generation
qrs7890 feat(backend): add mock data generator
tuv1234 docs: initialize project
```

This shows clear progression and good commit discipline! ✨

---

## Questions During CA3 Q&A

Be ready to answer:
- "Why did you organize commits this way?"
  - Answer: Each commit represents one feature/task, making it easy to review and rollback if needed.

- "How does Git help your team collaboration?"
  - Answer: Person A and I work on separate branches (feature/scanner and feature/dashboard), then merge via PRs. This prevents conflicts.

- "What's in each Docker service?"
  - Answer: Backend is FastAPI (port 8000), Dashboard is Streamlit (port 8501), connected via Docker network.

- "Can you explain the API flow?"
  - Answer: User uploads file → Dashboard calls /scan → Backend processes → Results stored → Frontend displays + SBOM exported.
