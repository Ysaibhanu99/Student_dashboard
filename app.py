import os
from flask import Flask, jsonify, render_template
from db import get_db_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/summary')
def summary():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get count, avg marks, avg attendance
        cur.execute("SELECT COUNT(*), AVG(marks), AVG(attendance) FROM students")
        count, avg_marks, avg_attendance = cur.fetchone()
        
        # Get top scorer
        cur.execute("SELECT name, marks FROM students ORDER BY marks DESC, name ASC LIMIT 1")
        top_scorer, top_marks = cur.fetchone()
        
        cur.close()
        return jsonify({
            "total_students": count,
            "avg_marks": round(float(avg_marks), 1) if avg_marks is not None else 0.0,
            "avg_attendance": round(float(avg_attendance), 1) if avg_attendance is not None else 0.0,
            "top_scorer": top_scorer if top_scorer else "N/A",
            "top_marks": int(top_marks) if top_marks is not None else 0
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/grade-distribution')
def grade_distribution():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT grade, COUNT(*) 
            FROM students 
            GROUP BY grade 
            ORDER BY grade
        """)
        rows = cur.fetchall()
        cur.close()
        
        labels = [row[0] for row in rows]
        values = [row[1] for row in rows]
        
        return jsonify({
            "labels": labels,
            "values": values
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/department-avg')
def department_avg():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT department, AVG(marks) 
            FROM students 
            GROUP BY department 
            ORDER BY department
        """)
        rows = cur.fetchall()
        cur.close()
        
        labels = [row[0] for row in rows]
        values = [round(float(row[1]), 1) for row in rows]
        
        return jsonify({
            "labels": labels,
            "values": values
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/marks-distribution')
def marks_distribution():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT marks FROM students")
        rows = cur.fetchall()
        cur.close()
        
        marks_list = [row[0] for row in rows]
        
        ranges = {
            "0-40": 0,
            "41-50": 0,
            "51-60": 0,
            "61-70": 0,
            "71-80": 0,
            "81-90": 0,
            "91-100": 0
        }
        for m in marks_list:
            if m <= 40:
                ranges["0-40"] += 1
            elif m <= 50:
                ranges["41-50"] += 1
            elif m <= 60:
                ranges["51-60"] += 1
            elif m <= 70:
                ranges["61-70"] += 1
            elif m <= 80:
                ranges["71-80"] += 1
            elif m <= 90:
                ranges["81-90"] += 1
            else:
                ranges["91-100"] += 1
                
        return jsonify({
            "labels": list(ranges.keys()),
            "values": list(ranges.values())
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/attendance-vs-marks')
def attendance_vs_marks():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, attendance, marks FROM students ORDER BY id")
        rows = cur.fetchall()
        cur.close()
        
        data = [{"name": row[0], "attendance": row[1], "marks": row[2]} for row in rows]
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
