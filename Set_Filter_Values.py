import os
import tkinter as tk

# Read the station_filter_list.py file and extract the variables
variables = {}
exec(open("userdata/station_filter_list.py").read(), variables)

# Filter the dictionary to remove the __builtins__ fields
filtered_variables = {name: value for name, value in variables.items() if name != "__builtins__"}

# Get the station_list variable
station_list = filtered_variables["station_list"]

# Check if the station_filter_values.py file exists
if os.path.exists("userdata/station_filter_values.py"):
    # Read the station_filter_values.py file and extract the variables
    variables = {}
    exec(open("userdata/station_filter_values.py").read(), variables)

    # Get the station_list variable from the file
    station_list = variables["station_list"]

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    stationlist = {}
    for line in data.splitlines():
        station_id, station_name = line.split(':')
        stationlist[station_id] = station_name
    return stationlist

stationcode = load_data('userdata/chosen_station_list')

# Create a window
window = tk.Tk()

# Create a frame to hold the widgets
frame = tk.Frame(window)
frame.pack(fill='both', expand=True)

# Create a canvas widget
canvas = tk.Canvas(frame)
canvas.pack(side='left', fill='both', expand=True)

def on_mouse_wheel(event):
    # Check the direction of the mouse wheel scroll
    if event.delta > 0:
        # Scroll up
        canvas.yview_scroll(-1, "units")
        scrollbar.set(canvas.yview()[0], canvas.yview()[1])
    else:
        # Scroll down
        canvas.yview_scroll(1, "units")
        scrollbar.set(canvas.yview()[0], canvas.yview()[1])

# Bind the <MouseWheel> event to the on_mouse_wheel function
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

def on_mouse_scroll(event):
    # Check the button number of the event
    if event.num == 4:
        # Scroll up
        canvas.yview_scroll(-1, "units")
        scrollbar.set(canvas.yview()[0], canvas.yview()[1])
    elif event.num == 5:
        # Scroll down
        canvas.yview_scroll(1, "units")
        scrollbar.set(canvas.yview()[0], canvas.yview()[1])

# Bind the <Button-4> and <Button-5> events to the on_mouse_scroll function
canvas.bind_all("<Button-4>", on_mouse_scroll)
canvas.bind_all("<Button-5>", on_mouse_scroll)

# Create a scrollbar widget
scrollbar = tk.Scrollbar(canvas, orient='vertical', command=canvas.yview)
scrollbar.pack(side='right', fill='y')

# Set the canvas widget's yscrollcommand to be the scrollbar's set method
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame to hold the widgets that will be added to the canvas
inner_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor='nw')

# Create a label and entry widget for each station in the station list
entry_vars = {}  # dictionary to store the entry widgets' StringVar objects
for i, (station_id, values) in enumerate(station_list.items()):
    # Create a label for the station
    label = tk.Label(inner_frame, text=stationcode[station_id])

    # Create a frame to hold the entry widgets for the station's values
    value_frame = tk.Frame(inner_frame)
    value_frame.grid(row=i, column=2)

    # Create an entry widget for each value
    for j, (name, value) in enumerate(values.items()):
        # Create a label for the value
        value_label = tk.Label(value_frame, text=name)
        value_label.grid(row=j, column=1)

        # Create a StringVar that is linked to the entry widget
        entry_var = tk.StringVar()
        entry_var.set(str(value))

        # Create an entry widget for the value
        entry = tk.Entry(value_frame, textvariable=entry_var)
        entry.grid(row=j, column=2)

        # Add the entry widget's StringVar object to the entry_vars dictionary
        entry_vars[(station_id, name)] = entry_var

    # Add the label and frame to the inner frame using the grid layout manager
    label.grid(row=i, column=1, sticky="n")

    # Create a separator widget
    separator = tk.Frame(inner_frame, width=2, background="black", bd=1, relief='sunken')

    # Add the separator to the inner frame below each set of labels and entry widgets
    separator.grid(row=i, column=1, columnspan=2, sticky="new", pady=0)

def save_changes():
    # Update the values in the station list with the values from the entry widgets
    for (station_id, name), entry_var in entry_vars.items():
        station_list[station_id][name] = entry_var.get()

    # Write the updated station list to the station_filter_values.py file
    with open("userdata/station_filter_values.py", "w") as f:
        f.write("station_list = {\n")
        for station_id, values in station_list.items():
            f.write(f"    '{station_id}': {{\n")
            for name, value in values.items():
                f.write(f"        '{name}': {value},\n")
            f.write("    },\n")
        f.write("}\n")
    print("Values saved")

button_frame = tk.Frame(window)

button_frame.pack()

# Create a button widget to save the changes
save_button = tk.Button(button_frame, text="Save", command=save_changes)

# Create a separator widget
separator = tk.Frame(inner_frame, width=2, background="black", bd=1, relief='sunken')

# Add the separator to the inner frame below each set of labels and entry widgets
separator.grid(row=i+1, column=1, columnspan=2, sticky="new", pady=0)

# Arrange the button widget using the grid layout manager
save_button.grid()

# Update the scrollregion of the canvas
canvas.update_idletasks()

# Configure the scrollregion to cover the entire inner frame
canvas.configure(scrollregion=canvas.bbox('all'))

window.wm_title("Filter Values:")

# Get the window size
window_width = window.winfo_width()
window_height = window.winfo_height()

window.geometry(f"245x400")

# Run the Tkinter event loop
window.mainloop()

