#!/usr/bin/env python
from tkinter import *


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title = "ScheduleBot a.01"
        self.grid(sticky=N+S+E+W, row=0, column=0)
        label = Label(root, text="Please fill out the information in the form below")
        label.grid(column=0, row=0)
        major_choices = ["AB Mathematics: Plan 1 - General Mathematics", "AB Mathematics: Plan 2 - Secondary Teaching", "BS Mathematics: Plan 1 - General Mathematics", "BS Mathematics: Plan 2 - Secondary Teaching", "Applied Mathematics", "Mathematical Analytics and Operations Research", "Mathematical and Scientific Computation - Computational and Mathematical Biology Emphasis", "Mathematical and Scientific Computation - Computational and Mathematics Emphasis"]
        # w = ComboBox(root, values=choices)  # need to talk to IT people about what libraries are okay to import

        root.columnconfigure(0, weight=1)



root = Tk()
w = '500'
h = '400'
root.geometry('{}x{}'.format(w, h))  # https://stackoverflow.com/questions/46069531/python-how-to-center-label-in-tkinter-window?rq=1
app = Window(root)
root.mainloop()


