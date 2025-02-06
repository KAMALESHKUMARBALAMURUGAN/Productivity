import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import openpyxl
import traceback

def process_file(input_file):
    # Ignore files that start with "ana"
    if os.path.basename(input_file).startswith('Ana'):
        return None, None

    # Determine the file extension and read the file accordingly
    if input_file.endswith('.csv'):
        df = pd.read_csv(input_file)
    elif input_file.endswith('.xlsx'):
        df = pd.read_excel(input_file)
    else:
        raise ValueError("Unsupported file format. Please provide a .csv or .xlsx file.")

    # Convert the 'time' column to datetime format
    df["updated_time"] = pd.to_datetime(df['time'], format='%H:%M:%S')

    # Calculate the time difference in seconds and create a new column 'time_diff'
    df['time_diff'] = df['updated_time'].diff().dt.total_seconds()

        # Initialize variables
    sum_time_diff = 0
    count = 0

    # Iterate through the 'time_diff' column
    for time_diff in df['time_diff'].dropna():
        sum_time_diff += time_diff
        if sum_time_diff >= 30:
            count += 1
            sum_time_diff = 0  # Reset the sum

    print("Filtered count---------->",count)



    # Count the number of times 'time_diff' is greater than 30, ignoring NaN values
    count_greater_than_30 = df['time_diff'].dropna().gt(30).sum()

    # Calculate cumulative time difference in minutes for segments where bmsStatVal starts with 0 and ends with 7
    cumulative_time_diff_minutes = 0
    if 'bmsStatVal' in df.columns:
        in_segment = False
        segment_start_index = None
        for index, row in df.iterrows():
            if row['bmsStatVal'] == 0 and not in_segment:
                in_segment = True
                segment_start_index = index
            elif row['bmsStatVal'] == 7 and in_segment:
                segment_end_index = index
                segment_df = df.loc[segment_start_index:segment_end_index]
                cumulative_time_diff_minutes += segment_df['time_diff'].sum() / 60
                in_segment = False

    # Count the number of instances of CANTime
    can_time_count = df['CANTime'].count()

    # Count the number of instances of each bmsStatus
    bms_status_counts = df['bmsStatus'].value_counts().to_dict()


    # Calculate ideal time in minutes and ideal time count
    ideal_time_mins = int(1440 - cumulative_time_diff_minutes)
    # print("Mins:",ideal_time_mins)
    ideal_time_count = ideal_time_mins * 2
    # print("Count:",ideal_time_count)

    

    # print("Ideal Count",ideal_time_count)
    # print("Ideal Time",ideal_time_mins)

    # Track continuous segments of 'DisCharging' and 'Charging'
    discharge_segments = []
    charging_segments = []
    current_discharge_count = 0
    current_charging_count = 0
    in_discharge = False
    in_charging = False

    for status in df['bmsStatus']:
        if status == 'DisCharging':
            if not in_discharge:
                in_discharge = True
                current_discharge_count = 1
            else:
                current_discharge_count += 1
        else:
            if in_discharge:
                discharge_segments.append(current_discharge_count)
                in_discharge = False

        if status == 'Charging':
            if not in_charging:
                in_charging = True
                current_charging_count = 1
            else:
                current_charging_count += 1
        else:
            if in_charging:
                charging_segments.append(current_charging_count)
                in_charging = False

    # Add the last segment if it ends at the last row
    if in_discharge:
        discharge_segments.append(current_discharge_count)
    if in_charging:
        charging_segments.append(current_charging_count)

    print("can_time_count",can_time_count)
    print("ideal_time_count",ideal_time_count)
    print("ideal_time_mins",ideal_time_mins)

    # Prepare analysis data
    analysis_data = {
        "Ideal Time (Minutes)": ideal_time_mins,
        "Ideal Time Count": ideal_time_count,
        "Available message count": can_time_count,
        "Available Message count(Filtered- data in less than 30 seconds)": count,
        "Number of times 'time_diff' is greater than 30": count_greater_than_30,
        "Cumulative time difference in minutes for bmsStatVal 0 or 7": f"{cumulative_time_diff_minutes:.2f}",
        "Idle count": bms_status_counts.get('Idle', 0),
        "Total DisCharging count": bms_status_counts.get('DisCharging', 0),
        "Total Charging count": bms_status_counts.get('Charging', 0),
       
    }

    # Add discharge and charging segments to analysis data
    for i, count in enumerate(discharge_segments, start=1):
        analysis_data[f"Discharge_{i}"] = count
    for i, count in enumerate(charging_segments, start=1):
        analysis_data[f"Charging_{i}"] = count

    return analysis_data, os.path.basename(input_file)

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

            # Process each file in the folder and collect analysis data
            all_analysis_data = []
            max_discharge_segments = 0
            max_charging_segments = 0

            for file_name in os.listdir(folder_path):
                input_file = os.path.join(folder_path, file_name)
                if input_file.endswith('.csv') or input_file.endswith('.xlsx'):
                    analysis_data, file_basename = process_file(input_file)
                    if analysis_data:
                        all_analysis_data.append((analysis_data, file_basename))
                        max_discharge_segments = max(max_discharge_segments, len([key for key in analysis_data.keys() if key.startswith("Discharge_")]))
                        max_charging_segments = max(max_charging_segments, len([key for key in analysis_data.keys() if key.startswith("Charging_")]))

            # Create a consistent set of keys
            consistent_keys = [
                "Available message count",
                "Available Message count(Filtered- data in less than 30 seconds)",
                "Number of times 'time_diff' is greater than 30",
                "Cumulative time difference in minutes for bmsStatVal 0 or 7",
                "Ideal Time (Minutes)",
                "Ideal Time Count",
                "Idle count",
                "Total DisCharging count",
                "Total Charging count"
            ]
            consistent_keys += [f"Discharge_{i}" for i in range(1, max_discharge_segments + 1)]
            consistent_keys += [f"Charging_{i}" for i in range(1, max_charging_segments + 1)]

            # Populate Excel sheet with consistent keys
            ws.cell(row=1, column=1, value="File name")
            for i, key in enumerate(consistent_keys, start=2):
                ws.cell(row=i, column=1, value=key)

            # Populate Excel sheet with analysis data
            start_col = 2
            for analysis_data, file_basename in all_analysis_data:
                ws.cell(row=1, column=start_col, value=file_basename)
                for i, key in enumerate(consistent_keys, start=2):
                    ws.cell(row=i, column=start_col, value=analysis_data.get(key, "N/A"))
                start_col += 1

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

instruction_label2 = tk.Label(root, text="Ensure that only the files to be analyzed are in the root folder and remove the 'ANALYSIS FILE' if it exists", bg='red', fg='white', font=('Arial', 14))
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