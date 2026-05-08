import requests

for i in range(5):
    r = requests.get("http://127.0.0.1:8000/ask-protected")
    print(r.json())