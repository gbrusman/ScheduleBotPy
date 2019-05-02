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
        start_time = AcademicTime(self.controller.student.start_time)
        grad_time = AcademicTime(self.controller.student.grad_time)
        table_start_time = AcademicTime(start_time)

        while table_start_time.quarter != "Fall":
            table_start_time = table_start_time.reverse_time()

        cur_time = AcademicTime(start_time)
        start = True
        first_year = True
        year_index = 0
        year_frame = Frame(self)
        quarter_index = 0

        while cur_time.year != grad_time.year or (cur_time.year == grad_time.year and cur_time.quarter != "Fall"):
            if cur_time.quarter == "Spring":
                if first_year:
                    year_frame.grid(self, row=year_index, in_=self)
                    first_year = False
                year_frame = Frame(self)
                year_index += 1
                year_frame.grid(self, row=year_index, in_=self)
                quarter_index = 0
            cur_time = AcademicTime(cur_time.progress_time())

            if start_time.quarter == "Spring":
                start = False
            if start:
                while table_start_time != cur_time:  # adding in invisible columns, could also try adding in real blank columns and setting min columnwidth
                    block_box = Frame(year_frame)
                    block_box.grid(column=quarter_index, in_=year_frame, sticky="ew") #sticky might be wrong, also might need row/column
                    title = Label(block_box, text=table_start_time.quarter + " " + table_start_time.year)
                    title.grid(row=0, column=0, in_=block_box)
                    quarter_index += 1

                if cur_time in schedule.keys():
                    if len(schedule.get(cur_time).courses) > 0:
                        course0 = Entry(block_box, width=20, state="readonly", text=schedule.get(cur_time).courses[0])
                        course0.grid(row=0, pady=5, sticky="w", in_=block_box)
                    if len(schedule.get(cur_time).courses) > 1:
                        course1 = Entry(block_box, width=20, state="readonly", text=schedule.get(cur_time).courses[1])
                        course1.grid(row=1, pady=5, sticky="w", in_=block_box)
                    if len(block_box.children) > 1:
                        block_box.grid(column=quarter_index, padx=10, sticky="ew", in_=year_frame)

