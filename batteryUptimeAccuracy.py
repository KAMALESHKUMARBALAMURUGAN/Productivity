import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import openpyxl
import traceback

def process_file(input_file, ws, start_col):
     # Ignore files that start with "ana"
    if os.path.basename(input_file).startswith('Ana'):
        return

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
    # if output_file.endswith('.csv'):
    #     df.to_csv(output_file, index=False)
    # elif output_file.endswith('.xlsx'):
    #     df.to_excel(output_file, index=False)

    # Prepare analysis data
    analysis_data = {
        "Available message count": can_time_count,
        "Number of times 'time_diff' is greater than 30": count_greater_than_30,
        "Time difference in minutes when the bmsStatVal '7'": f"{time_diff_minutes:.2f}" if time_diff_minutes is not None else "N/A"
    }

    # Populate Excel sheet with analysis data
    if start_col == 1:
        ws.cell(row=1, column=start_col, value="File name")
        for i, key in enumerate(analysis_data.keys(), start=2):
            ws.cell(row=i, column=start_col, value=key)

    ws.cell(row=1, column=start_col + 1, value=os.path.basename(input_file))
    for i, value in enumerate(analysis_data.values(), start=2):
        ws.cell(row=i, column=start_col + 1, value=value)

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_path_label.config(text=folder_path)
        submit_button.config(state=tk.NORMAL)

def submit_folder():
    folder_path = file_path_label.cget("text")
    if folder_path:
        try:
            # Create a new Excel workbook
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Analysis Results"

            # Process each file in the folder
            start_col = 1
            for file_name in os.listdir(folder_path):
                input_file = os.path.join(folder_path, file_name)
                if input_file.endswith('.csv') or input_file.endswith('.xlsx'):
                    process_file(input_file, ws, start_col)
                    start_col += 1  # Move to the next column for the next file

            # Save the Excel workbook
            excel_output_file = os.path.join(folder_path, 'Analysis_Results.xlsx')
            wb.save(excel_output_file)
            result_message = f"Analysis results saved to {excel_output_file}"
            messagebox.showinfo("Success", result_message)
            print(f"Analysis results saved to {excel_output_file}")
        except Exception as e:
            error_message = f"Error: {str(e)}\nLine: {traceback.format_exc()}"
            messagebox.showerror("Error Present", title="Error", message=error_message)

# Create the main window
root = tk.Tk()
root.title("Battery Uptime Accuracy Finder")
root.configure(bg='red')

# Instruction label
instruction_label = tk.Label(root, text="Click browse to choose the input folder", bg='red', fg='white', font=('Arial', 14))
instruction_label.pack(pady=10)

instruction_label2 =tk.Label(root, text = "Ensure that only the files to be analyzed are in the root folder and remove the 'ANALYSIS FILE' if it exists", bg='red', fg='white', font=('Arial', 14))
instruction_label2.pack(pady=10)

# Create a button to browse for the input folder
browse_button = tk.Button(root, text="Browse", command=browse_folder, bg='black', fg='white', font=('Arial', 14))
browse_button.pack(pady=10)

# Label to display the selected folder path
file_path_label = tk.Label(root, text="", bg='black', fg='white', font=('Arial', 14))
file_path_label.pack(pady=5)

# Create a submit button to process the folder
submit_button = tk.Button(root, text="Submit", command=submit_folder, state=tk.DISABLED, bg='black', fg='white', font=('Arial', 14))
submit_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()