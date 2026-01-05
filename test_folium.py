import streamlit as st
from streamlit_folium import st_folium
import folium

# 🌍 Crée une carte centrée sur Eeyou Istchee
m = folium.Map(location=[51.5, -74.0], zoom_start=6)

# 📍 Marqueurs sacrés
folium.Marker(
    location=[51.5275, -73.6789],
    popup="🌸 Mistissini — lieu sacré",
    icon=folium.Icon(color="purple"),
).add_to(m)

folium.Marker(
    location=[51.4733, -78.7500],
    popup="🪶 Waskaganish — berceau de la rivière",
    icon=folium.Icon(color="green"),
).add_to(m)

folium.Marker(
    location=[53.8050, -78.9167],
    popup="🌊 Chisasibi — là où l’eau parle",
    icon=folium.Icon(color="blue"),
).add_to(m)

# 🖼️ Affiche la carte dans Streamlit
st.title("🗺️ Carte sacrée des communautés")
st_folium(m, width=700, height=500)
