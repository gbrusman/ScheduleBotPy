import tkinter as tk
from tkinter.ttk import *
import tkinter.font as tkfont
from Course import Course
from Student import Student
from Schedule import Schedule
from AcademicTime import AcademicTime
from ScheduleBlock import ScheduleBlock


class ScheduleDisplayPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def init_schedule(self):
        schedule_data = Schedule(self.controller.student, self.controller.classes_offered)
        schedule = schedule_data.schedule
        start_time = AcademicTime(self.controller.student.start_time.year, self.controller.student.start_time.quarter)
        grad_time = AcademicTime(self.controller.student.grad_time.year,self.controller.student.grad_time.quarter)
        table_start_time = AcademicTime(start_time.year, start_time.quarter)

        while table_start_time.quarter != "Fall":
            table_start_time = table_start_time.reverse_time()

        cur_time = AcademicTime(start_time.year, start_time.quarter)
        start = True
        first_year = True
        year_index = 0
        year_frame = Frame(self)
        quarter_index = 0

        while cur_time.year != grad_time.year or (cur_time.year == grad_time.year and cur_time.quarter != "Fall"):
            if cur_time.quarter == "Fall":
                if first_year:
                    year_frame.grid(row=year_index, in_=self)
                    first_year = False
                year_frame = Frame(self)
                year_index += 1
                year_frame.grid(row=year_index, in_=self)
                quarter_index = 0
            cur_time = cur_time.progress_time()

            if start_time.quarter == "Spring":
                start = False
            if start:
                while table_start_time != cur_time:  # adding in invisible columns, could also try adding in real blank columns and setting min columnwidth
                    block_box = Frame(year_frame)
                    block_box.grid(column=quarter_index, in_=year_frame, sticky="ew")  #sticky might be wrong, also might need row/column
                    title = Label(block_box, text=table_start_time.quarter + " " + str(table_start_time.year))
                    title.grid(row=0, column=0, in_=block_box)
                    blank = Entry(block_box, width=20, state="readonly")
                    blank.grid(row=1, column=0, in_=block_box, sticky="w")
                    quarter_index += 1
                    table_start_time = table_start_time.progress_time()
                #start = False

            #block_box = Frame(year_frame)
            if cur_time in schedule:  # FIXME: this if statement is never getting triggered, NEED TO FIX __hash__ IN ACADEMIC TIME
                if len(schedule.get(cur_time).courses) > 0:
                    course0 = Entry(block_box, width=20)
                    course0.insert(0, schedule.get(cur_time).courses[0].name)  # https://stackoverflow.com/questions/14847243/how-can-i-insert-a-string-in-a-entry-widget-that-is-in-the-readonly-state
                    course0.configure(state='readonly')
                    course0.grid(row=1, pady=5, sticky="w", in_=block_box)
                if len(schedule.get(cur_time).courses) > 1:
                    course1 = Entry(block_box, width=20)
                    course1.insert(1, schedule.get(cur_time).courses[1].name)
                    course1.configure(state='readonly')
                    course1.grid(row=2, pady=5, sticky="w", in_=block_box)
                if len(block_box.children) > 1:
                    block_box.grid(row=0, column=quarter_index, padx=10, sticky="ew", in_=year_frame)

