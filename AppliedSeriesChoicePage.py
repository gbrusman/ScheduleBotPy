import tkinter as tk
from tkinter.ttk import *


class AppliedSeriesChoicePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        prompt_frame = Frame(self)
        prompt_frame.grid_columnconfigure(0, weight=1)
        prompt_frame.grid(sticky="nsew", row=0, columnspan=10)
        prompt = Label(prompt_frame, text="Please select which series you are most interested in taking")
        prompt.grid(column=0, row=0, columnspan=2, in_=prompt_frame)
        self.grid_rowconfigure(0, minsize=50)
        self.grid_columnconfigure(0, weight=1)

        self.button_var = tk.IntVar()
        self.button_var.set(0)
        radio_button_frame = Frame(self)
        radio_button_frame.grid(row=5, sticky="nsew")
        phy_button = Radiobutton(radio_button_frame, text="PHY 9A,B", variable=self.button_var, value=1).grid(in_=radio_button_frame, row=0, sticky="nsew", pady=5)
        bis_button = Radiobutton(radio_button_frame, text="BIS 2A,B", variable=self.button_var, value=2).grid(in_=radio_button_frame, row=1, sticky="nsew", pady=5)
        che_button = Radiobutton(radio_button_frame, text="CHE 2A,B", variable=self.button_var, value=3).grid(in_=radio_button_frame, row=2, sticky="nsew", pady=5)
        ecn_button = Radiobutton(radio_button_frame, text="ECN 1A,B", variable=self.button_var, value=4).grid(in_=radio_button_frame, row=3, sticky="nsew", pady=5)
        sta_button = Radiobutton(radio_button_frame, text="STA 32,100", variable=self.button_var, value=5).grid(in_=radio_button_frame, row=4, sticky="nsew", pady=5)

        button_frame = Frame(self)
        button_frame.grid(row=7, sticky="ew")
        back_button = Button(button_frame, text="Back", command=lambda: controller.show_frame("MajorSelectPage"))
        back_button.grid(row=25, column=0, padx=5, pady=10, sticky="sw", in_=button_frame)
        next_button = Button(button_frame, text="Next", command=lambda: self.goto_course_select())  # also need to change courseselect to go back to here if student is LAMA
        next_button.grid(row=25, column=1, padx=5, pady=10, sticky="se", in_=button_frame)

        col_count, row_count = self.grid_size() # sizing the window/spacing the rows
        for i in range(row_count):
            self.grid_rowconfigure(i, minsize=1)

        self.grid_rowconfigure(0, minsize=50)

    def goto_course_select(self):
        if self.button_var.get() != 0:
            self.get_info_from_rbuttons()
            self.controller.show_frame("CourseSelectPage")

    def get_info_from_rbuttons(self):  # This is a horrible way of doing this. Should use classes_by_name and get from dict instead
        if self.button_var.get() == 1:
            for course in self.controller.classes_offered:
                if course.name == "PHY9A" or course.name == "PHY9B":
                    course.required["LAMA"] = True
        elif self.button_var.get() == 2:
            for course in self.controller.classes_offered:
                if course.name == "BIS2A" or course.name == "BIS2B":
                    course.required["LAMA"] = True
        elif self.button_var.get() == 3:
            for course in self.controller.classes_offered:
                if course.name == "CHE2A" or course.name == "CHE2B":
                    course.required["LAMA"] = True
        elif self.button_var.get() == 4:
            for course in self.controller.classes_offered:
                if course.name == "ECN1A" or course.name == "ECN1B":
                    course.required["LAMA"] = True
        elif self.button_var.get() == 5:
            for course in self.controller.classes_offered:
                if course.name == "STA32" or course.name == "STA100":
                    course.required["LAMA"] = True
