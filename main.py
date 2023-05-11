# Import the relevant libraries
import requests
import json
import urllib.parse

# Prints a welcome message
print("### Welcome to the Weather CLI! ###")

# Asks for the postcode, uses OSM's restAPI to get the geo Co-ords, then stores them in a variable
address = input("Please enter the postcode: ")
url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'
response = requests.get(url).json()
lat = response[0]["lat"]
lon = response[0]["lon"]

# Set the OpenMeteo API endpoint and parameters from the above variables
url = "https://api.open-meteo.com/v1/forecast?daily=sunrise,sunset," \
      "precipitation_probability_max&current_weather=true&forecast_days=1&timezone=auto"
params = {
    "latitude": lat,
    "longitude": lon
}

# Send the GET request to the API endpoint
response = requests.get(url, params=params)

# Parse the response JSON data
data = json.loads(response.text)

# Stores the JSON data in separate variables
temp = json.dumps(data["current_weather"]["temperature"])
rain_chance = json.dumps(data["daily"]["precipitation_probability_max"])
wind_speed = json.dumps(data["current_weather"]["windspeed"])
sunrise = json.dumps(data["daily"]["sunrise"])
sunset = json.dumps(data["daily"]["sunset"])
timezone = json.dumps(data["timezone_abbreviation"])

# Strips certain variables of their leading and trialing characters, e.g. [ + ]
rain_chance = rain_chance.strip('[]')
sunrise = sunrise.strip('["]')
sunset = sunset.strip('["]')
timezone = timezone.strip('"')

# Splits the sunrise + sunset variables into two parts, and removes the seperator
sunrise = sunrise.split('T')
sunset = sunset.split('T')

# Converts the user's postcode to uppercase for aesthetics, and removes any space that was entered for validation
address = address.upper()
address = address.replace(" ", "")

# Queries where to split postcode, e.g. NP235QR would become NP23 5QR and SA31EU would become SA3 1EU
if len(address) == 6:
    address = address[:3] + " " + address[-3:]
else:
    address = address[:4] + " " + address[-3:]

# Print the response data, including a separation line
print("-----------------------------")
print("Current Weather for Postcode", address)
print("Temperature:", temp + "°C")
print("Chance of Rain:", rain_chance + "%")
print("Wind speed:", wind_speed + "kmh")
print("Next Sunrise:", sunrise[0], "@", sunrise[1], timezone)
print("Next Sunset:", sunset[0], "@", sunset[1], timezone)
