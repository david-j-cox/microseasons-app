import logging
from openai import OpenAI

def generate_microseason_description(weather_data, openai_api_key):
    """
    Generate a short description of the microseason encapsulated by the weather data.

    Args:
        weather_data (list): A list of dictionaries containing processed weather data.
        openai_api_key (str): Your OpenAI API key.

    Returns:
        str: A short description of the microseason.
    """
    logging.info("Generating description using OpenAI.")
    # Format weather data into a prompt
    prompt = (
        "Based on the following weather data, create a short and poetic description "
        "of the microseason (a brief period of weather and environmental characteristics) in the same "
        "poetic format that exists for Japan's 72 microseason descriptions:\n\n"
    )
    for entry in weather_data:
        prompt += (
            f"Date: {entry['date']}, Morning Temp: {entry['morning_temp']}°F, "
            f"Afternoon Temp: {entry['afternoon_temp']}°F, Evening Temp: {entry['evening_temp']}°F, "
            f"Night Temp: {entry['night_temp']}°F, Min Temp: {entry['min_temp']}°F, "
            f"Max Temp: {entry['max_temp']}°F, Temperature Difference: {entry['diff_temp']}, "
            f"Cloud Cover: {entry['cloud_cover']}, Precipitation: {entry['precipitation']}, "
            f"Humidity: {entry['humidity']}, Pressure: {entry['pressure']}, "
            f"Wind: {entry['wind_speed']} mph {entry['wind_direction']}.\n"
        )

    prompt += "\nCreate a description of this microseason in 1-2 poetic sentences."

    # Create an OpenAI client
    client = OpenAI(api_key=openai_api_key)

    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o",
        )

        # Access the generated content from the API response
        description = response.choices[0].message.content.strip().replace(';', ';\n')
        logging.info("Description generated successfully.")
        return description

    except AttributeError as e:
        print(f"AttributeError: {e}")
        return "Error parsing OpenAI API response."

    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Error generating microseason description."

def generate_microseason_image(description, openai_api_key, place, state):
    """
    Generate an image using DALL-E API based on the given description.

    Args:
        description (str): The poetic description of the microseason.
        openai_api_key (str): Your OpenAI API key.

    Returns:
        str: URL of the generated image.
    """
    logging.info("Generating image using OpenAI.")
    client = OpenAI(api_key=openai_api_key)

    try:
        # Enhance the description for Nihonga style
        prompt = f"An artistic image using only the local plants and animals of {place}, {state}. \
                   The artisitic style should be Nihonga and depict: {description}. \
                   There should not be any words in the image. Only painting. Do not include \
                   any words in the painting. No words should be visible anywhere in the painting."

        # Call the OpenAI DALL-E API
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        # Extract the image URL
        image_url = response.data[0].url
        print(image_url)
        logging.info("Image generated successfully.")
        return image_url
    
    except Exception as e:
        print(f"Error with DALL-E API: {e}")
        return "Error generating image."
