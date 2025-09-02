import subprocess
import sys
import os
import urllib.request

def install_requirements():
    """Install all required packages"""
    print("🔧 Installing required packages...")
    
    packages = [
        "opencv-python==4.8.1.78",
        "flask==2.3.3",
        "imutils==0.5.4",
        "scipy==1.11.3",
        "numpy==1.24.3"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    print("✅ All packages installed successfully!")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['templates', 'static']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

def check_camera():
    """Test camera availability"""
    print("📹 Testing camera...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Camera is accessible!")
            cap.release()
            return True
        else:
            print("❌ Camera not accessible")
            return False
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Setting up Anti-Spoofing Attendance System...")
    
    create_directories()
    
    if install_requirements():
        if check_camera():
            print("\n✅ Setup completed successfully!")
            print("📋 Next steps:")
            print("1. Run: python app.py")
            print("2. Open: http://localhost:5000")
            print("3. Test the system with different students")
        else:
            print("\n⚠️ Setup completed but camera issues detected")
            print("Please check your camera connection")
    else:
        print("\n❌ Setup failed during package installation")
