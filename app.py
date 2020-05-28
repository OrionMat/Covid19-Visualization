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
    confirmed = df[df.Confirmed != 0]
    return df, confirmed

df, confirmed = load_data(NROWS)

st.title("Covid-19 cases in the USA")

# all 2020 confirmed case map
st.header("All confirmed 2020 cases")
st.map(confirmed[["latitude", "longitude"]].dropna(how="any"))
if st.checkbox("Show Data - 162268 confirmed cases", False):
    st.subheader('Data')
    st.write(confirmed)

# confirmed cases for given month
st.header("Cases in a given month")
month = st.slider("con Month", 1, 5)
st.markdown("Covid-19 cases in 0%i/2020" % month)
data = confirmed[confirmed['Date'].dt.month == month]

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
if st.checkbox("Show Data - months cases", False):
    st.subheader('Data')
    st.write("Number of cases: %i" % data.shape[0])
    st.write(data)



# recovered vs fatality vs all
st.header("Recoveries and Fatalities")
recover = confirmed[confirmed.Deaths == 0]
die = confirmed[confirmed.Deaths == 1]

selection = st.selectbox("Show", ["Recoveries", "Fatalities", "All"])
if selection == "Recoveries":
    rec_midpoint = (np.average(recover["latitude"]), np.average(recover["longitude"]))
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": rec_midpoint[0],
            "longitude": rec_midpoint[1],
            "zoom": 2,
            "pitch": 0,
        },
        layers=[
            pdk.Layer(
            "ScatterplotLayer",
            data=recover[['Date', 'latitude', 'longitude']],
            get_position=["longitude", "latitude"],
            auto_highlight=False,
            get_radius=50000,
            get_fill_color=[9, 239, 9, 200],  # Set an RGBA value for fill
            pickable=True,
            ),
        ],
    ))
elif selection == "Fatalities":
    die_midpoint = (np.average(die["latitude"]), np.average(die["longitude"]))
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": die_midpoint[0],
            "longitude": die_midpoint[1],
            "zoom": 2,
            "pitch": 0,
        },
        layers=[
            pdk.Layer(
            "ScatterplotLayer",
            data=die[['Date', 'latitude', 'longitude']],
            get_position=["longitude", "latitude"],
            auto_highlight=False,
            get_radius=50000,
            get_fill_color=[239, 9, 9, 200],  # Set an RGBA value for fill
            pickable=True,
            ),
        ],
    ))
else:
    pass


if st.checkbox("Show Data - %s" % selection, False):
    st.subheader('Data')
    if selection == "Recoveries":
        st.write("Number of recoveries: %i" % recover.shape[0])
        st.write(recover)
    elif selection == "Fatalities":
        st.write("Number of deaths: %i" % die.shape[0])
        st.write(die)
    else:
        st.write("Number of deaths: %i" % confirmed.shape[0])
        st.write(confirmed)


data = df[df['Date'].dt.month == month]