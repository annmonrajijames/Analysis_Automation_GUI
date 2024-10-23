import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import mplcursors  # Import mplcursors

# Tkinter GUI Setup
class PlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Plotter")

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

        # Submit Button
        self.submit_button = tk.Button(self.control_frame, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)

        # Reset Button
        self.reset_button = tk.Button(self.control_frame, text="Reset View", command=self.reset_view)
        self.reset_button.pack(pady=10)

        # To hold the extracted column names and their corresponding checkboxes
        self.column_names = []
        self.checkbox_vars = {}  # To store the checkbox variables for each column
        self.data_frames = []  # List to store data from multiple files
        self.file_directory = ""  # Directory of the files
        self.zoomed_dataframe = None  # To store the zoomed data

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

                # Handle Serial Number addition if missing
                if 'Serial Number' not in self.data.columns:
                    self.data['Serial Number'] = range(1, len(self.data) + 1)

                # Handle Time conversion if present
                if 'Time' in self.data.columns:
                    try:
                        self.data['Time'] = pd.to_datetime(self.data['Time'], errors='coerce')
                    except Exception as e:
                        print(f"Error parsing Time column: {e}")

                # Store data for each file in the list
                self.data_frames.append(self.data)

                # Extract the column names
                self.column_names = self.data.columns.tolist()

                # Update the checkboxes with the full list of columns
                self.update_checkboxes()

                # Filter only 'Serial Number' and 'Time' columns for index selection
                filtered_index_columns = [col for col in self.column_names if col.lower() in ['serial number', 'time']]

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

if __name__ == "__main__":
    root = tk.Tk()
    app = PlotApp(root)
    root.mainloop()