from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Define the OpenWeatherMap API key
api_key = 'YOUR_API_KEY'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    postcode = request.args.get('postcode')
    country_code = request.args.get('country')

    if not postcode:
        return render_template('index.html', error='Postcode parameter is required')
    if not country_code:
        return render_template('index.html', error='Country code parameter is required')

    validation_url = f'https://api.openweathermap.org/data/2.5/weather?zip={postcode},{country_code}&appid={api_key}'

    try:
        # Validate postcode and country combination
        validation_response = requests.get(validation_url)
        validation_response.raise_for_status()
        validation_data = validation_response.json()

        if validation_data.get('cod') == '404':
            return render_template('index.html', error='Invalid postcode or country code')

        # If validation is successful, proceed to fetch detailed weather data
        url = f'https://api.openweathermap.org/data/2.5/weather?zip={postcode},{country_code}&appid={api_key}&units=metric'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract relevant weather data from the API response
        city = data['name']
        country = data['sys']['country']
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        temperature_feels = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        wind_direction = data['wind']['deg']
        temperature_max = data['main']['temp_max']
        temperature_min = data['main']['temp_min']
        wind_gust = data.get('wind', {}).get('gust', 'N/A')

        return render_template('weather.html', city=city, country=country, description=weather_description,
                               temperature=temperature, humidity=humidity, pressure=pressure,
                               wind_speed=wind_speed, wind_direction=wind_direction, temperature_feels=temperature_feels,
                               temperature_min=temperature_min, temperature_max=temperature_max, wind_gust=wind_gust)

    except requests.RequestException as e:
        return render_template('index.html', error=f'Request to OpenWeatherMap API failed: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
