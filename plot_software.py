import tkinter as tk
from tkinter import Button, filedialog, ttk, messagebox
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import mplcursors  # Import mplcursors
from datetime import datetime, timedelta
import mpld3
import webbrowser
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.dates as mdates

# Tkinter GUI Setup
class PlotApp:
    def __init__(self, root, input_file_name=None):
        self.root = root
        self.root.title("Data Plotter")

        # Initialize selected_checkbox_vars
        self.selected_checkbox_vars = {}  # This stores the variables associated with the checkboxes for selected columns

        # Create a main canvas for the entire page
        self.main_canvas = tk.Canvas(root)
        self.main_canvas.pack(side="left", fill=tk.BOTH, expand=True)

        # Add scrollbar to the canvas
        self.main_scrollbar = tk.Scrollbar(root, orient="vertical", command=self.main_canvas.yview)
        self.main_scrollbar.pack(side="right", fill="y")
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)

        # Create a frame inside the canvas to hold the actual content
        self.page_frame = tk.Frame(self.main_canvas)

        # Bind the frame configuration to update the scroll region
        self.page_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )

        # Create a window within the canvas to contain the frame
        self.main_canvas.create_window((0, 0), window=self.page_frame, anchor="nw")

        # Bind mouse wheel scrolling to the entire canvas
        self.page_frame.bind_all("<MouseWheel>", self._on_mousewheel)

        # Main content inside the frame
        self.build_ui()

        # Initialize input_file_name
        self.input_file_name = input_file_name

    def _on_mousewheel(self, event):
        """Enable scrolling the entire page with mouse wheel."""
        self.main_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    def build_ui(self):
        """Build the UI inside the scrollable page_frame."""
        # Control frame on the left
        self.control_frame = tk.Frame(self.page_frame)
        self.control_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        # Plot frame on the right
        self.plot_frame = tk.Frame(self.page_frame)
        self.plot_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Make the plot frame expand more
        self.page_frame.columnconfigure(1, weight=1)
        self.page_frame.rowconfigure(0, weight=1)

        #Influx data or not
        # Add a frame for influx data selection
        self.influx_frame = tk.LabelFrame(self.control_frame, text="Is data in influx?")
        self.influx_frame.pack(pady=10)

        self.influx_var = tk.StringVar(value="yes")
        self.influx_yes = tk.Radiobutton(self.influx_frame, text="Yes", variable=self.influx_var, value="yes")
        self.influx_yes.pack(side="left", padx=5)
        self.influx_no = tk.Radiobutton(self.influx_frame, text="No", variable=self.influx_var, value="no")
        self.influx_no.pack(side="left", padx=5)

        # File Path Input
        self.label = tk.Label(self.control_frame, text="Select Files:")
        self.label.pack(pady=5)

        self.file_listbox = tk.Listbox(self.control_frame, width=60, height=4)
        self.file_listbox.pack(pady=5)

        # Browse Button to select file
        self.browse_button = tk.Button(self.control_frame, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        # Search Box for filtering columns
        self.search_label = tk.Label(self.control_frame, text="Search Columns:")
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self.control_frame, width=50)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.update_checkboxes)

        # Scrollable Frame for checkboxes
        self.checkbox_frame = tk.Frame(self.control_frame)
        self.checkbox_frame.pack(pady=5)

        # Add a canvas with scrollbar for the checkboxes
        self.canvas = tk.Canvas(self.checkbox_frame)
        self.scrollbar = tk.Scrollbar(self.checkbox_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel scrolling to the checkboxes
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Checkbox for Select All
        self.select_all_var = tk.IntVar()
        self.select_all_checkbox = tk.Checkbutton(self.control_frame, text="Select All", variable=self.select_all_var, command=self.toggle_select_all)
        self.select_all_checkbox.pack(pady=5)

        # Search Box for Index Column Selection
        self.index_search_label = tk.Label(self.control_frame, text="Search Index Column:")
        self.index_search_label.pack(pady=5)
        self.index_search_entry = tk.Entry(self.control_frame, width=50)
        self.index_search_entry.pack(pady=5)
        self.index_search_entry.bind("<KeyRelease>", self.update_index_dropdown)

        # Dropdown for Index Column Selection
        self.index_label = tk.Label(self.control_frame, text="Select Index Column:")
        self.index_label.pack(pady=5)
        self.index_column_dropdown = ttk.Combobox(self.control_frame, state="readonly")
        self.index_column_dropdown.pack(pady=5)

        # Frame for checkboxes of selected columns
        self.selected_columns_frame = tk.Frame(self.control_frame)
        self.selected_columns_frame.pack(pady=5)

        # Submit Button
        self.submit_button = tk.Button(self.control_frame, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)

        # Add labels for first and last x-axis values
        self.x_axis_limits_frame = tk.Frame(self.control_frame)
        self.x_axis_limits_frame.pack(pady=10)

        # Initialize the selected_columns_display label without displaying it on the UI
        self.selected_columns_display = tk.Label(self.selected_columns_frame)

        self.first_x_label = tk.Label(self.x_axis_limits_frame, text="First X-axis Value: Not Loaded")
        self.first_x_label.pack(pady=5)

        self.last_x_label = tk.Label(self.x_axis_limits_frame, text="Last X-axis Value: Not Loaded")
        self.last_x_label.pack(pady=5)

        # Add input fields for custom x-axis range
        self.custom_x_axis_frame = tk.Frame(self.control_frame)
        self.custom_x_axis_frame.pack(pady=10)

        self.custom_x_label = tk.Label(self.custom_x_axis_frame, text="Set Custom X-Axis Range:")
        self.custom_x_label.pack(pady=5)

        self.custom_x_min_label = tk.Label(self.custom_x_axis_frame, text="Start Value:")
        self.custom_x_min_label.pack(pady=2)
        self.custom_x_min_entry = tk.Entry(self.custom_x_axis_frame, width=20)
        self.custom_x_min_entry.pack(pady=2)

        self.custom_x_max_label = tk.Label(self.custom_x_axis_frame, text="End Value:")
        self.custom_x_max_label.pack(pady=2)
        self.custom_x_max_entry = tk.Entry(self.custom_x_axis_frame, width=20)
        self.custom_x_max_entry.pack(pady=2)

        self.set_x_axis_button = tk.Button(self.custom_x_axis_frame, text="Apply X-Axis Range", command=self.apply_custom_x_axis)
        self.set_x_axis_button.pack(pady=5)

        # Button to open a new tab
        self.new_tab_button = tk.Button(self.control_frame, text="New Tab", command=self.open_new_tab)
        self.new_tab_button.pack(pady=10)

        # Opacity Slider
        self.opacity_label = tk.Label(self.control_frame, text="Adjust Plot Window Opacity:")
        self.opacity_label.pack(pady=5)
        self.opacity_slider = tk.Scale(self.control_frame, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.adjust_opacity)
        self.opacity_slider.set(1.0)  # Default opacity is 100%
        self.opacity_slider.pack(pady=5)

        self.download_graph_button = tk.Button(self.control_frame, text="Download Graph as HTML", command=self.save_plot_as_html)
        self.download_graph_button.pack(pady=10)

        self.download_zoomed_csv_button = tk.Button(self.control_frame, text="Download Zoomed index as CSV", command=self.download_zoomed_csv)
        self.download_zoomed_csv_button.pack(pady=10)

        self.download_all_parameters_button = tk.Button(self.control_frame, text="Download all parameters Zoomed index as CSV", command=self.download_all_Parameter_in_zoomed_csv)
        self.download_all_parameters_button.pack(pady=10)


        # To hold the extracted column names and their corresponding checkboxes
        self.column_names = []
        self.checkbox_vars = {}  # To store the checkbox variables for each column
        self.data_frames = []  # List to store data from multiple files
        self.file_directory = ""  # Directory of the files

        # Variables for plot management
        self.fig = None
        self.ax_primary = None
        self.ax_secondary = None
        self.ax_tertiary = None
        self.plot_initialized = False

        # Create a separate window for plotting
        self.plot_window = tk.Toplevel(self.root)
        self.plot_window.title("Data Plot")
        self.plot_window.geometry("800x600")  # Set the window size for the plot
        self.plot_frame = tk.Frame(self.plot_window)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

    def adjust_opacity(self, value):
        """Adjust the opacity of the plot window."""
        self.plot_window.attributes('-alpha', float(value))
        
    def open_new_tab(self):
        print("Opening new tab")
        new_window = tk.Toplevel(self.root)
        new_window.title("New Tab")
        new_app = PlotApp(new_window)
        print("Build UI called")

    def process_file(self, file_path):
        try:
            print("Processing file")
            # Determine the file type based on the extension
            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension not in ['.xlsx', '.xls', '.csv']:
                print(f"Skipped: {file_path} (Unsupported file type)")
                return

            # Read the first row to get the date and time from the header
            if file_extension in ['.xlsx', '.xls']:
                first_row = pd.read_excel(file_path, nrows=1, header=None)
            elif file_extension == '.csv':
                first_row = pd.read_csv(file_path, nrows=1, header=None)

            if first_row.empty:
                print(f"Skipped: {file_path} (File is empty)")
                return

            date_time = first_row.iloc[0, 0]
            if ':' in str(date_time):
                date_time = str(date_time).split(':', 1)[1].strip()

            # Read the rest of the data, skipping the first row
            if file_extension in ['.xlsx', '.xls']:
                data = pd.read_excel(file_path, skiprows=1)
            elif file_extension == '.csv':
                data = pd.read_csv(file_path, skiprows=1)

            # Check if "Time" column exists
            if "Time" not in data.columns:
                print(f"Skipped: {file_path} (No 'Time' column found)")
                return

            # Insert the date and time as a new column
            data.insert(0, 'Creation Time', date_time)

            # Drop the first three rows that were originally the 2nd, 3rd, and 4th rows in the file
            if len(data) > 3:
                data = data.drop(data.index[:3])

            # Save the processed data back to the same file
            if file_extension in ['.xlsx', '.xls']:
                data.to_excel(file_path, index=False, engine='openpyxl')
            elif file_extension == '.csv':
                data.to_csv(file_path, index=False)

            print(f"Processed and saved: {file_path}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")


    def browse_file(self):
        # Allow the user to select any file type
        file_paths = filedialog.askopenfilenames(filetypes=[("All files", "*.*")])
        if file_paths:
            # Store the directory path
            self.file_directory = os.path.dirname(file_paths[0])
 
            # Clear the current listbox
            self.file_listbox.delete(0, tk.END)
           
            for file_path in file_paths:
                self.file_listbox.insert(tk.END, os.path.basename(file_path))
                self.load_data_and_columns(file_path)
 
    def load_data_and_columns(self, file_path):
        # Clear previous selections
        self.index_column_dropdown.set('')
       
        if os.path.isfile(file_path):
            try:
                if file_path.endswith('.csv'):
                    # Load the CSV file directly
                    self.data = pd.read_csv(file_path)
    
                elif file_path.endswith('.xlsx'):
                    # Load the Excel file directly
                    self.data = pd.read_excel(file_path)
                    print("Excel file loaded",file_path)
 
                else:
                    raise ValueError("Unsupported file format")
 
                # Drop any fully empty rows
                self.data.dropna(how='all', inplace=True)

                if self.influx_var.get() == "yes":
                    messagebox.showinfo("Influx Data", "Influx data is given as input")
                    # Handle Time conversion if present
                    print("Input data is Influx data")

                    self.file_directory = self.process_file(file_path)

                    if file_path.endswith('.csv'):
                        # Load the CSV file directly
                        self.data = pd.read_csv(file_path)
        
                    if file_path.endswith('.xlsx'):
                        # Load the Excel file directly
                        self.data = pd.read_excel(file_path)
                        print("Excel file loaded",file_path)

                    # For converting Datetime timestamp to Time format
                    if 'DATETIME' not in self.data.columns:  # if 'DATETIME' not in column Present 
                        print("Column datas",self.data.columns)
                        print("DATETIME column not present")
                        self.data['DATETIME'] = self.data['Time']
                    
                    if 'DATETIME' not in self.data.columns:
                        print("DATETIME column not present, using Time column instead")
                        self.data['DATETIME'] = pd.to_datetime(self.data['Time'], errors='coerce')
                    else:
                        self.data['DATETIME'] = pd.to_numeric(self.data['DATETIME'], errors='coerce')
                        self.data.dropna(subset=['DATETIME'], inplace=True)
                        self.data['DATETIME'] = pd.to_datetime(self.data['DATETIME'], unit='s')

                    # Adjust timezone (if needed)
                    self.data['DATETIME'] += pd.to_timedelta('5h30m')  # Adjust timezone to IST

                    print("GPS DATA AVAILABLE")

                    # Store data for each file in the list
                    self.data_frames.append(self.data)
    
                    # Extract the column names
                    self.column_names = self.data.columns.tolist()
    
                    # Update the checkboxes with the full list of columns
                    self.update_checkboxes()
                    print(col.lower() for col in self.column_names)
                    filtered_index_columns = [col for col in self.column_names if col.lower() in ['datetime']]

                    # Populate the dropdown with filtered column names for index selection
                    self.index_column_dropdown['values'] = filtered_index_columns

                if self.influx_var.get() == "no":
                    messagebox.showinfo("Random Data", "Random data is given as input")
                    # Handle Time conversion if present
                    print("Input data is Random data")
                    
                    # Store data for each file in the list
                    self.data_frames.append(self.data)
    
                    # Extract the column names
                    self.column_names = self.data.columns.tolist()
    
                    # Update the checkboxes with the full list of columns
                    self.update_checkboxes()
    
                    # Populate the dropdown with all column names for index selection
                    self.index_column_dropdown['values'] = self.column_names
               
                # Fetch and print the first and last values of the x-axis (DATETIME or Time)
                x_column = 'DATETIME' if 'DATETIME' in self.data.columns else 'Time' if 'Time' in self.data.columns else None
                if x_column:
                    first_value = self.data[x_column].iloc[0]
                    last_value = self.data[x_column].iloc[-1]
                    # Update labels in the UI
                    self.first_x_label.config(text=f"First X-axis Value: {first_value}")
                    self.last_x_label.config(text=f"Last X-axis Value: {last_value}")

                    # Autofill the text boxes with the loaded values
                    self.custom_x_min_entry.delete(0, tk.END)
                    self.custom_x_min_entry.insert(0, str(first_value))

                    self.custom_x_max_entry.delete(0, tk.END)
                    self.custom_x_max_entry.insert(0, str(last_value))
                else:
                    print("No valid x-axis column found.")

                print("Columns available for plotting:", self.column_names)
            except Exception as e:
                print(f"Error loading data: {e}")

    def apply_custom_x_axis(self):
        try:
            # Get custom x-axis values from the user
            custom_min = self.custom_x_min_entry.get()
            custom_max = self.custom_x_max_entry.get()

            print(f"Custom X-axis range: {custom_min} to {custom_max}")

            # Ensure the values are not empty
            if not custom_min or not custom_max:
                raise ValueError("Both start and end values must be provided.")

            # Convert to the appropriate data type (e.g., datetime or numeric)
            x_axis_column = 'DATETIME' if 'DATETIME' in self.data.columns else None
            if x_axis_column:
                # If x-axis is datetime, convert to datetime objects
                try:
                    custom_min = pd.to_datetime(custom_min)
                    custom_max = pd.to_datetime(custom_max)
                except ValueError:
                    print("Invalid date format. Please provide dates in a valid format.")
                    return
                print("X-axis is datetime")
            else:  # Otherwise, treat them as numeric values
                try:
                    custom_min = float(custom_min)
                    custom_max = float(custom_max)
                except ValueError:
                    print("Invalid numeric input. Please enter valid numbers.")
                    return
                print("X-axis is not datetime")

            # Validate range
            first_x = self.data[x_axis_column].iloc[0]
            last_x = self.data[x_axis_column].iloc[-1]
            print(f"First and Last X-axis value: {first_x} , {last_x}")
            if custom_min < first_x or custom_max > last_x:
                print(f"Custom range must be within the first and last x-axis values.")
                raise ValueError("Custom range must be within the first and last x-axis values.")

            # Filter data to include only rows within the custom x-axis range
            filtered_data = self.data[(self.data[x_axis_column] >= custom_min) & (self.data[x_axis_column] <= custom_max)]
            print(f"Filtered data shape: {filtered_data.shape}")

            # Check if self.ax_primary is initialized
            if self.ax_primary is None:
                raise ValueError("Plot axis (self.ax_primary) is not initialized.")

            # Retrieve currently visible lines from the plot
            visible_lines = [line.get_label() for line in self.ax_primary.get_lines()]
            print(f"Currently visible lines: {visible_lines}")

            # Clear the previous plot and update with only the visible data
            self.ax_primary.clear()  # Clear the plot
            print("Plot cleared")

            # Plot only the visible columns
            for col in visible_lines:
                if col in filtered_data.columns and col != x_axis_column:  # Ensure the column is valid
                    self.ax_primary.plot(filtered_data[x_axis_column], filtered_data[col], label=col)

            # Set the new X-axis limits based on the custom range
            self.ax_primary.set_xlim(custom_min, custom_max)
            print("X-axis limits updated")

            # Add legend and refresh the plot
            self.ax_primary.legend(loc='best')
            self.fig.canvas.draw_idle()
            print("Plot updated")

            print(f"X-axis range updated: {custom_min} to {custom_max}")
        except Exception as e:
            print(f"Error applying custom x-axis range: {e}")


    def toggle_select_all(self):
        """Toggle all checkboxes that are currently visible (filtered)."""
        select_all = self.select_all_var.get()
        search_term = self.search_entry.get().lower()

        # Iterate only over the checkboxes that are currently visible (i.e., filtered)
        for col, var in self.checkbox_vars.items():
            if search_term in col.lower():  # Only toggle those that match the search
                var.set(select_all)
 
    def update_checkboxes(self, event=None):
        """Update checkboxes based on the filtered column names."""
        search_term = self.search_entry.get().lower()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Re-create checkboxes based on the filtered columns
        for column_name in self.column_names:
            if search_term in column_name.lower():
                var = self.checkbox_vars.get(column_name, tk.IntVar())
                checkbox = tk.Checkbutton(self.scrollable_frame, text=column_name, variable=var, command=self.update_select_all_checkbox)
                checkbox.pack(anchor="w")
                self.checkbox_vars[column_name] = var

        # Update the "Select All" checkbox state based on the visible checkboxes
        self.update_select_all_checkbox()

    def update_index_dropdown(self, event=None):
    # """Update the index column dropdown based on the search term."""
        search_term = self.index_search_entry.get().lower()
        filtered_index_columns = [col for col in self.column_names if search_term in col.lower()]
        self.index_column_dropdown['values'] = filtered_index_columns

    def update_select_all_checkbox(self):
        """Update the state of the Select All checkbox based on filtered checkboxes."""
        search_term = self.search_entry.get().lower()
        all_selected = True

        # Only check the visible (filtered) checkboxes
        for col, var in self.checkbox_vars.items():
            if search_term in col.lower():
                if var.get() == 0:  # If any visible checkbox is unchecked, all_selected becomes False
                    all_selected = False
                    break

        # Update the Select All checkbox based on the state of the visible checkboxes
        self.select_all_var.set(1 if all_selected else 0)
 
    def submit(self):
        # Get the columns that are checked
        selected_columns = [col for col, var in self.checkbox_vars.items() if var.get()]

        # Get the selected index column from the dropdown
        selected_index_column = self.index_column_dropdown.get()

        if self.data_frames and selected_columns and selected_index_column:
            # Display selected columns for verification
            if hasattr(self, 'selected_columns_display'):
                self.selected_columns_display.config(text="\n".join(selected_columns))

            # Clear previous selected columns checkboxes (excluding the label)
            for widget in self.selected_columns_frame.winfo_children():
                if widget != self.selected_columns_display:
                    widget.destroy()

            # Create checkboxes for selected columns and bind them
            for col in selected_columns:
                var = tk.IntVar(value=1)  # Start with the checkbox selected
                checkbox = tk.Checkbutton(self.selected_columns_frame, text=col, variable=var)
                checkbox.pack(anchor="w")
                checkbox.bind("<Button-1>", lambda event, col=col: self.toggle_column_visibility(col))
                self.selected_checkbox_vars[col] = var  # Store the variable

            if messagebox.askyesno("Confirm Plot", "Do you want to plot the selected columns?"):
                if not hasattr(self, 'plot_window') or not self.plot_window.winfo_exists():
                    self.plot_initialized = False

                if not self.plot_initialized:
                    # Initialize the plot window and plot the columns
                    self.plot_columns(selected_columns, selected_index_column, self.file_directory)
                    self.plot_initialized = True
                else:
                    # Update the plot with the selected columns
                    self.update_plot(selected_columns)

                # Store the original x-axis limits only the first time
                if not hasattr(self, 'original_x_min') or not hasattr(self, 'original_x_max'):
                    if self.ax_primary is not None:
                        self.original_x_min, self.original_x_max = self.ax_primary.get_xlim()

                # Get the zoomed x-axis limits if they exist
                if self.ax_primary is not None:
                    self.zoomed_x_min, self.zoomed_x_max = self.ax_primary.get_xlim()

                # Ensure the plot zooms according to the stored zoomed limits
                if hasattr(self, 'zoomed_x_min') and hasattr(self, 'zoomed_x_max'):
                    self.ax_primary.set_xlim(self.zoomed_x_min, self.zoomed_x_max)
                    self.fig.canvas.draw_idle()

            else:
                messagebox.showerror("Error", "Please select columns and an index column.")




    def download_zoomed_csv(self):
        """Exports the zoomed data to a CSV file."""
        try:
            if self.zoomed_data is None or self.zoomed_data.empty:
                print("No zoomed data available to export.")
                return

            # Prompt user to save the file
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save CSV File"
            )

            if file_path:
                # Save only the zoomed-in data
                self.zoomed_data.to_csv(file_path, index=False)
                print(f"CSV file saved at: {file_path}")
            else:
                print("File save canceled.")

        except Exception as e:
            print(f"Error while downloading zoomed data: {e}")

    def get_zoomed_x_range(self):
        """Returns the current zoomed x-axis range."""
        # Ensure that the plot has an axes object to work with
        if hasattr(self, 'ax_primary'):
            # Get the current x-axis limits from the axis object
            x_min, x_max = self.ax_primary.get_xlim()
            return x_min, x_max
        else:
            print("Error: Plot axes object not found.")
            return None, None

    def store_initial_x_limits(self):
        """Store the initial x-axis limits when the graph is plotted for the first time."""
        if hasattr(self, 'ax_primary'):
            self.initial_x_limits = self.ax_primary.get_xlim()
            print(f"Initial x-axis limits stored: {self.initial_x_limits}")
        else:
            print("Error: Plot axes object not found.")

    def download_all_Parameter_in_zoomed_csv(self):
        """Exports the full data filtered by the zoomed x-axis range to a CSV file, including all parameters."""
        try:
            # Ensure full data exists (replace with actual variable holding full dataset)
            if self.data is None or self.data.empty:
                print("No data available to export.")
                return

            # Ensure the zoom range (x-axis values) is available
            if hasattr(self, 'zoomed_x_min') and hasattr(self, 'zoomed_x_max'):
                # Filter the full data based on the zoomed x-axis range
                filtered_data = self.data[
                    (self.data['DATETIME'] >= self.zoomed_x_min) & 
                    (self.data['DATETIME'] <= self.zoomed_x_max)
                ]
            else:
                # If no zoom range, use full data
                filtered_data = self.data

            # Prompt user to save the filtered data as CSV
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save CSV File"
            )

            if file_path:
                # Save the filtered data (all parameters) to the CSV file
                filtered_data.to_csv(file_path, index=False)
                print(f"CSV file saved at: {file_path}")
            else:
                print("File save canceled.")

        except Exception as e:
            print(f"Error while downloading filtered data: {e}")

    def plot_columns(self, selected_columns, index_column, custom_x_min=None, custom_x_max=None, retain_zoom=False):
        # Ensure the figure and axes are initialized
        if not hasattr(self, 'fig') or self.fig is None:
            self.fig, self.ax_primary = plt.subplots(figsize=(10, 6))
        elif self.ax_primary is None:
            self.ax_primary = self.fig.add_subplot(111)
        else:
            self.ax_primary.clear()  # Safely clear the previous plot

        self.y_axes = [self.ax_primary]  # Start with primary y-axis only
        self.lines = {}  # Dictionary to store line objects

        # Add a horizontal line at y=0
        self.ax_primary.axhline(y=0, color='black', linestyle='--', linewidth=1, label='y=0')

        # Plot each selected column
        for i, col in enumerate(selected_columns):
            for df in self.data_frames:
                x = pd.to_datetime(df[index_column], errors='coerce').dt.tz_localize(None)
                y = df[col]

                # Check if the DataFrame is empty or if the column doesn't exist
                if df.empty:
                    print(f"Warning: DataFrame is empty for column: {col}")
                    continue
                if index_column not in df.columns or col not in df.columns:
                    print(f"Warning: Column '{index_column}' or '{col}' not found in DataFrame")
                    continue

                # Apply custom x-axis range
                if custom_x_min is not None and custom_x_max is not None:
                    mask = (x >= pd.to_datetime(custom_x_min)) & (x <= pd.to_datetime(custom_x_max))
                    x, y = x[mask], y[mask]

                # Apply condition to filter out MotorSpeed [SA: 02] values greater than 9000
                if col == "MotorSpeed [SA: 02]":
                    print(f"Applying filter to {col}: values greater than 9000 will be excluded.")
                    mask = y <= 9000
                    x, y = x[mask], y[mask]
                    print(f"Filtered x: {x[:5]}")  # Show first 5 x values after filtering
                    print(f"Filtered y: {y[:5]}")  # Show first 5 y values after filtering

                # Debugging: Print x and y values
                print(f"Plotting column: {col}")
                print(f"x: {x[:5]}")  # Show first 5 x values
                print(f"y: {y[:5]}")  # Show first 5 y values

                # Skip if x or y is empty
                if len(x) == 0 or len(y) == 0:
                    print(f"No data to plot for column: {col}")
                    continue

                # Add new secondary axis if needed
                if i > 0:
                    new_ax = self.ax_primary.twinx()
                    new_ax.spines['right'].set_position(('outward', 60 * (i - 1)))
                    self.y_axes.append(new_ax)
                    ax = new_ax
                else:
                    ax = self.ax_primary

                # Plot data
                line, = ax.plot(x, y, label=col, color=plt.cm.viridis(i / len(selected_columns)))
                ax.set_ylabel(f"{col} Values")
                self.lines[col] = line  # Store the line object

                # Adjust limits dynamically
                ax.relim()  # Recompute the limits based on the data
                ax.autoscale_view()  # Autoscale to fit the data

        # Set x-axis label and title
        self.ax_primary.set_xlabel(index_column)
        self.ax_primary.set_title("Data Plot")

        # If custom x-axis limits are given, apply them
        if custom_x_min is not None and custom_x_max is not None:
            self.ax_primary.set_xlim(custom_x_min, custom_x_max)

        # If retain_zoom is True, apply the stored zoom limits
        elif retain_zoom and hasattr(self, 'zoomed_x_min') and hasattr(self, 'zoomed_x_max'):
            self.ax_primary.set_xlim(self.zoomed_x_min, self.zoomed_x_max)

        # Set the X-axis format to Date and Time if applicable
        elif isinstance(self.data_frames[0][index_column].iloc[0], (np.datetime64, pd.Timestamp)):
            self.ax_primary.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
            self.ax_primary.xaxis.set_major_locator(mdates.AutoDateLocator())  # Automatically decide the date ticks
            self.fig.autofmt_xdate()  # Format the X-axis dates nicely

        # Update legends
        self.update_legends()

        # Add interactive data cursors (continuous mode)
        cursor = mplcursors.cursor(self.fig, hover=True)

        # Disable annotations from being shown
        cursor.connect("add", lambda sel: sel.annotation.set_visible(False))  # Hide annotations when hovering

        # # Create a vertical line for live tracking at the first x-axis limit
        # initial_x = None
        # for df in self.data_frames:
        #     if not df.empty and index_column in df.columns:
        #         initial_x = df[index_column].values[0]
        #         break  # Use the first valid x-value

        # if initial_x is not None and self.influx_var.get() == "yes":
        #     self.vertical_line = self.ax_primary.axvline(x=initial_x, color='red', linestyle='--', linewidth=1)
        # else:
        #     self.vertical_line = self.ax_primary.axvline(x=0, color='red', linestyle='--', linewidth=1)  # Fallback

        # # Debugging: Print the initial x-value
        # print(f"Initial vertical line position: {initial_x if initial_x is not None else 0}")

        # Tkinter window for displaying live values
        live_window = tk.Toplevel(self.root)
        live_window.title("Live Cursor Data")
        live_window.geometry("300x200")

        label_x = tk.Label(live_window, text="X-axis value: N/A")
        label_x.pack(padx=10, pady=5)

        label_y = {}
        for col in selected_columns:
            label_y[col] = tk.Label(live_window, text=f"{col}: N/A")
            label_y[col].pack(padx=10, pady=5)

        # Create a 'plus' symbol that follows the cursor
        plus_marker, = self.ax_primary.plot([], [], '|', color='red', markersize=1000, label='Cursor')  # '+' marker

        def update_live_values(sel):
            """Update live values whenever the cursor hovers over the plot."""
            if sel.artist is not None:
                # Retrieve X and Y values directly from the cursor selection
                x_val, y_val = sel.target

                # Update vertical line position
                # self.vertical_line.set_xdata([x_val, x_val])  # Update only x data of the vertical line

                # Check if the X data is in datetime format
                x_data = sel.artist.get_xdata()
                x_data = np.array(x_data)
                if np.issubdtype(x_data.dtype, np.datetime64):
                    # Convert x_data to Matplotlib's numeric date format for comparison
                    numeric_x_data = mdates.date2num(x_data)
                    closest_index = np.argmin(np.abs(numeric_x_data - x_val))
                    # Convert x_val to readable datetime format
                    x_val = mdates.num2date(x_val).strftime('%Y-%m-%d %H:%M:%S')
                    x_label_text = f"X-axis value: {x_val}"
                else:
                    # For non-datetime X values
                    closest_index = np.argmin(np.abs(x_data - x_val))

                # Update the X-axis label in the live window
                label_x.config(text=f"X-axis value: {x_val}")

                # Update all Y-axis values for the given X position
                for col, line in self.lines.items():
                    # Extract the Y data for the current line
                    y_data = line.get_ydata()

                    # Retrieve the Y value at the closest X index
                    y_val = y_data[closest_index]

                    # Update the Y-axis label with the parameter name and value
                    label_y[col].config(text=f"{col}: {y_val:.2f}")

                    # Ensure the mplcursor annotation shows the correct parameter name
                    sel.annotation.set_text(f"X: {x_val}\n{col}: {y_val:.2f}")

                # Redraw the plot to reflect the updated vertical line
                self.fig.canvas.draw_idle()

                # Move the 'plus' symbol to the cursor position
                plus_marker.set_data([x_val], [y_val])  # Update marker position

        # Connect the update function to the cursor hover event
        cursor.connect("add", update_live_values)

        # Automatically close live window with the plot
        def close_live_window(_):
            live_window.destroy()  # Destroy live window when plot closes

        # Attach the closing behavior to the figure's close event
        self.fig.canvas.mpl_connect('close_event', close_live_window)

        # Store current x-axis limits after zoom
        cursor.connect("add", self.store_zoom_limits)

        # Setup the canvas and toolbar
        self.setup_canvas_toolbar()

        # Capture zoomed values dynamically
        def on_zoom(event):
            """Callback to capture zoomed data."""
            if event.name == 'draw_event':  # Triggered after a zoom or pan
                # Get the current zoomed x-axis range
                x_min, x_max = self.ax_primary.get_xlim()
                x_min = mdates.num2date(x_min).replace(tzinfo=None)
                x_max = mdates.num2date(x_max).replace(tzinfo=None)

                print(f"Zoomed Range: {x_min} to {x_max}")  # Debugging output

                # Store the zoomed x-axis limits
                self.zoomed_x_min, self.zoomed_x_max = x_min, x_max

                # Collect data for all visible parameters within the zoomed range
                zoomed_data_frames = []

                for df in self.data_frames:
                    x = pd.to_datetime(df[index_column], errors='coerce').dt.tz_localize(None)
                    mask = (x >= x_min) & (x <= x_max)

                    # Filter the DataFrame for zoomed range and only include visible parameters
                    filtered_df = df.loc[mask, [index_column] + list(self.lines.keys())]

                    if not filtered_df.empty:
                        zoomed_data_frames.append(filtered_df)

                # Combine all filtered data
                if zoomed_data_frames:
                    self.zoomed_data = pd.concat(zoomed_data_frames, ignore_index=True)
                else:
                    self.zoomed_data = pd.DataFrame()  # No zoomed data available

        # Connect the zoom callback
        self.fig.canvas.mpl_connect('draw_event', on_zoom)

        # Store the original x-axis limits
        self.original_xlim = self.ax_primary.get_xlim()

        # Add a button callback to reset the zoom
        def reset_zoom(*args):
            self.ax_primary.set_xlim(self.original_xlim)
            self.fig.canvas.draw_idle()
            self.store_initial_x_limits()  # Store initial x-axis limits after resetting zoom

        # Connect the button callback
        if not hasattr(self, 'toolbar') or not self.toolbar.winfo_exists():
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
            self.toolbar.update()
            self.toolbar.home = reset_zoom

        # Override the home button in the toolbar
        def override_home():
            reset_zoom()
        self.toolbar.home = override_home


    def store_zoom_limits(self, sel):
        """Store the current zoom limits when the user zooms in/out."""
        self.zoomed_x_min, self.zoomed_x_max = self.ax_primary.get_xlim()
        print(f"Zoomed x-axis limits stored: {self.zoomed_x_min} to {self.zoomed_x_max}")

    def save_plot_as_html(self):
        selected_columns = [col for col, var in self.checkbox_vars.items() if var.get()]
        selected_index_column = self.index_column_dropdown.get()

        if not selected_columns or not selected_index_column:
            messagebox.showerror("Error", "Please select columns and an index column.")
            return

        # Prompt the user to select a folder and name the file
        save_path = filedialog.asksaveasfilename(defaultextension='.html', filetypes=[("HTML Files", "*.html")])
        if not save_path:
            return

        # Set the selected column as index
        if selected_index_column in selected_columns:
            self.data.set_index(selected_index_column, inplace=True)
            selected_columns.remove(selected_index_column)
        else:
            self.data.set_index(selected_index_column, inplace=True)

        # Use zoomed data if available, otherwise fall back to the full data
        if hasattr(self, 'zoomed_data') and not self.zoomed_data.empty:
            data_to_plot = self.zoomed_data
        else:
            data_to_plot = self.data

        # Plot using Plotly
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add trace for each selected column
        for i, col in enumerate(selected_columns):
            # Assign y-axis based on index (e.g., first column to 'y', second to 'y2', etc.)
            axis_name = f'y{i+1}' if i < 2 else f'y{i+2}'  # Primary ('y1') and secondary ('y2') for first two, then others
            fig.add_trace(go.Scatter(x=data_to_plot.index, y=data_to_plot[col], name=col), secondary_y=(i > 0))

        # Apply zoomed x-axis limits if available
        if hasattr(self, 'zoomed_range') and self.zoomed_range:
            x_min, x_max = self.zoomed_range
            fig.update_xaxes(range=[x_min, x_max])

        # Add opacity modification dropdown
        fig.update_layout(
            title=f'Plot_{self.input_file_name}',
            xaxis_title=selected_index_column,
            height=1000,
            yaxis=dict(title='Primary Y-Axis', showgrid=False),
            yaxis2=dict(title='Secondary Y-Axis', overlaying='y', side='right', showgrid=False),  # Overlay for secondary axis
            updatemenus=[
                {
                    'buttons': [
                        {
                            'args': [{'opacity': 0.2}],  # Low opacity
                            'label': 'Clarity- 20%',
                            'method': 'restyle'
                        },
                        {
                            'args': [{'opacity': 0.4}],  # Medium opacity
                            'label': '40%',
                            'method': 'restyle'
                        },
                        {
                            'args': [{'opacity': 0.6}],  # Default opacity
                            'label': '60%',
                            'method': 'restyle'
                        },
                        {
                            'args': [{'opacity': 0.8}],  # Higher opacity
                            'label': '80%',
                            'method': 'restyle'
                        },
                        {
                            'args': [{'opacity': 1}],  # Full opacity
                            'label': '100%',
                            'method': 'restyle'
                        }
                    ],
                    'direction': 'down',  # Dropdown direction
                    'showactive': True,
                    'x': 1.05,  # X position of dropdown
                    'xanchor': 'left',
                    'y': 1.20,
                    'yanchor': 'top'
                }
            ]
        )

        fig.update_xaxes(tickformat='%H:%M:%S')

        # Save the plot as an HTML file
        os.makedirs(save_path, exist_ok=True)
        graph_path = os.path.join(save_path, f'Dynamic_plot_{self.input_file_name}.html')  # Updated file name
        fig.write_html(graph_path)
        print(f"Plot saved at: {graph_path}")

        # Automatically open the saved plot in the default web browser
        webbrowser.open('file://' + os.path.realpath(graph_path))  # Open the HTML file


    def toggle_column_visibility(self, column):
        """Toggle visibility of a plot line and its associated y-axis."""
        line = self.lines[column]
        is_visible = line.get_visible()
        line.set_visible(not is_visible)  # Toggle line visibility

        # Ensure primary axis stays visible, especially the x-axis
        if column in self.lines:
            # Check if any line on the primary y-axis is visible
            any_visible_primary = any(l.get_visible() for l in self.ax_primary.get_lines())
            self.ax_primary.set_visible(any_visible_primary or True)  # Ensure primary y-axis stays visible

            # Explicitly keep the x-axis visible
            self.ax_primary.xaxis.set_visible(True)

        # Find which secondary y-axis the line is associated with (if any)
        for ax in self.y_axes[1:]:
            if line in ax.get_lines():
                # Toggle visibility of secondary y-axis only if any line is visible
                ax.set_visible(any(l.get_visible() for l in ax.get_lines()))

        # Refresh the legend and canvas
        self.update_legends()
        self.fig.canvas.draw_idle()



    def update_legends(self):
        """Update legends to show only visible lines."""
        handles, labels = [], []
        for ax in self.y_axes:
            for line in ax.get_lines():
                if line.get_visible():
                    handles.append(line)
                    labels.append(line.get_label())
        self.ax_primary.legend(handles, labels, loc='upper left')

    def setup_canvas_toolbar(self):
        # Ensure plot_frame exists and is properly initialized
        if not hasattr(self, 'plot_window') or not self.plot_window.winfo_exists():
            self.plot_window = tk.Toplevel(self.root)  # Create the plot window if it doesn't exist

        if not hasattr(self, 'plot_frame') or not self.plot_frame.winfo_exists():
            self.plot_frame = tk.Frame(self.plot_window)
            self.plot_frame.pack(fill=tk.BOTH, expand=True)

        # Remove old canvas if it exists
        if hasattr(self, 'canvas') and isinstance(self.canvas, FigureCanvasTkAgg):
            self.canvas.get_tk_widget().destroy()

        # Create new canvas and associate it with the frame
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()  # Draw the initial plot

        # Pack the canvas (ensure it's only packed once)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Optionally, create and pack the toolbar (if needed)
        # toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        # toolbar.update()
        # toolbar.pack(fill=tk.X)  # Pack toolbar along the x-axis

        # Ensure the canvas is packed properly after the toolbar (if toolbar is included)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def update_plot(self, selected_columns, retain_zoom=False):
        # Optionally save zoom state if required
        if retain_zoom:
            xlim = self.ax_primary.get_xlim()  # Store x-axis limits separately
            ylim_primary = self.ax_primary.get_ylim()
            ylim_secondary = [ax.get_ylim() for ax in self.y_axes[1:]]

        # Clear only lines without removing axes, to avoid losing state
        for line in self.ax_primary.get_lines():
            line.remove()
        for ax in self.y_axes[1:]:
            for line in ax.get_lines():
                line.remove()

        # Re-plot selected columns
        for i, col in enumerate(selected_columns):
            for df in self.data_frames:
                x = df[self.index_column_dropdown.get()]
                y = df[col]

                # Reuse or create y-axes
                if i >= len(self.y_axes):
                    new_ax = self.ax_primary.twinx()
                    new_ax.spines['right'].set_position(('outward', 60 * i))
                    self.y_axes.append(new_ax)
                    ax = new_ax
                else:
                    ax = self.y_axes[i]

                # Plot on the appropriate axis
                line, = ax.plot(x, y, label=col, color=plt.cm.viridis(i / len(selected_columns)))
                ax.set_ylabel(f"{col} Values")
                self.lines[col] = line  # Update lines dictionary

        # Set x-axis label and title
        self.ax_primary.set_xlabel(self.index_column_dropdown.get())
        self.ax_primary.set_title("Updated Data Plot")

        # Restore x-axis zoom if applicable
        if retain_zoom:
            self.ax_primary.set_xlim(xlim)  # Restore x-axis limits
            for ax, ylim in zip(self.y_axes, [ylim_primary] + ylim_secondary):
                ax.set_ylim(ylim)  # Restore y-axis limits

        # Update legends
        self.update_legends()

        # Redraw the canvas
        self.fig.canvas.draw_idle()



# Create the application window
if __name__ == "__main__":
    root = tk.Tk()
    app = PlotApp(root)
    root.mainloop()