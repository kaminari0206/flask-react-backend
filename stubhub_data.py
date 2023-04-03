import pandas as pd
import requests
import base64
import urllib.parse
from datetime import datetime
from datetime import time

clientSecret = 'M3OLBydVGSCl4KMF4F5RSClQ4PlO2LrdleXck7AJfOZHYavmeNWpW7NJS7Rw'
clientId = 'VyJB79jgZbCqwqTRuROg'


# URL encode the client ID and secret
encoded_client_id = urllib.parse.quote(clientId)
encoded_client_secret = urllib.parse.quote(clientSecret)

# Concatenate the encoded client ID, a colon character “:” and the encoded client secret into a single string
concatenated_string = "{}:{}".format(encoded_client_id, encoded_client_secret)

# Base64 encode the concatenated string
encoded_string = base64.b64encode(concatenated_string.encode()).decode()

# Create the Basic Authorization header
authorization_header = "Basic {}".format(encoded_string)


headers = {
    "Authorization": authorization_header, 
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "grant_type": "client_credentials",
    "scope": "read:events"
}

def format_date(date_string):
    dt_obj = datetime.fromisoformat(date_string[:19])
    return dt_obj.strftime('%m-%d-%Y')

def format_time(time_string):
    dt_obj = datetime.strptime(time_string, '%H:%M:%S')
    return dt_obj.strftime('%I:%M %p')

def get_data_frame_from_stubhub(keyword):

    number_events = 6

    data = {
    "grant_type": "client_credentials",
    "scope": "read:events"
    }

 
    url = "https://account.stubhub.com/oauth2/token"

    auth = requests.auth.HTTPBasicAuth(clientId, clientSecret)

    response = requests.post(url, auth=auth, headers=headers, data=data)

    access_token = response.json()['access_token']

    search_headers = {"Authorization": "Bearer {}".format(access_token)}

    params = {"country_code": "US",
              "q":keyword,
              "type":'Main'
            } 

    search_response = requests.get("https://api.stubhub.net/catalog/events/search", headers=search_headers, params=params)

    df = search_response.json()

    dtest=pd.DataFrame(df['_embedded']['items'])

    dmain=dtest[dtest['type']=='Main']

    dmain=dmain.sort_values('start_date',ascending=True)

    data = []

    output_events = dmain.shape[0]

    for i in range(min(number_events,output_events)):

        current_event = dmain.iloc[i]

        try:
            name = current_event['name']
        except:
            name = 'Not Found'

        try:
            url = current_event['_links']['event:webpage']['href']
        except:
            url = 'Not Found'

        try:
            date = current_event['start_date']
        except:
            date = 'Not Found'

        try:
            time = datetime.fromisoformat(current_event['start_date']).time()
            time = time.strftime("%H:%M:%S")
        except:
            time = 'Not Found'

        try:
            timeZone =datetime.fromisoformat(current_event['start_date']).tzinfo
            tz_offset = timeZone.utcoffset(None)
            tz_offset_str = '{:+03d}:{:02d}'.format(int(tz_offset.total_seconds() // 3600), abs(tz_offset.total_seconds() // 60 % 60))
            timeZone = 'UTC{}'.format(tz_offset_str)

        except:
            timezone = 'Not Found'

        try:
            minPrice = current_event['min_ticket_price']['amount']

        except:
            minPrice = 'Not Found'

        maxPrice = 'Not Available'

        try:
            venue = current_event['_embedded']['venue']['name']
        except:
            venue = 'Not Found'

        data.append((name,url,date,time,timeZone,minPrice,maxPrice,venue))

    d_final = pd.DataFrame(data)

    d_final.columns = ['name','url','date','time','timeZone','minPrice','maxPrice','venue']

    d_final['date'] = d_final['date'].apply(format_date)
    d_final['time'] = d_final['time'].apply(format_time)

    return d_final
