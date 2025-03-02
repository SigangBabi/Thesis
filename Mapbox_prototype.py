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
    "TEST": (120.56068854838901, 14.91398731640344)
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

origin = [120.56330961194001, 14.912845969145359]

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

