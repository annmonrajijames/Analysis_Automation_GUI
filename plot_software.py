import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import mplcursors  # Import mplcursors
from datetime import datetime, timedelta

# Tkinter GUI Setup
class PlotApp:
    def __init__(self, root):
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

        # # Display Selected Columns
        # self.selected_columns_label = tk.Label(self.control_frame, text="Selected Columns:")
        # self.selected_columns_label.pack(pady=5)
        # self.selected_columns_display = tk.Label(self.control_frame, text="", wraplength=400, justify="left")
        # self.selected_columns_display.pack(pady=5)

        # Frame for checkboxes of selected columns
        self.selected_columns_frame = tk.Frame(self.control_frame)
        self.selected_columns_frame.pack(pady=5)

        # Submit Button
        self.submit_button = tk.Button(self.control_frame, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)

        

   
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
 
                else:
                    raise ValueError("Unsupported file format")
 
                # Drop any fully empty rows
                self.data.dropna(how='all', inplace=True)
#                 print("before")
                # # Handle Serial Number addition if missing
                # if 'Serial Number' not in self.data.columns:
                #     self.data['Serial Number'] = range(1, len(self.data) + 1)
 
                if self.influx_var.get() == "yes":
                    messagebox.showinfo("Influx Data", "Influx data is given as input")
                    # Handle Time conversion if present
                    print("Input data is Influx data")

                

                #For converting Datetime timestamp to Time format
                    if 'DATETIME' not in self.data.columns:  #if 'DATETIME' not in column Present 
                        print("DATETIME column not present")
                        self.data['DATETIME'] = self.data['Time']
                    
                    else:                                                                                   #if 'DATETIME' column Present 
                        self.data['DATETIME'] = pd.to_numeric(self.data['DATETIME'], errors='coerce')
                
                        # Drop or handle NaN values
                        self.data = self.data.dropna(subset=['DATETIME'])
                    
                        # Convert the Unix timestamps to datetime
                        self.data['DATETIME'] = pd.to_datetime(self.data['DATETIME'], unit='s')
                    
                        # Print the converted DATETIME column
                        # data['DATETIME'] = pd.to_datetime(data['DATETIME'])

                        self.data['DATETIME'] = self.data['DATETIME'] + pd.to_timedelta('5h30m')

                        print("GPS DATA AVAILABLE")

                        # Store data for each file in the list
                    self.data_frames.append(self.data)
    
                    # Extract the column names
                    self.column_names = self.data.columns.tolist()
    
                    # Update the checkboxes with the full list of columns
                    self.update_checkboxes()
                    print(col.lower() for col in self.column_names)
                    # filtered_index_columns = [col for col in self.column_names if col.lower() in ['serial number','datetime']]
                    filtered_index_columns = [col for col in self.column_names if col.lower() in ['datetime']]

                    # Populate the dropdown with filtered column names for index selection
                    self.index_column_dropdown['values'] = filtered_index_columns

#  #######################
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
    
                    # filtered_index_columns = [col for col in self.column_names if col.lower() in ['serial number']]
                    # Populate the dropdown with all column names for index selection
                    self.index_column_dropdown['values'] = self.column_names
               
                #Filter only 'Serial Number' and 'Time' columns for index selection
                

                # filtered_index_columns = [col for col in self.column_names if col.lower() in ['datetime']]
 
                
 
                print("Columns available for plotting:", self.column_names)
            except Exception as e:
                print(f"Error loading data: {e}")

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
            # Clear previous selected columns checkboxes
            for widget in self.selected_columns_frame.winfo_children():
                widget.destroy()

            # Create checkboxes for selected columns and bind them
            for col in selected_columns:
                var = tk.IntVar(value=1)  # Start with the checkbox selected
                checkbox = tk.Checkbutton(self.selected_columns_frame, text=col, variable=var)
                checkbox.pack(anchor="w")
                checkbox.bind("<Button-1>", lambda event, col=col: self.toggle_column_visibility(col))
                self.selected_checkbox_vars[col] = var  # Store the variable

            if not hasattr(self, 'plot_window') or not self.plot_window.winfo_exists():
                # Create a new plot window if it does not exist
                self.plot_window = tk.Toplevel(self.root)
                self.plot_window.title("Data Plot")
                self.plot_window.geometry("800x600")  # Set the window size for the plot

                # Initialize plot components
                self.fig = None
                self.ax_primary = None
                self.ax_secondary = None
                self.ax_tertiary = None
                self.plot_initialized = False

            # Proceed to plot the columns
            self.plot_columns(selected_columns, selected_index_column, self.file_directory)
        else:
            messagebox.showerror("Error", "Please select columns and an index column.")

    def plot_columns(self, selected_columns, index_column, file_directory):
        # Clear previous plots if necessary
        if hasattr(self, 'fig') and self.fig:
            plt.close(self.fig)  # Close the previous figure

        # Create a new figure and primary axis if not already initialized
        if self.fig is None:
            self.fig, self.ax_primary = plt.subplots(figsize=(10, 6))
            self.y_axes = [self.ax_primary]  # Start with primary y-axis only
            self.lines = {}  # Dictionary to store line objects
        else:
            # Clear existing lines from the axes without removing the axes
            for line in self.ax_primary.get_lines():
                line.remove()
            for ax in self.y_axes[1:]:
                for line in ax.get_lines():
                    line.remove()

        # Plot each selected column
        for i, col in enumerate(selected_columns):
            for df in self.data_frames:
                x = df[index_column]
                y = df[col]

                # Add new secondary axis if needed
                if i > 0:
                    new_ax = self.ax_primary.twinx()
                    new_ax.spines['right'].set_position(('outward', 60 * (i - 1)))
                    self.y_axes.append(new_ax)
                    ax = new_ax
                else:
                    ax = self.ax_primary

                line, = ax.plot(x, y, label=col, color=plt.cm.viridis(i / len(selected_columns)))
                ax.set_ylabel(f"{col} Values")
                self.lines[col] = line  # Store the line object

        # Set x-axis label and title
        self.ax_primary.set_xlabel(index_column)
        self.ax_primary.set_title("Data Plot")

        # Update legends
        self.update_legends()

        # Add interactive data cursors
        mplcursors.cursor(hover=True)

        # Setup the canvas and toolbar
        self.setup_canvas_toolbar()

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
        if not hasattr(self, 'plot_frame') or not self.plot_frame.winfo_exists():
            self.plot_frame = tk.Frame(self.plot_window)
            self.plot_frame.pack(fill=tk.BOTH, expand=True)

        # Remove old canvas
        if hasattr(self, 'canvas') and isinstance(self.canvas, FigureCanvasTkAgg):
            self.canvas.get_tk_widget().destroy()

        # Create new canvas and toolbar
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()  # Draw the initial plot

        # Pack canvas (only once)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Create and pack the toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        toolbar.update()
        toolbar.pack(fill=tk.X)  # Pack toolbar along the x-axis

        # Ensure canvas is correctly packed after the toolbar
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