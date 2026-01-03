# GritCoin – Student Productivity Tracker

## Description
GritCoin is a full‑stack productivity and finance web application for students. It combines study session tracking and daily expense logging into one clean, data‑driven dashboard. The goal behind GritCoin is to help students visualize where they invest two of their scarcest resources — time and money — and manage both responsibly in a single place.

Built with Python (Flask) for the backend, SQLite for persistent storage, and a dynamic Bootstrap + Chart.js frontend, GritCoin demonstrates the full development cycle students learn in CS50: database design, secure authentication, frontend responsiveness, and server‑side logic integration.

The project emphasizes simplicity, security, and self‑containment: everything runs locally (no paid APIs or cloud dependencies). The app supports user registration and login with password hashing, full CRUD operations for both study sessions and expenses, real‑time data aggregation on a unified dashboard, and a Bootstrap 5‑based dark mode for nighttime study users.

## Design and Implementation Overview
At its core, GritCoin follows the Model‑View‑Controller (MVC) pattern:

      Models (via SQLAlchemy) define the User, StudySession, and Expense tables.

      Views (Jinja templates) determine all HTML rendered content.

      Controllers (Flask Blueprints) handle routing and business logic for authentication, data manipulation, and dashboard analytics.

      All session management is handled with Flask‑Login, ensuring only authenticated users access their personal data. Passwords are securely hashed with Werkzeug’s PBKDF2 algorithm, never stored in plain text.

      Chart.js dynamically pulls JSON data from Flask APIs (/dashboard/chart-data/<period>) to render weekly, monthly, and quarterly bar charts without page reloads — achieved via asynchronous Fetch calls.

      Data aggregation uses SQLAlchemy’s func.sum() to compute totals and daily groupings efficiently in SQL itself (not Python loops), highlighting the separation between application logic and data logic.

## Project Motivation and Design Choices
Students often juggle academics and budgets but track both separately — calendars for study and notebooks or apps for money. GritCoin merges those tasks in one web interface.
The design borrows UX from lightweight productivity tools — fast to load, responsive on mobile, with visual overviews instead of heavy analytics. Dark mode was implemented for accessibility and to recognize real student habits (late-night use).

SQLite was chosen for its zero‑setup simplicity — ideal for an educational prototype. The architecture allows switching to PostgreSQL by simply changing the SQLALCHEMY_DATABASE_URI.

## Features
Secure Authentication: Register/login/logout using Flask‑Login and password hashing.

Study Session Tracking: Record subject, duration (minutes), date, and notes.

Expense Management: Add spending by category, amount, and date with optional notes.

Interactive Dashboard:

   Total study time and spending are displayed per week, month, and quarter.

   Visualized through Chart.js bar graphs for quick pattern recognition.

Editing and Deletion: Full CRUD on study and expense entries.

Responsive UI: Uses Bootstrap 5 grid system and icons.

Dark Mode Toggle: Saves the user’s theme preference to localStorage.

## Tech Stack
Languages / Tools:
Python (Flask 3), HTML, CSS, JavaScript, Jinja2.

Frameworks & Libraries:
Flask‑Login, SQLAlchemy, Werkzeug Security (for password hashing).

Frontend:
Bootstrap 5.3, Chart.js 4.4, Bootstrap Icons.

Database:
SQLite (local file database.db, automatically created on first run).

## Installation and Setup

### Clone Repository

git clone <repository-url>
cd GritCoin

### Create Virtual Environment

python -m venv venv

### Activate venv

Windows: venv\Scripts\activate

macOS/Linux: source venv/bin/activate

### Install Dependencies

pip install -r requirements.txt

### Run

python app.py
Access at http://localhost:5000

## Usage Guide
Create an account (limited to 5 demo users).
Log in → Dashboard loads summary cards and empty charts.
Add Study Sessions → Provide subject, duration, and date; view instantly in table.
Add Expenses → Categorize spending, e.g., Food, Books, Transport.
View Dashboard → Switch between Week, Month, and Quarter to update charts live.
Dark Mode toggle for low‑light comfort; persists on refresh.

## Project Structure Explanation

GritCoin/
├─ app.py              → Application entry point; initializes Flask app, blueprints, error handlers.
├─ config.py           → All configuration variables (secret key, DB URI, session lifetime, user cap).
├─ models.py           → SQLAlchemy models: User, StudySession, Expense; defines relationships.
├─ routes/
│  ├─ auth.py          → Handles register, login, logout using Flask‑Login.
│  ├─ study.py         → CRUD routes for study sessions; ownership validation.
│  ├─ expense.py       → CRUD routes for expenses; ownership checks.
│  ├─ dashboard.py     → Analytics, JSON APIs for Chart.js, summarization by period.
│  └─ __init__.py      → Makes directory a Python package.
├─ templates/
│  ├─ base.html        → Parent layout (navbar, dark mode script, flash messages).
│  ├─ index.html       → Landing page highlighting app features.
│  ├─ auth/…           → Login and registration forms.
│  ├─ study/…          → List, add, edit templates for study sessions.
│  ├─ expense/…        → List, add, edit templates for expenses.
│  ├─ dashboard/…      → Dashboard view with canvases for Chart.js charts.
│  └─ errors/…         → Custom 404 and 500 pages for graceful error handling.
├─ static/
│  ├─ css/style.css    → Custom animations, hover effects, dark mode theme tweaks.
│  └─ js/dashboard.js  → Chart.js fetch logic, real‑time updates, theme control.
├─ requirements.txt    → Flask, SQLAlchemy, Flask‑Login, Werkzeug, python‑dotenv.
├─ README.md           → This documentation.
└─ database.db         → Auto‑generated SQLite file (when app runs).


## Configuration and Environment Variables
Create a .env file in the root directory:

SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///database.db
FLASK_DEBUG=True

## Design Decisions and Challenges
   Security: Strong hashing (PBKDF2) + session protection (HTTPOnly, SameSite=Lax).

   Error Handling: Custom 404 and 500 pages keep user experience consistent.

   Usability: Decided on Chart.js for responsive, free visualization versus heavier D3.

   Persistence: Kept SQLite for simplicity but abstracted layer to support migration.

   Scalability Thought: Structurally ready to move to PostgreSQL by changing config URI.

## Future Improvements
   CSV export for data.

   Email‑based password reset.

   AI‑based weekly productivity insights.

   Mobile PWA build for offline use.

## License
This project is open source under the MIT License.

## Credits
Developed by Surendra Tripathi as the CS50x 2025 Final Project.
Big thanks to the CS50 staff and community for documentation and testing utilities.

GritCoin – Encouraging balance between time, money, and growth.
