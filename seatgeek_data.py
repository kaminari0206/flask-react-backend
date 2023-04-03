import pandas as pd
import requests
from stubhub_data import format_date
from datetime import  datetime

YOUR_SEATGEEK_API_KEY = 'MzE3NTk2NDd8MTY3NTQ1NTk3My4xMDQzNjU2'


def format_time(datetime_string):
    dt_obj = datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S')
    return dt_obj.strftime('%I:%M %p')


def get_data_frame_from_seatgeek(keyword):
    
    number_events = 6

    data = []

    seatgeek_data = requests.get("https://api.seatgeek.com/2/events?q={}&client_id={}".format(keyword,YOUR_SEATGEEK_API_KEY)).json()

    df = pd.DataFrame(seatgeek_data['events'])

    output_events = df.shape[0]


    for i in range(min(number_events,output_events)):

        current_event = df.iloc[i]
        
        try:
            name = current_event['title']
        except:
            name = 'Not Found'
    
        try:
            url = current_event['url']
        except:
            url = 'Not Found'

        try:
            date = current_event['datetime_local']
        except:
            date = 'Not Found'

        try:
            time = current_event['datetime_local']
        except:
            time = 'Not Found'
        
        try:
            timeZone = current_event['venue']['timezone']
        except:
            timeZone = 'Not Found'

        try:
            minPrice = current_event['stats']['lowest_price']
        except:
            minPrice = 'Not Found'

        try:
            maxPrice = current_event['stats']['highest_price']
        except:
            maxPrice = 'Not Found'

        try:
            venue = current_event['venue']['name']
        except:
            venue = 'Not Found'

        data.append((name,url,date,time,timeZone,minPrice,maxPrice,venue))

    d_final = pd.DataFrame(data)
    d_final.columns = ['name','url','date','time','timeZone','minPrice','maxPrice','venue']

    d_final['date'] = d_final['date'].apply(format_date)
    d_final['time'] = d_final['time'].apply(format_time)

    d_final.fillna(value='Not Found', inplace=True)


    return d_final
        



