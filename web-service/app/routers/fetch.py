from fastapi import APIRouter, Response, BackgroundTasks
import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime
from datetime import timedelta
from pandas import json_normalize
from ta.volatility import BollingerBands
from ta.utils import dropna
import io

load_dotenv()
headers = { 'X-Cisco-Meraki-API-Key': os.getenv('API_KEY') }

router = APIRouter(
    prefix="/fetch",
    tags=["fetch"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def fetch_data(background_tasks: BackgroundTasks):
    
    t1 = str(datetime.now())
    t0 = str(datetime.now() - timedelta(days=21))
    
    jsonResponse = get_data_set(t0[0:10]+"T23:59:59Z",t1[0:10]+"T00:00:00Z")
    
    df = json_normalize(jsonResponse)
    df.rename(columns={'startTime':'START','endTime':'END','wan1.sent':'W1_SENT','wan1.received':'W1_RECEIVED','wan2.sent':'W2_SENT',"wan2.received":"W2_RECEIVED"},inplace=True)
    
    file = io.BytesIO()

    indicator_W1avgSent=BollingerBands(close=df["W1_SENT"],window=20,window_dev=2)
    indicator_W1avgReceived=BollingerBands(close=df["W1_RECEIVED"],window=20,window_dev=2)
    
    # Add Bollinger Bands features
    df['W1S_MIDDLE_BAND'] = indicator_W1avgSent.bollinger_mavg()
    df['W1S_HIGH_BAND'] = indicator_W1avgSent.bollinger_hband()
    df['W1S_LOW_BAND'] = indicator_W1avgSent.bollinger_lband()
    
    df['W1R_MIDDLE_BAND'] = indicator_W1avgReceived.bollinger_mavg()
    df['W1R_HIGH_BAND'] = indicator_W1avgReceived.bollinger_hband()
    df['W1R_LOW_BAND'] = indicator_W1avgReceived.bollinger_lband()
    
    df = dropna(df)
    df.to_csv(file,index=False)
    background_tasks.add_task(file.close)
    headers = {'Content-Disposition': 'attachment; filename="data_set.csv"'}
    return Response(file.getvalue(), headers=headers, media_type='text/csv')

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
def get_data_set(beginTimespan, endTimespan):
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
