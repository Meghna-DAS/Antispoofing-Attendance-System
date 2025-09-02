import sqlite3

def fix_attendance_table():
    """Add missing student_name column to attendance table"""
    
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    try:
        print("🔧 Checking if student_name column exists...")
        
        # Check current structure
        cursor.execute("PRAGMA table_info(attendance)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'student_name' not in column_names:
            print("❌ student_name column missing. Adding it now...")
            
            # Add the missing column
            cursor.execute("ALTER TABLE attendance ADD COLUMN student_name TEXT DEFAULT ''")
            
            print("✅ student_name column added successfully!")
            
            # Update existing records with student names
            print("🔄 Updating existing records...")
            cursor.execute("""
                UPDATE attendance 
                SET student_name = (
                    SELECT name FROM students 
                    WHERE students.student_id = attendance.student_id
                )
                WHERE student_name = '' OR student_name IS NULL
            """)
            
            updated_rows = cursor.rowcount
            print(f"✅ Updated {updated_rows} existing records with student names")
            
        else:
            print("✅ student_name column already exists!")
        
        # Verify the fix
        print("\n🔍 FINAL TABLE STRUCTURE:")
        cursor.execute("PRAGMA table_info(attendance)")
        columns = cursor.fetchall()
        for i, col in enumerate(columns, 1):
            print(f"  {i}. {col[1]} ({col[2]})")
        
        conn.commit()
        print("\n🎉 Database fix completed successfully!")
        
    except Exception as e:
        print(f"❌ Error fixing database: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    fix_attendance_table()
