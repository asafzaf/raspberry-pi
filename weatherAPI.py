import requests
import psycopg2

import dbconf

conn = psycopg2.connect(database=dbconf.name,
                        host=dbconf.host,
                        user=dbconf.user,
                        password=dbconf.dbpass,
                        port=dbconf.port)

cursor = conn.cursor()

res = cursor.execute(f'SELECT cities_weather.id, cities_weather.name_english FROM cities_weather;')

cities = cursor.fetchall()

for city in cities:
    
    (id, eng_name) = city
    
    headers = {'Accept': 'application/json'}
    url = f'http://api.weatherapi.com/v1/forecast.json?q={eng_name}'
    params = {'key': '88b85b34240745beba8184849241001'}

    r = requests.get(url, params=params, headers=headers)

    data = r.json()

    city_data = data['location']['name']
    forecast_data = data['forecast']['forecastday'][0]
    date = forecast_data['date']
    max_temp = forecast_data['day']['maxtemp_c']
    min_temp = forecast_data['day']['mintemp_c']
    avg_temp = forecast_data['day']['avgtemp_c']
    max_wind_kph = forecast_data['day']['maxwind_kph']
    will_it_rain = bool(forecast_data['day']['daily_will_it_rain'])
    daily_chance_of_rain = forecast_data['day']['daily_chance_of_rain']
    sunrise = forecast_data['astro']['sunrise']
    sunset = forecast_data['astro']['sunset']
    moonrise = forecast_data['astro']['moonrise']
    moonset = forecast_data['astro']['moonset']

    res = cursor.execute(f"INSERT INTO weather (
    city_id,
    date,
    max_temp,
    min_temp,
    avg_temp,
    max_wind_kph,
    will_it_rain,
    daily_rain_chance,
    sun_rise,
    sun_set,
    moon_rise,
    moon_set
    ) VALUES (
    {id},
    {date},
    {max_temp},
    {min_temp},
    {avg_temp},
    {max_wind_kph},
    {will_it_rain},
    {daily_chance_of_rain},
    '{sunrise}',
    '{sunset}',
    '{moonrise}',
    '{moonset}');
    ;")
    conn.commit()
    print(f"INSERTED: {eng_name}, {date}")
# print(f"Response:\ncity: {city_data}\n{date}\ntemp: {min_temp}°c - {max_temp}°c ({avg_temp}°c)\nwind: {max_wind_kph}/kph\nRain? {will_it_rain} ({daily_chance_of_rain}%)\nSun:\nRise: {sunrise}\nSet: {sunset}\nMoon:\nRise: {moonrise}\nSet: {moonset}")
