import sqlite3
from datetime import datetime

class AttendanceDB:
    def __init__(self, db_name='attendance.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Students table with email support
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                student_id TEXT UNIQUE NOT NULL,
                email TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Check if email column exists, if not add it (for existing databases)
        cursor.execute("PRAGMA table_info(students)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'email' not in columns:
            cursor.execute("ALTER TABLE students ADD COLUMN email TEXT DEFAULT ''")
        
        # Attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                student_id TEXT NOT NULL,
                status TEXT NOT NULL,
                blinks INTEGER DEFAULT 0,
                motion_detected BOOLEAN DEFAULT 0,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def add_student(self, name, student_id, email=''):
        """Add student with optional email"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO students (name, student_id, email) VALUES (?, ?, ?)",
                (name, student_id, email)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_students(self):
        """Get all students with their information"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, student_id, email FROM students ORDER BY name")
        results = cursor.fetchall()
        
        # Convert to list of dictionaries for easier use
        students = []
        for row in results:
            students.append({
                'name': row[0],
                'student_id': row[1],
                'email': row[2] if row[2] else ''
            })
        return students
    
    def get_student_by_id(self, student_id):
        """Get specific student by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, student_id, email FROM students WHERE student_id = ?", (student_id,))
        result = cursor.fetchone()
        if result:
            return {
                'name': result[0],
                'student_id': result[1],
                'email': result[2] if result[2] else ''
            }
        return None
    
    def update_student(self, student_id, name=None, email=None):
        """Update student information"""
        try:
            cursor = self.conn.cursor()
            if name and email is not None:
                cursor.execute(
                    "UPDATE students SET name = ?, email = ? WHERE student_id = ?",
                    (name, email, student_id)
                )
            elif name:
                cursor.execute(
                    "UPDATE students SET name = ? WHERE student_id = ?",
                    (name, student_id)
                )
            elif email is not None:
                cursor.execute(
                    "UPDATE students SET email = ? WHERE student_id = ?",
                    (email, student_id)
                )
            self.conn.commit()
            return True
        except Exception:
            return False
    
    def delete_student(self, student_id):
        """Delete student and their attendance records"""
        try:
            cursor = self.conn.cursor()
            
            # Delete attendance records first
            cursor.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))
            
            # Delete student
            cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            
            self.conn.commit()
            return cursor.rowcount > 0  # Returns True if student was deleted
        except Exception:
            return False
    
    def mark_attendance(self, student_name, student_id, status, blinks, motion_detected, details):
        """Mark attendance for a student"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO attendance 
            (student_name, student_id, status, blinks, motion_detected, details)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (student_name, student_id, status, blinks, motion_detected, details))
        self.conn.commit()
    
    def get_records(self, limit=None):
        """Get attendance records with optional limit"""
        cursor = self.conn.cursor()
        query = '''
            SELECT student_name, student_id, status, blinks, motion_detected, 
                   details, timestamp 
            FROM attendance 
            ORDER BY timestamp DESC
        '''
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Convert to list of dictionaries
        records = []
        for row in results:
            records.append({
                'student_name': row[0],
                'student_id': row[1],
                'status': row[2],
                'blinks': row[3],
                'motion_detected': bool(row[4]),
                'details': row[5],
                'timestamp': row[6]
            })
        return records
    
    def get_student_records(self, student_id):
        """Get attendance records for specific student"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT student_name, student_id, status, blinks, motion_detected, 
                   details, timestamp 
            FROM attendance 
            WHERE student_id = ?
            ORDER BY timestamp DESC
        ''', (student_id,))
        
        results = cursor.fetchall()
        records = []
        for row in results:
            records.append({
                'student_name': row[0],
                'student_id': row[1],
                'status': row[2],
                'blinks': row[3],
                'motion_detected': bool(row[4]),
                'details': row[5],
                'timestamp': row[6]
            })
        return records
    
    def clear_records(self):
        """Clear all attendance records"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM attendance")
        self.conn.commit()
    
    def clear_student_records(self, student_id):
        """Clear attendance records for specific student"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))
        self.conn.commit()
    
    def get_statistics(self):
        """Get comprehensive attendance statistics"""
        cursor = self.conn.cursor()
        
        # Total students
        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]
        
        # Total records
        cursor.execute("SELECT COUNT(*) FROM attendance")
        total_records = cursor.fetchone()[0]
        
        # Present count
        cursor.execute("SELECT COUNT(*) FROM attendance WHERE status = 'PRESENT'")
        present_count = cursor.fetchone()[0]
        
        # Spoofing detected count
        cursor.execute("SELECT COUNT(*) FROM attendance WHERE status = 'SPOOFING_DETECTED'")
        spoofing_count = cursor.fetchone()[0]
        
        # No face detected count
        cursor.execute("SELECT COUNT(*) FROM attendance WHERE status = 'NO_FACE_DETECTED'")
        no_face_count = cursor.fetchone()[0]
        
        # Today's records
        cursor.execute("""
            SELECT COUNT(*) FROM attendance 
            WHERE DATE(timestamp) = DATE('now')
        """)
        today_records = cursor.fetchone()[0]
        
        # Success rate
        success_rate = round((present_count / total_records * 100) if total_records > 0 else 0, 1)
        
        return {
            'total_students': total_students,
            'total_records': total_records,
            'present_count': present_count,
            'spoofing_count': spoofing_count,
            'no_face_count': no_face_count,
            'today_records': today_records,
            'success_rate': success_rate
        }
    
    def get_daily_stats(self, date=None):
        """Get statistics for a specific date (default: today)"""
        cursor = self.conn.cursor()
        
        if date is None:
            date_filter = "DATE('now')"
        else:
            date_filter = f"'{date}'"
        
        cursor.execute(f"""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) as present,
                SUM(CASE WHEN status = 'SPOOFING_DETECTED' THEN 1 ELSE 0 END) as spoofing,
                SUM(CASE WHEN status = 'NO_FACE_DETECTED' THEN 1 ELSE 0 END) as no_face
            FROM attendance 
            WHERE DATE(timestamp) = DATE({date_filter})
        """)
        
        result = cursor.fetchone()
        return {
            'total': result[0],
            'present': result[1],
            'spoofing': result[2],
            'no_face': result[3],
            'success_rate': round((result[1] / result[0] * 100) if result[0] > 0 else 0, 1)
        }
    
    def student_exists(self, student_id):
        """Check if student exists"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM students WHERE student_id = ?", (student_id,))
        return cursor.fetchone() is not None
    
    def get_student_count(self):
        """Get total number of students"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        return cursor.fetchone()[0]
    
    def close(self):
        """Close database connection"""
        self.conn.close()
    
    def __del__(self):
        """Ensure connection is closed when object is destroyed"""
        try:
            self.conn.close()
        except:
            pass
