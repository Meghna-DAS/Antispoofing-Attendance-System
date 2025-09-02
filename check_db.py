import sqlite3

# Connect to your database
conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

print("🔍 CHECKING ATTENDANCE TABLE STRUCTURE:")
print("=" * 50)

try:
    cursor.execute("PRAGMA table_info(attendance)")
    columns = cursor.fetchall()
    
    print("Current columns in attendance table:")
    for i, col in enumerate(columns, 1):
        print(f"  {i}. {col[1]} ({col[2]})")
    
    # Check if student_name exists
    column_names = [col[1] for col in columns]
    if 'student_name' in column_names:
        print("\n✅ student_name column EXISTS")
    else:
        print("\n❌ student_name column MISSING!")
        print("🔧 Need to add this column...")
        
except Exception as e:
    print(f"❌ Error checking table: {e}")

conn.close()
