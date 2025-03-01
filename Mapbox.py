import mapbox
import folium
import tkinter as tk
from tkinter import messagebox

def getCoordinates(locationName):
    global destination
    destination = locations[locationName]

# Replace with your Mapbox access token
ACCESS_TOKEN = "pk.eyJ1IjoianVsZTEyMTIiLCJhIjoiY203OHZmNXR5MDBvcjJpcXlib2todm5zaCJ9.b_2vUI0vMpBLOpdHbJ5I4Q"

# Initialize Mapbox Directions API
directions = mapbox.Directions(access_token=ACCESS_TOKEN)

# Define start and destination coordinates (longitude, latitude)
locations = {
    "College of Education": (120.65434000238541, 14.998032387891913),
    "College of Engineering and Architecture": (120.65501377769775, 14.997547390312992),
    "DHVSU HOSTEL": (120.65619931397212, 14.998358323147109),
    "Auditorium": (120.65564825272104, 14.9984024789093),
    "DHVSU Library": (14.997401562440091, 120.65435701696899),
    "CCS Building": (14.997580978478762, 120.65447101085248),
    "University Food Center": (14.99742617548149, 120.65448844521839),
    "High School Building": (14.997255179570727, 120.65367305372277),
    "College of Arts and Sciences": (14.997889936428535, 120.65485322561476),
    "Administration Building": (14.997269429229796, 120.65384069173324)
}

destination = None


root = tk.Tk()
root.title("Location Selector")
root.geometry("500x500")

# Create buttons for each location

for location in locations:
    tk.Button(root, text=location, command=lambda loc=location: getCoordinates(loc)).pack(pady=5)

tk.Button(root, text="Finish", command=root.destroy).pack(pady=10)

# Run GUI
root.mainloop()

origin = [120.65326376907757, 14.997405005390407]

# Request directions from Mapbox
response = directions.directions(
    [{"type": "Feature", "geometry": {"type": "Point", "coordinates": origin}},
     {"type": "Feature", "geometry": {"type": "Point", "coordinates": destination}}],
    profile="mapbox/walking",
    geometries="geojson"
)

# Extract route geometry
if response.status_code == 200:
    route = response.json()["routes"][0]["geometry"]
else:
    print("Error:", response.text)
    exit()

# Create Folium map
midpoint = [(origin[1] + destination[1]) / 2, (origin[0] + destination[0]) / 2]
m = folium.Map(location=midpoint, zoom_start=50)


# Add markers and route
folium.Marker(location=[origin[1], origin[0]], popup="Start").add_to(m)
folium.Marker(location=[destination[1], destination[0]], popup="End").add_to(m)
folium.PolyLine(locations=[(lat, lon) for lon, lat in route["coordinates"]],
                color="blue", weight=5, opacity=0.7).add_to(m)

# Save map to an HTML file
map_file = "maps.html"
m.save(map_file)

