import Tkinter as tk
import Tkinter.font as tkfont
from Tkinter.ttk import *

from AcademicTime import AcademicTime


class MajorSelectPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.major = tk.StringVar()
        self.cur_quarter = tk.StringVar()
        self.cur_year = 0
        prompt_frame = tk.Frame(self)
        prompt_frame.grid_columnconfigure(0, weight=1)
        prompt_frame.grid(sticky="nsew", row=0, columnspan=2)
        prompt = tk.Label(prompt_frame, text="Please fill out the information in the form below")
        prompt.grid(column=0, row=0, columnspan=2, in_=prompt_frame)
        self.err_msg = tk.Label(prompt_frame, text="", fg="red")  # needed to use tk label here for fg option
        self.err_msg.grid(column=0, row=1, columnspan=2, in_=prompt_frame)
        info_frame = tk.Frame(self)
        info_frame.grid(row=1, sticky="nsew", columnspan=2)
        info_frame.columnconfigure(0, weight=1)

        major_frame = tk.Frame(info_frame)
        major_frame.grid(column=0, row=5, pady=10)
        major_label = tk.Label(major_frame, text="Major: ")
        major_label.grid(column=0, row=0, in_=major_frame, pady=20, sticky="e", padx=5)
        self.major_choices = ["AB Mathematics: Plan 1 - General Mathematics", "AB Mathematics: Plan 2 - Secondary Teaching",
                         "BS Mathematics: Plan 1 - General Mathematics", "BS Mathematics: Plan 2 - Secondary Teaching",
                         "Applied Mathematics", "Mathematical Analytics and Operations Research",
                         "Mathematical and Scientific Computation - Bio Emphasis",
                         "Mathematical and Scientific Computation - Math Emphasis"]
        self.major_select_box = tk.Combobox(major_frame, values=self.major_choices, textvariable=self.major, state="readonly", width=45)  # need to talk to IT people about what libraries are okay to import
        self.major_select_box.bind('<Configure>', self.on_combo_configure)
        self.major_select_box.grid(row=0, column=1, in_=major_frame, sticky=tk.E + tk.W, padx=5)
        self.major_select_box.bind("<<ComboboxSelected>>", self.get_major_value)


        cur_quarter_label = tk.Label(major_frame, text="Current Quarter: ")
        cur_quarter_label.grid(column=0, row=1, in_=major_frame, pady=10, sticky="e", padx=5)
        cur_quarter_choices = ["Fall", "Winter", "Spring"]
        self.cur_quarter_select_box = tk.Combobox(major_frame, values=cur_quarter_choices, textvariable=self.cur_quarter, state="readonly", width=25)
        self.cur_quarter_select_box.grid(row=1, column=1, in_=major_frame, sticky=tk.W, padx=5)


        cur_year_label = tk.Label(major_frame, text="Current Year: ")
        cur_year_label.grid(column=0, row=2, in_=major_frame, pady=0, sticky="e", padx=5)
        self.cur_year_entry = tk.Entry(major_frame, width=15)
        self.cur_year_entry.grid(row=2, column=1, in_=major_frame, sticky=tk.W, padx=5)

        next_button = tk.Button(self, text="Next", command=lambda: self.goto_course_select())
        next_button.grid(row=2, padx=5, pady=10, sticky=tk.S + tk.E)

        col_count, row_count = self.grid_size()
        self.grid_columnconfigure(0, weight=1)

        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=20, weight=1)

        major_frame.grid_rowconfigure(3, minsize=20)  # separates current year stuff from grad year stuff


    def on_combo_configure(self, event):
        """Function to expand ComboBox dropdown menu so all text fits on screen for the major select box."""
        # https://stackoverflow.com/questions/39915275/change-width-of-dropdown-listbox-of-a-ttk-combobox
        combo = event.widget
        style = tk.ttk.Style()

        long = max(combo.cget('values'), key=len)

        font = tkfont.nametofont(str(combo.cget('font')))
        width = max(0, font.measure(long.strip() + '0') - combo.winfo_width())

        style.configure('TCombobox', postoffset=(0, 0, width, 0))
        combo.configure(style='TCombobox')

    def goto_course_select(self):
        if self.validate_input():
            cur_year = int(self.cur_year_entry.get())

            #Set Student times here
            self.controller.student.cur_time = AcademicTime(cur_year, self.cur_quarter.get())
            self.controller.student.start_time = AcademicTime(cur_year, self.cur_quarter.get())

            if self.controller.student.major == "LAMA":
                self.controller.show_frame("AppliedSeriesChoicePage")
            else:
                self.controller.show_frame("CourseSelectPage")


    def validate_input(self):
        if not self.major.get():
            self.err_msg["text"] = "Please select a major"
            return False
        if not self.cur_quarter.get():
            self.err_msg["text"] = "Please select a value for Current Quarter"
            return False
        if self.cur_year_entry.get() == "":
            self.err_msg["text"] = "Please ensure you have entered values for Current Year and Graduation Year"
            return False
        if not self.cur_year_entry.get().isdigit():   # checks if year entries are integers
            self.err_msg["text"] = "Please ensure your year values are integers"
            return False

        return True

    def get_major_value(self, *args):
        selected_major_index = self.major_select_box.current()
        major_map = {
                0: "LMATAB1",
                1: "LMATAB2",
                2: "LMATBS1",
                3: "LMATBS2",
                4: "LAMA",
                5: "LMOR",
                6: "LMCOBIO",
                7: "LMCOMATH"}
        self.controller.student.major = major_map[selected_major_index]
