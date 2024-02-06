import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
headers = { 'X-Cisco-Meraki-API-Key': os.getenv('API_KEY') }

def get_organization_id():
    url = f"{os.getenv('BASE_URL')}/organizations"
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text)[0]['id']
    
#request to fetch network id using organization id by organizationId() function
def get_network_id():
    #print("Env")
    #print(os.getenv('ORG_ID'))
    url = f"{os.getenv('BASE_URL')}/organizations/{get_organization_id()}/networks" if os.getenv('ORG_ID') is None else f"{os.getenv('BASE_URL')}/organizations/{os.getenv('ORG_ID')}/networks"
    #print (url)
    response = requests.request("GET", url, headers=headers)
    #print(response.text)
    return json.loads(response.text)[0]['id']
    
#request to fetch the sent and received bytes for each uplink of a network.
def get_bb_data_set(beginTimespan, endTimespan):
    url = f"{os.getenv('BASE_URL')}/networks/{get_network_id()}/appliance/uplinks/usageHistory?t0={beginTimespan}&t1={endTimespan}&resolution=3600"
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    dataset = []

    #build the list of objects to be returned filtering only the non-null data
    for index in range(0,len(data)):
        try:
            dataset.append({   
                'startTime': data[index]['startTime'][0:10], 
                'endTime': data[index]['endTime'][0:10],
                'wan1': {
                    'sent':data[index]['byInterface'][0]['sent'],
                    'received':data[index]['byInterface'][0]['received']
                    }
            })
        except Exception:
            print (Exception)
            break
    return dataset

def get_if_data_set(beginTimespan, endTimespan):
    url = f"{os.getenv('BASE_URL')}/networks/{get_network_id()}/appliance/uplinks/usageHistory?t0={beginTimespan}&t1={endTimespan}&resolution=3600"
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    dataset = []

    #build the list of objects to be returned filtering only the non-null data
    for index in range(0,len(data)):
        try:
            dataset.append({   
                'date': data[index]['startTime'][0:10],
                'hour': {
                    'start':data[index]['startTime'][11:19],
                    'end':data[index]['endTime'][11:19]
                    },
                'wan1': {
                    'sent':data[index]['byInterface'][0]['sent'],
                    'received':data[index]['byInterface'][0]['received']
                    }
            })
        except Exception:
            print (Exception)
            break
    return dataset
