import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

NROWS = None

@st.cache
def load_data(NROWS):
    df = pd.read_csv("covid19_data//USA.csv", nrows=NROWS, parse_dates=['Date'])
    df.drop(columns=['Combined_Key', 'Country_Region', 'Admin2', 'FIPS', 'code3', 'iso3', 'UID'], inplace=True)
    # df = df[df.Province_State == 'New York']
    df = df[df.Long_ <= -40]


    # rename for streamlit map to work
    df.rename(columns={'Lat' : 'latitude', 'Long_' : 'longitude'}, inplace=True)
    return df

df = load_data(NROWS)

st.title("Covid-19 cases in the USA")

# all 2020 case map
st.header("All 2020 cases")
st.map(df[["latitude", "longitude"]].dropna(how="any"))
if st.checkbox("Show All Data", False):
    st.subheader('Data')
    st.write(df)



# cases for given month
st.header("Cases in a given month (Jan-01 to May-05 2020)")
month = st.slider("Month", 1, 5)
st.markdown("Covid-19 cases in 0%i/2020" % month)
data = df[df['Date'].dt.month == month]

midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 2,
        "pitch": 30,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data=data[['Date', 'latitude', 'longitude']],
        get_position=["longitude", "latitude"],
        auto_highlight=True,
        radius=50000,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0, 100000],
        ),
    ],
))
if st.checkbox("Show Moth Data", False):
    st.subheader('Data')
    st.write(data.shape)
    st.write(data)