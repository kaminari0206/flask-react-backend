import pandas as pd
import requests
from datetime import datetime, timedelta
from pytz import timezone 

YOUR_TICKETMASTER_API_KEY = 'ubvsB7JzYwGyAJ42JVdm1QdDszow132e'


# function to convert time to string format
def format_time(time):
    dt = datetime.combine(datetime.today(),time)
    return dt.strftime('%I:%M %p')

def format_date(date):
    return date.strftime('%m-%d-%Y')



def convert_to_iso(date_str):
    # Convert date string to datetime object
    dt = datetime.strptime(date_str, '%Y-%m-%d')

    # Create time zone object for Eastern time
    eastern_tz = timezone('US/Eastern')

    # Combine datetime object with Eastern time zone
    dt_eastern = eastern_tz.localize(dt)

    # Compute end of day as start of next day minus one second
    end_of_day = (dt_eastern + timedelta(days=1)).replace(hour=0, minute=0, second=0) - timedelta(seconds=1)

    # Format start and end of day as ISO strings with -04:00 time zone
    start_iso_str = dt_eastern.isoformat(timespec='seconds', sep='T') #+ '-04:00'
    end_iso_str = end_of_day.isoformat(timespec='seconds', sep='T') #+ '-04:00'

    return (start_iso_str, end_iso_str)




def get_data_frame_from_ticketmaster(keyword,startDateTime,endDateTime):

    
   
    # if not endDateTime was specified
    if not endDateTime:
        start_first, end_last = convert_to_iso(startDateTime)
    else:
        #get the right format for the ticketmaster API
        start_first, start_last = convert_to_iso(startDateTime)

        end_first, end_last = convert_to_iso(endDateTime)



    print('start_first={}'.format(start_first))
    print('end_last={}'.format(end_last))

    number_events = 6

    data = []

    #ticketmaster_data = requests.get("https://app.ticketmaster.com/discovery/v2/events.json?keyword={}&countryCode={}&apikey={}".format(keyword,'US',YOUR_TICKETMASTER_API_KEY)).json()

    ticketmaster_data = requests.get("https://app.ticketmaster.com/discovery/v2/events.json?keyword={}&countryCode={}&startDateTime={}&endDateTime={}&apikey={}".format('lakers','US',start_first,end_last,YOUR_TICKETMASTER_API_KEY)).json()

    df = pd.DataFrame(ticketmaster_data['_embedded']['events'])

    output_events = df.shape[0]

    for i in range(min(number_events,output_events)):

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
            time = pd.to_datetime(time)
            time = time.time()
            time = format_time(time)
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

    #return d_final


    #d_final['time'] = pd.to_datetime(d_final['time'])
    #d_final['time'] = d_final['time'].dt.time
    #d_final['time'] = d_final['time'].apply(format_time)
    

    d_final['date'] = pd.to_datetime(d_final['date'])
    d_final['date'] = d_final['date'].apply(format_date)

    return d_final
        


