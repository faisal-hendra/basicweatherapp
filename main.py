# The GUI was generated using Tkinter Designer by Parth Jadhav.
# Check the github page:
# https://github.com/ParthJadhav/Tkinter-Designer

# GUI concept and functionality was created and added by Faisal aka ellesdee.
# To find out on how to convert Figma draft into Tkinter code, you may want to watch this video:
# https://youtu.be/mFjE2-rbpm8?si=EuF4SBoWY4gjqr4O

# Special thanks to Arpan Neupane for the tutorial on how utilize the OpenWeatherMap.org API
# and for the inspiration to build this app in the first place!
# https://github.com/arpanneupane19
# https://www.youtube.com/@ArpanNeupaneProductions

# Shout out to two-toner and pouty

import requests
import datetime
import sys
import os
import json

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, PhotoImage, messagebox 
import pyglet

# To let the EXE know that the resource files are bundled within the package
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Access all files in the ./assets folder
assets_folder = resource_path("assets")
for file_name in os.listdir(assets_folder):
    file_path = os.path.join(assets_folder, file_name)
    print(file_path)  # List each file for debug

# Import custom font using pyglet
pyglet.options['win32_gdi_font'] = True
fontpath = resource_path("assets/Inter.ttf")
pyglet.font.add_file(str(fontpath))

# API Key for weather data from OpenWeather
# Ik storing API key like this is a bad practice, but I'm new to python so idc.

with open(resource_path("assets/.api")) as config_file:
    config = json.load(config_file)

API_key = config['API_key']
    
# Get geolocation
# Old API that I used:
# IP = requests.get("https://api.ipify.org").text 
# But working with json is fun so i changed it lol.

# API for Geo Data

try:
    IP_String = requests.get(f"https://api-bdc.net/data/client-ip").json()['ipString']
# Dsiplay error if requests failed
except Exception as e:
   messagebox.showerror(title="Error", 
                        message="Connection failed, please check your internet connection!"
                        )
   exit()

IP_Type = requests.get(f"https://api-bdc.net/data/client-ip").json()['ipType']
geo_data = requests.get(f"https://get.geojs.io/v1/ip/geo/{IP_String}.json").json()

# Location variables
city = geo_data['city']
country = geo_data['country_code']

# Request JSON for weather data in current location from OpenWeather
weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={API_key}")

weather_general= weather_data.json()['weather'][0]['main']
get_weather_description = weather_data.json()['weather'][0]['description']
weather_description = get_weather_description.title() # Title is used to capitalize the words bcoz it looks gutwhy not?

# Get temperature info
temp = round(weather_data.json()['main']['temp'])
temp_max = round(weather_data.json()['main']['temp_max'])
temp_min = round(weather_data.json()['main']['temp_min'])

# Print to terminal, for debugging reasons. . . Gonna delete it later
print("Temp Min: " + str(temp_min))
print("Temp    : " + str(temp))
print("Temp Max: " + str(temp_max))
print("General Weather : " + weather_general)
print("Detailed Weather: " + weather_description)
print("User IP Address : " + IP_String)
print("User IP Type    : " + IP_Type)

# Get today's date
today = datetime.date.today()

# GUI

# Set window position to the center of the screen
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

window = Tk()

window.geometry("500x480")
window.configure(bg = "#FFFFFF")
window.title("Weather App")
window.iconbitmap(resource_path("assets/icon.ico"))
window.resizable(False, False)

center_window(window)

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 500,
    width = 500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

# Logic to determine which background to use, depending on the current weather
if weather_general == "Clear" or weather_general == "Clouds": 
    background_image = PhotoImage(file = resource_path("assets/background_clear.png")) 
elif weather_general == "Rain":
    background_image = PhotoImage(file = resource_path("assets/background_dark.png")) 

canvas.place(x = 0, y = 0)
background = canvas.create_image(
    250.0,
    250.0,
    image=background_image
)

# Logic to determine which weather illustration to use
if weather_general == "Clouds":
    illustration_image = PhotoImage(file=resource_path("assets/cloudy.png"))
elif weather_general == "Clear":
    illustration_image = PhotoImage(file=resource_path("assets/sunny.png"))
elif weather_general == "Rain":
    illustration_image = PhotoImage(file=resource_path("assets/rainy.png"))

illustration = canvas.create_image(
    250.0,
    215.0,
    image=illustration_image
    )

humidity_image = PhotoImage(
    file=resource_path("assets/humidity_alt.png")
)
humidity_illustration = canvas.create_image(
    220,
    420,
    image=humidity_image
)

canvas.create_text(
    250,
    45.0,
    text=today.strftime("%B %d, %Y"),
    fill="#FFFFFF",
    font=("Inter Light", 24 * -1)
)

canvas.create_text(
    250,
    87.5,
    text=city + ", " + country,
    fill="#FFFFFF",
    font=("Inter Bold", 24 * -1)
)

canvas.create_text(
    250.0,
    335.0,
    text=str(temp) + " °C",
    fill="#FFFFFF",
    font=("Inter Bold", 36 * -1)
)

canvas.create_text(
    250,
    375.0,
    text=weather_description,
    fill="#FFFFFF",
    font=("Inter", 24 * -1)
)

canvas.create_text(
    266,
    417.5,
    text=str(weather_data.json()['main']['humidity']) + "%",
    fill="#FBFBFB",
    font=("Inter", 24 * -1)
)

window.mainloop()
