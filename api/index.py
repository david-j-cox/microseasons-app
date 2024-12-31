import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session
from weather import fetch_and_process_weather
from openai_utils import generate_microseason_description, generate_microseason_image
import os
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

API_KEY = os.getenv('API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        zip_code = request.form['zip_code']
        # Process data directly here
        result_df, place, state = fetch_and_process_weather(zip_code, API_KEY)
        microseason_description = generate_microseason_description(result_df, OPENAI_API_KEY)
        image_url = generate_microseason_image(microseason_description, OPENAI_API_KEY, place, state)
        result_df = pd.DataFrame(result_df)
        print("\n\n", result_df, "\n\n")
        print("\n\n", result_df.columns, "\n\n")
        avg_temp = round((result_df['morning_temp'].sum() + result_df['afternoon_temp'].sum() + result_df['evening_temp'].sum() + result_df['night_temp'].sum()) / (4 * len(result_df)), 2)
        if str(result_df['precipitation'].mean())=='nan':
            avg_precipitation = 0
        else:
            avg_precipitation = result_df['precipitation'].mean()
        avg_wind_speed = round(result_df['wind_speed'].mean(), 2)
        avg_wind_direction = result_df['wind_direction'].mode()[0]

        # Store values in session
        session['avg_temp'] = avg_temp
        session['avg_precipitation'] = avg_precipitation
        session['avg_wind_speed'] = avg_wind_speed
        session['avg_wind_direction'] = avg_wind_direction

        # Redirect to result page with data
        return redirect(url_for('result', description=microseason_description, image_url=image_url))
    return render_template('index.html')

@app.route('/result')
def result():
    description = request.args.get('description')
    image_url = request.args.get('image_url')
    
    # Retrieve values from session
    avg_temp = session.get('avg_temp')
    avg_precipitation = session.get('avg_precipitation')
    avg_wind_speed = session.get('avg_wind_speed')
    avg_wind_direction = session.get('avg_wind_direction')

    return render_template(
        'result.html', 
        description=description, 
        image_url=image_url, 
        avg_temp=avg_temp,
        avg_precipitation=avg_precipitation,
        avg_wind_speed=avg_wind_speed,
        avg_wind_direction=avg_wind_direction
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 