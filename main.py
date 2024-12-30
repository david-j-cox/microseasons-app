import os
import logging
from dotenv import load_dotenv
from weather import fetch_and_process_weather
from openai_utils import generate_microseason_description, generate_microseason_image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
    logging.info("Starting the microseasons application.")
    zip_code = input("Enter your ZIP code: ")
    logging.info(f"Fetching weather data for ZIP code: {zip_code}")
    result_df, place, state = fetch_and_process_weather(zip_code, API_KEY)
    logging.info("Weather data fetched successfully.")

    logging.info("Generating microseason description.")
    microseason_description = generate_microseason_description(result_df, OPENAI_API_KEY)
    logging.info("Microseason description generated successfully.")

    logging.info("Generating microseason image.")
    image_url = generate_microseason_image(microseason_description, OPENAI_API_KEY, place, state)
    logging.info(f"Microseason image generated successfully. Image URL: {image_url}") 