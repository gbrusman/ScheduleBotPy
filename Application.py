#!/usr/bin/env python
from tkinter import *
from tkinter.ttk import *

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title = "ScheduleBot a.01"
        label_frame = Frame(root)
        label_frame.columnconfigure(0, weight=1)
        label = Label(label_frame, text="Please fill out the information in the form below")
        label.grid(column=0, row=0)
        label_frame.grid(sticky=N+S+E+W, row=0, column=0)
        major_choices = ["AB Mathematics: Plan 1 - General Mathematics", "AB Mathematics: Plan 2 - Secondary Teaching", "BS Mathematics: Plan 1 - General Mathematics", "BS Mathematics: Plan 2 - Secondary Teaching", "Applied Mathematics", "Mathematical Analytics and Operations Research", "Mathematical and Scientific Computation - Computational and Mathematical Biology Emphasis", "Mathematical and Scientific Computation - Computational and Mathematics Emphasis"]
        major_select_box = Combobox(root, values=major_choices, state="readonly", width=45)  # need to talk to IT people about what libraries are okay to import
        major_select_box.grid(row=5, column=0)

        col_count, row_count = root.grid_size()
        root.columnconfigure(0, weight=1)
        for row in range(row_count):
            root.grid_rowconfigure(row, minsize=20)



root = Tk()
w = '500'
h = '400'
root.geometry('{}x{}'.format(w, h))  # https://stackoverflow.com/questions/46069531/python-how-to-center-label-in-tkinter-window?rq=1
app = Window(root)
root.mainloop()


