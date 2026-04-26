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

TThis project implements a DevSecOps pipeline using GitHub Actions to integrate automated security controls into the development lifecycle.

## SAST - Static Application Security Testing

Static analysis is performed using SonarQube.

Detects vulnerabilities and security issues in source code
Applies a Quality Gate based on severity

The pipeline fails if the Quality Gate conditions are not met.

## SCA - Software Composition Analysis

Dependency analysis is performed using:
pip-audit

- Identifies known vulnerabilities in third-party dependencies
- Uses public vulnerability databases
- The pipeline fails if vulnerable dependencies are detected

## DAST - Dynamic Application Security Testing

Dynamic analysis is performed using OWASP ZAP against the deployed application.

- Scans the running application
- Detects runtime vulnerabilities (headers, misconfigurations, etc.)

The pipeline fails if vulnerabilities are detected..

---

## Deployment (Render)

The application is deployed on Render and publicly accessible at:

https://implementacion-devsecops.onrender.com

## Configuration

Build command:
pip install -r requirements.txt

Start command:
gunicorn main:app --bind 0.0.0.0:$PORT

## Deployment Control (DevSecOps)

Deployment is configured as:
Auto-Deploy: After CI Checks Pass

This ensures:

The application is deployed only if all CI/CD checks pass
Deployments are blocked when security vulnerabilities are detected

This integrates security validation directly into the deployment process.

---

## Docker Deployment (Optional)

Build:
docker build -t novacorp-app .

Run:
docker run -p 10000:10000 novacorp-app

Access:
http://localhost:10000

## Docker Design Decisions

The Dockerfile was designed following best practices:

Use of a lightweight base image (python:3.11-slim)
Separation of dependency installation to optimize build caching
Use of --no-cache-dir to reduce image size
Execution using Gunicorn for production readiness
Environment-based configuration for portability

This approach improves reproducibility, portability, and security.

---

## Docker CI Validation

A GitHub Actions workflow validates the Docker image build on every push.

Workflow location:

.github/workflows/docker.yml

Pipeline steps:

- Repository checkout
- Docker Buildx setup
- Docker image build validation

The image is not published to a registry in this setup. The objective is to ensure that the application can be reliably packaged and executed in a containerized environment.

---

## Security Coverage

This project implements a multi-layer security approach:

- SAST → Source code analysis
- SCA → Dependency analysis
- DAST → Runtime analysis 

---

## Summary

This project demonstrates a complete DevSecOps implementation by integrating automated security analysis, controlled deployment, and containerization practices.

Security checks are enforced throughout the CI/CD pipeline, ensuring that only validated and secure code is deployed.
