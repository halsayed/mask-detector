import os
import requests
import time


application_uuid = os.environ.get('APPLICATION_UUID', '817c6f3c-7f0b-4189-83b6-07d6966e4546')
url = f'https://karbon.nutanix.com/v1.0/applications/{application_uuid}'
token = os.environ.get('KPS_API_KEY')
headers = {'Authorization': f'Bearer {token}',
           'Content-Type': 'application/json'}


resp = requests.get(url, headers=headers)
if resp.status_code == 200:
    print(f'INFO - Application {application_uuid} found on kps')
    payload = resp.json()
    del (payload['version'])
    del (payload['createdAt'])
    del (payload['updatedAt'])
    payload['state'] = 'UNDEPLOY'
    resp = requests.put(url, json=payload, headers=headers)
    if resp.status_code == 200:
        print(f'INFO - application stopped, waiting 4 seconds')
        time.sleep(4)
        payload['state'] = 'DEPLOY'
        resp = requests.put(url, json=payload, headers=headers)
        if resp.status_code == 200:
            print(f'INFO - Application restart successfully')
    else:
        print(f'ERROR - failed to stop application, status code: {resp.status_code}')
        print(f'ERROR - Message: {resp.content}')

else:
    print(f'ERROR - API call failed with status code: {resp.status_code}')
    print(f'ERROR - Message: {resp.content}')
