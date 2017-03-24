import tkinter as tk
from tkinter import ttk
from ScaleMethods import getWeightInGrams
from tkinter import *

MAX = 100

root = Tk()
root.geometry('{}x{}'.format(400, 100))
progress_var = DoubleVar()
theLabel = Label(root, text="Sample text to show")
theLabel.pack()
progressbar = ttk.Progressbar(root, variable=progress_var, maximum=MAX)
progressbar.pack(fill=X, expand=1)

def progress_function():
    print(getWeightInGrams())
    progress_var.set(getWeightInGrams()/10)
    root.update_idletasks()
    root.after(1, progress_function)

progress_function()
root.mainloop()