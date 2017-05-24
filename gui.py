#!/usr/bin/env python3

import os
import tkinter.ttk
from tkinter.filedialog import askdirectory
import backend
import time
import threading

extractor_object = backend.ImageExtractor()


def set_widgets():
    input_path_label.configure(text=extractor_object.input_path)
    output_path_label.configure(text=extractor_object.output_path)
    if extractor_object.check_for_ready():
        if extractor_object.is_extracting:
            for child in input_frame.winfo_children():
                child.configure(state='disabled')
            for child in output_frame.winfo_children():
                child.configure(state='disabled')
            extractor_toggle_button.configure(text="Cancel", state='normal')
        else:
            extractor_toggle_button.configure(text="Start Extracting", state='normal')
            for child in input_frame.winfo_children():
                child.configure(state='normal')
            for child in output_frame.winfo_children():
                child.configure(state='normal')
    else:
        extractor_toggle_button.configure(text="Select Folders First", state='disabled')
    update_progressbar()


def set_directory(is_input):
    if is_input:
        suggested_path = extractor_object.input_path
    else:
        suggested_path = extractor_object.output_path
    proposed_path = askdirectory(initialdir=suggested_path)
    if os.path.isdir(proposed_path):
        if is_input:
            extractor_object.input_path = proposed_path
        else:
            extractor_object.output_path = proposed_path
    set_widgets()


def create_and_run_processing_thread():
    extractor_object_thread = threading.Thread(target=extractor_object.start_extracting)
    extractor_object_thread.start()
    set_widgets()
    while extractor_object_thread.is_alive():
        time.sleep(0.1)
        update_progressbar()
        root_window.update()
    set_widgets()


def update_progressbar():
    extractor_progressbar.configure(maximum=extractor_object.total_file_number,
                                    value=extractor_object.working_file_number)


def toggle_extractor():
    if not extractor_object.is_extracting:
        create_and_run_processing_thread()
    else:
        extractor_object.cancel_extractor = True


root_window = tkinter.Tk()
root_window.title("Label Image Extractor")
root_window.resizable(width=tkinter.FALSE, height=tkinter.FALSE)

input_frame = tkinter.ttk.Frame(root_window)
input_path_button = tkinter.Button(master=input_frame, text="Select Input Directory",
                                   command=lambda: set_directory(True))
input_path_button.pack(side=tkinter.TOP, anchor=tkinter.W)
input_path_label = tkinter.ttk.Label(input_frame)
input_path_label.pack(side=tkinter.TOP, anchor=tkinter.W)


output_frame = tkinter.ttk.Frame(root_window)
output_path_button = tkinter.Button(master=output_frame, text="Select Output Directory",
                                    command=lambda: set_directory(False))
output_path_button.pack(side=tkinter.TOP, anchor=tkinter.W)
output_path_label = tkinter.ttk.Label(output_frame)
output_path_label.pack(side=tkinter.TOP, anchor=tkinter.W)


bottom_frame = tkinter.ttk.Frame(root_window)

extractor_progressbar = tkinter.ttk.Progressbar(bottom_frame)
extractor_progressbar.pack(side=tkinter.LEFT)

extractor_toggle_button = tkinter.ttk.Button(bottom_frame, text="Select Folders First", command=toggle_extractor)
extractor_toggle_button.pack(side=tkinter.RIGHT)
set_widgets()

input_frame.grid(row=0, column=0, sticky=tkinter.W)
output_frame.grid(row=1, column=0, sticky=tkinter.W)
bottom_frame.grid(row=2, column=0, columnspan=2, sticky=tkinter.W+tkinter.E)

root_window.mainloop()
