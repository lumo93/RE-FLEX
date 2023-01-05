import tkinter as tk
import os

def save_string():
    # Get the string to save
    string_to_save = input_field.get()
    
    # Open the file in write mode
    with open('userdata/version', 'w') as f:
        # Write the string to the file
        f.write(string_to_save)

# Create the main window
window = tk.Tk()

label = tk.Label(window, text='Set current Android Flex app Version:')
label.pack()

file_contents = None

# Check if the station_filter_values.py file exists
if os.path.exists("userdata/version"):
    # Read the contents of the file into a string
    with open("userdata/version", "r") as f:
        file_contents = f.read()

# Create a text entry field and pre-load it with the contents of the file
input_field = tk.Entry(window)
input_field.pack()

# Check if the station_filter_values.py file exists
if os.path.exists("userdata/version"):

    # Insert the contents of the file into the input field
    input_field.insert(0, file_contents)

# Create a button to save the string
save_button = tk.Button(window, text='Save', command=save_string)
save_button.pack()

# Get the window size
window_width = window.winfo_width()
window_height = window.winfo_height()

window.geometry(f"200x80")

window.wm_title("")

# Run the main loop
window.mainloop()
