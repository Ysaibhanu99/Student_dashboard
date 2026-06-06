# Student Performance Analytics Dashboard

A responsive, light-themed analytics dashboard built with Python, Flask, Neon PostgreSQL, and Chart.js. This application demonstrates a complete database-to-visualization pipeline (DB → API → JSON → Chart.js), displaying key student performance indicators and interactive data charts.

## 🚀 Features

- **Live Summary KPIs**: Dynamic count of students, average marks, average attendance, and top scorer statistics.
- **Grade Distribution (Doughnut Chart)**: Visual breakdown of student performance categories (A, B, C, D, F).
- **Department Averages (Bar Chart)**: Average academic marks grouped across departments (CSE, ECE, MECH).
- **Marks Distribution (Horizontal Bar Chart)**: Frequency distribution of marks in range intervals.
- **Attendance vs. Marks Correlation (Scatter Plot)**: Interactive scatter chart with customized hover states revealing student-specific details.
- **Aesthetic UI**: Modern, premium light theme utilizing the *Outfit* and *Inter* Google Fonts, FontAwesome icons, responsive flex/grid layouts, and clean transition hover states.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Database**: PostgreSQL (hosted on Neon)
- **DB Driver**: psycopg2-binary
- **Charting Library**: Chart.js (CDN-delivered)
- **Frontend**: HTML5, Vanilla JavaScript, CSS3 variables, FontAwesome

---

## 📂 Project Structure

```text
student-dashboard/
│
├── app.py               # Main Flask application and API endpoints
├── db.py                # Database connection utility
├── verify_db.py         # DB verification and seeding helper
│
├── templates/
│   └── dashboard.html   # Frontend interface layout & Chart.js wiring
│
├── static/
│   └── style.css        # Clean, light-themed styles and animations
│
├── .env                 # Local environment configurations (ignored by git)
├── .gitignore           # File/folder patterns to exclude from git
├── requirements.txt     # Python requirements manifest
└── README.md            # Project guide and documentation
```

---

## ⚡ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Ysaibhanu99/Student_dashboard.git
cd Student_dashboard
```

### 2. Set Up Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a file named `.env` in the root directory and add your Neon PostgreSQL connection string:
```env
DATABASE_URL=postgresql://neondb_owner:npg_I7rtceAjR4Yl@ep-cool-field-ap38r44l-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
FLASK_ENV=development
PORT=5000
```

### 5. Seed the Database
Verify the PostgreSQL connection and seed the initial student records into the database:
```bash
python verify_db.py
```

### 6. Run the Application
Start the local development server:
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000` to interact with the dashboard.

---

## 🔌 API Reference

The dashboard dynamically fetches its data from the following RESTful API endpoints:

| Endpoint | Method | Response Description |
| :--- | :--- | :--- |
| `/api/summary` | `GET` | Returns overall KPIs: total student count, average marks, average attendance, top scorer name, and top score. |
| `/api/grade-distribution` | `GET` | Returns grades count grouped by labels (`['A', 'B', 'C', 'D', 'F']`). |
| `/api/department-avg` | `GET` | Returns average marks grouped by department. |
| `/api/marks-distribution` | `GET` | Returns count frequency of students inside specific marks brackets. |
| `/api/attendance-vs-marks` | `GET` | Returns individual coordinate maps of attendance and marks. |
