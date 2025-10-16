# Django Template Project Structure

## 📁 Organized Project Layout

```
django_template/
├── 📁 django_app/                    # Main Django application
│   ├── 📁 django_template/           # Django project settings
│   ├── 📁 main/                      # Main app with views, models, templates
│   ├── 📁 static/                    # Static files
│   ├── manage.py                     # Django management script
│   └── db.sqlite3                    # Local development database
│
├── 📁 docs/                         # All documentation
│   ├── 📁 deployment/               # Deployment guides
│   │   ├── RENDER_DEPLOYMENT_RUNBOOK.md
│   │   ├── RENDER_DEPLOYMENT_INSTRUCTIONS.md
│   │   └── RENDER_DEPLOYMENT_CHECKLIST.md
│   ├── 📁 oauth/                    # OAuth setup guides
│   │   ├── GOOGLE_OAUTH_RENDER_SETUP.md
│   │   ├── google_oauth_manual_setup.md
│   │   └── google_oauth_setup.md
│   ├── architecture.mermaid         # System architecture
│   ├── status.md                    # Project status
│   ├── technical.md                 # Technical specifications
│   ├── REQUIREMENTS_MANAGEMENT.md   # Dependency management guide
│   └── SUCCESSFUL_DEPLOYMENT_LOG.md # Deployment success log
│
├── 📁 scripts/                      # Deployment and utility scripts
│   ├── 📁 legacy/                   # Old/unused scripts
│   │   ├── requirements_old.txt
│   │   ├── requirements_clean.txt
│   │   ├── requirements.prod.txt
│   │   └── oauth-config.yaml
│   └── build.sh                     # Render build script
│
├── 📁 tasks/                        # Project tasks and requirements
│   └── tasks.md
│
├── 📁 django_template_env/          # Local virtual environment (gitignored)
│
├── 📄 requirements.in               # High-level dependencies
├── 📄 requirements.txt               # Generated complete dependencies
├── 📄 render.yaml                    # Render deployment configuration
├── 📄 pytest.ini                    # Testing configuration
├── 📄 README.md                      # Project overview
└── 📄 PROJECT_STRUCTURE.md          # This file
```

## 🚀 How to Run the Project

### 1. **Local Development**
```bash
# Create and activate virtual environment
python -m venv django_template_env
source django_template_env/bin/activate  # On Windows: django_template_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
cd django_app
python manage.py migrate

# Start development server
python manage.py runserver
```

### 2. **Deploy to Render**
```bash
# Push to GitHub (triggers automatic deployment)
git add .
git commit -m "Update project"
git push origin main

# Or manually trigger deployment
export RENDER_API_KEY=your_api_key
render deploys create srv-your-service-id --confirm
```

### 3. **Update Dependencies**
```bash
# Edit requirements.in
# Then regenerate requirements.txt
pip-compile requirements.in
pip install -r requirements.txt
```

## 📚 Documentation Navigation

- **Getting Started**: `README.md`
- **Deployment**: `docs/deployment/`
- **OAuth Setup**: `docs/oauth/`
- **Requirements**: `docs/REQUIREMENTS_MANAGEMENT.md`
- **Architecture**: `docs/architecture.mermaid`
- **Success Log**: `docs/SUCCESSFUL_DEPLOYMENT_LOG.md`

## 🧹 Cleanup Notes

- **Removed**: Scattered documentation files
- **Organized**: All docs into `docs/` with subfolders
- **Moved**: Scripts to `scripts/` with legacy folder
- **Kept**: Only essential files in root directory
- **Preserved**: All functionality and deployment capability
