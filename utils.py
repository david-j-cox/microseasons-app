from datetime import datetime, timedelta
import requests

def create_date_list():
    today = datetime.today()
    current_year = today.year
    dates_list = []

    for year in range(current_year - 3, current_year + 1):
        for offset in range(-2, 3):
            date = today.replace(year=year) + timedelta(days=offset)
            dates_list.append(date.strftime('%Y-%m-%d'))

    return dates_list

def deg_to_compass(deg):
    """
    Convert wind direction in degrees to compass direction.

    Args:
        deg (float): The wind direction in degrees (0-360).

    Returns:
        str: The compass direction corresponding to the input degrees.

    Example:
        If the input is 45, the output will be "NE".

    Compass Directions:
        - N: 0°
        - NNE: 22.5°
        - NE: 45°
        - ENE: 67.5°
        - E: 90°
        - ESE: 112.5°
        - SE: 135°
        - SSE: 157.5°
        - S: 180°
        - SSW: 202.5°
        - SW: 225°
        - WSW: 247.5°
        - W: 270°
        - WNW: 292.5°
        - NW: 315°
        - NNW: 337.5°
    """
    val = int((deg / 22.5) + 0.5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
           "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]

def fetch_weather_data(day, latitude, longitude, api_key):
    url = (
        f"https://api.openweathermap.org/data/3.0/onecall/day_summary"
        f"?lat={latitude}&lon={longitude}&date={day}&appid={api_key}&units=imperial"
    )
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    else:
        print(f"Error fetching data for {day}: {res.status_code}")
        return None

def process_weather_data(data):
    """
    Process raw weather data into a structured format for analysis.

    Args:
        data (dict): The raw JSON data from the weather API.

    Returns:
        dict: A dictionary containing processed weather data with relevant metrics.

    Example:
        process_weather_data(api_response)
    """
    def safe_mean(values):
        """Calculate mean while safely ignoring invalid entries."""
        valid_values = [v for v in values if isinstance(v, (int, float))]
        return sum(valid_values) / len(valid_values) if valid_values else None

    return {
        "date": data.get("date"),
        "cloud_cover": safe_mean(data.get("cloud_cover", [])),
        "humidity": safe_mean(data.get("humidity", [])),
        "precipitation": safe_mean(data.get("precipitation", [])),
        "morning_temp": data.get("temperature", {}).get("morning"),
        "afternoon_temp": data.get("temperature", {}).get("afternoon"),
        "evening_temp": data.get("temperature", {}).get("evening"),
        "night_temp": data.get("temperature", {}).get("night"),
        "min_temp": data.get("temperature", {}).get("min"),
        "max_temp": data.get("temperature", {}).get("max"),
        "diff_temp": round(data.get("temperature", {}).get("max", 0) - data.get("temperature", {}).get("min", 0), 2),
        "pressure": safe_mean(data.get("pressure", [])),
        "wind_speed": data.get("wind", {}).get("max", {}).get("speed"),
        "wind_direction": deg_to_compass(data.get("wind", {}).get("max", {}).get("direction")),
    }