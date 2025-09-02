<!DOCTYPE html>
<html>
<body>

<h1>Face Recognition & Anti-Spoofing Attendance System</h1>

<p>
  <strong>Welcome!</strong> This repository provides a secure, real-time attendance system using face recognition and anti-spoofing techniques. The solution ensures that only genuine users can mark attendance by combining facial, eye, blink, and motion detection.
</p>

<h2>🚀 Features</h2>
<ul>
  <li>Real-time camera initialization and video capture</li>
  <li>Face and eye detection</li>
  <li>Blink pattern and motion analysis for anti-spoofing</li>
  <li>Screen pattern checks to prevent spoofing attempts</li>
  <li>Face recognition for user identification</li>
  <li>Attendance marking and database updates</li>
  <li>Clear user feedback and security alerts</li>
</ul>

<h2>🛠️ Setup Instructions</h2>
<ol>
  <li><strong>Clone the repository</strong>
    <pre><code>git clone https://github.com/yourusername/face-attendance-antispoofing.git
cd face-attendance-antispoofing</code></pre>
  </li>
  <li><strong>Install dependencies</strong>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li><strong>Configure the database</strong>
    <br>
    Update <code>config.py</code> or the relevant configuration file with your database credentials.
  </li>
  <li><strong>Run the application</strong>
    <pre><code>python main.py</code></pre>
  </li>
</ol>

<h2>📖 Usage</h2>
<ul>
  <li>Start the application and allow camera access.</li>
  <li>Follow on-screen instructions for face, eye, blink, and motion checks.</li>
  <li>If recognized, your attendance will be marked and confirmed.</li>
  <li>If spoofing or unknown user is detected, appropriate alerts will be displayed.</li>
</ul>

<h2>🤝 Contributing</h2>
<ul>
  <li>Fork the repository and create a new branch for your feature or bugfix.</li>
  <li>Submit a pull request describing your changes.</li>
  <li>For major changes, please open an issue to discuss your ideas first.</li>
</ul>

<h2>🧩 Troubleshooting</h2>
<ul>
  <li><strong>Camera not detected:</strong> Ensure your webcam is connected and accessible.</li>
  <li><strong>Face not detected:</strong> Check lighting and camera angle.</li>
  <li><strong>Blink/motion not detected:</strong> Blink clearly or move slightly as prompted.</li>
  <li><strong>Spoofing detected:</strong> Do not use photos or screens; ensure a real face is present.</li>
</ul>

<h2>📄 License</h2>
<p>
  This project is licensed under the MIT License.
</p>

<h2>📬 Contact</h2>
<p>
  For questions or support, open an issue or email <a href="mailto:meghna1512das@gmail.com">meghna1512das@gmail.com</a>.
</p>

</body>
</html>


