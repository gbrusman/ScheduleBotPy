import tkinter as tk
from tkinter.ttk import *
import tkinter.font as tkfont
from Course import Course
from Student import Student
from Schedule import Schedule
from AcademicTime import AcademicTime
from ScheduleBlock import ScheduleBlock

class InterestSelectPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        prompt_frame = Frame(self)
        prompt_frame.grid_columnconfigure(0, weight=1)
        prompt_frame.grid(sticky="nsew", row=0, columnspan=2)
        prompt = Label(prompt_frame, text="OPTIONAL: Please select which fields of mathematics interest you.")
        prompt.grid(column=0, row=0, columnspan=2, in_=prompt_frame)

        cbox_frame = Frame(self)
        cbox_frame.grid(row=6, column=0, sticky="nsew")
        self.cbox_list = []
        interests = ["Teaching", "Geometry", "Physics", "Biology", "Computers", "Finance", "Abstract", "Data Analysis"]
        row = 0
        for interest in interests:
            checkbox = Checkbutton(cbox_frame, text=interest)
            checkbox.invoke()  # turns checkbox from default to on
            checkbox.invoke()  # turns checkbox from on to off
            checkbox.grid(row=row, sticky="nsew", padx=5, in_=cbox_frame)
            self.cbox_list.append(checkbox)
            row += 1
        for i in range(len(interests)):
            cbox_frame.grid_rowconfigure(i, weight=1)
        #cbox_frame.grid_columnconfigure(1, weight=1)

        button_frame = Frame(self)
        button_frame.grid(row=14, sticky="ew")
        back_button = Button(button_frame, text="Back", command=lambda: controller.show_frame("CourseSelectPage"))
        back_button.grid(row=25, column=0, padx=5, pady=10, sticky="sw", in_=button_frame)
        next_button = Button(button_frame, text="Next", command=lambda: self.goto_schedule_display())
        next_button.grid(row=25, column=1, padx=5, pady=10, sticky="se", in_=button_frame)

        for i in range(2):
            button_frame.grid_columnconfigure(i, weight=1)

        num_cols, num_rows = self.grid_size()
        for i in range(num_rows):
            self.grid_rowconfigure(i, minsize=20)
        #for i in range(num_cols):
            #self.grid_columnconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def goto_schedule_display(self):
        self.get_info_from_cboxes()
        sched_display = self.controller.get_page('ScheduleDisplayPage')
        sched_display.init_schedule()
        self.controller.show_frame("ScheduleDisplayPage")


    def get_info_from_cboxes(self):
        self.controller.student.interests.clear()
        for cbox in self.cbox_list:
            if cbox.instate(['selected']):  # https://stackoverflow.com/questions/4236910/getting-tkinter-check-box-state
                self.controller.student.interests.append(cbox.cget("text"))  # https://stackoverflow.com/questions/33545085/how-to-get-the-text-from-a-checkbutton-in-python-tkinter

