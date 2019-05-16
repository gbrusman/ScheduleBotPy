import tkinter as tk
from tkinter.ttk import *
import tkinter.font as tkfont
from Course import Course
from Student import Student
from Schedule import Schedule
from AcademicTime import AcademicTime
from ScheduleBlock import ScheduleBlock
import copy


class ScheduleDisplayPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.schedule_frame = Frame(self)
        self.schedule_frame.grid(row=1, sticky="ew")
        button_frame = Frame(self)
        button_frame.grid(row=14, sticky="ew")
        back_button = Button(button_frame, text="Back", command=lambda: controller.show_frame("InterestSelectPage"))
        back_button.grid(row=25, column=0, padx=5, pady=10, sticky="sw", in_=button_frame)
        color_frame = Frame(self)
        color_frame.grid(row=13, sticky="ew", in_=self)
        color_frame.columnconfigure(0, weight=1)
        color_canvas = tk.Canvas(self, width=100, height=25)
        color_canvas.create_rectangle(5, 0, 30, 25, fill="#43f2c0")
        color_canvas.create_text(150, 10, text="= Enrichment Course", anchor="e")
        color_canvas.grid(sticky="nsew", in_=color_frame)

    def init_schedule(self):
        failed = False
        # Need to clear frame
        for widget in self.schedule_frame.winfo_children():
            widget.destroy()
        # Need to make new student object because it gets mutated when creating schedule, need to handle case where user hits back button.
        student = copy.deepcopy(self.controller.student)
        classes_offered = self.controller.classes_offered.copy()  # Need to make copy of classes_offered for same reason as above
        schedule_data = Schedule(student, classes_offered)
        if not schedule_data.is_success():
            failed = True
        schedule = schedule_data.schedule
        start_time = AcademicTime(student.start_time.year, student.start_time.quarter)
        grad_time = AcademicTime(student.grad_time.year, student.grad_time.quarter)
        table_start_time = AcademicTime(start_time.year, start_time.quarter)

        failed_label = tk.Label(self, fg="red",
                                text="")
        failed_label.grid(row=0, column=0, pady=10, padx=10, sticky="new", in_=self)

        while table_start_time.quarter != "Fall":
            table_start_time = table_start_time.reverse_time()

        cur_time = AcademicTime(start_time.year, start_time.quarter)
        start = True
        first_year = True
        year_index = 0
        year_frame = Frame(self)
        quarter_index = 0
        finish_time = grad_time.progress_time()  # probably doesn't work because need copy of grad_time

        while cur_time != finish_time and cur_time != finish_time.progress_time() and cur_time != finish_time.progress_time().progress_time():
            if cur_time.quarter == "Spring":
                if first_year:
                    year_frame.grid(row=year_index, in_=self.schedule_frame)
                    first_year = False
                year_frame = Frame(self.schedule_frame)
                year_index += 1
                year_frame.grid(row=year_index, in_=self.schedule_frame, pady=10)
                quarter_index = 0
            cur_time = cur_time.progress_time()

            if start_time.quarter == "Spring":
                start = False
            if start:
                while table_start_time != cur_time:  # adding in invisible columns, could also try adding in real blank columns and setting min columnwidth
                    block_box = Frame(year_frame)
                    block_box.grid(row=0, column=quarter_index, in_=year_frame, sticky="ew", padx=10)  # sticky might be wrong, also might need row/column
                    title = Label(block_box, text="", width=20)  # display blank columns to make display uniform. Width = 20 because that is width of regular block_box
                    title.grid(row=0, column=0, in_=block_box)
                    quarter_index += 1
                    table_start_time = table_start_time.progress_time()
                start = False

            block_box = Frame(year_frame)
            title = Label(block_box, text=cur_time.quarter + " " + str(cur_time.year))
            title.grid(row=0, column=0, in_=block_box)

            if cur_time == finish_time:  # insert blank columns after end to keep the layout consistent
                while cur_time.quarter != "Fall":
                    block_box = Frame(year_frame)
                    title = Label(block_box, text="", width=20)
                    title.grid(row=0, column=0, in_=block_box)
                    block_box.grid(row=0, column=quarter_index, in_=year_frame, sticky="ew", padx=10)
                    cur_time = cur_time.progress_time()
                    quarter_index += 1

            if cur_time in schedule:
                if len(schedule.get(cur_time).courses) > 0:
                    course0 = tk.Entry(block_box, width=20, readonlybackground="White")  # http://www.tcl.tk/man/tcl/TkCmd/entry.htm#M9
                    course0.insert(0, schedule.get(cur_time).courses[0].name)  # https://stackoverflow.com/questions/14847243/how-can-i-insert-a-string-in-a-entry-widget-that-is-in-the-readonly-state
                    course0.configure(state='readonly')
                    if not schedule.get(cur_time).courses[0].required[student.major]:
                        course0.configure(readonlybackground="#43f2c0")
                    course0.grid(row=1, pady=5, sticky="w", in_=block_box)
                if len(schedule.get(cur_time).courses) > 1:
                    course1 = tk.Entry(block_box, width=20, readonlybackground="White")
                    course1.insert(1, schedule.get(cur_time).courses[1].name)
                    course1.configure(state='readonly')
                    if not schedule.get(cur_time).courses[1].required[student.major]:
                        course1.configure(readonlybackground="#43f2c0")
                    course1.grid(row=2, pady=5, sticky="w", in_=block_box)
                else:
                    blank_course = Label(block_box, width=20, text="")
                    blank_course.grid(row=2, pady=5, sticky="w", in_=block_box)
                if len(block_box.children) > 1:
                    block_box.grid(row=0, column=quarter_index, padx=10, sticky="ew", in_=year_frame)
                    quarter_index += 1

        if failed:
            failed_label.configure(text="WARNING: This schedule does not contain all of the classes you will need to graduate. Consider talking to an advisor in person for additional advice.")
            self.grid_rowconfigure(0, minsize=35)
        col_size, row_size = self.grid_size()  # do the same thing with schedule_frame
        for i in range(row_size):
            self.grid_rowconfigure(i, weight=1)
        for i in range(col_size):
            self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(row_size - 1, minsize=35)

        col_size, row_size = self.schedule_frame.grid_size()  # do the same thing with schedule_frame
        for i in range(row_size):
            self.schedule_frame.grid_rowconfigure(i, weight=1, minsize=7)
        for i in range(col_size):
            self.schedule_frame.grid_columnconfigure(i, weight=1)

