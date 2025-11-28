import subprocess
from time import sleep
import requests

print("Starting Server")
server = subprocess.Popen(["python","app.py"])

print("Waiting to start")

attempt = 0
max_attempts = 25

while attempt < max_attempts:
    try:
        req = requests.get("http://127.0.0.1:5000", timeout=5)
        break;
    except:
        attempt+=1
        sleep(5)

if attempt == max_attempts:
    exit(-1)

print("Starting pytest")

test = subprocess.Popen(["pytest"])
test.communicate()

server.terminate()

exit(test.returncode)