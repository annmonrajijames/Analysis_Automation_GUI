import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

class FileProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Processor")

        # File Path Input
        self.label = tk.Label(root, text="Select File (CSV or Excel):")
        self.label.pack(pady=5)

        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack(pady=5)

        # Browse Button to select file
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        # Process Button to process the selected file
        self.process_button = tk.Button(root, text="Process File", command=self.process_file)
        self.process_button.pack(pady=10)

    def browse_file(self):
        # Allow the user to select any file
        file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*"), ("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        if file_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, file_path)

    def process_file(self):
        file_path = self.path_entry.get()

        if not file_path:
            messagebox.showerror("Error", "Please select a file to process.")
            return

        # Check file extension and read accordingly
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format. Please select a CSV or Excel file.")

            # Separate the initial mapping rows and the log data
            name_display_mapping = df.iloc[:153, :3]  # Adjust the row count as needed

            log_data = pd.read_csv(file_path, skiprows=154) if file_path.endswith('.csv') else pd.read_excel(file_path, skiprows=154)

            # Create a dictionary mapping from Name to DisplayName 
            mapping_dict = pd.Series(name_display_mapping['DisplayName'].values, 
                                     index=name_display_mapping['Name']).to_dict()

            # Replace the column names in the log data using the mapping dictionary
            log_data.rename(columns=mapping_dict, inplace=True)

            # Get the directory of the input file
            input_directory = os.path.dirname(file_path)

            # Create the output file path in the same directory
            output_file_path = os.path.join(input_directory, 'modified_log_data.csv') if file_path.endswith('.csv') else os.path.join(input_directory, 'modified_log_data.xlsx')

            # Save the modified log data to the new file
            if file_path.endswith('.csv'):
                log_data.to_csv(output_file_path, index=False)
                print("Modified Data saved to:", output_file_path)
            else:
                log_data.to_excel(output_file_path, index=False)
                print("Modified Data saved to:", output_file_path)

            messagebox.showinfo("Success", f"Modified log data saved to: {output_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process the file. Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileProcessorApp(root)
    root.mainloop()
