
import requests
import json

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MjVhYTk3Yy03OTU5LTRkY2QtODAwOS0wOTRjNDllOWUzZmQiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzcwOTg1NTU3fQ.G9vRrlr7AfSwZwM7rk45Ro9HjhgAmFGYADrWt1hjIso'
BASE_URL = 'https://n8n.srv1004677.hstgr.cloud/api/v1'
headers = {'X-N8N-API-KEY': API_KEY}

def get_data():
    wid = 'c0PvOAByBBAK3k9T' # Cristian Workflow
    params = {'workflowId': wid, 'limit': 10, 'status': 'success'}
    r = requests.get(BASE_URL + '/executions', headers=headers, params=params)
    if r.status_code != 200:
        print(f"Error listing: {r.status_code}")
        return

    for exe in r.json().get('data', []):
        eid = exe.get('id')
        det_r = requests.get(BASE_URL + '/executions/' + str(eid), headers=headers)
        if det_r.status_code == 200:
            det = det_r.json()
            runData = det.get('data', {}).get('resultData', {}).get('runData', {})
            for node_name, runs in runData.items():
                if 'Trigger' in node_name or 'Webhook' in node_name or 'Edit Fields' in node_name:
                    data = runs[0].get('data', {}).get('main', [[]])[0]
                    if isinstance(data, list): data = data[0]
                    if data and data.get('json'):
                        print(f"--- Data from Exe {eid} ---")
                        print(json.dumps(data['json'], indent=2))
                        return data['json']
    print("No data found in recent successful executions.")

if __name__ == "__main__":
    get_data()
