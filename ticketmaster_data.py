import pandas as pd
import requests

YOUR_TICKETMASTER_API_KEY = 'ubvsB7JzYwGyAJ42JVdm1QdDszow132e'

def get_data_frame_from_ticketmaster(keyword):
    

    number_events = 3

    data = []

    ticketmaster_data = requests.get("https://app.ticketmaster.com/discovery/v2/events.json?keyword={}&countryCode={}&apikey={}".format(keyword,'US',YOUR_TICKETMASTER_API_KEY)).json()

    
    df = pd.DataFrame(ticketmaster_data['_embedded']['events'])

    for i in range(number_events):

        current_event = df.iloc[i]
        
        try:
            name = current_event['name']
        except:
            name = 'Not Found'
    
        try:
            url = current_event['url']
        except:
            url = 'Not Found'

        try:
            date = current_event['dates']['start']['localDate']
        except:
            date = 'Not Found'

        try:
            time = current_event['dates']['start']['localTime']
        except:
            time = 'Not Found'
        
        try:
            timeZone = current_event['dates']['timezone']
        except:
            timeZone = 'Not Found'

        try:
            minPrice = current_event['priceRanges'][0]['min']
        except:
            minPrice = 'Not Found'

        try:
            maxPrice = current_event['priceRanges'][0]['max']
        except:
            maxPrice = 'Not Found'

        try:
            venue = current_event['_embedded']['venues'][0]['name']
        except:
            venue = 'Not Found'

        data.append((name,url,date,time,timeZone,minPrice,maxPrice,venue))

    d_final = pd.DataFrame(data)

    d_final.columns = ['name','url','date','time','timeZone','minPrice','maxPrice','venue']

    return d_final
        


