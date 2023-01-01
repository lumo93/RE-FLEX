import re
import tkinter as tk
import generatestationforfilters
import os

def delete_old():
    try:
        # Delete the file
        os.remove("userdata/station_filter_values.py")
    except FileNotFoundError:
        raise


def load_data(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    stationlist = {}
    for line in data.splitlines():
        station_id, station_name = line.split(':')
        stationlist[station_id] = station_name
    return stationlist

stationlist = load_data('userdata/serviceAreaIds')


# Create the main window
root = tk.Tk()
root.title("Station List Generator")

# Create a list box and add the items from the stationlist dictionary
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
for station_id, station_name in stationlist.items():
    listbox.insert(tk.END, station_name)

# Load the station list from the chosen_station_list.py file, if it exists
try:
    station_list = load_data('userdata/chosen_station_list')
    # Preselect the options in the list box that are in the station list
    for index in range(listbox.size()):
        station_name = listbox.get(index)
        station_id = list(stationlist.keys())[index]
        if station_id in station_list.keys():
            listbox.select_set(index)
except FileNotFoundError:
    pass

# Create a function to generate the list file when the button is clicked
def generate_list():
    # Compile the regular expression pattern to match the 4-character code
    pattern = re.compile(r'\(([A-Z0-9]{4})\)')

    # Open the file in write mode
    with open("userdata/chosen_station_list", 'w') as f:
        # Iterate over the selected items in the list box
        for index in listbox.curselection():
            # Get the station name and ID for the current item
            station_name = listbox.get(index)
            station_id = list(stationlist.keys())[index]

            # Use the regular expression to extract the 4-character code from the station name
            match = pattern.search(station_name)
            code = match.group(1) if match else ''

            # Write the current item to the file
            f.write("{}:{}\n".format(station_id, code))
    generatestationforfilters.generate()
    print("Station Filters Generated")
    try:
        delete_old()
        print("Values cleared, please set new values")
    except FileNotFoundError:
        print("Please set your values")

# Create a button and set its command
button = tk.Button(root, text="Generate List", command=generate_list)

# Pack the widgets
listbox.pack(fill=tk.BOTH, expand=True)
button.pack(fill=tk.BOTH)

root.geometry("350x700")
root.resizable(True, True)

root.wm_title("Select advanced filter stations:")
# Run the main loop
root.mainloop()
