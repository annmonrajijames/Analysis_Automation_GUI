import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mplcursors import cursor as mplcursor
from matplotlib.ticker import MaxNLocator

class DynamicPlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Plotting GUI")
        self.root.geometry("1200x700")

        self.files = []
        self.dataframes = []
        self.parameters = {}
        self.selected_parameters = {}

        self.setup_gui()

    def setup_gui(self):
        left_frame = tk.Frame(self.root, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.file_button = tk.Button(left_frame, text="Select Files", command=self.load_files)
        self.file_button.pack(pady=10)

        self.x_axis_var = tk.StringVar(value="Serial Number")
        x_axis_label = tk.Label(left_frame, text="Select X-Axis:")
        x_axis_label.pack(pady=5)
        self.x_axis_dropdown = ttk.Combobox(left_frame, textvariable=self.x_axis_var, values=["Serial Number", "Time"], state="readonly")
        self.x_axis_dropdown.pack(pady=5)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_parameter_list)
        self.search_entry = tk.Entry(left_frame, textvariable=self.search_var)
        self.search_entry.pack(pady=5)

        self.select_all_var = tk.BooleanVar()
        self.select_all_check = tk.Checkbutton(left_frame, text="Select All", variable=self.select_all_var, command=self.toggle_select_all)
        self.select_all_check.pack(pady=5)

        self.param_frame = tk.Frame(left_frame)
        self.param_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas_param = tk.Canvas(self.param_frame)
        self.scrollbar = ttk.Scrollbar(self.param_frame, orient="vertical", command=self.canvas_param.yview)
        self.scrollable_frame = tk.Frame(self.canvas_param)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_param.configure(scrollregion=self.canvas_param.bbox("all"))
        )

        self.canvas_param.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_param.configure(yscrollcommand=self.scrollbar.set)

        self.canvas_param.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.plot_button = tk.Button(left_frame, text="Plot", command=self.plot_selected_parameters)
        self.plot_button.pack(pady=10)

        self.selected_param_frame = tk.LabelFrame(left_frame, text="Selected Parameters")
        self.selected_param_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Initialize mplcursor
        self.cursor = mplcursor(self.ax, hover=True)

    def load_files(self):
        filenames = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")])
        if filenames:
            self.files = filenames
            self.load_parameters_from_files()

    def load_parameters_from_files(self):
        self.parameters.clear()
        self.dataframes.clear()

        for file in self.files:
            try:
                if file.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.endswith('.xlsx'):
                    df = pd.read_excel(file)
                else:
                    messagebox.showerror("Unsupported File Type", f"{file} is not a supported file type.")
                    continue

                if df.empty:
                    print(f"Warning: {file} is empty.")
                    continue

                self.dataframes.append(df)
                print(f"Loaded {file} with columns: {df.columns.tolist()}")  # Debugging line

                for param in df.columns:
                    if param not in self.parameters:
                        self.parameters[param] = tk.BooleanVar()

            except Exception as e:
                print(f"Error loading {file}: {e}")

        self.update_parameter_list()

    def update_parameter_list(self, *args):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        search_term = self.search_var.get().lower()
        filtered_params = [param for param in self.parameters if search_term in param.lower()]

        for param in filtered_params:
            check = tk.Checkbutton(self.scrollable_frame, text=param, variable=self.parameters[param], command=self.update_selected_parameters)
            check.pack(anchor='w')

        self.select_all_check.deselect()

    def toggle_select_all(self):
        select_all = self.select_all_var.get()
        for param in self.parameters:
            if self.search_var.get().lower() in param.lower():
                self.parameters[param].set(select_all)
        self.update_selected_parameters()

    def update_selected_parameters(self):
        self.selected_parameters.clear()

        for widget in self.selected_param_frame.winfo_children():
            widget.destroy()

        for param, var in self.parameters.items():
            if var.get():
                self.selected_parameters[param] = var
                check = tk.Checkbutton(self.selected_param_frame, text=param, variable=var, command=self.plot_selected_parameters)
                check.pack(anchor='w')

    def plot_selected_parameters(self):
        print("Plotting selected parameters...")  # Debugging line

        # Clear the axes before plotting
        self.ax.clear()
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.figure.set_facecolor("#f7f7f7")

        # Determine x-axis data based on selection
        if self.x_axis_var.get() == "Time" and "Time" in self.dataframes[0].columns:
            x_data = self.dataframes[0]["Time"]
            x_label = "Time"
        else:
            x_data = list(range(len(self.dataframes[0])))  # Generate a serial number range
            x_label = "Serial Number"

        color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
        color_index = 0
        num_axes = 0

        selected_params = [param for param, var in self.parameters.items() if var.get()]
        print("Selected parameters:", selected_params)  # Debugging line

        # Check if any parameters are selected
        if not selected_params:
            print("No parameters selected for plotting.")  # Debugging line
            return

        # Plot selected parameters
        for param in selected_params:
            ax = self.ax if num_axes == 0 else self.ax.twinx()
            ax.spines["right"].set_position(("axes", 1 + 0.1 * num_axes))
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax.tick_params(axis='y', colors=color_cycle[color_index % len(color_cycle)])
            ax.set_ylabel(param, color=color_cycle[color_index % len(color_cycle)])

            for df in self.dataframes:
                if param in df.columns:
                    # Drop rows where the current parameter or x_data has NaN values
                    if self.x_axis_var.get() == "Time":
                        df_cleaned = df[['Time', param]].dropna()
                    else:
                        df_cleaned = df[[param]].dropna()
                        x_data_cleaned = list(range(len(df_cleaned)))  # Regenerate serial number range

                    print(f"Data for {param} before plotting:")
                    print(df_cleaned)  # Debugging line: check cleaned data

                    # Ensure that we have valid data for plotting
                    if not df_cleaned.empty:
                        if self.x_axis_var.get() == "Time":
                            x_data_cleaned = df_cleaned["Time"]
                        else:
                            x_data_cleaned = list(range(len(df_cleaned)))  # Ensure x_data aligns

                        ax.plot(x_data_cleaned, df_cleaned[param].values, label=param, color=color_cycle[color_index % len(color_cycle)], linewidth=2)
                        print(f"Plotted {param} with {len(df_cleaned)} points.")  # Debugging line
                    else:
                        print(f"No valid data points for {param}.")  # Debugging line

            color_index += 1
            num_axes += 1

        self.ax.set_xlabel(x_label)

        # Update legend to show currently plotted parameters only
        self.ax.legend(loc="upper right")

        self.canvas.draw()
        self.cursor.connect("add", lambda sel: self.update_zoom(sel))

    def update_zoom(self, sel):
        if sel.artist:
            sel.annotation.set_text(f'{sel.artist.get_label()}\n{sel.index}: {sel.artist.get_ydata()[sel.index]}')

# Run the application
root = tk.Tk()
app = DynamicPlotApp(root)
root.mainloop()
