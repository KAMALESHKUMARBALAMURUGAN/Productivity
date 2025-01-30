import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import openpyxl

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
    df["updated_time"] = pd.to_datetime(df['time'], format='%H:%M:%S')

    # Calculate the time difference in seconds and create a new column 'time_diff'
    df['time_diff'] = df['updated_time'].diff().dt.total_seconds()

    # Count the number of times 'time_diff' is greater than 30, ignoring NaN values
    count_greater_than_30 = df['time_diff'].dropna().gt(30).sum()

    # Calculate time_diff in minutes for rows where bmsStatVal is '7'
    time_diff_minutes = None
    time_diff_message = ""
    if 'bmsStatVal' in df.columns:
        bms_stat_val_7 = df[df['bmsStatVal'] == 7]
        if not bms_stat_val_7.empty:
            idx = bms_stat_val_7.index[0]
            if idx > 0:
                time_diff_minutes = (df.loc[idx, 'updated_time'] - df.loc[idx - 1, 'updated_time']).total_seconds() / 60
                time_diff_message = f"Time(idx): {df.loc[idx, 'updated_time']}, Time(idx-1): {df.loc[idx - 1, 'updated_time']}"

    # Count the number of instances of CANTime
    can_time_count = df['CANTime'].count()

    # Save the dataframe to the appropriate file format
    if output_file.endswith('.csv'):
        df.to_csv(output_file, index=False)
    elif output_file.endswith('.xlsx'):
        df.to_excel(output_file, index=False)

    # Prepare analysis data
    analysis_data = {
        "Available message count": can_time_count,
        "Number of times 'time_diff' is greater than 30": count_greater_than_30,
        "Time difference in minutes when the bmsStatVal '7'": f"{time_diff_minutes:.2f}" if time_diff_minutes is not None else "N/A"
    }

    # Create a new Excel workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Analysis Results"

        # Add the input file name to the first row
    ws.cell(row=1, column=1, value="File name")
    ws.cell(row=1, column=2, value=os.path.basename(input_file))


    # Populate Excel sheet with analysis data
    for i, (key, value) in enumerate(analysis_data.items(), start=2):
        ws.cell(row=i, column=1, value=key)
        ws.cell(row=i, column=2, value=value)

    # Save the Excel workbook
    excel_output_file = os.path.join(os.path.dirname(input_file), 'Analysis_Results.xlsx')
    wb.save(excel_output_file)
    result_message = f"Analysis results saved to {excel_output_file}"
    messagebox.showinfo("Success", result_message)
    print(f"Analysis results saved to {excel_output_file}")

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
            messagebox.showerror("Error Present", str(e))

# Create the main window
root = tk.Tk()
root.title("Battery Uptime Accuracy Finder")
root.configure(bg='red')

# Instruction label
instruction_label = tk.Label(root, text="Click browse to choose the input file", bg='red', fg='white',font=('Arial', 14))
instruction_label.pack(pady=10)

# Create a button to browse for the input file
browse_button = tk.Button(root, text="Browse", command=browse_file, bg='black', fg='white',font=('Arial', 14))
browse_button.pack(pady=10)

# Label to display the selected file path
file_path_label = tk.Label(root, text="", bg='black', fg='white',font=('Arial', 14))
file_path_label.pack(pady=5)

# Create a submit button to process the file
submit_button = tk.Button(root, text="Submit", command=submit_file, state=tk.DISABLED, bg='black', fg='white',font=('Arial', 14))
submit_button.pack(pady=10)


# Run the Tkinter event loop
root.mainloop()