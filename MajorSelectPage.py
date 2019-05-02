import tkinter as tk
from tkinter.ttk import *
import tkinter.font as tkfont
from Course import Course
from Student import Student
from Schedule import Schedule
from AcademicTime import AcademicTime
from ScheduleBlock import ScheduleBlock


class MajorSelectPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.major = tk.StringVar()
        self.cur_quarter = tk.StringVar()
        self.grad_quarter = tk.StringVar()
        self.cur_year = 0
        self.grad_year = 0
        prompt_frame = Frame(self)
        prompt_frame.grid_columnconfigure(0, weight=1)
        prompt_frame.grid(sticky="nsew", row=0, columnspan=2)
        prompt = Label(prompt_frame, text="Please fill out the information in the form below")
        prompt.grid(column=0, row=0, columnspan=2, in_=prompt_frame)
        self.err_msg = tk.Label(prompt_frame, text="", fg="red")  # needed to use tk label here for fg option
        self.err_msg.grid(column=0, row=1, columnspan=2, in_=prompt_frame)

        major_frame = Frame(self)
        major_frame.grid(column=0, row=5)
        major_label = Label(major_frame, text="Major: ")
        major_label.grid(column=0, row=0, in_=major_frame, pady=20)
        major_choices = ["AB Mathematics: Plan 1 - General Mathematics", "AB Mathematics: Plan 2 - Secondary Teaching",
                         "BS Mathematics: Plan 1 - General Mathematics", "BS Mathematics: Plan 2 - Secondary Teaching",
                         "Applied Mathematics", "Mathematical Analytics and Operations Research",
                         "Mathematical and Scientific Computation - Bio Emphasis",
                         "Mathematical and Scientific Computation - Math Emphasis"]
        self.major_select_box = Combobox(major_frame, values=major_choices, textvariable=self.major, state="readonly",
                                    width=45)  # need to talk to IT people about what libraries are okay to import

        self.major_select_box.grid(row=0, column=1, in_=major_frame, sticky=tk.E + tk.W, padx=5)
        self.major_select_box.bind("<<ComboboxSelected>>", self.get_major_value)


        cur_quarter_label = Label(major_frame, text="Current Quarter: ")
        cur_quarter_label.grid(column=0, row=1, in_=major_frame, pady=10)
        cur_quarter_choices = ["Fall", "Winter", "Spring"]
        self.cur_quarter_select_box = Combobox(major_frame, values=cur_quarter_choices, textvariable=self.cur_quarter, state="readonly", width=25)
        self.cur_quarter_select_box.grid(row=1, column=1, in_=major_frame, sticky=tk.W, padx=5)
        #self.cur_quarter_select_box.bind("<<ComboboxSelected>>", self.get_cur_quarter_value)

        cur_year_label = Label(major_frame, text="Current Year: ")
        cur_year_label.grid(column=0, row=2, in_=major_frame, pady=0)
        self.cur_year_entry = Entry(major_frame, width=15)
        self.cur_year_entry.grid(row=2, column=1, in_=major_frame, sticky=tk.W, padx=5)

        grad_quarter_label = Label(major_frame, text="Graduation Quarter: ")
        grad_quarter_label.grid(column=0, row=4, in_=major_frame, pady=10)
        grad_quarter_choices = ["Fall", "Winter", "Spring"]
        self.grad_quarter_select_box = Combobox(major_frame, values=grad_quarter_choices, textvariable=self.grad_quarter, state="readonly", width=25)
        self.grad_quarter_select_box.grid(row=4, column=1, in_=major_frame, sticky=tk.W, padx=5)

        grad_year_label = Label(major_frame, text="Graduation Year: ")
        grad_year_label.grid(column=0, row=5, in_=major_frame, pady=0)
        self.grad_year_entry = Entry(major_frame, width=15)
        self.grad_year_entry.grid(row=5, column=1, in_=major_frame, sticky=tk.W, padx=5)

        next_button = Button(self, text="Next", command=lambda: self.goto_course_select())
        next_button.grid(row=12, padx=5, pady=10, sticky=tk.S + tk.E)

        col_count, row_count = self.grid_size()
        self.grid_columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=20)

        major_frame.grid_rowconfigure(3, minsize=20)  # separates current year stuff from grad year stuff


    def goto_course_select(self):
        if self.validate_input():
            cur_year = int(self.cur_year_entry.get())
            grad_year = int(self.grad_year_entry.get())

            #Set Student times here
            self.controller.student.cur_time = AcademicTime(cur_year, self.cur_quarter.get())
            self.controller.student.start_time = AcademicTime(cur_year, self.cur_quarter.get())
            self.controller.student.grad_time = AcademicTime(grad_year, self.grad_quarter.get())

            self.controller.show_frame("CourseSelectPage")


    def validate_input(self):
        if not self.major.get():
            self.err_msg["text"] = "Please select a major"
            return False
        if not self.cur_quarter.get():
            self.err_msg["text"] = "Please select a value for Current Quarter"
            return False
        if self.cur_year_entry.get() == "" or self.grad_year_entry.get() == "":
            self.err_msg["text"] = "Please ensure you have entered values for Current Year and Graduation Year"
            return False
        if not self.grad_quarter.get():
            self.err_msg["text"] = "Please select a value for Graduation Quarter"
            return False
        if not self.cur_year_entry.get().isdigit() and self.grad_year_entry.get().isdigit():   # checks if year entries are integers
            self.err_msg["text"] = "Please ensure your year values are integers"
            return False
        time_balance = self.are_times_balanced()
        if not time_balance:
            self.err_msg["text"] = "Please ensure the Graduation Time is after the Current Time"
            return False
        return True

    def are_times_balanced(self):
        year_balance = int(self.grad_year_entry.get()) > int(self.cur_year_entry.get())
        years_equal = int(self.cur_year_entry.get()) == int(self.grad_year_entry.get())
        if years_equal:
            if self.cur_quarter.get() == "Fall":  # if FALL and years are equal, then cur_time >= grad_time
                return False
            elif self.cur_quarter.get() == "Spring":  # if SPRING and years are equal, then WINTER of same year is before SPRING
                if self.grad_quarter.get() == "Winter" or self.grad_quarter.get() == "Spring":
                    return False
            elif self.cur_quarter.get() == "Winter":  # if WINTER and years are equal, then only WINTER is invalid since grad time would equal cur time
                if self.grad_quarter.get() == "Winter":
                    return False
            return True  # none of the falses were triggered
        return year_balance  # if years aren't equal then just return whether they're balanced



    def get_major_value(self, *args):
        selected_major_index = self.major_select_box.current()
        major_map = {0: "LMATAB1",
                1: "LMATAB2",
                2: "LMATBS1",
                3: "LMATBS2",
                4: "LAMA",
                5: "LMOR",
                6: "LMCOBIO",
                7: "LMCOMATH"}
        self.controller.student.major = major_map[selected_major_index]
        #self.controller.student.major = self.major.get()
