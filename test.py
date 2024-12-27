import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import os
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import webbrowser  # Add the webbrowser module

# Tkinter GUI Setup
class PlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Plotter")

        # File Path Input
        self.label = tk.Label(root, text="Select File (CSV or Excel):")
        self.label.pack(pady=5)

        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack(pady=5)

        # Browse Button to select file
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        # Search Box for filtering columns
        self.search_label = tk.Label(root, text="Search Columns:")
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(root, width=50)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.update_checkboxes)  # Bind the search entry to key releases

        # Scrollable Frame for checkboxes
        self.checkbox_frame = tk.Frame(root)
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

        # "Select All" checkbox
        self.select_all_var = tk.BooleanVar()
        self.select_all_checkbox = tk.Checkbutton(
            self.scrollable_frame,
            text="Select All",
            variable=self.select_all_var,
            command=self.toggle_all_checkboxes
        )
        self.select_all_checkbox.pack(anchor='w')

        # Dropdown for Index Column Selection
        self.index_label = tk.Label(root, text="Select Index Column:")
        self.index_label.pack(pady=5)
        self.index_column_dropdown = ttk.Combobox(root, state="readonly")
        self.index_column_dropdown.pack(pady=5)

        # Submit Button
        self.submit_button = tk.Button(root, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)

        # To hold the extracted column names and their corresponding checkboxes
        self.column_names = []
        self.checkbox_vars = {}  # To store the checkbox variables for each column
        self.data = None

    def browse_file(self):
        
        
        # Allow the user to select either a CSV or Excel file
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*"),("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, file_path)

         # Extract the input file name and base name
        self.input_file_name = os.path.basename(file_path)  # File name with extension
        
        #self.input_file_base_name = os.path.splitext(self.input_file_name)[0]  # Base name without extension

        # After file selection, extract columns
        self.load_data_and_columns(file_path)
        

    def load_data_and_columns(self, file_path):
        # Clear the previous checkboxes and dropdown
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.index_column_dropdown.set('')
        self.checkbox_vars.clear()

        # Re-add the "Select All" checkbox
        self.select_all_checkbox = tk.Checkbutton(
            self.scrollable_frame,
            text="Select All",
            variable=self.select_all_var,
            command=self.toggle_all_checkboxes
        )
        self.select_all_checkbox.pack(anchor='w')

        # Load the file based on its extension
        if os.path.isfile(file_path):
            try:
                if file_path.endswith('.csv'):
                    self.data = pd.read_csv(file_path)
                elif file_path.endswith('.xlsx'):
                    self.data = pd.read_excel(file_path)
                else:
                    raise ValueError("Unsupported file format")
                
                 # Add an explicit index column to the data
                self.data.insert(0, 'Index', range(1, len(self.data) + 1))
                
                

                # Extract column names
                self.column_names = self.data.columns.tolist()

                # Initialize checkboxes with the full list of columns
                self.update_checkboxes()

                # Populate the dropdown with column names for index selection
                self.index_column_dropdown['values'] = self.column_names

                # print("Columns available for plotting:", self.column_names)
            except Exception as e:
                print(f"Error loading data: {e}")

    def update_checkboxes(self, event=None):
        # Get the search query
        search_query = self.search_entry.get().lower()

        # Filter the column names based on the search query
        filtered_columns = [col for col in self.column_names if search_query in col.lower()]

        # Clear the current checkboxes except the "Select All" checkbox
        for widget in self.scrollable_frame.winfo_children():
            if widget != self.select_all_checkbox:
                widget.destroy()

        # Add checkboxes for the filtered columns
        for col in filtered_columns:
            # Retain the checkbox state using self.checkbox_vars
            if col not in self.checkbox_vars:
                self.checkbox_vars[col] = tk.BooleanVar()

            cb = tk.Checkbutton(self.scrollable_frame, text=col, variable=self.checkbox_vars[col])
            cb.pack(anchor='w')

        # Update the "Select All" checkbox state based on the filtered checkboxes
        self.update_select_all_state()

    def update_select_all_state(self):
        # Check if all filtered checkboxes are selected
        all_selected = all(var.get() for col, var in self.checkbox_vars.items() if col in self.column_names)
        self.select_all_var.set(all_selected)

    def toggle_all_checkboxes(self):
        # Toggle all checkboxes based on the "Select All" checkbox state
        select_all_state = self.select_all_var.get()
        for col, var in self.checkbox_vars.items():
            var.set(select_all_state)

    def submit(self):
        # Get the columns that are checked
        selected_columns = [col for col, var in self.checkbox_vars.items() if var.get()]

        # Get the selected index column from the dropdown
        selected_index_column = self.index_column_dropdown.get()

        if self.data is not None and selected_columns and selected_index_column:
            # Plot the selected columns with the selected index
            self.plot_columns(selected_columns, selected_index_column, os.path.dirname(self.path_entry.get()))

    def plot_columns(self, columns, index_column, save_path):
        print("chosen columns",columns)
        # Set the selected column as index
        if index_column in columns:
            self.data.set_index(index_column, inplace=True)
            columns.remove(index_column)

        else:
            self.data.set_index(index_column, inplace=True)

        # Plot using Plotly
        fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add trace for each selected column
        for i, col in enumerate(columns):
            # Assign y-axis based on index (e.g., first column to 'y', second to 'y2', etc.)
            axis_name = f'y{i+1}' if i < 2 else f'y{i+2}'  # Primary ('y1') and secondary ('y2') for first two, then others
            fig.add_trace(go.Scatter(x=self.data.index, y=self.data[col], name=col), secondary_y=(i > 0))

    
        # Add opacity modification dropdown
        fig.update_layout(
            title=f'Plot_{self.input_file_name}',
            xaxis_title=index_column,
            height=1000,
            yaxis=dict(title='Primary Y-Axis', showgrid=False),
            yaxis2=dict(title='Secondary Y-Axis', overlaying='y', side='right', showgrid=False),  # Overlay for secondary axis
            # yaxis3=dict(title='Tertiary Y-Axis', overlaying='y', side='right', position=0.85),  # Add third axis at a different position
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
        # graph_path = os.path.join(save_path, 'Dynamic_plot.html')
        graph_path = os.path.join(save_path, f'Dynamic_plot_{self.input_file_name}.html')  # Updated file name
        fig.write_html(graph_path)
        print(f"Plot saved at: {graph_path}")

        # Automatically open the saved plot in the default web browser
        webbrowser.open('file://' + os.path.realpath(graph_path))  # Open the HTML file


if __name__ == "__main__":
    root = tk.Tk()
    app = PlotApp(root)
    root.mainloop()
