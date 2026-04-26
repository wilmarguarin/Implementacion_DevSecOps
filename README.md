# NovaCorp — Company Management Platform

NovaCorp Platform is an internal web application for managing companies and their associated comments. It supports three roles (`admin`, `owner`, `user`) with different access levels.

---

## Installation

```bash
pip install -r requirements.txt
pip install flask-wtf
python main.py
```

Visit: http://127.0.0.1:5000

The database is automatically initialized on first run.

---

## Default Users

| Username | Password   | Role   | Notes                      |
|----------|------------|--------|----------------------------|
| alice    | password1  | user   | Standard employee          |
| bob      | password2  | owner  | Owns "Insegura Corp"       |
| admin    | admin123   | admin  | Full access                |

---

## Project Structure

```
.
├── Dockerfile               
├── main.py                 # Entry point
├── server.py               # Flask app configuration
├── db/
│   └── \_\_init\_\_.py         # Database initialization and helpers
├── routes/
│   ├── auth.py             # Login/logout
│   ├── companies.py        # Company views, dashboard, search
│   ├── companies\_admin.py  # Admin company management
│   ├── users\_admin.py      # Admin user management
│   └── profile.py          # User profiles
├── templates/
│   ├── base.html           # Shared layout
│   ├── dashboard.html      # Main dashboard
│   ├── auth/               # Login page
│   ├── companies/          # Company pages
│   ├── admin/              # Admin panels
│   ├── profile/            # User profile pages
│   └── errors/             # 404, 403 pages
├── static/
│   └── css/style.css       # Custom styles
└── requirements.txt
```


---

## Technologies

- Python 3 + Flask  
- SQLite  
- Bootstrap 5.3  
- Jinja2  
- Gunicorn  

---

## DevSecOps Integration

This project implements a DevSecOps pipeline using GitHub Actions.

### SAST
SonarQube is used for static analysis. The pipeline fails if the Quality Gate is not met.

### SCA
pip-audit is used for dependency analysis. The pipeline fails if vulnerabilities are found.

### DAST
OWASP ZAP is used for dynamic analysis against the deployed application.

---

## Deployment (Render)

Public URL: https://implementacion-devsecops.onrender.com

### Configuration

Build:
pip install -r requirements.txt

Start:
gunicorn main:app --bind 0.0.0.0:$PORT

### Deployment Control

Auto-Deploy is configured as:
After CI Checks Pass

This ensures deployment only happens if all security checks pass.

---

## Docker (Optional)

Build:
docker build -t novacorp-app .

Run:
docker run -p 10000:10000 novacorp-app

Access:
http://localhost:10000

---

## Docker CI Validation

The project includes a Dockerfile to containerize the Flask application.

A GitHub Actions workflow validates the Docker image build on every push to the main branch.

Workflow:

.github/workflows/docker.yml

The Docker pipeline performs:

1. Repository checkout.
2. Docker Buildx setup.
3. Docker image build validation.

The image is not pushed to a registry in this academic setup. The objective is to verify that the application can be packaged and executed in a reproducible containerized environment.

---

## Security Coverage

- SAST → Source code analysis  
- SCA  → Dependency analysis  
- DAST → Runtime analysis  

---

## Summary

This project demonstrates a complete DevSecOps implementation with automated security checks and controlled deployment.
