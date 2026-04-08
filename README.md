# 🚀 Mahi Job Portal (SkillSync)
**A high-performance Job Aggregator Ecosystem built for the modern tech market.**

The Mahi Job Portal is a backend-centric web application designed to bridge the gap between job seekers and employers. Built with a focus on **relational data integrity** and **clean system architecture**, the platform specializes in aggregating technical opportunities and matching them with candidate skill sets.

---

## 🏗️ System Architecture
The project follows the **Application Factory Pattern** using Flask, ensuring the codebase remains modular, scalable, and easy to maintain.

* **Backend:** Python 3.14 + Flask (Modular Blueprints)
* **Database:** PostgreSQL (Relational mapping via SQLAlchemy)
* **Authentication:** Session-based with Flask-Login & Security via JWT
* **Frontend:** Minimalist Jinja2 Templates + Vanilla CSS (No-decoration philosophy)
* **Environment:** Decoupled configuration using `.env` for security



---

## 🛠️ Core Features

### 1. Advanced Search & Filtering
* **Multi-Parametric Querying:** Filter jobs by Keyword, City (Hyderabad, Bangalore, Remote), and Company.
* **Skill-Based Matching:** A Many-to-Many relationship model allowing users to find jobs based on specific technical stacks (e.g., Python, React, Next.js).
* **Optimized Performance:** Implements SQL `GROUP BY` logic to handle complex joins without triggering JSON equality errors.

### 2. User & Role Management
* **Secure Authentication:** Protected routes for job posting and application tracking.
* **Role-Based Access (RBAC):** Distinct logic paths for "Job Seekers" and "Employers/Companies."

### 3. "Quick Apply" Engine
* **Frictionless UX:** Single-click application logic that records intent and prevents duplicate entries through database-level constraints.

### 4. Minimalist UI/UX
* **Typography-First Design:** Leveraging clean fonts and generous whitespace to prioritize readability.
* **Responsive Feed:** A mobile-friendly job board that adapts to any screen size.

---

## 📂 Project Structure
```text
D:\SoW\job-agg-an-pf\
├── app/
│   ├── models/          # SQLAlchemy Database Models (User, Job, Skill)
│   ├── routes/          # Blueprint-based Route Handlers (job_routes.py, etc.)
│   ├── static/          # Professional Minimalist CSS & Assets
│   ├── templates/       # Jinja2 HTML Templates (explore.html, etc.)
│   ├── extensions.py    # Database & Login Manager Initialization
│   └── __init__.py      # The App Factory (create_app)
├── .env                 # Environment Secrets (DB_URL, SECRET_KEY)
├── run.py               # Application Entry Point
└── requirements.txt     # Dependency Manifest