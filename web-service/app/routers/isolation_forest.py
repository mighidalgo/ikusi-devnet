import numpy as np
from sklearn.ensemble import IsolationForest
from fastapi import APIRouter, Response, BackgroundTasks
from datetime import datetime
from datetime import timedelta
from pandas import json_normalize
from ta.utils import dropna
import io
import os
from dotenv import load_dotenv

load_dotenv()
from app.templates.fetch_dataset import get_if_data_set

isolation_forest_router = APIRouter()

@isolation_forest_router.get("/")
async def detect_outliers(background_tasks: BackgroundTasks):
    #Parameters for the date range to be consumed by the API
    t1 = str(datetime.now())
    t0 = str(datetime.now() - timedelta(days=21))
    #Get API data
    jsonResponse = get_if_data_set(t0[0:10]+"T23:59:59Z",t1[0:10]+"T00:00:00Z")
    
    #The response to the data frame is loaded
    df = json_normalize(jsonResponse)
    
    """
    Function for the calculation of the "Isolation Forest" algorithm.
        The function will return two lists, one with the labels of each data 
        (1 for normal, -1 for atypical) and a list of scores, 
        if the value is closer to -1; it is more likely to be atypical, otherwise, 
        if they are closer to 1 it is more likely to be normal values.
    """
    def get_outliers(X, cont=None):

        if cont is None and os.getenv('ISOLATION_SENSITIVITY') is not None and os.getenv('ISOLATION_SENSITIVITY') != "":
            #print("Using current value from envioration variable")
            cont = float(os.getenv('ISOLATION_SENSITIVITY'))
        else:
            #print("Assing default value")
            cont = cont if cont is not None else 0.001
        
        model = IsolationForest(n_estimators=100, contamination=cont, max_features= 2)
        yp = model.fit_predict(X)
        scores = model.decision_function(X)
        return yp, scores
    
    sent_value = []
    received_value = []
    hour = []
    #Construct the list of values that will be used for the function that executes the algorithm.
    for index in range(0,len(jsonResponse)):
       try:
            sent_value.append(
                float(jsonResponse[index]['wan1']['sent'])
                )
            received_value.append(
                float(jsonResponse[index]['wan1']['received'])
                )
            hour.append(
                (jsonResponse[index]['hour']['start'][0:2])
                )
       except Exception:
            print(Exception)
            break
    #Converting lists into two-dimensional arrays
    x_sent = np.array([sent_value, hour])
    x__received = np.array([received_value, hour])
    
    yp_sent, scores_sent = get_outliers(x_sent.T)
    #print(yp_sent)
    #print(scores_sent)
    yp_received, scores_received = get_outliers(x__received.T)
    #"print(yp_received)
    #print(scores_received)
    
    #Rename column headers
    df.rename(columns={
                'date':'DATE',
                'hour.start':'START HOUR',
                'hour.end':'END HOUR',
                'wan1.sent':'W1_SENT',
                'wan1.received':'W1_RECEIVED',
                'wan2.sent':'W2_SENT',
                "wan2.received":"W2_RECEIVED"
            },
        inplace=True
        )
    #The results of the algorithm are added in their respective column.
    df['SENT OUTLIERS'] = yp_sent
    df['SENT SCORE'] = scores_sent
    df['RECEIVED OUTLIERS'] = yp_received
    df['RECEIVED SCORE'] = scores_received
    
    file = io.BytesIO()

    df = dropna(df) 
    df.to_csv(file,index=False)
    background_tasks.add_task(file.close) 
    headers = {'Content-Disposition': 'attachment; filename="data_set.csv"'} 
    
    return Response(file.getvalue(), headers=headers, media_type='text/csv') 
