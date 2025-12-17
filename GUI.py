import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import Tk, font
from PIL import Image, ImageTk
import os
import threading
from app_core import geocode_city, get_weather_data
from hot import hot
from cold import cold
from mid import mid
from subz import subz
import random 


"""Weird weather GUI application."""

random_hot_message = random.choice(hot)
random_cold_message = random.choice(cold)
random_mid_message = random.choice(mid)
random_subz_message = random.choice(subz)


def update_result(text):
    """Thread-compatible update for the result."""
    window.after(0, lambda: result_text.set(text))

def show_error(message):
    """Thread compatible error handling."""
    window.after(0, lambda: messagebox.showerror("Error", message))

def run_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name!")
        return
    
    result_text.set("Loading weather data....")

    def task1(city_name):
        try:
                location = geocode_city(city_name)
                data = get_weather_data(location)

                temp = data["temperature"]
                temp2 = round(temp, 2)
                humidity = data["humidity"]
                
                if temp > 27.0:
                    msg = random_hot_message
                elif 15 <= temp <= 27.0:
                    msg = random_mid_message
                elif 0 <= temp < 15:
                     msg = random_cold_message
                else:
                    msg = random_subz_message

                output = (
                    f"Weather for {city_name}:\n"
                    f"Temperature: {temp2}°C\n"
                    f"Humidity: {humidity}%\n"
                    f"{msg}"
                )

                update_result(output)

        except Exception as e:
                show_error(str(e))

    threading.Thread(target=lambda: task1(city)).start()

# GUI Setup
window = tk.Tk()
window.title("Weird_Weather")
window.geometry("800x500")
window.configure(bg="black")

# Set universal font
default_font = font.nametofont("TkDefaultFont")
default_font.configure(family="Times New Roman", size=12, weight="bold")
window.option_add("*Font", default_font)

# ----- Left stacked panels -----
left_frame = tk.Frame(window, width=250, bg="grey")
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

panel1 = tk.Frame(left_frame, width=250, height=250, bg="lightgrey")
panel1.pack(fill=tk.X, padx=5, pady=5)
tk.Label(panel1, text="Panel 1 - Under Development, will be a news portal", bg="lightgrey", wraplength=230, justify="center").pack(expand=True)
panel1.pack_propagate(False)

panel2 = tk.Frame(left_frame, width=250, height=250, bg="darkgrey")
panel2.pack(fill=tk.X, padx=5, pady=5)
tk.Label(panel2, text="Panel 2 - Under Development unsure of what this will be, something fun maybe", bg="darkgrey", wraplength=230, justify="center").pack(expand=True)
panel2.pack_propagate(False)

# ----- Right panel with background image -----
right_frame = tk.Frame(window, width=550, bg="black")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
right_frame.pack_propagate(False)

# Load background image
bg_path = os.path.join("images", "cool_sun.jpg")
bg_img = Image.open(bg_path).resize((550, 500))
bg_photo = ImageTk.PhotoImage(bg_img)

# Background label
bg_label = tk.Label(right_frame, image=bg_photo)
bg_label.image = bg_photo
bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # fill the frame

#Place Widgets on top of background
tk.Label(right_frame, text="Enter a city name:", bg="black", fg="white").pack(pady=10)
city_entry = tk.Entry(right_frame, width=30)
city_entry.pack()
tk.Button(right_frame, text="Get Weather", command=run_weather).pack(pady=10)

result_text = tk.StringVar()
tk.Label(right_frame, textvariable=result_text, bg="black", fg="white", wraplength=500, justify="left").pack(pady=20)

window.mainloop()
