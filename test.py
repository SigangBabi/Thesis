import tkinter as tk
from tkinter import messagebox

# Predefined coordinates for each button
locations = {
    "College of Education": (14.998032387891913, 120.65434000238541),  # Example: Manila, PH
    "College of Engineering and Architecture": (14.997547390312992, 120.65501377769775), # Example: San Francisco, USA
    "DHVSU HOSTEL": (14.998358323147109, 120.65619931397212),   # Example: London, UK
    "Auditorium": (14.9984024789093, 120.65564825272104)   # Example: Tokyo, Japan
}

destination = None


def getCoordinates(locationName):
    global destination
    destination = locations[locationName]
    print(destination)



root = tk.Tk()
root.title("Location Selector")
root.geometry("300x250")

# Create buttons for each location

for location in locations:
    tk.Button(root, text=location, command=lambda loc=location: getCoordinates(loc)).pack(pady=5)



# Run GUI
root.mainloop()