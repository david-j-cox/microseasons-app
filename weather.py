import logging
import pgeocode
from concurrent.futures import ThreadPoolExecutor
from utils import create_date_list, fetch_weather_data, process_weather_data

def fetch_and_process_weather(zip_code, api_key):
    logging.info("Starting weather data fetching and processing.")
    nomi = pgeocode.Nominatim("us")
    location = nomi.query_postal_code(zip_code)
    latitude = location.latitude
    longitude = location.longitude
    place_name = location.place_name
    state_name = location.state_code

    days = create_date_list()
    weather_data = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_weather_data, day, latitude, longitude, api_key) for day in days]
        results = [f.result() for f in futures]

    for data in results:
        if data:
            weather_data.append(process_weather_data(data))

    logging.info("Weather data processing completed.")
    return weather_data, place_name, state_name