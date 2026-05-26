
import requests
import json
import os

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MjVhYTk3Yy03OTU5LTRkY2QtODAwOS0wOTRjNDllOWUzZmQiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzcwOTg1NTU3fQ.G9vRrlr7AfSwZwM7rk45Ro9HjhgAmFGYADrWt1hjIso"
BASE_URL = "https://n8n.srv1004677.hstgr.cloud/api/v1"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def create_workflow(payload_file):
    with open(payload_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    response = requests.post(f"{BASE_URL}/workflows", headers=headers, json=data)
    if response.status_code == 200 or response.status_code == 201:
        print(f"Successfully created workflow from {payload_file}")
        return response.json()
    else:
        print(f"Failed to create workflow from {payload_file}: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    # Create Dispatcher
    dispatcher = create_workflow("n8n_dispatcher.json")
    if dispatcher:
        print(f"Dispatcher ID: {dispatcher.get('id')}")
