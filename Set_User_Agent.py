import tkinter as tk
import random

def select_from_list():
    # Get the index of the currently selected item in the listbox
    index = listbox.curselection()[0]
    
    # Get the item from the listbox at the selected index
    selection = listbox.get(index)
    
    # Write the selected item to the new file
    with open('userdata/useragent', 'w') as f:
        f.write(f"{selection}")

def random_selection():
    # Get the number of items in the listbox
    num_items = listbox.size()
    
    # Choose a random index
    index = random.randint(0, num_items - 1)
    
    # Select the item at the random index
    listbox.selection_set(index)
    
    # Write the selected item to the new file
    with open('userdata/useragent', 'w') as f:
        f.write(f"{listbox.get(index)}")

# Load the list of items from the file
with open('useragentlist', 'r') as f:
    lines = f.readlines()

items = [line.strip() for line in lines]

# Create the main window
root = tk.Tk()

# Create a frame for the listbox and buttons
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Create a scrollbar
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a listbox and attach it to the scrollbar
listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=30, height=10)
listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Attach the scrollbar to the listbox
scrollbar.config(command=listbox.yview)

# Add the items to the listbox
for item in items:
    listbox.insert(tk.END, item)

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM)

# Create a button to select the item from the list
select_button = tk.Button(button_frame, text='Select', command=select_from_list)
select_button.pack(side=tk.LEFT)

# Create a button to select a random item from the list
random_button = tk.Button(button_frame, text='Random', command=random_selection)
random_button.pack(side=tk.LEFT)

root.geometry("500x300")

# Run the main loop
root.mainloop()
