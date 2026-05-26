
import requests
import json

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MjVhYTk3Yy03OTU5LTRkY2QtODAwOS0wOTRjNDllOWUzZmQiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzcwOTg1NTU3fQ.G9vRrlr7AfSwZwM7rk45Ro9HjhgAmFGYADrWt1hjIso'
BASE_URL = 'https://n8n.srv1004677.hstgr.cloud/api/v1'
headers = {'X-N8N-API-KEY': API_KEY}

def analyze_errors():
    # 1. Get all workflows for mapping IDs to Names
    wf_map = {}
    wf_res = requests.get(BASE_URL + '/workflows', headers=headers)
    if wf_res.status_code == 200:
        for wf in wf_res.json().get('data', []):
            wf_map[wf['id']] = wf['name']
    
    # 2. List 20 most recent errors
    params = {'limit': 20, 'status': 'error'}
    r = requests.get(BASE_URL + '/executions', headers=headers, params=params)
    if r.status_code != 200:
        print(f"Error listing: {r.status_code}")
        return

    for exe in r.json().get('data', []):
        eid = exe.get('id')
        wid = exe.get('workflowId')
        wf_name = wf_map.get(wid, wid)
        print(f"\n--- [ERROR] ID: {eid} | Workflow: {wf_name} ({wid}) ---")
        
        # Get details
        det_r = requests.get(BASE_URL + '/executions/' + str(eid), headers=headers)
        if det_r.status_code == 200:
            det = det_r.json()
            err_msg = det.get('data', {}).get('resultData', {}).get('error', {}).get('message', 'No error message')
            print(f"Error Message: {err_msg}")
            
            # Extract input data from trigger/webhook
            runData = det.get('data', {}).get('resultData', {}).get('runData', {})
            for node_name, runs in runData.items():
                if any(k in node_name for k in ['Webhook', 'Trigger', 'Edit Fields']):
                    try:
                        main_data = runs[0].get('data', {}).get('main', [[]])[0]
                        if isinstance(main_data, list): main_data = main_data[0]
                        if main_data and main_data.get('json'):
                            print("Input Data:")
                            print(json.dumps(main_data['json'], indent=2))
                    except:
                        pass
        else:
            print("Could not retrieve execution details.")

if __name__ == "__main__":
    analyze_errors()
