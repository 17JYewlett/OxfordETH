# Test Google API request.py

import requests

api_key = "AIzaSyBBEmOS2cnLUK9NkEvq4qk4LB9IgN5luoE"  # OKAY TO USE WHEN USING GITHUB!!!!
origin = ""  # Replace with actual postcode
destination = ""  # Replace with actual postcode

def distance_time_between_postcodes(origin, destination):
    # URL encoding spaces
    origin = origin.upper()
    destination = destination.upper()
    origin = origin.replace(" ", "%20")
    destination = destination.replace(" ", "%20")

    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&units=imperial&key={api_key}"


    # Create importable FUNCTION that will RETURN distance between
    response = requests.get(url)
    data = response.json()

    # Extracting distance and duration
    if "rows" in data and data["rows"]:
        elements = data["rows"][0]["elements"][0]
        if "distance" in elements and "duration" in elements:
            distance = elements["distance"]["text"]
            duration = elements["duration"]["text"]
            print(f"Distance: {distance}, Duration: {duration}")
            return distance, duration  # returns as a tuple: (dist: String, dur: String)
        else:
            print("Could not retrieve distance data.")
            return "--mi", "--mins"
    else:
        print("Invalid response from API.")
        return "--mi", "--mins"
    

x, y = distance_time_between_postcodes( "Kemp Porter, North Acton", "LE67 2DU")

print("*"*35)
print(f"Andy Murray (coach): {x}, {y}")