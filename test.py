import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataPlottingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Plotting Application")
        self.root.geometry("1000x700")

        self.data_frames = []
        self.checkbox_vars = {}
        self.selected_checkbox_vars = {}

        self.create_widgets()

    def create_widgets(self):
        # File selection frame
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10)

        tk.Label(file_frame, text="Select File:").pack(side=tk.LEFT, padx=5)

        self.file_entry = tk.Entry(file_frame, width=50)
        self.file_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(file_frame, text="Load", command=self.load_file).pack(side=tk.LEFT, padx=5)

        # Checkboxes frame
        self.checkboxes_frame = tk.Frame(self.root)
        self.checkboxes_frame.pack(pady=10)

        # Selected columns frame
        self.selected_columns_frame = tk.Frame(self.root)
        self.selected_columns_frame.pack(pady=10)

        # Index column dropdown
        dropdown_frame = tk.Frame(self.root)
        dropdown_frame.pack(pady=10)

        tk.Label(dropdown_frame, text="Index Column:").pack(side=tk.LEFT, padx=5)

        self.index_column_dropdown = ttk.Combobox(dropdown_frame, state="readonly")
        self.index_column_dropdown.pack(side=tk.LEFT, padx=5)

        # Apply button
        tk.Button(self.root, text="Submit", command=self.submit).pack(pady=10)

        # Custom X-axis range frame
        custom_x_frame = tk.Frame(self.root)
        custom_x_frame.pack(pady=10)

        tk.Label(custom_x_frame, text="Custom X-axis Min:").pack(side=tk.LEFT, padx=5)
        self.custom_x_min_entry = tk.Entry(custom_x_frame, width=20)
        self.custom_x_min_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(custom_x_frame, text="Custom X-axis Max:").pack(side=tk.LEFT, padx=5)
        self.custom_x_max_entry = tk.Entry(custom_x_frame, width=20)
        self.custom_x_max_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(custom_x_frame, text="Apply Custom X-axis", command=self.apply_custom_x_axis).pack(side=tk.LEFT, padx=5)

        # X-axis labels
        self.first_x_label = tk.Label(self.root, text="First X-axis Value: ")
        self.first_x_label.pack(pady=5)
        self.last_x_label = tk.Label(self.root, text="Last X-axis Value: ")
        self.last_x_label.pack(pady=5)

    def load_file(self):
        file_path = self.file_entry.get()
        self.load_data_and_columns(file_path)

    def load_data_and_columns(self, file_path):
        self.index_column_dropdown.set('')
        if os.path.isfile(file_path):
            try:
                if file_path.endswith('.csv'):
                    self.data = pd.read_csv(file_path)
                elif file_path.endswith('.xlsx'):
                    self.data = pd.read_excel(file_path)
                else:
                    raise ValueError("Unsupported file format")

                self.data.dropna(how='all', inplace=True)

                if 'Time' in self.data.columns:
                    self.data['DATETIME'] = pd.to_datetime(self.data['Time'], errors='coerce')

                self.data_frames.append(self.data)
                self.column_names = self.data.columns.tolist()
                self.update_checkboxes()

                filtered_index_columns = [col for col in self.column_names if col.lower() in ['datetime']]
                self.index_column_dropdown['values'] = filtered_index_columns

                x_column = 'DATETIME' if 'DATETIME' in self.data.columns else 'Time'
                if x_column:
                    first_value = self.data[x_column].iloc[0]
                    last_value = self.data[x_column].iloc[-1]
                    self.first_x_label.config(text=f"First X-axis Value: {first_value}")
                    self.last_x_label.config(text=f"Last X-axis Value: {last_value}")

            except Exception as e:
                print(f"Error loading data: {e}")

    def update_checkboxes(self):
        for widget in self.checkboxes_frame.winfo_children():
            widget.destroy()

        for col in self.column_names:
            var = tk.IntVar()
            checkbox = tk.Checkbutton(self.checkboxes_frame, text=col, variable=var)
            checkbox.pack(anchor="w")
            self.checkbox_vars[col] = var

    def submit(self):
        selected_columns = [col for col, var in self.checkbox_vars.items() if var.get()]
        selected_index_column = self.index_column_dropdown.get()

        if self.data_frames and selected_columns and selected_index_column:
            for widget in self.selected_columns_frame.winfo_children():
                widget.destroy()

            for col in selected_columns:
                var = tk.IntVar(value=1)
                checkbox = tk.Checkbutton(self.selected_columns_frame, text=col, variable=var)
                checkbox.pack(anchor="w")
                self.selected_checkbox_vars[col] = var

            self.plot_columns(selected_columns, selected_index_column)
        else:
            messagebox.showerror("Error", "Please select columns and an index column.")

    def plot_columns(self, selected_columns, index_column, custom_x_min=None, custom_x_max=None):
        if hasattr(self, 'fig'):
            plt.close(self.fig)

        self.fig, self.ax_primary = plt.subplots(figsize=(10, 6))

        for i, col in enumerate(selected_columns):
            for df in self.data_frames:
                x = pd.to_datetime(df[index_column], errors='coerce')
                y = df[col]

                if custom_x_min and custom_x_max:
                    mask = (x >= custom_x_min) & (x <= custom_x_max)
                    x = x[mask]
                    y = y[mask]

                if len(x) > 0 and len(y) > 0:
                    self.ax_primary.plot(x, y, label=col, color=plt.cm.viridis(i / len(selected_columns)))

        self.ax_primary.set_xlabel(index_column)
        self.ax_primary.set_title("Data Plot")
        self.ax_primary.legend()
        canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def apply_custom_x_axis(self):
        try:
            custom_min = self.custom_x_min_entry.get()
            custom_max = self.custom_x_max_entry.get()

            if not custom_min or not custom_max:
                raise ValueError("Both start and end values must be provided.")

            custom_min = pd.to_datetime(custom_min)
            custom_max = pd.to_datetime(custom_max)

            self.plot_columns(self.selected_checkbox_vars.keys(), 'DATETIME', custom_min, custom_max)

        except Exception as e:
            print(f"Error applying custom x-axis range: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataPlottingApp(root)
    root.mainloop()
