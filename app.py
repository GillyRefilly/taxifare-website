import streamlit as st
import datetime
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon
import requests
from streamlit_extras.let_it_rain import rain

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

'''
# :money_with_wings: Taxi Fare Predictinator :money_with_wings:

#### Watch that hard earned cash fly out the window
'''



#date-time
d = st.sidebar.date_input(
    "Select the date of the ride.",
    datetime.date(2019, 7, 6))
t = st.sidebar.time_input('Select the time of the ride', datetime.time(8, 45))

date = datetime.datetime.combine(d, t)

#pickup and dropoff locations

st.sidebar.write("Pickup address")
street_p = st.sidebar.text_input("Street", "75 Bay Street")
city_p = st.sidebar.text_input("City", "Toronto")
province_p = st.sidebar.text_input("Province/State", "Ontario")
country_p = st.sidebar.text_input("Country", "Canada")

geolocator = Nominatim(user_agent="GTA Lookup",timeout=100)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
location_p = geolocator.geocode(street_p+", "+city_p+", "+province_p+", "+country_p)

lat_p = location_p.latitude
lon_p = location_p.longitude

# lat_p = st.sidebar.number_input('Insert your pickup latitutde')
# lon_p = st.sidebar.number_input('Insert your pickup longitude')


st.sidebar.write("Dropoff address")
street_d = st.sidebar.text_input("Street","Rudi-Dutschke-Straße 26")
city_d = st.sidebar.text_input("City","Berlin")
province_d = st.sidebar.text_input("Province/State","Berlin")
country_d = st.sidebar.text_input("Country","Germany")

geolocator = Nominatim(user_agent="GTA Lookup",timeout=100)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
location_d = geolocator.geocode(street_d+", "+city_d+", "+province_d+", "+country_d)

lat_d = location_d.latitude
lon_d = location_d.longitude
# lat_d = st.sidebar.number_input('Insert your dropoff latitutde')
# lon_d = st.sidebar.number_input('Insert your dropoff longitutdakjhsfkwh')

map_data = pd.DataFrame({'lat': [lat_p,lat_d], 'lon': [lon_p,lon_d]})
st.map(map_data)

#passenger count

number = st.slider('Number of passengers', min_value=1, max_value=12, value=5, step=1)

st.write('You need transportation for ', number, 'people')

#Confirm selected params

'''## Interesting choices you've just made there...'''

st.write('Your selected date and time are:', date)
st.write('Your pickup address translates to:', lat_p,lon_p)
st.write('Your pickup address translates to:', lat_d,lon_d)
st.write('Your passenger number is:', number)


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
    exclamation = 'Mr. Moneybags'
    rain(
        emoji="💸",
        font_size=54,
        falling_speed=5,
        animation_length="infinite",
    )
elif fare > 20:
    exclamation = 'Naja...Sometimes you just really need a lazy bolt'
else:
    exclamation = 'Sick Deal!'
f'''
# {exclamation}
Based on our model calulation your fare will be
# {round(float(fare),2):.2f} buckaroos
'''

if st.button('More 🎈🎈🎈 please!'):
    st.balloons()
