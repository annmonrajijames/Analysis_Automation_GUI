import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import sys
 
# Importing the analysis scripts directly
import Bytebeam_LX70
import Bytebeam_LXS
import Bytebeam_NDuro
import Influx_LX70
import Influx_LXS
# import Influx_NDuro
import Influx_NDuro_NoGPS

def open_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        path_label.config(text=folder_path)
        run_button.config(state='normal')
 
def copy_folder():
    destination_path = filedialog.askdirectory(title="Select Destination for Copy")
    if destination_path:
        destination_folder = os.path.join(destination_path, os.path.basename(folder_path))
        shutil.copytree(folder_path, destination_folder)
        save_output_label.config(text=destination_folder)
        return destination_folder
    else:
        return folder_path

def reset_gui():
    global folder_path, destination_folder
    folder_path = ""
    destination_folder = ""
    file_var.set(next(iter(scripts.values())))  # Reset to the first script
    path_label.config(text="Click Choose Folder- Input Folder's path will be shown here")
    save_output_label.config(text="Output folder path will be shown here")
    copy_var.set(False)
    run_button.config(state='disabled')

def run_script():
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

    if copy_var.get():
        new_path = destination_folder if 'destination_folder' in globals() else folder_path
    else:
        new_path = folder_path

    script = file_var.get()
    # Mapping script names to function calls
    script_functions = {
        "Bytebeam_LX70.py": Bytebeam_LX70.Bytebeam_LX70_input,
        "Bytebeam_LXS.py": Bytebeam_LXS.Bytebeam_LXS_input,
        "Bytebeam_NDuro.py": Bytebeam_NDuro.Bytebeam_NDuro_input,
        "Influx_LX70.py": Influx_LX70.Influx_LX70_input,
        "Influx_LXS.py": Influx_LXS.Influx_LXS_input,
        # "Influx_NDuro.py": Influx_NDuro.Influx_NDuro_input,
        "Influx_NDuro_NoGPS.py": Influx_NDuro_NoGPS.Influx_NDuro_NoGPS_input,
    }

    # Call the corresponding function
    if script in script_functions:
        script_functions[script](new_path)
        reset_gui()  # Reset the GUI after the script is run
 
def handle_copy_check():
    if copy_var.get():
        global destination_folder
        destination_folder = copy_folder()  # Trigger folder selection upon checking
 
app = tk.Tk()
app.title("LECTRIX-Complete Analysis 2.0")
app.configure(bg="lightblue")  # Set the background color
 
# Global variable to store the folder path
folder_path = ""
 
# Label for the dropdown menu
label = tk.Label(app, text="Choose the Analysis", bg="lightblue", fg="black")
label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
 
# Dropdown for selecting the Python script
file_var = tk.StringVar(app)
file_var.set("Select a script")
scripts = {
    "Daily analysis LX70": "Bytebeam_LX70.py",
    "Daily analysis Enduro": "Bytebeam_NDuro.py",
    "Daily analysis LXS": "Bytebeam_LXS.py",
    "Daily analysis Influx LX70" : "Influx_LX70.py",
    # "Daily analysis Influx Enduro" : "Influx_NDuro.py",
    "Daily analysis Influx LXS" : "Influx_LXS.py",
    "Daily analysis Influx NDuro NoGPS": "Influx_NDuro_NoGPS.py",
}
dropdown = tk.OptionMenu(app, file_var, *scripts.values())
dropdown.config(bg="lightblue", fg="black", width=20)
dropdown.grid(row=0, column=1, padx=10, pady=10, sticky='w')  # Align to the left (west)
 
# Set the default value to the first script
file_var.set(next(iter(scripts.values())))
 
# Label for displaying the folder path
path_label = tk.Label(app, text="Click Choose Folder- Input Folder's path will be shown here", bg="lightblue", fg="black", wraplength=100)
path_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
 
# Button to choose the folder
folder_button = tk.Button(app, text="Choose Folder", command=open_folder, bg="lightblue", fg="black")
folder_button.grid(row=1, column=1, padx=10, pady=10, sticky='nw')  # Align to the left (west)
 
# Label for the "Save output in preferred location" checkbox
save_output_label = tk.Label(app, text="Output folder path will be shown here", bg="lightblue", fg="black", wraplength=100)
save_output_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
 
# Checkbox for copying the folder
copy_var = tk.BooleanVar()
copy_check = tk.Checkbutton(app, text="Save output in preferred location", variable=copy_var, bg="lightblue", fg="black", command=handle_copy_check)
copy_check.grid(row=2, column=1, padx=10, pady=5, sticky='w')  # Align to the left (west)
 
# Button to run the script (initially disabled)
run_button = tk.Button(app, text="Run", command=run_script, bg="lightblue", fg="black", state='disabled')
run_button.grid(row=3, columnspan=2, padx=10, pady=20)
 
app.mainloop()