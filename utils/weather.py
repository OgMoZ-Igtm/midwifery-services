import requests

# Traductions des conditions en cri
CREE_CONDITIONS = {
    0: "Wāwīpān",
    1: "Mīna wāwīpān",
    2: "Mīna wāwīpān",
    3: "Yūtin",
    45: "Wāpiskāw mīna yūtin",
    48: "Wāpiskāw mīna yūtin",
    51: "Nipīhūn",
    61: "Nipīhūn",
    71: "Wāpiskāw",
    80: "Nipīhūn mīna yūtin",
    95: "Nipīhūn mīna yūtin",
}

# Icônes visuelles
WEATHER_ICONS = {
    0: "☀️",
    1: "🌤️",
    2: "⛅",
    3: "☁️",
    45: "🌫️",
    48: "🌫️",
    51: "🌦️",
    61: "🌧️",
    71: "❄️",
    80: "🌧️",
    95: "⛈️",
}


def get_current_weather(lat, lon):
    """
    Récupère la météo actuelle (température, code météo, vent).
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,weathercode,wind_speed_10m&timezone=auto"
    )
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json().get("current", {})
        return {
            "temp": data.get("temperature_2m"),
            "weather_code": data.get("weathercode"),
            "wind": data.get("wind_speed_10m"),
        }
    return None


def get_forecast(lat, lon, days=3):
    """
    Récupère les prévisions météo pour les `days` prochains jours.
    Donne températures max/min et codes météo quotidiens.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,weathercode"
        f"&forecast_days={days}&timezone=auto"
    )
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json().get("daily", {})
        forecasts = []
        for i in range(len(data["time"])):
            forecasts.append(
                {
                    "date": data["time"][i],
                    "temp_max": data["temperature_2m_max"][i],
                    "temp_min": data["temperature_2m_min"][i],
                    "weather_code": data["weathercode"][i],
                }
            )
        return forecasts
    return []
