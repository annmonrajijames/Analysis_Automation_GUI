import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import os
from tkcalendar import DateEntry

def browse_file():
    excel_path = filedialog.askopenfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    excel_path_var.set(excel_path)

def save_to_excel():
    date = date_var.get()
    time_from = f"{time_from_hour_var.get()}:{time_from_minute_var.get()}:{time_from_second_var.get()}"
    time_to = f"{time_to_hour_var.get()}:{time_to_minute_var.get()}:{time_to_second_var.get()}"
    bytebeam_influx = bytebeam_influx_var.get()
    bytebeam_number = bytebeam_number_var.get()
    
    eco_percentage = eco_percentage_var.get()
    power_percentage = power_percentage_var.get()
    custom_percentage = custom_percentage_var.get()
    
    battery_number = battery_number_var.get()
    soc_from = soc_from_var.get()
    soc_to = soc_to_var.get()
    shift = shift_var.get()
    condition = condition_var.get()
    rider_weight = rider_weight_var.get()
    spare_battery = spare_battery_var.get()
    carrying_charger = carrying_charger_var.get()
    route = route_var.get()
    excel_path_selected = excel_path_var.get()
    
    if not all([date, time_from, time_to, bytebeam_influx, bytebeam_number, eco_percentage, power_percentage, custom_percentage, battery_number, soc_from, soc_to, shift, condition, rider_weight, route, excel_path_selected]):
        messagebox.showwarning("Input Error", "All fields and file path must be filled out!")
        return

    data = {
        "Date": [date],
        "Time From": [time_from],
        "Time To": [time_to],
        "Bytebeam/Influx": [bytebeam_influx],
        "Bytebeam ID": [bytebeam_number],
        "Eco Mode(%)": [eco_percentage],
        "Power Mode(%)": [power_percentage],
        "Custom Mode(%)": [custom_percentage],
        "Battery Number": [battery_number],
        "SOC From": [soc_from],
        "SOC To": [soc_to],
        "Shift": [shift],
        "Condition": [condition],
        "Rider Weight": [rider_weight],
        "Spare Battery": ["Yes" if spare_battery else "No"],
        "Carrying Charger": ["Yes" if carrying_charger else "No"],
        "Route": [route]
    }
    
    df = pd.DataFrame(data)
    if os.path.exists(excel_path_selected):
        existing_df = pd.read_excel(excel_path_selected)
        new_df = pd.concat([existing_df, df], ignore_index=True)
        new_df.to_excel(excel_path_selected, index=False)
    else:
        df.to_excel(excel_path_selected, index=False)
    
    messagebox.showinfo("Success", "Data saved successfully!")
    for var in (date_var, time_from_hour_var, time_from_minute_var, time_from_second_var, time_to_hour_var, time_to_minute_var, time_to_second_var, bytebeam_influx_var, eco_percentage_var, power_percentage_var, custom_percentage_var, battery_number_var, soc_from_var, soc_to_var, shift_var, condition_var, rider_weight_var, route_var):
        var.set('')
    spare_battery_var.set(0)
    carrying_charger_var.set(0)
    excel_path_var.set('')
    bytebeam_number_var.set('')

def update_mode_labels(*args):
    vehicle_type = vehicle_type_var.get()
    if vehicle_type == "LX70":
        eco_mode_label.config(text="Eco Mode(%):")
        power_mode_label.config(text="Fast Mode(%):")
        custom_mode_label.config(text="Custom Mode(%):")
    elif vehicle_type == "Nduro":
        eco_mode_label.config(text="Eco Mode(%):")
        power_mode_label.config(text="Normal Mode(%):")
        custom_mode_label.config(text="Fast Mode(%):")
    elif vehicle_type == "M100":
        eco_mode_label.config(text="Eco Mode(%):")
        power_mode_label.config(text="Normal Mode(%):")
        custom_mode_label.config(text="Fast Mode(%):")

def update_bytebeam_field(*args):
    bytebeam_influx = bytebeam_influx_var.get()
    if bytebeam_influx in ["Bytebeam", "Influx"]:
        bytebeam_number_label.config(text=f"{bytebeam_influx} id:")
    else:
        bytebeam_number_label.config(text="Bytebeam id:")
    bytebeam_number_entry.grid(row=5, column=1, padx=10, pady=10)  # Ensure the entry is always shown

def open_time_picker(entry_var):
    time_picker = tk.Toplevel(root)
    time_picker.title("Select Time")

    def set_time():
        hours = hour_var.get()
        minutes = minute_var.get()
        seconds = second_var.get()
        entry_var.set(f"{hours:02}:{minutes:02}:{seconds:02}")
        time_picker.destroy()

    hour_var = tk.StringVar(value="00")
    minute_var = tk.StringVar(value="00")
    second_var = tk.StringVar(value="00")

    tk.Label(time_picker, text="Hours:").grid(row=0, column=0)
    tk.Entry(time_picker, textvariable=hour_var, width=5).grid(row=0, column=1)

    tk.Label(time_picker, text="Minutes:").grid(row=1, column=0)
    tk.Entry(time_picker, textvariable=minute_var, width=5).grid(row=1, column=1)

    tk.Label(time_picker, text="Seconds:").grid(row=2, column=0)
    tk.Entry(time_picker, textvariable=second_var, width=5).grid(row=2, column=1)

    tk.Button(time_picker, text="OK", command=set_time).grid(row=3, column=0, columnspan=2)

# Tkinter window setup
root = tk.Tk()
root.title("Vehicle Data Logger")

# Create a Frame with Scrollbars
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

scrollable_frame = tk.Frame(canvas)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Enable mouse scrolling
scrollbar.config(command=canvas.yview)

# Bind mouse scrolling to the canvas
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

root.bind_all("<MouseWheel>", on_mouse_wheel)

# Use scrollable_frame instead of root for all widgets
scrollable_frame.update_idletasks()

# Date Picker
date_var = tk.StringVar()
date_label = tk.Label(scrollable_frame, text="Select Date:")
date_label.grid(row=0, column=0, padx=10, pady=10)
date_entry = DateEntry(scrollable_frame, textvariable=date_var, date_pattern='yyyy-mm-dd')
date_entry.grid(row=0, column=1, padx=10, pady=10)

# Time Period From and To (Hours, Minutes, Seconds)
time_from_var = tk.StringVar()
time_to_var = tk.StringVar()
time_from_label = tk.Label(scrollable_frame, text="Time From (HH:MM:SS):")
time_from_label.grid(row=1, column=0, padx=10, pady=10)
time_from_button = tk.Button(scrollable_frame, text="Select Time", command=lambda: open_time_picker(time_from_var))
time_from_button.grid(row=1, column=1, padx=10, pady=10)
time_to_label = tk.Label(scrollable_frame, text="Time To (HH:MM:SS):")
time_to_label.grid(row=2, column=0, padx=10, pady=10)
time_to_button = tk.Button(scrollable_frame, text="Select Time", command=lambda: open_time_picker(time_to_var))
time_to_button.grid(row=2, column=1, padx=10, pady=10)

# Vehicle Type Dropdown
vehicle_type_var = tk.StringVar()
vehicle_type_label = tk.Label(scrollable_frame, text="Vehicle Type:")
vehicle_type_label.grid(row=3, column=0, padx=10, pady=10)
vehicle_type_menu = ttk.Combobox(scrollable_frame, textvariable=vehicle_type_var, values=["LX70", "Nduro", "M100"])
vehicle_type_menu.grid(row=3, column=1, padx=10, pady=10)
vehicle_type_menu.bind("<<ComboboxSelected>>", update_mode_labels)

# Dropdown for Bytebeam/Influx
bytebeam_influx_var = tk.StringVar()
bytebeam_influx_label = tk.Label(scrollable_frame, text="Bytebeam/Influx:")
bytebeam_influx_label.grid(row=4, column=0, padx=10, pady=10)
bytebeam_influx_menu = ttk.Combobox(scrollable_frame, textvariable=bytebeam_influx_var, values=["Bytebeam", "Influx"])
bytebeam_influx_menu.grid(row=4, column=1, padx=10, pady=10)
bytebeam_influx_menu.bind("<<ComboboxSelected>>", update_bytebeam_field)

# Bytebeam Number
bytebeam_number_var = tk.StringVar()
bytebeam_number_label = tk.Label(scrollable_frame, text="Bytebeam ID:")
bytebeam_number_label.grid(row=5, column=0, padx=10, pady=10)
bytebeam_number_entry = tk.Entry(scrollable_frame, textvariable=bytebeam_number_var)
bytebeam_number_entry.grid(row=5, column=1, padx=10, pady=10)

# Eco Mode and Percentage
eco_percentage_var = tk.StringVar()
eco_mode_label = tk.Label(scrollable_frame, text="Mode 1(%):")
eco_mode_label.grid(row=6, column=0, padx=10, pady=10)
eco_percentage_entry = tk.Entry(scrollable_frame, textvariable=eco_percentage_var)
eco_percentage_entry.grid(row=6, column=1, padx=10, pady=10)

# Power Mode and Percentage
power_percentage_var = tk.StringVar()
power_mode_label = tk.Label(scrollable_frame, text="Mode 2(%):")
power_mode_label.grid(row=7, column=0, padx=10, pady=10)
power_percentage_entry = tk.Entry(scrollable_frame, textvariable=power_percentage_var)
power_percentage_entry.grid(row=7, column=1, padx=10, pady=10)

# Custom Mode and Percentage
custom_percentage_var = tk.StringVar()
custom_mode_label = tk.Label(scrollable_frame, text="Mode 3(%):")
custom_mode_label.grid(row=8, column=0, padx=10, pady=10)
custom_percentage_entry = tk.Entry(scrollable_frame, textvariable=custom_percentage_var)
custom_percentage_entry.grid(row=8, column=1, padx=10, pady=10)

# Battery Number
battery_number_var = tk.StringVar()
battery_number_label = tk.Label(scrollable_frame, text="Battery Number:")
battery_number_label.grid(row=9, column=0, padx=10, pady=10)
battery_number_entry = tk.Entry(scrollable_frame, textvariable=battery_number_var)
battery_number_entry.grid(row=9, column=1, padx=10, pady=10)

# SOC From and To
soc_from_var = tk.StringVar()
soc_from_label = tk.Label(scrollable_frame, text="SOC From:")
soc_from_label.grid(row=10, column=0, padx=10, pady=10)
soc_from_entry = tk.Entry(scrollable_frame, textvariable=soc_from_var)
soc_from_entry.grid(row=10, column=1, padx=10, pady=10)
soc_to_var = tk.StringVar()
soc_to_label = tk.Label(scrollable_frame, text="SOC To:")
soc_to_label.grid(row=10, column=2, padx=10, pady=10)
soc_to_entry = tk.Entry(scrollable_frame, textvariable=soc_to_var)
soc_to_entry.grid(row=10, column=3, padx=10, pady=10)

# Shift Dropdown
shift_var = tk.StringVar()
shift_label = tk.Label(scrollable_frame, text="Shift:")
shift_label.grid(row=11, column=0, padx=10, pady=10)
shift_menu = ttk.Combobox(scrollable_frame, textvariable=shift_var, values=["Morning", "Night"])
shift_menu.grid(row=11, column=1, padx=10, pady=10)

# Condition Dropdown
condition_var = tk.StringVar()
condition_label = tk.Label(scrollable_frame, text="Condition:")
condition_label.grid(row=12, column=0, padx=10, pady=10)
condition_menu = ttk.Combobox(scrollable_frame, textvariable=condition_var, values=["Single", "Dual"])
condition_menu.grid(row=12, column=1, padx=10, pady=10)

# Rider Weight
rider_weight_var = tk.StringVar()
rider_weight_label = tk.Label(scrollable_frame, text="Rider Weight:")
rider_weight_label.grid(row=13, column=0, padx=10, pady=10)
rider_weight_entry = tk.Entry(scrollable_frame, textvariable=rider_weight_var)
rider_weight_entry.grid(row=13, column=1, padx=10, pady=10)

# Spare Battery and Carrying Charger Checkboxes
spare_battery_var = tk.IntVar()
spare_battery_check = tk.Checkbutton(scrollable_frame, text="Spare Battery", variable=spare_battery_var)
spare_battery_check.grid(row=14, column=0, padx=10, pady=10)
carrying_charger_var = tk.IntVar()
carrying_charger_check = tk.Checkbutton(scrollable_frame, text="Carrying Charger", variable=carrying_charger_var)
carrying_charger_check.grid(row=14, column=1, padx=10, pady=10)

# Route Entry
route_var = tk.StringVar()
route_label = tk.Label(scrollable_frame, text="Route:")
route_label.grid(row=15, column=0, padx=10, pady=10)
route_entry = tk.Entry(scrollable_frame, textvariable=route_var)
route_entry.grid(row=15, column=1, padx=10, pady=10)

# File Path
excel_path_var = tk.StringVar()
excel_path_label = tk.Label(scrollable_frame, text="Excel File Path:")
excel_path_label.grid(row=16, column=0, padx=10, pady=10)
excel_path_entry = tk.Entry(scrollable_frame, textvariable=excel_path_var, state="readonly")
excel_path_entry.grid(row=16, column=1, padx=10, pady=10)
browse_button = tk.Button(scrollable_frame, text="Browse", command=browse_file)
browse_button.grid(row=16, column=2, padx=10, pady=10)

# Save Button
save_button = tk.Button(scrollable_frame, text="Save", command=save_to_excel, width=20)
save_button.grid(row=17, column=0, columnspan=4, padx=10, pady=10, sticky=tk.E)

root.mainloop()
