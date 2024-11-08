import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import mplcursors  # Import mplcursors
<<<<<<< HEAD
=======
from datetime import datetime, timedelta
>>>>>>> 983d8280db6ab5f94918c4eae79a34543bcad18b

# Tkinter GUI Setup
class PlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Plotter")

<<<<<<< HEAD
        # Main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Control frame on the left
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.grid(row=0, column=0, sticky="ns")

        # Plot frame on the right
        self.plot_frame = tk.Frame(self.main_frame)
        self.plot_frame.grid(row=0, column=1, sticky="nsew")

        # Make the plot frame expand more
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
=======
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
>>>>>>> 983d8280db6ab5f94918c4eae79a34543bcad18b

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

<<<<<<< HEAD
=======
        # Bind mouse wheel scrolling to the checkboxes
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Checkbox for Select All
        self.select_all_var = tk.IntVar()
        self.select_all_checkbox = tk.Checkbutton(self.control_frame, text="Select All", variable=self.select_all_var, command=self.toggle_select_all)
        self.select_all_checkbox.pack(pady=5)

>>>>>>> 983d8280db6ab5f94918c4eae79a34543bcad18b
        # Dropdown for Index Column Selection
        self.index_label = tk.Label(self.control_frame, text="Select Index Column:")
        self.index_label.pack(pady=5)
        self.index_column_dropdown = ttk.Combobox(self.control_frame, state="readonly")
        self.index_column_dropdown.pack(pady=5)

        # Display Selected Columns
        self.selected_columns_label = tk.Label(self.control_frame, text="Selected Columns:")
        self.selected_columns_label.pack(pady=5)
        self.selected_columns_display = tk.Label(self.control_frame, text="", wraplength=400, justify="left")
        self.selected_columns_display.pack(pady=5)

<<<<<<< HEAD
=======
        # Frame for checkboxes of selected columns
        self.selected_columns_frame = tk.Frame(self.control_frame)
        self.selected_columns_frame.pack(pady=5)

>>>>>>> 983d8280db6ab5f94918c4eae79a34543bcad18b
        # Submit Button
        self.submit_button = tk.Button(self.control_frame, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)

<<<<<<< HEAD
        # Reset Button
        self.reset_button = tk.Button(self.control_frame, text="Reset View", command=self.reset_view)
        self.reset_button.pack(pady=10)
=======
        # Final Submit Button
        self.index_label = tk.Label(self.control_frame, text="After Doing, Modification in the existing plot(Click 'Re-set' Button for 'submit'):")
        self.index_label.pack(pady=2)
        self.final_submit_button = tk.Button(self.control_frame, text="Re-set", command=self.final_submit)
        self.final_submit_button.pack(pady=10)
>>>>>>> 983d8280db6ab5f94918c4eae79a34543bcad18b

        # To hold the extracted column names and their corresponding checkboxes
        self.column_names = []
        self.checkbox_vars = {}  # To store the checkbox variables for each column
        self.data_frames = []  # List to store data from multiple files
        self.file_directory = ""  # Directory of the files
<<<<<<< HEAD
        self.zoomed_dataframe = None  # To store the zoomed data
=======

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
>>>>>>> 983d8280db6ab5f94918c4eae79a34543bcad18b

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
       
        # Define a function to detect valid header row
        def detect_header_row(df):
            # Check the first two rows to determine which contains the headers
            for i in range(2):
                row = df.iloc[i]
                if all(isinstance(x, str) for x in row):  # Check if all entries are strings (likely headers)
                    return i  # Return the index of the row containing headers
            return 0  # Default to first row if no string-based header is found

        # Load the file based on its extension
        if os.path.isfile(file_path):
            try:
                if file_path.endswith('.csv'):
                    # Load the first few rows to check for header location
                    df = pd.read_csv(file_path, nrows=5, skip_blank_lines=True)

                    # Detect where the header row is
                    header_row = detect_header_row(df)

                    # Reload the CSV using the detected header row
                    self.data = pd.read_csv(file_path, header=header_row, skip_blank_lines=True)

                elif file_path.endswith('.xlsx'):
                    # Load the first few rows to check for header location
                    df = pd.read_excel(file_path, nrows=5, skip_blank_lines=True)

                    # Detect where the header row is
                    header_row = detect_header_row(df)

                    # Reload the Excel file using the detected header row
                    self.data = pd.read_excel(file_path, header=header_row, skip_blank_lines=True)

                else:
                    raise ValueError("Unsupported file format")

                # Drop any fully empty rows
                self.data.dropna(how='all', inplace=True)
<<<<<<< HEAD

=======
                print("before")
>>>>>>> 983d8280db6ab5f94918c4eae79a34543bcad18b
                # Handle Serial Number addition if missing
                if 'Serial Number' not in self.data.columns:
                    self.data['Serial Number'] = range(1, len(self.data) + 1)

                # Handle Time conversion if present
                print("after")
                print(self.data['Serial Number'].iloc[0])
                if 'Time' in self.data.columns:
                    try:
                        self.data['Time'] = pd.to_datetime(self.data['Time'], errors='coerce')
                        # self.data['Time'] = self.data['Time'].astype(str)
                        
                    except Exception as e:
                        print(f"Error parsing Time column: {e}")
<<<<<<< HEAD

=======
 
 #######################For converting Datetime timestamp to Time format
                print("Initial")
                if 'DATETIME' not in self.data.columns:  #if 'DATETIME' not in column Present 
                    # start_time_str = '01-08-24 14:16:00'  # Update this with your actual start time
                    start_time_str = self.data['Creation Time'].iloc[0]  # Update this with your actual start time
                    # Parse the time, defaulting to ":00" if seconds are missing
                    start_time = datetime.strptime(start_time_str, '%d-%m-%y %H:%M')
                    print("Start_time--->",start_time)

                    # Function to convert fractional seconds to hh:mm:ss format
                    def convert_to_hhmmss(row, start_time):
                        # Calculate the time in seconds
                        seconds = row['Time'] 
                        # Add these seconds to the start time
                        new_time = start_time + timedelta(seconds=seconds)
                        # Return the time in 'dd-mm-yy hh:mm:ss' format
                        return new_time.strftime('%d-%m-%y %H:%M:%S')

                    # Apply the function to create a new column
                    self.data['DATETIME'] = self.data.apply(convert_to_hhmmss, start_time=start_time, axis=1)

                    self.data['DATETIME'] = pd.to_datetime(self.build_uidata['DATETIME'])


                    self.data = self.data.dropna(subset=['DATETIME'])
                
                    self.data['DATETIME'] = pd.to_datetime(self.data['DATETIME'], unit='s')
                

                    self.data['DATETIME'] = pd.to_datetime(self.data['DATETIME'])

                    print("GPS DATA NOT AVAILABLE , SO USED CREATION TIME TO CALCULATE DATETIME")

                
                else:    
                    print("Final")                                                                                   #if 'DATETIME' column Present 
                    self.data['DATETIME'] = pd.to_numeric(self.data['DATETIME'], errors='coerce')
            
                    # Drop or handle NaN values
                    self.data = self.data.dropna(subset=['DATETIME'])
                
                    # Convert the Unix timestamps to datetime
                    self.data['DATETIME'] = pd.to_datetime(self.data['DATETIME'], unit='s')
                
                    # Print the converted DATETIME column
                    # data['DATETIME'] = pd.to_datetime(data['DATETIME'])

                    self.data['DATETIME'] = self.data['DATETIME'] + pd.to_timedelta('5h30m')

                    print("GPS DATA AVAILABLE")

 #######################
>>>>>>> 983d8280db6ab5f94918c4eae79a34543bcad18b
                # Store data for each file in the list
                self.data_frames.append(self.data)

                # Extract the column names
                self.column_names = self.data.columns.tolist()

                # Update the checkboxes with the full list of columns
                self.update_checkboxes()

                # Filter only 'Serial Number' and 'Time' columns for index selection
<<<<<<< HEAD
                filtered_index_columns = [col for col in self.column_names if col.lower() in ['serial number', 'time']]

=======
                # filtered_index_columns = [col for col in self.column_names if col.lower() in ['serial number', 'datetime']]

                filtered_index_columns = [col for col in self.column_names if col.lower() in ['datetime']]
 
>>>>>>> 983d8280db6ab5f94918c4eae79a34543bcad18b
                # Populate the dropdown with filtered column names for index selection
                self.index_column_dropdown['values'] = filtered_index_columns

                print("Columns available for plotting:", self.column_names)
            except Exception as e:
                print(f"Error loading data: {e}")

    def update_checkboxes(self, event=None):
        # Get the search query
        search_query = self.search_entry.get().lower()

        # Filter the column names based on the search query
        filtered_columns = [col for col in self.column_names if search_query in col.lower()]

        # Clear the current checkboxes
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Add checkboxes for the filtered columns
        for col in filtered_columns:
            # Retain the checkbox state using self.checkbox_vars
            if col not in self.checkbox_vars:
                self.checkbox_vars[col] = tk.BooleanVar()

            cb = tk.Checkbutton(self.scrollable_frame, text=col, variable=self.checkbox_vars[col])
            cb.pack(anchor='w')

    def submit(self):
        selected_columns = [col for col, var in self.checkbox_vars.items() if var.get()]
    
        # Get the selected index column from the dropdown
        selected_index_column = self.index_column_dropdown.get()
    
        if self.data_frames and selected_columns and selected_index_column:
            # Display selected columns for verification
            self.selected_columns_display.config(text="\n".join(selected_columns))
<<<<<<< HEAD
    
=======

            # Clear previous selected columns checkboxes
            for widget in self.selected_columns_frame.winfo_children():
                widget.destroy()

            # Create checkboxes for selected columns
            self.selected_checkbox_vars = {}
            for col in selected_columns:
                var = tk.IntVar(value=1)
                checkbox = tk.Checkbutton(self.selected_columns_frame, text=col, variable=var)
                checkbox.pack(anchor="w")
                self.selected_checkbox_vars[col] = var

>>>>>>> 983d8280db6ab5f94918c4eae79a34543bcad18b
            # Ask for confirmation before plotting
            if messagebox.askyesno("Confirm Plot", "Do you want to plot the selected columns?"):
                # Use zoomed_dataframe if it exists, otherwise use the original data
                if self.zoomed_dataframe is not None:
                    data_to_plot = self.zoomed_dataframe
                    print("Using zoomed_dataframe for plotting.")
                else:
                    data_to_plot = self.data_frames[0]
                    print("Using original data for plotting.")
    
                # Plot the selected columns with the selected index
                self.plot_columns(data_to_plot, selected_columns, selected_index_column, self.file_directory)

    def plot_columns(self, data, columns, index_column, save_path):
        fig, ax_primary = plt.subplots(figsize=(10, 6))

        # Create secondary and tertiary y-axes
        ax_secondary = ax_primary.twinx()
        ax_tertiary = ax_primary.twinx()
        ax_tertiary.spines["right"].set_position(("outward", 25))  # Move it outward

        ax_primary.set_ylabel("Primary Axis (Y1)", color='b')
        ax_secondary.set_ylabel("Secondary Axis (Y2)", color='g')
        ax_tertiary.set_ylabel("Tertiary Axis (Y3)", color='r')

        # Define a color palette
        color_palette = plt.cm.get_cmap('tab10', len(columns))  # Use a colormap with a specific number of colors

        # Store the lines for toggling later
        all_lines = []

        # Determine the x-axis based on the selected index column
        if index_column == 'Serial Number':
            x_axis = np.arange(len(data))  # Use row numbers as the x-axis
            ax_primary.set_xlabel("Serial Number")
        elif index_column == 'Time':
            if not pd.api.types.is_datetime64_any_dtype(data['Time']):
                data['Time'] = pd.to_datetime(data['Time'], errors='coerce')
            x_axis = data['Time']
            ax_primary.set_xlabel("Time")
        else:
            raise ValueError(f"Unknown index column: {index_column}")

<<<<<<< HEAD
        # Assign columns to the different y-axes
        for j, col in enumerate(columns):
            if col in data.columns:
                numeric_data = pd.to_numeric(data[col], errors='coerce')

                # Check if there are valid numeric values to plot
                if numeric_data.notna().any():
                    trace_name = f"{col}"

                    # Get a unique color for each parameter
                    color = color_palette(j % len(color_palette.colors))

                    # Plot on the primary, secondary, or tertiary y-axis based on index
                    if j % 3 == 0:  # First column goes on the primary y-axis
                        line, = ax_primary.plot(x_axis, numeric_data, label=trace_name, color=color, picker=True)
                    elif j % 3 == 1:  # Second column goes on the secondary y-axis
                        line, = ax_secondary.plot(x_axis, numeric_data, label=trace_name, color=color, picker=True)
                    elif j % 3 == 2:  # Third column goes on the tertiary y-axis
                        line, = ax_tertiary.plot(x_axis, numeric_data, label=trace_name, color=color, picker=True)
                   
                    all_lines.append(line)  # Store the line for toggling later
=======
    def final_submit(self):
        # Get the columns that are checked in the selected columns frame
        final_selected_columns = [col for col, var in self.selected_checkbox_vars.items() if var.get()]

        if final_selected_columns:
            # Display final selected columns for verification
            self.selected_columns_display.config(text="\n".join(final_selected_columns))

            # Proceed with the final selected columns
            messagebox.showinfo("Final Selection", f"Final selected columns: {', '.join(final_selected_columns)}")

            # Update the plot with the final selected columns without resetting zoom
            self.update_plot(final_selected_columns, retain_zoom=True)
        else:
            messagebox.showerror("Error", "Please select at least one column.")


 
    def plot_columns(self, selected_columns, index_column, file_directory):
        # Clear previous plots if necessary
        if hasattr(self, 'fig') and self.fig:
            plt.close(self.fig)

        # Create a new figure and primary axis
        self.fig, self.ax_primary = plt.subplots(figsize=(10, 6))
        self.y_axes = [self.ax_primary]  # Start with primary y-axis only

        # Plot each selected column
        for i, col in enumerate(selected_columns):
            for df in self.data_frames:
                x = df[index_column]  # X-axis data
                y = df[col]

                # Add new secondary axis if needed
                if i > 0:
                    new_ax = self.ax_primary.twinx()
                    new_ax.spines['right'].set_position(('outward', 60 * (i - 1)))
                    self.y_axes.append(new_ax)
                    ax = new_ax
                else:
                    ax = self.ax_primary

                ax.plot(x, y, label=col, color=plt.cm.viridis(i / len(selected_columns)))
                ax.set_ylabel(f"{col} Values")

        # Set x-axis label and title
        self.ax_primary.set_xlabel(index_column)
        self.ax_primary.set_title("Data Plot")

        # Update legends
        handles, labels = self.ax_primary.get_legend_handles_labels()
        for ax in self.y_axes[1:]:
            h, l = ax.get_legend_handles_labels()
            handles.extend(h)
            labels.extend(l)

        self.ax_primary.legend(handles, labels, loc='upper left')
>>>>>>> 983d8280db6ab5f94918c4eae79a34543bcad18b

                else:
                    print(f"Column '{col}' contains no valid numeric data after conversion.")
            else:
                print(f"Column '{col}' not found in data")

        ax_primary.set_title("Comparison Plot with Multiple Y-Axes")

        # Combine legends from all axes
        lines, labels = ax_primary.get_legend_handles_labels()
        lines2, labels2 = ax_secondary.get_legend_handles_labels()
        lines3, labels3 = ax_tertiary.get_legend_handles_labels()
        legend = ax_primary.legend(lines + lines2 + lines3, labels + labels2 + labels3)

        # Set the picker on the legend's text and line (to make them clickable)
        for legline in legend.get_lines():
            legline.set_picker(True)  # Enable picker on legend lines
       
        for legtext in legend.get_texts():
            legtext.set_picker(True)  # Enable picker on legend text

        # Function to toggle the line visibility when legend is clicked
        def on_pick(event):
            # Check if the picked object is a legend line or legend text
            for legend_line in legend.get_lines():
                if event.artist == legend_line:
                    # Find the corresponding plot line by matching labels
                    label = legend_line.get_label()
                    for line in all_lines:
                        if line.get_label() == label:
                            # Toggle the line's visibility
                            visible = not line.get_visible()
                            line.set_visible(visible)
                            # Adjust the legend line's transparency
                            legend_line.set_alpha(1.0 if visible else 0.2)
                            fig.canvas.draw()

        # Connect the pick event to the toggle function
        fig.canvas.mpl_connect('pick_event', on_pick)

        # Add mplcursors for interactive annotations
        mplcursors.cursor(hover=True)

<<<<<<< HEAD
        # Save the plot as an image file
        os.makedirs(save_path, exist_ok=True)
        graph_path = os.path.join(save_path, 'Generated_Plot.png')
        plt.savefig(graph_path)
        print(f"Plot saved at: {graph_path}")

        # Display the plot in the Tkinter application
        self.display_plot(fig, ax_primary)

    def display_plot(self, fig, legend):
        print("<-----------------kamal--------------->")
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self.plot_frame)
        toolbar.update()
        canvas._tkcanvas.pack(fill=tk.BOTH, expand=True)

        # Connect the pick event to toggle visibility
        print("1")
        fig.canvas.mpl_connect('pick_event', self.toggle_visibility)

        # Connect the zoom event to capture the zoomed area
        print("2")
        fig.canvas.mpl_connect('button_release_event', self.on_zoom)

        print("3")
        # Connect the legend click event to toggle visibility
        for legend_line, original_line in zip(legend.get_lines(), fig.axes[0].get_lines()):
            legend_line.set_picker(True)
            legend_line.set_pickradius(5)
            legend_line.original_line = original_line

        fig.canvas.mpl_connect('pick_event', self.toggle_legend_visibility)

    def toggle_visibility(self, event):
        line = event.artist
        visible = not line.get_visible()
        line.set_visible(visible)
        line.figure.canvas.draw()
        # print("Toggle")

    def toggle_legend_visibility(self, event):
        legend_line = event.artist
        original_line = legend_line.original_line
        visible = not original_line.get_visible()
        original_line.set_visible(visible)
        legend_line.set_alpha(1.0 if visible else 0.2)
        original_line.figure.canvas.draw()
        print("Toggle Legend")

    def on_zoom(self, event):
        print("on_1")
        if event.button == 1:  # Left mouse button
            print("on_2")
            ax = event.inaxes
            if ax is not None:
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()

                print(f"Zoom limits: xlim={xlim}, ylim={ylim}")

                # Filter the data based on the zoomed area
                if self.index_column_dropdown.get() == 'Serial Number':
                    self.zoomed_dataframe = self.data_frames[0][(self.data_frames[0]['Serial Number'] >= xlim[0]) & (self.data_frames[0]['Serial Number'] <= xlim[1])]
                elif self.index_column_dropdown.get() == 'Time':
                    self.zoomed_dataframe = self.data_frames[0][(self.data_frames[0]['Time'] >= pd.to_datetime(xlim[0])) & (self.data_frames[0]['Time'] <= pd.to_datetime(xlim[1]))]

                print("Zoomed DataFrame:")
                print(self.zoomed_dataframe)

    def reset_view(self):
        self.zoomed_dataframe = None
        self.submit()

=======
        # Make sure the plot window is shown
        if hasattr(self, 'plot_window'):
            self.plot_window.deiconify()  # Show the plot window

        # Draw the canvas
        if hasattr(self, 'plot_frame'):
            canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar = NavigationToolbar2Tk(canvas, self.plot_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            canvas.draw()

        # Connect the toolbar's 'home' button (reset zoom functionality)
        if toolbar:
            toolbar.home = lambda: (
                self.ax_primary.set_xlim(None), 
                self.ax_primary.set_ylim(None), 
                [ax.set_ylim(None) for ax in self.y_axes[1:]]
            )

    def update_plot(self, selected_columns, retain_zoom=False):
        # Step 1: Retain zoom if requested
        if retain_zoom:
            xlim = self.ax_primary.get_xlim()
            ylim_primary = self.ax_primary.get_ylim()
            ylim_secondary = [ax.get_ylim() for ax in self.y_axes[1:]]
        else:
            xlim, ylim_primary, ylim_secondary = None, None, []

        # Step 2: Clear the previous plot
        self.ax_primary.clear()
        for ax in self.y_axes[1:]:
            ax.remove()  # Remove all secondary y-axes
        self.y_axes = [self.ax_primary]  # Reset y_axes to contain only primary axis

        # Step 3: If no columns are selected, don't plot anything
        if not selected_columns:
            self.fig.canvas.draw_idle()  # Clear the canvas
            return

        # Step 4: Plot the selected columns
        for i, col in enumerate(selected_columns):
            for df in self.data_frames:
                # Ensure the index column is numeric and usable
                x = df[self.index_column_dropdown.get()]
                y = df[col]

                # Create a new y-axis for each additional parameter beyond the first
                if i > 0:
                    new_ax = self.ax_primary.twinx()
                    new_ax.spines['right'].set_position(('outward', 60 * (i - 1)))  # Offset each new axis
                    self.y_axes.append(new_ax)  # Keep track of new axes
                    ax = new_ax
                else:
                    ax = self.ax_primary  # Use primary axis for the first parameter

                ax.plot(x, y, label=col, color=plt.cm.viridis(i / len(selected_columns)))
                ax.set_ylabel(f"{col} Values")

        # Step 5: Set labels and titles
        self.ax_primary.set_xlabel(self.index_column_dropdown.get())
        self.ax_primary.set_title("Updated Data Plot")

        # Step 6: Update legends for all axes
        handles, labels = self.ax_primary.get_legend_handles_labels()
        for ax in self.y_axes[1:]:
            h, l = ax.get_legend_handles_labels()
            handles.extend(h)
            labels.extend(l)
        self.ax_primary.legend(handles, labels, loc='upper left')

        # Step 7: Restore zoom if applicable
        if retain_zoom and xlim and ylim_primary:
            self.ax_primary.set_xlim(xlim)
            self.ax_primary.set_ylim(ylim_primary)
            for ax, ylim in zip(self.y_axes[1:], ylim_secondary):
                ax.set_ylim(ylim)

        # Step 8: Redraw the canvas with the updated plot
        self.fig.canvas.draw_idle()

# Create the application window
>>>>>>> 983d8280db6ab5f94918c4eae79a34543bcad18b
if __name__ == "__main__":
    root = tk.Tk()
    app = PlotApp(root)
    root.mainloop()