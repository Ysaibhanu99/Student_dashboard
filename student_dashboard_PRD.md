# PRD — Student Performance Dashboard (Day 8 Foundation Project)

---

## 1. Purpose

Build a Flask + Neon dashboard where dedicated API endpoints return JSON
data and Chart.js renders multiple chart types on a single page.
**Core goal:** Build the complete DB → API → JSON → Chart.js pipeline
that powers every analytics dashboard — including Smart Attendance.

---

## 2. Success Criteria

By end of Day 8, you should be able to say:

> "I built Flask API endpoints that return JSON, called them with JavaScript
> fetch(), and rendered bar, doughnut, and line charts from real database
> data — and I understand every line."

---

## 3. Tech Stack

| Layer         | Technology                              |
|---------------|-----------------------------------------|
| Backend       | Python + Flask                          |
| Database      | PostgreSQL (Neon)                       |
| DB Driver     | psycopg2-binary                         |
| Charting      | Chart.js (CDN)                          |
| Frontend      | HTML + JavaScript (fetch API)           |

---

## 4. Database Schema

**New Neon project:** `student_dashboard`

```sql
CREATE TABLE students (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    roll_number VARCHAR(20)  UNIQUE NOT NULL,
    department  VARCHAR(50)  NOT NULL,
    marks       INT          NOT NULL CHECK (marks >= 0 AND marks <= 100),
    grade       CHAR(1)      NOT NULL,
    attendance  INT          NOT NULL CHECK (attendance >= 0 AND attendance <= 100)
);

INSERT INTO students (name, roll_number, department, marks, grade, attendance) VALUES
('Bhanu Prasad',  'CS001', 'CSE', 92, 'A', 95),
('Ravi Kumar',    'CS002', 'CSE', 78, 'B', 82),
('Sita Devi',     'CS003', 'ECE', 85, 'A', 90),
('Arjun Reddy',   'CS004', 'CSE', 60, 'C', 74),
('Priya Lakshmi', 'CS005', 'ECE', 45, 'F', 60),
('Kiran Babu',    'CS006', 'MECH',88, 'A', 88),
('Anjali Singh',  'CS007', 'CSE', 73, 'B', 79),
('Suresh Naidu',  'CS008', 'MECH',55, 'D', 65),
('Divya Rao',     'CS009', 'ECE', 91, 'A', 93),
('Manoj Varma',   'CS010', 'MECH',67, 'C', 71),
('Lakshmi Nair',  'CS011', 'CSE', 80, 'B', 85),
('Venkat Rao',    'CS012', 'ECE', 95, 'A', 97),
('Swathi Reddy',  'CS013', 'MECH',70, 'B', 76),
('Harish Kumar',  'CS014', 'CSE', 50, 'D', 68),
('Meena Kumari',  'CS015', 'ECE', 83, 'A', 89),
('Ganesh Prasad', 'CS016', 'MECH',76, 'B', 80),
('Sunita Devi',   'CS017', 'CSE', 62, 'C', 73),
('Ramesh Babu',   'CS018', 'ECE', 89, 'A', 92),
('Kavitha Nair',  'CS019', 'MECH',44, 'F', 58),
('Vijay Kumar',   'CS020', 'CSE', 71, 'B', 77);
```

---

## 5. Routes

### Page Route
| Method | Route | What it does              |
|--------|-------|---------------------------|
| GET    | `/`   | Render dashboard.html     |

### API Routes (return JSON only)
| Method | Route                      | What it returns                          |
|--------|----------------------------|------------------------------------------|
| GET    | `/api/summary`             | Total students, avg marks, avg attendance|
| GET    | `/api/grade-distribution`  | Count of students per grade              |
| GET    | `/api/department-avg`      | Average marks per department             |
| GET    | `/api/marks-distribution`  | Count of students in mark ranges         |
| GET    | `/api/attendance-vs-marks` | Scatter data: attendance + marks per student |

5 API endpoints + 1 page route.

---

## 6. API Response Formats

### GET /api/summary
```json
{
    "total_students": 20,
    "avg_marks": 74.5,
    "avg_attendance": 79.6,
    "top_scorer": "Venkat Rao",
    "top_marks": 95
}
```

### GET /api/grade-distribution
```json
{
    "labels": ["A", "B", "C", "D", "F"],
    "values": [8, 6, 3, 2, 1]
}
```

### GET /api/department-avg
```json
{
    "labels": ["CSE", "ECE", "MECH"],
    "values": [72.3, 84.5, 68.8]
}
```

### GET /api/marks-distribution
```json
{
    "labels": ["0-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91-100"],
    "values": [0, 3, 2, 4, 5, 4, 2]
}
```

### GET /api/attendance-vs-marks
```json
{
    "data": [
        {"name": "Bhanu Prasad", "attendance": 95, "marks": 92},
        {"name": "Ravi Kumar",   "attendance": 82, "marks": 78}
    ]
}
```

---

## 7. Dashboard UI

### Single page: `dashboard.html`

**Section 1 — Summary Cards (top row)**
- 4 cards: Total Students | Avg Marks | Avg Attendance | Top Scorer
- Values loaded via `fetch('/api/summary')`

**Section 2 — Charts (grid layout)**

| Chart | Type | API endpoint |
|---|---|---|
| Grade Distribution | Doughnut | `/api/grade-distribution` |
| Department Average Marks | Bar | `/api/department-avg` |
| Marks Distribution | Bar (horizontal) | `/api/marks-distribution` |
| Attendance vs Marks | Scatter | `/api/attendance-vs-marks` |

---

## 8. Core Code Patterns

### Flask API endpoint pattern
```python
@app.route('/api/grade-distribution')
def grade_distribution():
    conn = get_db_connection()
    cur  = conn.cursor()
    cur.execute("""
        SELECT grade, COUNT(*) 
        FROM students 
        GROUP BY grade 
        ORDER BY grade
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    labels = [row[0] for row in rows]
    values = [row[1] for row in rows]

    return jsonify({"labels": labels, "values": values})
```

### JavaScript fetch + Chart.js pattern
```javascript
async function loadGradeChart() {
    const res  = await fetch('/api/grade-distribution');
    const data = await res.json();

    new Chart(document.getElementById('gradeChart'), {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: ['#4CAF50','#2196F3','#FF9800','#F44336','#9C27B0']
            }]
        }
    });
}

loadGradeChart();
```

### Loading summary cards
```javascript
async function loadSummary() {
    const res  = await fetch('/api/summary');
    const data = await res.json();

    document.getElementById('total-students').textContent = data.total_students;
    document.getElementById('avg-marks').textContent      = data.avg_marks;
    document.getElementById('avg-attendance').textContent = data.avg_attendance + '%';
    document.getElementById('top-scorer').textContent     = data.top_scorer;
}

loadSummary();
```

---

## 9. Folder Structure

```
student-dashboard/
│
├── app.py               ← Page route + 5 API routes
├── db.py                ← Connection function
│
├── templates/
│   └── dashboard.html   ← All charts rendered here
│
├── static/
│   └── style.css        ← Dashboard layout CSS
│
├── .env
├── requirements.txt
└── .gitignore
```

---

## 10. Build Order (follow exactly)

```
Step 1 → Create Neon project, create table, run seed data.
         Verify: SELECT COUNT(*) FROM students → 20 rows.
Step 2 → Set up folder, copy db.py from previous project.
Step 3 → Write GET / route + empty dashboard.html skeleton.
         Confirm page loads.
Step 4 → Write GET /api/summary — test in browser, confirm JSON response.
Step 5 → Write GET /api/grade-distribution — test in browser.
Step 6 → Write GET /api/department-avg — test in browser.
Step 7 → Write GET /api/marks-distribution — test in browser.
Step 8 → Write GET /api/attendance-vs-marks — test in browser.
Step 9 → Add Chart.js CDN to dashboard.html.
         Load summary cards with fetch().
Step 10 → Add doughnut chart for grade distribution.
Step 11 → Add bar chart for department averages.
Step 12 → Add bar chart for marks distribution.
Step 13 → Add scatter chart for attendance vs marks.
Step 14 → Style the dashboard — cards, grid layout, colors.
```

---

## 11. Strictly Out of Scope

- ❌ Authentication
- ❌ Add / edit / delete students
- ❌ Date filters or time range selection
- ❌ Export to PDF or CSV
- ❌ Real-time updates (that was Day 7)
- ❌ Deployment (optional only if you finish early)

---

## 12. What This Teaches You

| Concept                          | Where you use it in future                    |
|---------------------------------|-----------------------------------------------|
| Dedicated `/api/` routes         | Clean separation of data and presentation     |
| `GROUP BY` in SQL                | Every aggregation query in every dashboard    |
| `AVG()`, `COUNT()` SQL functions | Smart Attendance reports, marks summaries     |
| JavaScript `fetch()` API         | How React/Vue talks to your Flask backend     |
| Chart.js setup pattern           | Every dashboard you'll ever build             |
| Multiple chart types             | Bar, doughnut, line, scatter — all from today |
| Scatter plot pattern             | Correlation analysis — attendance vs marks    |

---

## 13. The Bigger Picture

After today all 8 blocks are complete:

```
✅ Block 1 — CRUD + DB          (Expense Tracker)
✅ Block 2 — Authentication      (Auth Boilerplate)
✅ Block 3 — REST API            (Contact Book API)
✅ Block 4 — File Handling       (Farmers Notice Board)
✅ Block 5 — Search/Filter/Page  (Student Marks Lookup)
✅ Block 6 — Email/Notifications (OTP Login)
✅ Block 7 — Real-time           (Live Attendance)
✅ Block 8 — Data Visualization  (Student Dashboard) ← TODAY
```

Tomorrow: Smart Attendance with Marks Management.
Every wall you hit last time now has a solution you've already built.

---

*PRD version: 1.0 | Project: Foundation Block 8 — Data Visualization*
