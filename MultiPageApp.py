#!/usr/bin/env python
import tkinter as tk
from tkinter.ttk import *
import tkinter.font as tkfont

#  https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

class MultiPageApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.page_names = [MajorSelectPage]
        for F in self.page_names:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MajorSelectPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class MajorSelectPage(tk.Frame):
    def __init__(self, parent, controller):
        prompt_frame = Frame(parent)
        prompt_frame.grid_columnconfigure(0, weight=1)
        prompt_frame.grid(sticky=tk.N + tk.S + tk.E + tk.W, row=0, columnspan=2)
        prompt = Label(prompt_frame, text="Please fill out the information in the form below")
        prompt.grid(column=0, row=0, columnspan=2, in_=prompt_frame)

        major_frame = Frame(parent)
        major_frame.grid(column=0, row=5)
        major_label = Label(major_frame, text="Major: ")
        major_label.grid(column=0, row=0, in_=major_frame, pady=20)
        major_choices = ["AB Mathematics: Plan 1 - General Mathematics", "AB Mathematics: Plan 2 - Secondary Teaching",
                         "BS Mathematics: Plan 1 - General Mathematics", "BS Mathematics: Plan 2 - Secondary Teaching",
                         "Applied Mathematics", "Mathematical Analytics and Operations Research",
                         "Mathematical and Scientific Computation - Bio Emphasis",
                         "Mathematical and Scientific Computation - Math Emphasis"]
        major_select_box = Combobox(major_frame, values=major_choices, state="readonly",
                                    width=45)  # need to talk to IT people about what libraries are okay to import

        major_select_box.grid(row=0, column=1, in_=major_frame, sticky=tk.E + tk.W, padx=5)

        cur_quarter_label = Label(major_frame, text="Current Quarter: ")
        cur_quarter_label.grid(column=0, row=1, in_=major_frame, pady=10)
        cur_quarter_choices = ["Fall", "Winter", "Spring"]
        cur_quarter_select_box = Combobox(major_frame, values=cur_quarter_choices, state="readonly", width=25)
        cur_quarter_select_box.grid(row=1, column=1, in_=major_frame, sticky=tk.W, padx=5)

        cur_year_label = Label(major_frame, text="Current Year: ")
        cur_year_label.grid(column=0, row=2, in_=major_frame, pady=0)
        cur_quarter_entry = Entry(major_frame, width=15)
        cur_quarter_entry.grid(row=2, column=1, in_=major_frame, sticky=tk.W, padx=5)

        grad_quarter_label = Label(major_frame, text="Graduation Quarter: ")
        grad_quarter_label.grid(column=0, row=4, in_=major_frame, pady=10)
        grad_quarter_choices = ["Fall", "Winter", "Spring"]
        grad_quarter_select_box = Combobox(major_frame, values=grad_quarter_choices, state="readonly", width=25)
        grad_quarter_select_box.grid(row=4, column=1, in_=major_frame, sticky=tk.W, padx=5)

        grad_year_label = Label(major_frame, text="Graduation Year: ")
        grad_year_label.grid(column=0, row=5, in_=major_frame, pady=0)
        grad_quarter_entry = Entry(major_frame, width=15)
        grad_quarter_entry.grid(row=5, column=1, in_=major_frame, sticky=tk.W, padx=5)

        next_button = Button(parent, text="Next")
        next_button.grid(row=9, padx=5, pady=10, sticky=tk.S + tk.E)

        col_count, row_count = parent.grid_size()
        parent.grid_columnconfigure(0, weight=1)
        # parent.rowconfigure(0, weight=1)
        for row in range(row_count):
            parent.grid_rowconfigure(row, minsize=20)

        major_frame.grid_rowconfigure(3, minsize=20)  # separates current year stuff from grad year stuff


if __name__ == "__main__":
    app = MultiPageApp()
    app.mainloop()