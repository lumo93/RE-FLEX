import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import tkinter.ttk as ttk
import os

def update_window(filename, text_widget):
    with open(f"debugging/{filename}", "r") as f:
        contents = f.read()
    text_widget.delete("1.0", tk.END)  # clear the text widget
    text_widget.insert("1.0", contents)  # insert the new contents
    text_widget.see(tk.END)  # scroll to the bottom of the textbox

def save_to_file(filename, text_widget):
    # get the contents of the text widget
    contents = text_widget.get("1.0", tk.END)
    
    # write the contents to the file
    with open(f"debugging/{filename}", "w") as f:
        f.write(contents)

def check_for_changes(filename, text_widget):
    # get the current modification time of the file
    current_mtime = os.stat(f"debugging/{filename}").st_mtime
    
    # check if the file has been modified since the last time we checked
    if current_mtime != text_widget.last_mtime:
        # update the text widget with the new contents of the file
        with open(f"debugging/{filename}", "r") as f:
            contents = f.read()
        text_widget.delete("1.0", tk.END)  # clear the text widget
        text_widget.insert("1.0", contents)  # insert the new contents
        text_widget.see(tk.END)  # scroll to the bottom of the textbox
        text_widget.last_mtime = current_mtime  # store the current modification time for later comparison
    else:
        # the file has not been modified, so do nothing
        pass
    
    # schedule another call to this function in 500 milliseconds
    text_widget.after(500, lambda: check_for_changes(filename, text_widget))

def clear_file(filename, text_widget):
    with open(f"debugging/{filename}", "w") as f:
        f.write("")  # write an empty string to the file
    with open(f"debugging/{filename}", "r") as f:
        contents = f.read()
    text_widget.delete("1.0", tk.END)  # clear the text widget
    text_widget.insert("1.0", contents)  # insert the new contents (which should be empty)
    text_widget.see(tk.END)  # scroll to the bottom of the textbox

# create the main window
window = tk.Tk()

# get a list of all the filenames in the debugging directory
filenames = os.listdir("debugging")

# create an empty list to hold the text widgets and button sets
text_widgets = []
button_sets = []

# create a frame for each file
for i, filename in enumerate(filenames):
    frame = ttk.Frame(window)
    frame.pack(side="left", fill="both", expand=True)
    
    # create a label for the filename
    label = ttk.Label(frame, text=filename)
    label.pack(side="top", fill="x")

    # create a scrolled text widget and place it inside the frame
    text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=39)
    text.pack(side="top", fill="both", expand=True)
    text_widgets.append(text)
    
    # store the initial modification time of the file in the text widget
    text.last_mtime = os.stat(f"debugging/{filename}").st_mtime
    
    # start checking for changes to the file
    update_window(filenames[i], text_widgets[i])
    check_for_changes(filename, text)
    
    # create a set of buttons and place them inside the frame
    button_update = ttk.Button(frame, text="Save", command=lambda i=i: save_to_file(filenames[i], text_widgets[i]))
    button_update.pack(side="left", fill="x", expand=True)
    button_clear = ttk.Button(frame, text="Clear", command=lambda i=i: clear_file(filenames[i], text_widgets[i]))
    button_clear.pack(side="right", fill="x", expand=True)
    button_sets.append((button_update, button_clear))

window.wm_title("Debugging")
# start the main loop
window.mainloop()