import subprocess
import tkinter as tk
from tkinter import messagebox
from urllib.request import urlopen
from urllib.error import URLError

SERVER_ROOT = r"D:\GPT-Quant-Platform-Server"
SERVER_URL = "http://127.0.0.1:5000"
RUN_SCRIPT = SERVER_ROOT + r"\server\run_server.ps1"
STOP_EXE = SERVER_ROOT + r"\gpt-quant-platform-stop.exe"


def server_is_running():
    try:
        with urlopen(SERVER_URL, timeout=1.0) as response:
            return 200 <= response.status < 500
    except (URLError, OSError):
        return False


def refresh_status():
    running = server_is_running()

    if running:
        status_var.set("RUNNING")
        detail_var.set("\uc11c\ubc84\uac00 \uc815\uc0c1 \uc2e4\ud589 \uc911\uc785\ub2c8\ub2e4.")
        start_button.config(state="disabled")
        stop_button.config(state="normal")
        open_button.config(state="normal")
    else:
        status_var.set("STOPPED")
        detail_var.set("\uc11c\ubc84\uac00 \uc815\uc9c0\ub418\uc5b4 \uc788\uc2b5\ub2c8\ub2e4.")
        start_button.config(state="normal")
        stop_button.config(state="disabled")
        open_button.config(state="disabled")

    root.after(3000, refresh_status)


def start_server():
    try:
        subprocess.Popen(
            [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                RUN_SCRIPT,
            ],
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        detail_var.set("\uc11c\ubc84 \uc2dc\uc791\uc744 \uc694\uccad\ud588\uc2b5\ub2c8\ub2e4...")
        root.after(2000, refresh_status)
    except Exception as exc:
        messagebox.showerror("START \uc624\ub958", str(exc))


def stop_server():
    if not messagebox.askyesno(
        "\uc11c\ubc84 \uc885\ub8cc",
        "GPT Quant Platform \uc11c\ubc84\ub97c \uc885\ub8cc\ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?",
    ):
        return

    try:
        subprocess.Popen([STOP_EXE])
        detail_var.set("\uc11c\ubc84 \uc885\ub8cc\ub97c \uc694\uccad\ud588\uc2b5\ub2c8\ub2e4...")
        root.after(2000, refresh_status)
    except Exception as exc:
        messagebox.showerror("STOP \uc624\ub958", str(exc))


def open_dashboard():
    import webbrowser
    webbrowser.open(SERVER_URL)


root = tk.Tk()
root.title("GPT Quant Platform - Control")
root.geometry("430x260")
root.resizable(False, False)

title = tk.Label(
    root,
    text="GPT Quant Platform",
    font=("Segoe UI", 18, "bold"),
)
title.pack(pady=(22, 4))

subtitle = tk.Label(
    root,
    text="Server Control",
    font=("Segoe UI", 10),
)
subtitle.pack()

status_frame = tk.Frame(root)
status_frame.pack(pady=(18, 4))

tk.Label(
    status_frame,
    text="SERVER STATUS :",
    font=("Segoe UI", 10, "bold"),
).pack(side="left")

status_var = tk.StringVar(value="CHECKING")
tk.Label(
    status_frame,
    textvariable=status_var,
    font=("Segoe UI", 11, "bold"),
).pack(side="left", padx=(8, 0))

detail_var = tk.StringVar(value="\uc11c\ubc84 \uc0c1\ud0dc\ub97c \ud655\uc778\ud558\uace0 \uc788\uc2b5\ub2c8\ub2e4...")
tk.Label(
    root,
    textvariable=detail_var,
    font=("Malgun Gothic", 9),
).pack(pady=(0, 16))

button_frame = tk.Frame(root)
button_frame.pack()

start_button = tk.Button(
    button_frame,
    text="START",
    width=12,
    height=2,
    command=start_server,
)
start_button.grid(row=0, column=0, padx=5)

stop_button = tk.Button(
    button_frame,
    text="STOP",
    width=12,
    height=2,
    command=stop_server,
)
stop_button.grid(row=0, column=1, padx=5)

open_button = tk.Button(
    root,
    text="OPEN DASHBOARD",
    width=27,
    command=open_dashboard,
)
open_button.pack(pady=(12, 0))

root.after(200, refresh_status)
root.mainloop()
