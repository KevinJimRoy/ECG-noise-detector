import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import subprocess
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def run_matlab_detection(file_path):
    try:
        file_path_unix = file_path.replace("\\", "/")
        cmd = f'matlab -batch "ecg_detect(\'{file_path_unix}\')"'
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        messagebox.showerror("MATLAB Error", f"MATLAB failed: {e}")
        return False


def plot_spectrum(frame):
    try:
        df = pd.read_csv("spectrum.csv", header=None)
        freq = df[0]
        mag = df[1]

        fig, ax = plt.subplots(figsize=(7, 4.5), dpi=100) 
        ax.plot(freq, mag)
        ax.set_title("ECG Frequency Spectrum", fontsize=14)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        toolbar.pack()

    except Exception as e:
        messagebox.showerror("Plot Error", f"Could not load spectrum: {e}")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    status_label.config(text="Running MATLAB...")
    for widget in spectrum_frame.winfo_children():
        widget.destroy()

    success = run_matlab_detection(file_path)
    if not success:
        return

    try:
        df = pd.read_csv("results.csv", header=None)
        baseline_detected = bool(int(df.iloc[1, 0]))
        powerline_detected = bool(int(df.iloc[1, 1]))


        baseline_msg = "⚠️ Baseline Wander Detected" if baseline_detected else "✅ No Baseline Wander"
        powerline_msg = "⚠️ Powerline Interference Detected" if powerline_detected else "✅ No Powerline Interference"

        baseline_label.config(text=baseline_msg)
        powerline_label.config(text=powerline_msg)
        status_label.config(text="Done ✅")

        plot_spectrum(spectrum_frame)

    except Exception as e:
        messagebox.showerror("Processing Error", str(e))

root = tk.Tk()
root.title("ECG Signal Analyzer")
root.geometry("600x500")

tk.Label(root, text="ECG Noise Detection", font=("Helvetica", 16, "bold")).pack(pady=10)
tk.Button(root, text="Select ECG CSV File", command=select_file, font=("Helvetica", 12)).pack(pady=10)

baseline_label = tk.Label(root, text="", font=("Helvetica", 12))
baseline_label.pack(pady=5)

powerline_label = tk.Label(root, text="", font=("Helvetica", 12))
powerline_label.pack(pady=5)

status_label = tk.Label(root, text="", font=("Helvetica", 11, "italic"))
status_label.pack(pady=5)

spectrum_frame = tk.Frame(root)
spectrum_frame.pack(pady=10)

root.mainloop()
