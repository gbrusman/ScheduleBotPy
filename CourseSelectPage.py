import tkinter as tk
from tkinter.ttk import *
import tkinter.font as tkfont
from Course import Course
from Student import Student
from Schedule import Schedule
from AcademicTime import AcademicTime
from ScheduleBlock import ScheduleBlock
#import psycopg2
import csv

class CourseSelectPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        prompt_frame = Frame(self)
        prompt_frame.grid_columnconfigure(0, weight=1)
        prompt_frame.grid(sticky="nsew", row=0, columnspan=10)
        prompt = Label(prompt_frame, text="Please select which classes you have taken, or are currently taking.")
        prompt.grid(column=0, row=0, columnspan=2, in_=prompt_frame)

        #self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, minsize=50)
        self.grid_columnconfigure(0, weight=1)


        self.cbox_frame = Frame(self)
        self.cbox_frame.grid(row=3, sticky="nsew")
        self.cbox_list = []
        self.create_checkboxes()

        for i in range(10):
            self.cbox_frame.grid_rowconfigure(i, weight=1)

        button_frame = Frame(self)
        button_frame.grid(row=7, sticky="ew")
        back_button = Button(button_frame, text="Back", command=lambda: self.go_back())
        back_button.grid(row=25, column=0, padx=5, pady=5, sticky="sw", in_=button_frame)
        next_button = Button(button_frame, text="Next", command=lambda: self.goto_interest_select())
        next_button.grid(row=25, column=1, padx=5, pady=5, sticky="se", in_=button_frame)
        for i in range(2):
            button_frame.grid_columnconfigure(i, weight=1)
        col_size, row_size = self.grid_size()
        for i in range(row_size):
            self.grid_rowconfigure(i, minsize=20, weight=1)


    def create_checkboxes(self):
        col = 0
        row = 1
        count = 0
        # try:
        #     conn = psycopg2.connect(host="localhost", database="Math Courses", user="postgres", password="MN~D=bp~+WR2/ppy")
        #     cur = conn.cursor()
        #     cur.execute("SELECT name FROM courses ORDER BY display_index ASC;")
        #     for record in cur:
        #         checkbox = Checkbutton(self.cbox_frame, text=record[0].replace("_", " "))
        #         checkbox.invoke()  # turns checkbox from default to on
        #         checkbox.invoke()  # turns checkbox from on to off
        #         checkbox.grid(row=row, column=col, sticky="nsew", padx=5, in_=self.cbox_frame)
        #         self.cbox_list.append(checkbox)
        #         row += 1
        #         count += 1
        #         if count == 10:  # only 10 checkboxes per column
        #             self.cbox_frame.grid_columnconfigure(col, weight=1)
        #             col += 1
        #             row = 1
        #             count = 0
        #     conn.close()
        # except:
        #     with open('database/test/courses_string.csv', newline='') as courses_csv:
        #         reader = csv.reader(courses_csv)
        #         for record in reader:
        #             if record[0] == 'name':
        #                 continue
        #             checkbox = Checkbutton(self.cbox_frame, text=record[0].replace("_", " "))
        #             checkbox.invoke()  # turns checkbox from default to on
        #             checkbox.invoke()  # turns checkbox from on to off
        #             checkbox.grid(row=row, column=col, sticky="nsew", padx=5, in_=self.cbox_frame)
        #             self.cbox_list.append(checkbox)
        #             row += 1
        #             count += 1
        #             if count == 10:  # only 10 checkboxes per column
        #                 self.cbox_frame.grid_columnconfigure(col, weight=1)
        #                 col += 1
        #                 row = 1
        #                 count = 0

        with open('database/test/courses_string.csv', newline='') as courses_csv:

            reader = csv.reader(courses_csv)
            for record in reader:
                if record[0] == 'name':
                    continue
                checkbox = Checkbutton(self.cbox_frame, text=record[0].replace("_", " "))
                checkbox.invoke()  # turns checkbox from default to on
                checkbox.invoke()  # turns checkbox from on to off
                checkbox.grid(row=row, column=col, sticky="nsew", padx=5, in_=self.cbox_frame)
                self.cbox_list.append(checkbox)
                row += 1
                count += 1
                if count == 10:  # only 10 checkboxes per column
                    self.cbox_frame.grid_columnconfigure(col, weight=1)
                    col += 1
                    row = 1
                    count = 0

    def go_back(self):
        if self.controller.student.major == "LAMA":
            self.controller.show_frame("AppliedSeriesChoicePage")
        else:
            self.controller.show_frame("MajorSelectPage")

    def goto_interest_select(self):
        self.get_info_from_cboxes()
        self.controller.show_frame("InterestSelectPage")

    def get_info_from_cboxes(self):
        self.controller.student.classes_taken.clear()
        for cbox in self.cbox_list:
            if cbox.instate(['selected']):  # https://stackoverflow.com/questions/4236910/getting-tkinter-check-box-state
                self.controller.student.classes_taken[(cbox.cget("text")).replace(" ", "_")] = self.controller.classes_by_name[(cbox.cget("text")).replace(" ", "_")]  # https://stackoverflow.com/questions/33545085/how-to-get-the-text-from-a-checkbutton-in-python-tkinter

