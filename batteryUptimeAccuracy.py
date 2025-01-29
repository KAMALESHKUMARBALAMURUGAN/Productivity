import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def process_file(input_file):
    # Determine the file extension and read the file accordingly
    if input_file.endswith('.csv'):
        df = pd.read_csv(input_file)
        output_file = os.path.join(os.path.dirname(input_file), 'Updated.csv')
    elif input_file.endswith('.xlsx'):
        df = pd.read_excel(input_file)
        output_file = os.path.join(os.path.dirname(input_file), 'Updated.xlsx')
    else:
        raise ValueError("Unsupported file format. Please provide a .csv or .xlsx file.")

    # Convert the 'time' column to datetime format
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S')

    # Calculate the time difference in seconds and create a new column 'time_diff'
    df['time_diff'] = df['time'].diff().dt.total_seconds()

    # Print the dataframe to show the output
    print(df)

    # Save the dataframe to the appropriate file format
    if output_file.endswith('.csv'):
        df.to_csv(output_file, index=False)
    elif output_file.endswith('.xlsx'):
        df.to_excel(output_file, index=False)

    messagebox.showinfo("Success", f"File processed and saved as {output_file}")

def browse_file():
    input_file = filedialog.askopenfilename(filetypes=[("All files", "*.*"), ("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
    if input_file:
        file_path_label.config(text=input_file)
        submit_button.config(state=tk.NORMAL)

def submit_file():
    input_file = file_path_label.cget("text")
    if input_file:
        try:
            process_file(input_file)
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Battery Uptime Accuracy Finder")

# Create a button to browse for the input file
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=10)

# Label to display the selected file path
file_path_label = tk.Label(root, text="")
file_path_label.pack(pady=5)

# Create a submit button to process the file
submit_button = tk.Button(root, text="Submit", command=submit_file, state=tk.DISABLED)
submit_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()