import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def verify_and_seed_db():
    if not DATABASE_URL:
        print("Error: DATABASE_URL not found in environment variables.")
        return

    print("Connecting to Neon PostgreSQL database...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        print("Connected successfully!")

        # Create table if it doesn't exist
        print("Checking if 'students' table exists...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id          SERIAL PRIMARY KEY,
                name        VARCHAR(100) NOT NULL,
                roll_number VARCHAR(20)  UNIQUE NOT NULL,
                department  VARCHAR(50)  NOT NULL,
                marks       INT          NOT NULL CHECK (marks >= 0 AND marks <= 100),
                grade       CHAR(1)      NOT NULL,
                attendance  INT          NOT NULL CHECK (attendance >= 0 AND attendance <= 100)
            );
        """)
        conn.commit()
        print("Table 'students' created or verified.")

        # Check if table is empty
        cur.execute("SELECT COUNT(*) FROM students;")
        count = cur.fetchone()[0]
        print(f"Current student count in DB: {count}")

        if count == 0:
            print("Seeding database with initial student records...")
            seed_data = [
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
                ('Vijay Kumar',   'CS020', 'CSE', 71, 'B', 77)
            ]
            
            cur.executemany("""
                INSERT INTO students (name, roll_number, department, marks, grade, attendance)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, seed_data)
            conn.commit()
            
            # Verify record count
            cur.execute("SELECT COUNT(*) FROM students;")
            new_count = cur.fetchone()[0]
            print(f"Database seeded successfully! Total records: {new_count}")
        else:
            print("Database already contains data. Seeding skipped.")

        cur.close()
        conn.close()
        print("Database verification finished successfully!")

    except Exception as e:
        print(f"Database error occurred: {e}")

if __name__ == "__main__":
    verify_and_seed_db()
