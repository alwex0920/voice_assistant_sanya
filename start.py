import subprocess

command = ["python", "assistant.py"]

process = subprocess.Popen(command)

process.wait()
