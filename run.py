import os
import sys
import subprocess

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'detector.py', 
        'database.py',
        'templates/index.html',
        'templates/records.html',
        'templates/add_student.html',
        'static/style.css'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found!")
    return True

def start_application():
    """Start the Flask application"""
    print("🚀 Starting Anti-Spoofing Attendance System...")
    print("📱 The application will open at: http://localhost:5000")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")

if __name__ == "__main__":
    if check_files():
        start_application()
    else:
        print("\n🔧 Please ensure all files are in place before running")
