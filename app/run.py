import subprocess
import time

print("[SYSTEM] Starting Face Recognition Production System")

# Start AI
ai = subprocess.Popen(["python", "main.py"])

time.sleep(2)

# Start Dashboard
dashboard = subprocess.Popen(["python", "dashboard.py"])

print("[SYSTEM] AI + Dashboard Running")
print("[SYSTEM] Dashboard -> http://127.0.0.1:5001")

ai.wait()
dashboard.wait()
