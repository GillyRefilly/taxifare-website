import streamlit as st
import datetime
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon
import requests

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Where would you like to go?

'''

#date-time
d = st.date_input(
    "Select the date of the ride.",
    datetime.date(2019, 7, 6))
t = st.time_input('Select the time of the ride', datetime.time(8, 45))

date = datetime.datetime.combine(d, t)
st.write('Your selected date and time are:', date, 'cool')

#pickup and dropoff locations

st.sidebar.write("Pickup address")
# street_p = st.sidebar.text_input("Street", "75 Bay Street")
# city_p = st.sidebar.text_input("City", "Toronto")
# province_p = st.sidebar.text_input("Province", "Ontario")
# country_p = st.sidebar.text_input("Country", "Canada")

# geolocator = Nominatim(user_agent="GTA Lookup")
# geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
# location = geolocator.geocode(street_p+", "+city_p+", "+province_p+", "+country_p)


lat_p = st.sidebar.number_input('Insert your pickup latitutde')
lon_p = st.sidebar.number_input('Insert your pickup longitude')

st.write('Your pickup location is ', lat_p, lon_p)

st.sidebar.write("Pickup address")
# street_d = st.sidebar.text_input("Street", "446 Keith Rd E")
# city_d = st.sidebar.text_input("City", "North Vancouver")
# province_d = st.sidebar.text_input("Province", "British Columbia")
# country_d = st.sidebar.text_input("Country")

# geolocator = Nominatim(user_agent="GTA Lookup")
# geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
# location = geolocator.geocode(street_d+", "+city_d+", "+province_d+", "+country_d)

# lat_d = location.latitude
# lon_d = location.longitude
lat_d = st.sidebar.number_input('Insert your dropoff latitutde')
lon_d = st.sidebar.number_input('Insert your dropoff longitutdakjhsfkwh')


st.write('Your dropoff location is ', lat_d, lon_d)

map_data = pd.DataFrame({'lat': [lat_p,lat_d], 'lon': [lon_p,lon_d]})
st.map(map_data)

#passenger count

number = st.slider('Number of passengers', min_value=1, max_value=12, value=5, step=1)

st.write('You need transportation for ', number, 'people')
'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''


url = 'https://taxifare.lewagon.ai/predict'

params = {
    'pickup_datetime': date, # 0 for Sunday, 1 for Monday, ...
    'pickup_latitude': lat_p,
    'pickup_longitude': lon_p,
    'dropoff_latitude': lat_d,
    'dropoff_longitude': lon_d,
    'passenger_count': number
}

response = requests.get(url, params=params).json()
fare = response['fare']

if fare > 100:
    exclamation = 'Oooff.. expensive'
elif fare > 20:
    exclamation = 'Gotta pay to get somewhere...'
else:
    exclamation = 'Good Deal!'
f'''
# {exclamation}
Based on our model calulation your fare will be
# {fare}
'''

if st.button('More 🎈🎈🎈 please!'):
    st.balloons()

# st.write('Predicted fare ', response.json(), 'buckaroos')
