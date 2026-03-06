import streamlit as st
import datetime
import requests
import pandas as pd
import streamlit.components.v1 as components
from geopy.geocoders import Nominatim


# Definimos el bloque de HTML
html_title = """
<div style="background-color: #95DBD9; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
    <h1 style="color: #0369a1; margin-bottom: 5px; font-style: italic;">TaxiFare Predictor</h1>
    <h3 style="color: #0284c7; margin-top: 0; font-style: italic; font-weight: normal;">Calculate the cost of your ride!</h3>
</div>
"""

# Inyectamos el HTML
st.sidebar.markdown(html_title, unsafe_allow_html=True)


st.sidebar.markdown("Ride Details")

d = st.sidebar.date_input("Pickup Date", datetime.date(2014, 7, 6))
t = st.sidebar.time_input("Pickup Time", datetime.time(19, 18, 00))
passenger_count= st.sidebar.selectbox("Select the number of passengers:", range(1,9))
#passenger_count = st.number_input("Number of passengers", min_value=1, max_value=8, value=2)
address_pickup = st.sidebar.text_input("Address point of pickup")
address_dropoff = st.sidebar.text_input("Address point of dropoff")

#pickup_longitude = st.number_input("Pickup Longitude", value=-73.950655, format="%.6f")
#pickup_latitude = st.number_input("Pickup Latitude", value=40.783282, format="%.6f")
#dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.984365, format="%.6f")
#dropoff_latitude = st.number_input("Dropoff Latitude", value=40.769802, format="%.6f")

if st.button("Predict Fare"):

    pickup_datetime = f"{d} {t}"

    # 1. Cambiamos el user_agent por uno más único y personal
    geolocator = Nominatim(user_agent="taxifare_daniel_lewagon_app")

    try:
        # 2. Añadimos un timeout de 10 segundos por si la red va lenta
        location_pickup = geolocator.geocode(address_pickup, timeout=10)
        location_dropoff = geolocator.geocode(address_dropoff, timeout=10)

        # Comprobamos que Nominatim realmente encontró las direcciones
        if location_pickup is None or location_dropoff is None:
            st.warning("⚠️ No pudimos encontrar una de las direcciones. Por favor, sé más específico (ej. 'Eiffel Tower, Paris').")
        else:
            pickup_longitude = location_pickup.longitude
            pickup_latitude = location_pickup.latitude
            dropoff_longitude = location_dropoff.longitude
            dropoff_latitude = location_dropoff.latitude
            url = 'https://taxifare.lewagon.ai/predict'

            params = {
                "pickup_datetime": pickup_datetime,
                "pickup_longitude": pickup_longitude,
                "pickup_latitude": pickup_latitude,
                "dropoff_longitude": dropoff_longitude,
                "dropoff_latitude": dropoff_latitude,
                "passenger_count": passenger_count
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                prediction = response.json()
                fare = round(prediction['fare'], 2)
                st.success(f"### The estimated fare is: ${fare}")

                st.write("## *Here is your ride!!*")
                google_maps_url = f"https://maps.google.com/maps?saddr={pickup_latitude},{pickup_longitude}&daddr={dropoff_latitude},{dropoff_longitude}&dirflg=d&output=embed"

                components.html(
                    f'<iframe width="100%" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="{google_maps_url}"></iframe>',
                    height=400,
                )
            else:
                st.error("Oops! Something went wrong with the API call.")

    except Exception as e:
        # 3. Si Nominatim nos bloquea, mostramos este mensaje en lugar de romper la app
        st.error("El servicio de mapas está temporalmente saturado o no disponible. Por favor, intenta de nuevo en unos segundos.")


#    mapa = pd.DataFrame({
#        "lat" : [pickup_latitude, dropoff_latitude],
#        "lon" : [pickup_longitude, dropoff_longitude]
 #   })


 #   st.map(mapa)
