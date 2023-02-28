def load_data(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    stationlist = {}
    for line in data.splitlines():
        station_id, station_name = line.split(':')
        stationlist[station_id] = station_name
    return stationlist

def generate_station_list(station_list, filepath):
    # Unpack the dictionary into two lists
    station_ids, letters = zip(*station_list.items())

    # Open the file in write mode
    with open(filepath, 'w') as f:
        f.write(f"# Default Values\n")
        f.write(f"def_headstart = 60\n")
        f.write(f"def_rate = 25\n")
        f.write(f"def_minlength = 1\n")
        f.write(f"def_maxlength = 5\n")
        f.write(f"def_lowprice = 120\n")
        f.write("\n")
        for station_id, station_name in station_list.items():
            # Write the station name as a comment
            f.write(f"# {station_name}\n")
            # Write the variables to the file
            f.write(f"{station_name}_headstart = def_headstart\n")
            f.write(f"{station_name}_rate = def_rate\n")
            f.write(f"{station_name}_minlength = def_minlength\n")
            f.write(f"{station_name}_maxlength = def_maxlength\n")
            f.write(f"{station_name}_lowprice = def_lowprice\n")
            # Write the opening line of the output to the file
        f.write("\n")
        f.write("station_list = {\n")

        # Iterate over the station IDs and letters
        for station_id, letter in zip(station_ids, letters):
            # Construct the dictionary for the current station and write it to the file
            f.write("    '{}': {{'headstart': {}, 'minlength': {}, 'maxlength': {}, 'rate': {}, 'lowprice': {}}},\n".format(
                station_id,
                f"{letter}_headstart",
                f"{letter}_minlength",
                f"{letter}_maxlength",
                f"{letter}_rate",
                f"{letter}_lowprice"
            ))

        # Write the closing line of the output to the file
        f.write("}")

# Example usage
def generate():
    station_list = load_data('userdata/chosen_station_list')
    filepath = 'userdata/station_filter_list.py'
    generate_station_list(station_list, filepath)
