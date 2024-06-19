import threading
import tkinter as tk
import os
import subprocess
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
import speech_recognition as sr
from tkinter import *
from email1 import send_email_alert
import datetime

stop_event = threading.Event()


def fim_logic(res,tbm):
    try:
        if res < 1 or res > 3:
            messagebox.showerror("Invalid choice","Please enter a number between 1 and 3.")
            return
        
        script_path = './fim.ps1'
        if not os.path.exists(script_path):
            print(f"Error: The script {script_path} does not exist.")
            return

        def run_script():
            try:
                result = subprocess.run(['powershell', '-File', script_path, tbm, str(res)], capture_output=True, text=True)
                output_text.config(state=tk.NORMAL)
                output_text.delete(1.0, tk.END)
                output_text.insert(tk.END, result.stdout)
                output_text.config(state=tk.DISABLED)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Script Error", f"An error occurred while running the PowerShell script: {e}")

        stop_event = threading.Event()
        def run_monitoring():
            alerted_events = set()
            try:
                process = subprocess.Popen(['powershell', '-File', script_path, tbm, str(res)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                for line in iter(process.stdout.readline, ''):
                    if stop_event.is_set():
                        break
                    output_text.config(state=tk.NORMAL)
                    output_text.insert(tk.END, line)
                    output_text.see(tk.END)
                    output_text.config(state=tk.DISABLED)
                    if "compromised" in line or "deleted or moved or renamed" in line or "inserted" in line:
                        now = datetime.datetime.now()
                        if line not in alerted_events:
                            receiver_email = email_entry.get()
                            if(receiver_email):
                                send_email_alert("File Integrity Alert", line, now, receiver_email)
                            alerted_events.add(line)
                process.stdout.close()
                process.wait()
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Script Error", f"An error occurred while running the PowerShell script: {e}")

        if res == 3:
            thread = threading.Thread(target=run_monitoring)
            thread.daemon = True
            thread.start()
        else:
            run_script()
        


    except ValueError:
        messagebox.showerror("Invalid input. Please enter a valid number.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror(f"An error occurred while running the PowerShell script: {e}")



main = tk.Tk()
main.title("FileSec")
main.geometry("1080x720")
main.resizable(width=FALSE, height=FALSE)

def select_folder():
    tbm = filedialog.askdirectory()
    if tbm:
        tbm_entry.delete(0,tk.END)
        tbm_entry.insert(0,tbm)
def run_fim_logic():
    try:
        res = int(choice_var.get())
        tbm = tbm_entry.get()
        fim_logic(res, tbm)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the choice.")


choice_label = tk.Label(main, text="Select your choice")
choice_label.pack(pady=5)
choice_var = tk.IntVar()
choice_var.set(1)


radio1 = tk.Radiobutton(main, text="Create baseline", variable=choice_var, value=1)
radio1.pack(anchor=tk.W)

radio2 = tk.Radiobutton(main, text="Update baseline", variable=choice_var, value=2)
radio2.pack(anchor=tk.W)

radio3 = tk.Radiobutton(main, text="Monitor", variable=choice_var, value=3)
radio3.pack(anchor=tk.W)

email_label = tk.Label(main, text="[Optional]Enter email for alerts:")
email_entry = tk.Entry(main, width=50)
email_label.pack()
email_entry.pack()


# Path input
tbm_label = tk.Label(main, text="Enter the path:")
tbm_label.pack(pady=5)
tbm_entry = tk.Entry(main, width=50)
tbm_entry.pack(pady=5)

# Browse button for path selection
browse_button = tk.Button(main, text="Browse", command=select_folder)
browse_button.pack(pady=5)


# Run button
run_button = tk.Button(main, text="Run", command=run_fim_logic)
run_button.pack(pady=5)

#output
output_text = scrolledtext.ScrolledText(main, wrap=tk.WORD, width=80, height=20)
output_text.pack(pady=10)
output_text.config(state=tk.DISABLED)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # Set the stop event to stop the monitoring thread
        stop_event.set()
        main.destroy()

# Bind closing event to window
main.protocol("WM_DELETE_WINDOW", on_closing)

main.mainloop()