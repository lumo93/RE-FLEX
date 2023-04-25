import tkinter as tk
from tkinter import ttk
import subprocess
import time
import os

python = "python"  # default value of the python variable

class App:
    def __init__(self, master):
        self.master = master
        self.scripts = []

        # Create a frame to hold the start and stop buttons
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack()

        label = tk.Label(self.master, text="Select python system variable:")
        label.pack()

        # Create a listbox widget to hold the options for the python variable
        self.python_listbox = tk.Listbox(self.master, width=20, height=5)
        self.python_listbox.pack()
        
        # Add options to the listbox
        self.python_listbox.insert(1, "python")
        self.python_listbox.insert(2, "python3")
        self.python_listbox.insert(3, "python3.9")
        self.python_listbox.insert(4, "python3.10")
        self.python_listbox.insert(5, "python3.11")
        
        # Set up a callback function to update the value of the python variable when an item is selected
        self.python_listbox.bind('<<ListboxSelect>>', self.on_python_select)
        
    def on_python_select(self, event):
        # Get the selected index
        index = self.python_listbox.curselection()[0]
        
        # Update the value of the python variable based on the selected index
        global python
        python = self.python_listbox.get(index)
        
    def add_script(self, script_name, has_stop_button=True):
        # Create a start button for the script
        start_button_text = f"Start {script_name}" if has_stop_button else f"{script_name}"
        start_button = ttk.Button(self.button_frame, text=start_button_text, command=lambda: self.start(script_name))
        start_button.pack(side="top")
            
        if has_stop_button:
            # Create a stop button for the script
            stop_button = ttk.Button(self.button_frame, text=f"Stop {script_name}", command=lambda: self.stop(script_name))
            stop_button.pack(side="top")

        # Add the script to the list of scripts
        self.scripts.append({
            "name": script_name,
            "process": None,
            "thread": None,
            "stopped": False
        })

    def start(self, script_name):
        # Find the script in the list of scripts
        script = next(s for s in self.scripts if s["name"] == script_name)

        if script["process"] is not None and script["process"].poll() is None:
            # The script is already running, so don't start another process
            print(f"{script_name} is already running")
            return

        # Start the main script in the current terminal window
        script["process"] = subprocess.Popen([python, script_name + ".py"])


    def check_status(self, script_name):
        # Find the script in the list of scripts
        script = next(s for s in self.scripts if s["name"] == script_name)

        # Check the status of the subprocess every 1 second
        while script["thread"].is_alive():
            if script["process"].poll() is not None:
                
                # The subprocess has finished, so stop the thread
                self.stop(script_name)
                return

            # Sleep for 1 second
            time.sleep(1)

    def stop(self, script_name):
        # Find the script in the list of scripts
        script = next(s for s in self.scripts if s["name"] == script_name)

        if script["process"] is not None:
            # Terminate the subprocess
            script["process"].terminate()

            # Set the stopped flag to True
            script["stopped"] = True

            print(f"\n{script_name} stopped")

root = tk.Tk()
root.geometry("240x310")
root.wm_title("Script Dock")
app = App(root)

# Add some scripts to the app
scripts = ["main"]

for script in scripts:
    app.add_script(script)

if not os.path.exists("userdata/useragent"):

    scriptsn = ["Check_Logs", "Choose_Station_Filter", "Set_Filter_Values", "Set_App_Version", "Set_Speeds_and_Behavior", "Offer_List_Debug", "Set_User_Agent", "delete_access_token"]
else:
    scriptsn = ["Check_Logs", "Choose_Station_Filter", "Set_Filter_Values", "Set_App_Version", "Set_Speeds_and_Behavior", "Offer_List_Debug", "delete_access_token"]

for script in scriptsn:
    app.add_script(script, has_stop_button=False)

root.mainloop()
