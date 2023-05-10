import requests
import json
import urllib.parse

address = input("Enter the postcode for the location: ")
url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'

response = requests.get(url).json()

lat = response[0]["lat"]
lon = response[0]["lon"]


# Set the OpenWeatherMap API endpoint and API key
url = "https://api.open-meteo.com/v1/forecast?daily=sunrise,sunset,precipitation_probability_max&current_weather=true&forecast_days=1&timezone=auto"
params = {
    "latitude": lat,
    "longitude": lon
}

# Send the GET request to the API endpoint
response = requests.get(url, params=params)

# Parse the response JSON data
data = json.loads(response.text)

temp = json.dumps(data["current_weather"]["temperature"])
rain_chance = json.dumps(data["daily"]["precipitation_probability_max"])
wind_speed = data["current_weather"]["windspeed"]
sunrise = json.dumps(data["daily"]["sunrise"])
sunset = json.dumps(data["daily"]["sunset"])
timezone = json.dumps(data["timezone_abbreviation"])

rain_chance = rain_chance.strip('[]')
sunrise = sunrise.strip('["]')
sunset = sunset.strip('["]')
timezone = timezone.strip('"')

sunrise = sunrise.split('T')
sunset = sunset.split('T')

address = address.upper()
address = address.replace(" ", "")

if len(address) == 6:
    address = address[:3] + " " + address[-3:]
else:
    address = address[:4] + " " + address[-3:]


# Print the response data
print("Weather for Postcode:", address)
print("Temperature:", temp, "C")
print("Chance of Rain:", rain_chance, "%")
print("Wind speed:", wind_speed, "kmh")
print("Next Sunrise:", sunrise[0], "@", sunrise[1] + timezone)
print("Next Sunset:", sunset[0], "@", sunset[1] + timezone)
print(response.text)