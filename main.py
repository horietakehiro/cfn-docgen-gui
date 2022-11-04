import time
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pathlib import Path
import os
import subprocess

import config

manage_cache = config.cache_manager()

def monitor_exec_status(proc:subprocess.Popen, msg:str, dirname:str):
    exec_button["state"] = "disable"
    reset_str = ".........."
    if proc.poll() is None:
        if msg.endswith(reset_str):
            msg = msg.replace(reset_str, "")
        msg = msg + "."
        exec_message.set(msg)
        root.after(500, monitor_exec_status, proc, msg, dirname)
    else:
        if proc.returncode == 0:
            exec_message.set(f"Succeeded!!\nDocs has been saved at {dirname}")
            subprocess.Popen(args=["explorer.exe", dirname])

        else:
            log_path = str(Path(config.LOG_FILE))
            exec_message.set(f"Failed!!\nSee log messages at {log_path}")
            subprocess.Popen(args=["explorer.exe", log_path])
        exec_button["state"] = "normal"
        return


def on_file_select():
    cache = manage_cache()
    prev_dir = cache["PrevDir"]

    file = filedialog.askopenfile(
        initialdir=prev_dir, filetypes=[("json", "*.json"), ("yaml", "*.yaml")],

    )
    if file:
        selected_filename.set(str(Path(file.name)))
        cache = manage_cache("PrevDir", str(Path(os.path.dirname(file.name))))

def exec():

    dirname = os.path.dirname(selected_filename.get())

    args = ["cfn-docgen", "--in", selected_filename.get(), "--fmt", selected_fmt.get()]
    proc = subprocess.Popen(args)
    # create process file
    root.after(0, monitor_exec_status, proc, "cfn-docgen is now running", dirname)


if __name__ == "__main__":

    root = Tk()
    root.title('cfn-docgen')
    root.geometry("500x500")

    file_frame = ttk.Frame(root, padding=10)
    file_frame.grid(sticky=(N, W, S, E))

    fmt_frame = ttk.Frame(root, padding=10)
    fmt_frame.grid(sticky=(N, W, S, E))

    exec_frame = ttk.Frame(root, padding=10)
    exec_frame.grid(sticky=(N, W, S, E))


    file_button = ttk.Button(
        file_frame, text='Select File', width=10,
        command=on_file_select,
    )
    file_button.grid(row=0, column=0, sticky=(W))
    selected_filename = StringVar()
    selected_filename_label = ttk.Label(file_frame, textvariable=selected_filename)
    selected_filename_label.grid(row=0, column=1)


    cache = manage_cache()
    selected_fmt = StringVar(value=cache["PrevFmt"])
    fmt_buttons = []
    for i, fmt in enumerate(["xlsx", "csv", "md", "html"]):
        fmt_buttons.append(
            ttk.Radiobutton(
                fmt_frame,
                text=fmt,
                value=fmt,
                variable=selected_fmt,
                command=lambda: manage_cache("PrevFmt", selected_fmt.get())
            )
        )
        fmt_buttons[i].grid(row=1, column=i)


    exec_message = StringVar()
    exec_message_label = ttk.Label(exec_frame, textvariable=exec_message)
    exec_message_label.grid(row=3, column=0)
    exec_button = ttk.Button(
        exec_frame, text="Run", width=10,
        command=exec,
    )
    exec_button.grid(row=2, column=0, sticky=(W))


    root.mainloop()
