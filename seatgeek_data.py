import pandas as pd
import requests

YOUR_SEATGEEK_API_KEY = 'MzE3NTk2NDd8MTY3NTQ1NTk3My4xMDQzNjU2'

def get_data_frame_from_seatgeek(keyword):
    
    number_events = 3

    data = []

    #ticketmaster_data = requests.get("https://app.ticketmaster.com/discovery/v2/events.json?keyword={}&countryCode={}&apikey={}".format(keyword,'US',YOUR_TICKETMASTER_API_KEY)).json()

    seatgeek_data = requests.get("https://api.seatgeek.com/2/events?q={}&client_id={}".format(keyword,YOUR_SEATGEEK_API_KEY)).json()

    df = pd.DataFrame(seatgeek_data['events'])

    for i in range(number_events):

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

    return d_final
        


