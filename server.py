from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve
from datetime import datetime
import logging
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/weather")
def get_weather():
    city = request.args.get('city')

    #checking for empty string
    if not bool(city.strip()):
        city = "Warszawa"

    weather_data = get_current_weather(city)

    if not weather_data['cod'] == 200:
        return render_template('city_not_found.html')

    return render_template(
        "weather.html",
        title=weather_data["name"],
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}",
        humidity=weather_data['main']['humidity'],
        pressure=weather_data['main']['pressure'],
        wind_speed=weather_data['wind']['speed'],
        wind_deg=weather_data['wind']['deg'],
        visibility=weather_data['visibility'],
        clouds=weather_data['clouds']['all'],
        desc=weather_data["weather"][0]["description"].capitalize(),
        icon=weather_data["weather"][0]["icon"]
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    author_name = "Mateusz Kozieł"
    port = 8000
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Aplikacja uruchomiona {current_time} | Autor: {author_name} | Port: {port}")
    serve(app, host="0.0.0.0", port=port)

