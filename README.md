---

# 🚀 SkillSync (Mahi Job Portal)
**A high-performance Job Aggregator Ecosystem built for the modern tech market.**

SkillSync is a backend-centric web application designed to bridge the gap between job seekers and employers. Built with a focus on **relational data integrity** and **clean system architecture**, the platform specializes in aggregating technical opportunities and matching them with candidate skill sets using a robust Many-to-Many mapping system.

---

## 🏗️ System Architecture
The project leverages the **Application Factory Pattern** via Flask, promoting a decoupled architecture where configurations, routes, and extensions are isolated.

* **Backend:** Python 3.14 + Flask (Modular Blueprints)
* **Database:** PostgreSQL (Relational mapping via SQLAlchemy ORM)
* **Logic Layer:** Implements complex SQL joins to facilitate skill-to-job matching.
* **Authentication:** Hybrid approach using **Flask-Login** for session persistence and **JWT** for secure API interactions.
* **Frontend:** "No-decoration" philosophy using **Jinja2 Templates** and **Vanilla CSS**, ensuring sub-100ms render times.



---

## 🛠️ Core Features

### 1. Skill-Centric Discovery
Unlike traditional boards, SkillSync uses a **Many-to-Many (M2M)** relationship model.
* **Dynamic Tagging:** Jobs are tagged with specific technical stacks (e.g., Python, React).
* **Relational Filtering:** Uses optimized SQL `JOIN` and `GROUP BY` logic to filter jobs by multiple skill IDs simultaneously without performance degradation.

### 2. Multi-Parametric Search
* **Contextual Queries:** Integrated search across Keywords, Locations (Hyderabad, Bangalore, Remote), and Company profiles.
* **Constraint-Based Logic:** Database-level constraints prevent duplicate applications and ensure data consistency.

### 3. Role-Based Access Control (RBAC)
* **Job Seekers:** Profile management, application tracking, and skill-matching dashboard.
* **Employers:** Job lifecycle management (Create, Update, Delete) and applicant review interface.

### 4. Minimalist "Typography-First" UI
* High-contrast, mobile-responsive design.
* Focus on **Readability over Ornamentation**, reducing cognitive load for users scanning high volumes of data.

---

## 📊 Database Schema
The heart of SkillSync lies in its relational structure, designed for referential integrity:

| Entity | Description | Key Relationships |
| :--- | :--- | :--- |
| **Users** | Core account data & Roles | 1:M with Applications |
| **Jobs** | Job metadata & requirements | M:M with Skills, 1:M with Applications |
| **Skills** | Technical stack definitions | M:M with Jobs |
| **Applications** | The "Join" entity for tracking | Links Users to Jobs |

---

## 📂 Project Structure
```text
job-agg-an-pf/
├── app/
│   ├── models/          # SQLAlchemy Models (User, Job, Skill, Association Tables)
│   ├── routes/          # Blueprints (auth_routes.py, job_routes.py, main_routes.py)
│   ├── static/          # Modular CSS (layout.css, components.css)
│   ├── templates/       # Jinja2 (base.html, job_detail.html, search.html)
│   ├── extensions.py    # Global init for SQLAlchemy, Migrate, and LoginManager
│   └── __init__.py      # App Factory (create_app)
├── .env                 # Environment Secrets (DATABASE_URL, SECRET_KEY)
├── run.py               # Entry point
└── requirements.txt     # Python 3.14+ Dependencies
```

---

## 🚀 Getting Started

1.  **Clone & Environment:**
    ```bash
    git clone https://github.com/ManideepK007/job-agg-an-pf.git
    cd job-agg-an-pf
    python -m venv venv
    source venv/bin/activate  # venv\Scripts\activate on Windows
    ```

2.  **Dependencies & Database:**
    ```bash
    pip install -r requirements.txt
    # Ensure PostgreSQL is running and update .env
    flask db upgrade
    ```

3.  **Execution:**
    ```bash
    python run.py
    ```

---

### 💡 Pro-Tip for your README
Since you mentioned using **Python 3.14**, make sure your `requirements.txt` specifically includes `psycopg2-binary` for PostgreSQL support and `python-dotenv` to handle that `.env` file you've smartly included in your structure! 
