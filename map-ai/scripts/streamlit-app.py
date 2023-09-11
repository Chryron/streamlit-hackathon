import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import openrouteservice
from openrouteservice import convert
load_dotenv()
OPENROUTESERVICE_API_KEY = os.getenv("OPENROUTESERVICE_API_KEY")
coords = ((8.34234,48.23424),(8.34423,48.26424))

client = openrouteservice.Client(key=OPENROUTESERVICE_API_KEY) # Specify your personal API key
routes = client.directions(coords)
geometry = routes['routes'][0]['geometry']
decoded = convert.decode_polyline(geometry)


route_df = pd.DataFrame(
    decoded['coordinates'],
    columns=['lat', 'lon'])

st.map(route_df)