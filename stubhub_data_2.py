import pandas as pd
import requests
import base64
import urllib.parse

clientSecret = 'M3OLBydVGSCl4KMF4F5RSClQ4PlO2LrdleXck7AJfOZHYavmeNWpW7NJS7Rw'
clientId = 'VyJB79jgZbCqwqTRuROg'


# URL encode the client ID and secret
encoded_client_id = urllib.parse.quote(clientId)
encoded_client_secret = urllib.parse.quote(clientSecret)

# Concatenate the encoded client ID, a colon character “:” and the encoded client secret into a single string
concatenated_string = "{}:{}".format(encoded_client_id, encoded_client_secret)

# Base64 encode the concatenated string
encoded_string = base64.b64encode(concatenated_string.encode("utf8")).decode("utf8")

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



def get_data_frame_from_stubhub(keyword):
    # print("-------------------------------------------")

    number_events = 3

    ##data = []
    
    url = "https://account.stubhub.com/oauth2/token"

    auth = requests.auth.HTTPBasicAuth(clientId, clientSecret)

    response = requests.post(url, auth=auth, headers=headers, data=data)

    return
    
    stubhub_data = requests.get("https://app.ticketmaster.com/discovery/v2/events.json?keyword={}&countryCode={}&apikey={}".format(keyword,'US',YOUR_TICKETMASTER_API_KEY)).json()
    ##print("XXXXXXXXXXXXXXXXXX" +str(stubhub_data.status))
    df = pd.DataFrame(ticketmaster_data['_embedded']['events'])
    # print("---------------------------------------")
    # print("df:", df)

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
        
get_data_frame_from_stubhub('nada')

