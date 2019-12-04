import tkinter as tk
import tkinter.font as tkfont
from tkinter.ttk import *

from AcademicTime import AcademicTime


class MajorSelectPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.major = tk.StringVar()
        self.cur_quarter = tk.StringVar()
        self.cur_year = 0
        self.cur_summer_row_index = 5
        prompt_frame = Frame(self)
        prompt_frame.grid_columnconfigure(0, weight=1)
        prompt_frame.grid(sticky="nsew", row=0, columnspan=2)
        prompt = Label(prompt_frame, text="Please fill out the information in the form below")
        prompt.grid(column=0, row=0, columnspan=2, in_=prompt_frame)
        self.err_msg = tk.Label(prompt_frame, text="", fg="red")  # needed to use tk label here for fg option
        self.err_msg.grid(column=0, row=1, columnspan=2, in_=prompt_frame)
        info_frame = Frame(self)
        info_frame.grid(row=1, sticky="nsew", columnspan=2)
        info_frame.columnconfigure(0, weight=1)

        major_frame = Frame(info_frame)
        major_frame.grid(column=0, row=5, pady=10)
        self.major_frame = major_frame
        major_label = Label(major_frame, text="Major: ")
        major_label.grid(column=0, row=0, in_=major_frame, pady=20, sticky="e", padx=5)
        self.major_choices = ["AB Mathematics: Plan 1 - General Mathematics", "AB Mathematics: Plan 2 - Secondary Teaching",
                         "BS Mathematics: Plan 1 - General Mathematics", "BS Mathematics: Plan 2 - Secondary Teaching",
                         "Applied Mathematics", "Mathematical Analytics and Operations Research",
                         "Mathematical and Scientific Computation - Bio Emphasis",
                         "Mathematical and Scientific Computation - Math Emphasis"]

        # For styling the white backgrounds: https://wiki.tcl-lang.org/page/Changing+Widget+Colors
        style = Style()
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])

        self.major_select_box = Combobox(major_frame, values=self.major_choices, textvariable=self.major, state="readonly", width=45)  # need to talk to IT people about what libraries are okay to import
        self.major_select_box.bind('<Configure>', self.on_combo_configure)
        self.major_select_box.grid(row=0, column=1, in_=major_frame, sticky=tk.E + tk.W, padx=5)
        self.major_select_box.bind("<<ComboboxSelected>>", self.get_major_value)


        cur_quarter_label = Label(major_frame, text="Current Quarter: ")
        cur_quarter_label.grid(column=0, row=1, in_=major_frame, pady=10, sticky="e", padx=5)
        cur_quarter_choices = ["Fall", "Winter", "Spring"]
        self.cur_quarter_select_box = Combobox(major_frame, values=cur_quarter_choices, textvariable=self.cur_quarter, state="readonly", width=25)
        self.cur_quarter_select_box.grid(row=1, column=1, in_=major_frame, sticky=tk.W, padx=5)


        cur_year_label = Label(major_frame, text="Current Year: ")
        cur_year_label.grid(column=0, row=2, in_=major_frame, pady=0, sticky="e", padx=5)
        self.cur_year_entry = Entry(major_frame, width=15)
        self.cur_year_entry.grid(row=2, column=1, in_=major_frame, sticky=tk.W, padx=5)

        summer_session_label = Label(major_frame, text="Are you planning on taking any summer sessions?")
        summer_session_label.grid(column=0, row=4, in_=major_frame, pady=0, sticky="e", padx=5)
        self.summer_session_checkbox_value = tk.IntVar()
        summer_session_checkbox = tk.Checkbutton(major_frame, anchor='w', command=self.create_summer_options, variable=self.summer_session_checkbox_value)
        summer_session_checkbox.flash()
        summer_session_checkbox.grid(column=1, row=4, in_=major_frame, pady=0, sticky="w", padx=0)
        self.add_new_entry_button = Button(self.major_frame, text="Add New Summer Session", command=self.create_summer_options)
        self.remove_entry_button = Button(self.major_frame, text="Remove Summer Session", command=self.remove_summer_session_entry)
        self.summer_session_array = []

        next_button = Button(self, text="Next", command=lambda: self.goto_course_select())
        next_button.grid(row=2, padx=5, pady=10, sticky=tk.S + tk.E)

        col_count, row_count = self.grid_size()
        self.grid_columnconfigure(0, weight=1)

        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=20, weight=1)

        major_frame.grid_rowconfigure(3, minsize=20)  # separates current year stuff from grad year stuff

    def remove_summer_session_entry(self):
        if self.cur_summer_row_index > 5:
            self.summer_session_array[self.cur_summer_row_index - 6][0].grid_forget()
            self.summer_session_array[self.cur_summer_row_index - 6][1].grid_forget()
            self.summer_session_array.pop(self.cur_summer_row_index - 6)
            self.add_new_entry_button.grid_forget()
            self.remove_entry_button.grid_forget()

            self.add_new_entry_button.grid(row=self.cur_summer_row_index - 1, column=1, sticky=tk.W, padx=2)
            self.remove_entry_button.grid(row=self.cur_summer_row_index - 1, column=1, sticky=tk.E, padx=2)
            self.cur_summer_row_index -= 1
        else:
            self.summer_combo_label.grid_forget()

    def create_summer_options(self):

        if self.summer_session_checkbox_value.get():
            if(self.cur_summer_row_index == 5):
                self.summer_combo_label = Label(self.major_frame, text="Please select which summer sessions you will be taking (Quarter/Year):")
                self.summer_combo_label.grid(column=0, row=self.cur_summer_row_index, in_=self.major_frame, pady=0, sticky="e", padx=5)

            session_choices = ["Summer Session 1", "Summer Session 2"]
            summer_select_box = Combobox(self.major_frame, values=session_choices, state="readonly", width=25)
            summer_select_box.bind('<Configure>', self.on_combo_configure)
            summer_select_box.grid(row=self.cur_summer_row_index, column=1, in_=self.major_frame, sticky=tk.W, padx=5, pady=2)

            summer_year_entry = Entry(self.major_frame, width=15)
            summer_year_entry.grid(row=self.cur_summer_row_index, column=1, in_=self.major_frame, sticky=tk.E, padx=5, pady=2)

            self.summer_session_array.append((summer_select_box, summer_year_entry))

            self.add_new_entry_button.grid_forget()
            self.add_new_entry_button.grid(row=self.cur_summer_row_index+1, column=1, sticky=tk.W, padx=2)
            self.remove_entry_button.grid_forget()
            self.remove_entry_button.grid(row=self.cur_summer_row_index+1, column=1, sticky=tk.E, padx=2)


            self.cur_summer_row_index += 1
        else:
            self.summer_combo_label.grid_forget()
            self.add_new_entry_button.grid_forget()
            self.remove_entry_button.grid_forget()
            for tuple in self.summer_session_array:
                tuple[0].grid_forget()
                tuple[1].grid_forget()
            self.summer_session_array.clear()
            self.cur_summer_row_index = 5


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

            #Set Student summer sessions
            self.controller.student.summer_quarters.clear()
            for tuple in self.summer_session_array:
                if tuple[0].get() and tuple[1].get() != "":
                    self.controller.student.summer_quarters.append(AcademicTime(int(tuple[1].get()), tuple[0].get()))

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
            self.err_msg["text"] = "Please ensure you have entered a value for the Current Year."
            return False
        if not self.cur_year_entry.get().isdigit():   # checks if year entries are integers
            self.err_msg["text"] = "Please ensure your year values are integers"
            return False

        # Validate summer session entries
        for tuple in self.summer_session_array:
            if (tuple[0].get() and tuple[1].get() == "" or tuple[1].get() == "Enter Year") or (not tuple[0].get() and tuple[1].get().isdigit()):
                self.err_msg["text"] = "Please finish filling out your summer session information."
                return False
            if tuple[0].get() and not tuple[1].get().isdigit():
                self.err_msg["text"] = "Please ensure your summer session year values are integers."
                return False
            if self.cur_quarter.get() == "Fall":
                if tuple[0].get() and tuple[1].get().isdigit() and int(tuple[1].get()) <= int(self.cur_year_entry.get()):
                    self.err_msg["text"] = "Your summer session is before your start date."
                    return False
            else:
                if tuple[0].get() and tuple[1].get().isdigit() and int(tuple[1].get()) < int(self.cur_year_entry.get()):
                    self.err_msg["text"] = "Your summer session is before your start date."
                    return False




        self.err_msg["text"] = ""
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
