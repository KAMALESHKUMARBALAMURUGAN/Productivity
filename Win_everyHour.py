import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

def save_to_excel():
    time_period = time_period_var.get()
    comment = comment_text.get("1.0", "end-1c")
    win_or_lost = win_or_lost_var.get()

    if not time_period or not win_or_lost or not comment.strip():
        messagebox.showwarning("Input Error", "All fields must be filled out!")
        return

    data = {
        "Time Period": [time_period],
        "Comments": [comment],
        "Win/Lost": [win_or_lost]
    }

    df = pd.DataFrame(data)

    if not os.path.exists(excel_path.get()):
        df.to_excel(excel_path.get(), index=False)
    else:
        existing_df = pd.read_excel(excel_path.get())
        new_df = pd.concat([existing_df, df], ignore_index=True)
        new_df.to_excel(excel_path.get(), index=False)

    messagebox.showinfo("Success", "Data saved successfully!")

    # Reset the fields after saving
    time_period_var.set('')
    win_or_lost_var.set('')
    comment_text.delete("1.0", "end")

# Tkinter window setup
root = tk.Tk()
root.title("Hourly Productivity Tracker")

# Time Period Dropdown
time_period_var = tk.StringVar()
time_period_label = tk.Label(root, text="Time Period:")
time_period_label.grid(row=0, column=0, padx=10, pady=10)
time_period_options = [f"{i}-{i+1}" for i in range(1, 24)]
time_period_menu = ttk.Combobox(root, textvariable=time_period_var, values=time_period_options)
time_period_menu.grid(row=0, column=1, padx=10, pady=10)

# Comments Textbox
comment_label = tk.Label(root, text="Comments:")
comment_label.grid(row=1, column=0, padx=10, pady=10)
comment_text = tk.Text(root, width=40, height=5)
comment_text.grid(row=1, column=1, padx=10, pady=10)

# Win or Lost Dropdown
win_or_lost_var = tk.StringVar()
win_or_lost_label = tk.Label(root, text="Win/Lost:")
win_or_lost_label.grid(row=2, column=0, padx=10, pady=10)
win_or_lost_menu = ttk.Combobox(root, textvariable=win_or_lost_var, values=["Win", "Lost"])
win_or_lost_menu.grid(row=2, column=1, padx=10, pady=10)

# Excel Path Entry
excel_path_label = tk.Label(root, text="Excel Path:")
excel_path_label.grid(row=3, column=0, padx=10, pady=10)
excel_path = tk.Entry(root, width=40)
excel_path.grid(row=3, column=1, padx=10, pady=10)

# Save Button
save_button = tk.Button(root, text="Save", command=save_to_excel)
save_button.grid(row=4, column=1, padx=10, pady=10)

root.mainloop()
