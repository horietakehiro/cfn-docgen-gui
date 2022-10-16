import time
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import os
import subprocess

import config

manage_cache = config.cache_manager()

def monitor_exec_status(proc:subprocess.Popen, msg:str):
    exec_button["state"] = "disable"
    reset_str = ".........."
    if proc.poll() is None:
        if msg.endswith(reset_str):
            msg = msg.replace(reset_str, "")
        msg = msg + "."
        exec_message.set(msg)
        root.after(500, monitor_exec_status, proc, msg)
    else:
        if proc.returncode == 0:
            exec_message.set("Succeeded!!")
        else:
            exec_message.set("Failed.")
        exec_button["state"] = "normal"
        return


def on_file_select():
    cache = manage_cache()
    prev_dir = cache["prev_dir"]

    file = filedialog.askopenfile(
        initialdir=prev_dir, filetypes=[("json", "*.json"), ("yaml", "*.yaml")]
    )
    if file:
        selected_filename.set(file.name)
        cache = manage_cache("prev_dir", os.path.dirname(file.name))    

def exec():

    args = ["cfn-docgen", "--in", selected_filename.get(), "--fmt", selected_fmt.get()]
    proc = subprocess.Popen(args)
    # create process file
    root.after(0, monitor_exec_status, proc, "cfn-docgen is now running")


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
    selected_fmt = StringVar(value=cache["prev_fmt"])
    fmt_buttons = []
    for i, fmt in enumerate(["xlsx", "csv", "md", "html"]):
        fmt_buttons.append(
            ttk.Radiobutton(
                fmt_frame,
                text=fmt,
                value=fmt,
                variable=selected_fmt,
                command=lambda: manage_cache("prev_fmt", selected_fmt.get())
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
