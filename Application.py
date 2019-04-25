#!/usr/bin/env python
from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkfont

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        

    def init_window(self):
        self.master.title = "ScheduleBot a.01"
        prompt_frame = Frame(root)
        prompt_frame.grid_columnconfigure(0, weight=1)
        prompt_frame.grid(sticky=N + S + E + W, row=0, columnspan=2)
        prompt = Label(prompt_frame, text="Please fill out the information in the form below")
        prompt.grid(column=0, row=0, columnspan=2, in_=prompt_frame)


        major_frame = Frame(root)
        major_frame.grid(column=0,row=5)
        major_label = Label(major_frame, text="Major: ")
        major_label.grid(column=0, row=0, in_=major_frame, pady=20)
        major_choices = ["AB Mathematics: Plan 1 - General Mathematics", "AB Mathematics: Plan 2 - Secondary Teaching", "BS Mathematics: Plan 1 - General Mathematics", "BS Mathematics: Plan 2 - Secondary Teaching", "Applied Mathematics", "Mathematical Analytics and Operations Research", "Mathematical and Scientific Computation - Bio Emphasis", "Mathematical and Scientific Computation - Math Emphasis"]
        major_select_box = Combobox(major_frame, values=major_choices, state="readonly", width=45)  # need to talk to IT people about what libraries are okay to import

        major_select_box.grid(row=0, column=1, in_=major_frame, sticky=E+W, padx=5)

        cur_quarter_label = Label(major_frame, text="Current Quarter: ")
        cur_quarter_label.grid(column=0, row=1, in_=major_frame, pady=10)
        cur_quarter_choices = ["Fall", "Winter", "Spring"]
        cur_quarter_select_box=Combobox(major_frame, values=cur_quarter_choices, state="readonly", width=25)
        cur_quarter_select_box.grid(row=1, column=1, in_=major_frame, sticky=W, padx=5)

        cur_year_label = Label(major_frame, text="Current Year: ")
        cur_year_label.grid(column=0, row=2, in_=major_frame, pady=0)
        cur_quarter_entry = Entry(major_frame, width=15)
        cur_quarter_entry.grid(row=2, column=1, in_=major_frame, sticky=W, padx=5)

        grad_quarter_label = Label(major_frame, text="Graduation Quarter: ")
        grad_quarter_label.grid(column=0, row=4, in_=major_frame, pady=10)
        grad_quarter_choices = ["Fall", "Winter", "Spring"]
        grad_quarter_select_box = Combobox(major_frame, values=grad_quarter_choices, state="readonly", width=25)
        grad_quarter_select_box.grid(row=4, column=1, in_=major_frame, sticky=W, padx=5)

        grad_year_label = Label(major_frame, text="Graduation Year: ")
        grad_year_label.grid(column=0, row=5, in_=major_frame, pady=0)
        grad_quarter_entry = Entry(major_frame, width=15)
        grad_quarter_entry.grid(row=5, column=1, in_=major_frame, sticky=W, padx=5)

        next_button = Button(root, text="Next")
        next_button.grid(row=9, padx=5, pady=10, sticky=S+E)



        col_count, row_count = root.grid_size()
        root.grid_columnconfigure(0, weight=1)
        #root.rowconfigure(0, weight=1)
        for row in range(row_count):
            root.grid_rowconfigure(row, minsize=20)

        major_frame.grid_rowconfigure(3, minsize=20)  # separates current year stuff from grad year stuff




root = Tk()
w = '500'
h = '400'
root.geometry('{}x{}'.format(w, h))  # https://stackoverflow.com/questions/46069531/python-how-to-center-label-in-tkinter-window?rq=1
app = Window(root)
root.mainloop()


