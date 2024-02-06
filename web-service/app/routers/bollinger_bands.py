from fastapi import APIRouter, Response, BackgroundTasks
from datetime import datetime
from datetime import timedelta
from pandas import json_normalize
from ta.volatility import BollingerBands
from ta.utils import dropna
import io
from app.templates.fetch_dataset import get_bb_data_set

bollinger_bands_router = APIRouter()

@bollinger_bands_router.get("/")
async def calculate_bollinger_bands(background_tasks: BackgroundTasks):
    
    t1 = str(datetime.now())
    t0 = str(datetime.now() - timedelta(days=21))
    
    jsonResponse = get_bb_data_set(t0[0:10]+"T23:59:59Z",t1[0:10]+"T00:00:00Z")
    
    df = json_normalize(jsonResponse)
    df.rename(columns={
                'startTime':'START',
                'endTime':'END',
                'wan1.sent':'W1_SENT',
                'wan1.received':'W1_RECEIVED',
                'wan2.sent':'W2_SENT',
                "wan2.received":"W2_RECEIVED"
            },
        inplace=True
        )
    
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