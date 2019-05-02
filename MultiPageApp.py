#!/usr/bin/env python
import tkinter as tk
from tkinter.ttk import *
import tkinter.font as tkfont
from Course import Course
from Student import Student
from Schedule import Schedule
from AcademicTime import AcademicTime
from ScheduleBlock import ScheduleBlock

#  https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

class MultiPageApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.app_data = {}
        self.student = Student()
        self.classes_offered = self.init_classes_offered()
        self.classes_by_name = {}

        for course in self.classes_offered:
            self.classes_by_name[course.name] = course

        self.frames = {}
        self.page_names = [MajorSelectPage, CourseSelectPage, InterestSelectPage, ScheduleDisplayPage]
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

    # https://stackoverflow.com/questions/33646605/how-to-access-variables-from-different-classes-in-tkinter
    def get_page(self, page_class):
        return self.frames[page_class]

    def init_classes_offered(self):
        classes_offered = []

        # MAT21A
        required_21A = {}
        required_21A["LMATBS1"] = True
        required_21A["LMATBS2"] = True
        required_21A["LMATAB1"] = True
        required_21A["LMATAB2"] = True
        required_21A["LAMA"] = True
        required_21A["LMOR"] = True
        required_21A["LMCOMATH"] = True
        required_21A["LMCOBIO"] = True
        quarters_offered_21A = ["Fall", "Winter", "Spring"]
        MAT21A = Course("MAT21A", None, "MAT21B", required_21A, quarters_offered_21A, "ALWAYS")

        # MAT21B
        required_21B = {}
        required_21B["LMATBS1"] = True
        required_21B["LMATBS2"] = True
        required_21B["LMATAB1"] = True
        required_21B["LMATAB2"] = True
        required_21B["LAMA"] = True
        required_21B["LMOR"] = True
        required_21B["LMCOMATH"] = True
        required_21B["LMCOBIO"] = True
        quarters_offered_21B = ["Fall", "Winter", "Spring"]
        MAT21B = Course("MAT21B", None, "MAT21C", required_21B, quarters_offered_21B, "ALWAYS")

        # MAT21C
        required_21C = {}
        required_21C["LMATBS1"] = True
        required_21C["LMATBS2"] = True
        required_21C["LMATAB1"] = True
        required_21C["LMATAB2"] = True
        required_21C["LAMA"] = True
        required_21C["LMOR"] = True
        required_21C["LMCOMATH"] = True
        required_21C["LMCOBIO"] = True
        quarters_offered_21C = ["Fall", "Winter", "Spring"]
        MAT21C = Course("MAT21C", None, "MAT21D", required_21C, quarters_offered_21C, "ALWAYS")

        # MAT21D
        required_21D = {}
        required_21D["LMATBS1"] = True
        required_21D["LMATBS2"] = True
        required_21D["LMATAB1"] = True
        required_21D["LMATAB2"] = True
        required_21D["LAMA"] = True
        required_21D["LMOR"] = True
        required_21D["LMCOMATH"] = True
        required_21D["LMCOBIO"] = True
        quarters_offered_21D = ["Fall", "Winter", "Spring"]
        MAT21D = Course("MAT21D", None, None, required_21D, quarters_offered_21D, "ALWAYS")

        # MAT22A
        required_22A = {}
        required_22A["LMATBS1"] = True
        required_22A["LMATBS2"] = True
        required_22A["LMATAB1"] = True
        required_22A["LMATAB2"] = True
        required_22A["LAMA"] = True
        required_22A["LMOR"] = True
        required_22A["LMCOMATH"] = True
        required_22A["LMCOBIO"] = True
        quarters_offered_22A = ["Fall", "Winter", "Spring"]
        MAT22A = Course("MAT22A", None, None, required_22A, quarters_offered_22A, "ALWAYS")

        # MAT22AL
        required_22AL = {}
        required_22AL["LMATBS1"] = False
        required_22AL["LMATBS2"] = False
        required_22AL["LMATAB1"] = False
        required_22AL["LMATAB2"] = False
        required_22AL["LAMA"] = False
        required_22AL["LMOR"] = False
        required_22AL["LMCOMATH"] = False
        required_22AL["LMCOBIO"] = False
        quarters_offered_22AL = ["Fall", "Winter", "Spring"]
        MAT22AL = Course("MAT22AL", None, None, required_22AL, quarters_offered_22AL, "ALWAYS")

        # ENG06
        required_ENG06 = {}
        required_ENG06["LMATBS1"] = True
        required_ENG06["LMATBS2"] = True
        required_ENG06["LMATAB1"] = True
        required_ENG06["LMATAB2"] = True
        required_ENG06["LAMA"] = True
        required_ENG06["LMOR"] = True
        required_ENG06["LMCOMATH"] = True
        required_ENG06["LMCOBIO"] = True
        quarters_offered_ENG06 = ["Fall", "Winter", "Spring"]
        ENG06 = Course("ENG06", None, None, required_ENG06, quarters_offered_ENG06, "ALWAYS")

        # MAT67
        required_67 = {}
        required_67["LMATBS1"] = False
        required_67["LMATBS2"] = False
        required_67["LMATAB1"] = False
        required_67["LMATAB2"] = False
        required_67["LAMA"] = False
        required_67["LMOR"] = False
        required_67["LMCOMATH"] = False
        required_67["LMCOBIO"] = False
        quarters_offered_67 = ["Winter"]
        MAT67 = Course("MAT67", None, None, required_67, quarters_offered_67, "ALWAYS")

        # MAT22B
        required_22B = {}
        required_22B["LMATBS1"] = True
        required_22B["LMATBS2"] = True
        required_22B["LMATAB1"] = True
        required_22B["LMATAB2"] = True
        required_22B["LAMA"] = True
        required_22B["LMOR"] = True
        required_22B["LMCOMATH"] = True
        required_22B["LMCOBIO"] = True
        quarters_offered_22B = ["Fall", "Winter", "Spring"]
        MAT22B = Course("MAT22B", None, None, required_22B, quarters_offered_22B, "ALWAYS")

        # MAT108
        required_108 = {}
        required_108["LMATBS1"] = True
        required_108["LMATBS2"] = True
        required_108["LMATAB1"] = True
        required_108["LMATAB2"] = True
        required_108["LAMA"] = True
        required_108["LMOR"] = True
        required_108["LMCOMATH"] = True
        required_108["LMCOBIO"] = True
        quarters_offered_108 = ["Fall", "Winter", "Spring"]
        MAT108 = Course("MAT108", None, "MAT127A", required_108, quarters_offered_108, "ALWAYS")

        # MAT111
        required_111 = {}
        required_111["LMATBS1"] = False
        required_111["LMATBS2"] = True
        required_111["LMATAB1"] = False
        required_111["LMATAB2"] = True
        required_111["LAMA"] = False
        required_111["LMOR"] = False
        required_111["LMCOMATH"] = False
        required_111["LMCOBIO"] = False
        quarters_offered_111 = ["Winter"]
        interests_111 = ["Teaching"]
        MAT111 = Course("MAT111", interests_111, None, required_111, quarters_offered_111, "ALWAYS")

        # MAT114
        required_114 = {}
        required_114["LMATBS1"] = False
        required_114["LMATBS2"] = False
        required_114["LMATAB1"] = False
        required_114["LMATAB2"] = False
        required_114["LAMA"] = False
        required_114["LMOR"] = False
        required_114["LMCOMATH"] = False
        required_114["LMCOBIO"] = False
        quarters_offered_114 = ["Winter"]
        interests_114 = ["Geometry"]
        MAT114 = Course("MAT114", interests_114, None, required_114, quarters_offered_114, "EVENALTERNATE")

        # MAT115A
        required_115A = {}
        required_115A["LMATBS1"] = False
        required_115A["LMATBS2"] = True
        required_115A["LMATAB1"] = False
        required_115A["LMATAB2"] = True
        required_115A["LAMA"] = False
        required_115A["LMOR"] = False
        required_115A["LMCOMATH"] = False
        required_115A["LMCOBIO"] = False
        quarters_offered_115A = ["Fall"]
        interests_115A = ["Teaching"]
        MAT115A = Course("MAT115A", interests_115A, "MAT115B", required_115A, quarters_offered_115A, "ALWAYS")

        # MAT115B
        required_115B = {}
        required_115B["LMATBS1"] = False
        required_115B["LMATBS2"] = False
        required_115B["LMATAB1"] = False
        required_115B["LMATAB2"] = False
        required_115B["LAMA"] = False
        required_115B["LMOR"] = False
        required_115B["LMCOMATH"] = False
        required_115B["LMCOBIO"] = False
        quarters_offered_115B = ["Winter"]
        interests_115B = ["Teaching"]
        MAT115B = Course("MAT115B", interests_115B, None, required_115B, quarters_offered_115B, "EVENALTERNATE")

        # MAT116
        required_116 = {}
        required_116["LMATBS1"] = False
        required_116["LMATBS2"] = False
        required_116["LMATAB1"] = False
        required_116["LMATAB2"] = False
        required_116["LAMA"] = False
        required_116["LMOR"] = False
        required_116["LMCOMATH"] = False
        required_116["LMCOBIO"] = False
        quarters_offered_116 = ["Spring"]
        interests_116 = ["Geometry"]
        MAT116 = Course("MAT116", interests_116, None, required_116, quarters_offered_116, "ODDALTERNATE")

        # MAT118A
        required_118A = {}
        required_118A["LMATBS1"] = False
        required_118A["LMATBS2"] = False
        required_118A["LMATAB1"] = False
        required_118A["LMATAB2"] = False
        required_118A["LAMA"] = False
        required_118A["LMOR"] = False
        required_118A["LMCOMATH"] = False
        required_118A["LMCOBIO"] = False
        quarters_offered_118A = ["Fall"]
        interests_118A = ["Physics"]
        MAT118A = Course("MAT118A", interests_118A, "MAT118B", required_118A, quarters_offered_118A, "ALWAYS")

        # MAT118B
        required_118B = {}
        required_118B["LMATBS1"] = False
        required_118B["LMATBS2"] = False
        required_118B["LMATAB1"] = False
        required_118B["LMATAB2"] = False
        required_118B["LAMA"] = False
        required_118B["LMOR"] = False
        required_118B["LMCOMATH"] = False
        required_118B["LMCOBIO"] = False
        quarters_offered_118B = ["Winter"]
        interests_118B = ["Physics"]
        MAT118B = Course("MAT118B", interests_118B, None, required_118B, quarters_offered_118B, "ODDALTERNATE")

        # MAT119A
        required_119A = {}
        required_119A["LMATBS1"] = False
        required_119A["LMATBS2"] = False
        required_119A["LMATAB1"] = False
        required_119A["LMATAB2"] = False
        required_119A["LAMA"] = True
        required_119A["LMOR"] = False
        required_119A["LMCOMATH"] = False
        required_119A["LMCOBIO"] = False
        quarters_offered_119A = ["Fall", "Winter"]
        interests_119A = ["Physics"]
        MAT119A = Course("MAT119A", interests_119A, "MAT119B", required_119A, quarters_offered_119A, "ALWAYS")

        # MAT119B
        required_119B = {}
        required_119B["LMATBS1"] = False
        required_119B["LMATBS2"] = False
        required_119B["LMATAB1"] = False
        required_119B["LMATAB2"] = False
        required_119B["LAMA"] = False
        required_119B["LMOR"] = False
        required_119B["LMCOMATH"] = False
        required_119B["LMCOBIO"] = False
        quarters_offered_119B = ["Spring"]
        interests_119B = ["Physics"]
        MAT119B = Course("MAT119B", interests_119B, None, required_119B, quarters_offered_119B, "EVENALTERNATE")

        # MAT124
        required_124 = {}
        required_124["LMATBS1"] = False
        required_124["LMATBS2"] = False
        required_124["LMATAB1"] = False
        required_124["LMATAB2"] = False
        required_124["LAMA"] = False
        required_124["LMOR"] = False
        required_124["LMCOMATH"] = False
        required_124["LMCOBIO"] = True
        quarters_offered_124 = ["Spring"]
        interests_124 = ["Biology"]
        MAT124 = Course("MAT124", interests_124, None, required_124, quarters_offered_124, "ODDALTERNATE")

        # MAT127A
        required_127A = {}
        required_127A["LMATBS1"] = True
        required_127A["LMATBS2"] = True
        required_127A["LMATAB1"] = True
        required_127A["LMATAB2"] = True
        required_127A["LAMA"] = True
        required_127A["LMOR"] = True
        required_127A["LMCOMATH"] = True
        required_127A["LMCOBIO"] = True
        quarters_offered_127A = ["Fall", "Winter", "Spring"]
        MAT127A = Course("MAT127A", None, "MAT127B", required_127A, quarters_offered_127A, "ALWAYS")

        # MAT127B
        required_127B = {}
        required_127B["LMATBS1"] = True
        required_127B["LMATBS2"] = True
        required_127B["LMATAB1"] = True
        required_127B["LMATAB2"] = True
        required_127B["LAMA"] = True
        required_127B["LMOR"] = True
        required_127B["LMCOMATH"] = True
        required_127B["LMCOBIO"] = True
        quarters_offered_127B = ["Fall", "Winter", "Spring"]
        MAT127B = Course("MAT127B", None, "MAT127C", required_127B, quarters_offered_127B, "ALWAYS")

        # MAT127C
        required_127C = {}
        required_127C["LMATBS1"] = True
        required_127C["LMATBS2"] = True
        required_127C["LMATAB1"] = True
        required_127C["LMATAB2"] = True
        required_127C["LAMA"] = True
        required_127C["LMOR"] = True
        required_127C["LMCOMATH"] = True
        required_127C["LMCOBIO"] = True
        quarters_offered_127C = ["Fall", "Winter", "Spring"]
        MAT127C = Course("MAT127C", None, None, required_127C, quarters_offered_127C, "ALWAYS")

        # MAT128A
        required_128A = {}
        required_128A["LMATBS1"] = False
        required_128A["LMATBS2"] = False
        required_128A["LMATAB1"] = False
        required_128A["LMATAB2"] = False
        required_128A["LAMA"] = True
        required_128A["LMOR"] = True
        required_128A["LMCOMATH"] = True
        required_128A["LMCOBIO"] = True
        quarters_offered_128A = ["Fall"]
        interests_128A = ["Computers"]
        MAT128A = Course("MAT128A", interests_128A, None, required_128A, quarters_offered_128A, "ALWAYS")

        # MAT128B
        required_128B = {}
        required_128B["LMATBS1"] = False
        required_128B["LMATBS2"] = False
        required_128B["LMATAB1"] = False
        required_128B["LMATAB2"] = False
        required_128B["LAMA"] = True
        required_128B["LMOR"] = True
        required_128B["LMCOMATH"] = True
        required_128B["LMCOBIO"] = True
        quarters_offered_128B = ["Winter"]
        interests_128B = ["Computers"]
        MAT128B = Course("MAT128B", interests_128B, None, required_128B, quarters_offered_128B, "ALWAYS")

        # MAT128C
        required_128C = {}
        required_128C["LMATBS1"] = False
        required_128C["LMATBS2"] = False
        required_128C["LMATAB1"] = False
        required_128C["LMATAB2"] = False
        required_128C["LAMA"] = True
        required_128C["LMOR"] = True
        required_128C["LMCOMATH"] = True
        required_128C["LMCOBIO"] = True
        quarters_offered_128C = ["Spring"]
        interests_128C = ["Computers"]
        MAT128C = Course("MAT128C", interests_128C, None, required_128C, quarters_offered_128C, "ALWAYS")

        # MAT129
        required_129 = {}
        required_129["LMATBS1"] = False
        required_129["LMATBS2"] = False
        required_129["LMATAB1"] = False
        required_129["LMATAB2"] = False
        required_129["LAMA"] = False
        required_129["LMOR"] = False
        required_129["LMCOMATH"] = False
        required_129["LMCOBIO"] = False
        quarters_offered_129 = ["Fall"]
        MAT129 = Course("MAT129", None, None, required_129, quarters_offered_129, "ODDALTERNATE")

        # MAT133
        required_133 = {}
        required_133["LMATBS1"] = False
        required_133["LMATBS2"] = False
        required_133["LMATAB1"] = False
        required_133["LMATAB2"] = False
        required_133["LAMA"] = False
        required_133["LMOR"] = False
        required_133["LMCOMATH"] = False
        required_133["LMCOBIO"] = False
        quarters_offered_133 = ["Spring"]
        interests_133 = ["Finance"]
        MAT133 = Course("MAT133", interests_133, None, required_133, quarters_offered_133, "ALWAYS")

        # MAT135A
        required_135A = {}
        required_135A["LMATBS1"] = True
        required_135A["LMATBS2"] = True
        required_135A["LMATAB1"] = True
        required_135A["LMATAB2"] = True
        required_135A["LAMA"] = True
        required_135A["LMOR"] = True
        required_135A["LMCOMATH"] = True
        required_135A["LMCOBIO"] = True
        quarters_offered_135A = ["Fall", "Winter", "Spring"]
        MAT135A = Course("MAT135A", None, "MAT135B", required_135A, quarters_offered_135A, "ALWAYS")

        # MAT135B
        required_135B = {}
        required_135B["LMATBS1"] = False
        required_135B["LMATBS2"] = False
        required_135B["LMATAB1"] = False
        required_135B["LMATAB2"] = False
        required_135B["LAMA"] = False
        required_135B["LMOR"] = True
        required_135B["LMCOMATH"] = False
        required_135B["LMCOBIO"] = False
        quarters_offered_135B = ["Spring"]
        MAT135B = Course("MAT135B", None, None, required_135B, quarters_offered_135B, "ALWAYS")

        # MAT141
        required_141 = {}
        required_141["LMATBS1"] = False
        required_141["LMATBS2"] = True
        required_141["LMATAB1"] = False
        required_141["LMATAB2"] = True
        required_141["LAMA"] = False
        required_141["LMOR"] = False
        required_141["LMCOMATH"] = False
        required_141["LMCOBIO"] = False
        quarters_offered_141 = ["Winter", "Spring"]
        interests_141 = ["Geometry", "Teaching"]
        MAT141 = Course("MAT141", interests_141, None, required_141, quarters_offered_141, "ALWAYS")

        # MAT145
        required_145 = {}
        required_145["LMATBS1"] = False
        required_145["LMATBS2"] = False
        required_145["LMATAB1"] = False
        required_145["LMATAB2"] = False
        required_145["LAMA"] = False
        required_145["LMOR"] = False
        required_145["LMCOMATH"] = False
        required_145["LMCOBIO"] = False
        quarters_offered_145 = ["Fall", "Winter", "Spring"]
        interests_145 = ["Teaching"]
        MAT145 = Course("MAT145", interests_145, None, required_145, quarters_offered_145, "ALWAYS")

        # MAT146
        required_146 = {}
        required_146["LMATBS1"] = False
        required_146["LMATBS2"] = False
        required_146["LMATAB1"] = False
        required_146["LMATAB2"] = False
        required_146["LAMA"] = False
        required_146["LMOR"] = False
        required_146["LMCOMATH"] = False
        required_146["LMCOBIO"] = False
        quarters_offered_146 = ["Spring"]
        MAT146 = Course("MAT146", None, None, required_146, quarters_offered_146, "EVENALTERNATE")

        # MAT147
        required_147 = {}
        required_147["LMATBS1"] = False
        required_147["LMATBS2"] = False
        required_147["LMATAB1"] = False
        required_147["LMATAB2"] = False
        required_147["LAMA"] = False
        required_147["LMOR"] = False
        required_147["LMCOMATH"] = False
        required_147["LMCOBIO"] = False
        quarters_offered_147 = ["Winter"]
        interests_147 = ["Abstract"]
        MAT147 = Course("MAT147", interests_147, None, required_147, quarters_offered_147, "ALWAYS")

        # MAT148
        required_148 = {}
        required_148["LMATBS1"] = False
        required_148["LMATBS2"] = False
        required_148["LMATAB1"] = False
        required_148["LMATAB2"] = False
        required_148["LAMA"] = False
        required_148["LMOR"] = False
        required_148["LMCOMATH"] = False
        required_148["LMCOBIO"] = False
        quarters_offered_148 = ["Winter"]
        MAT148 = Course("MAT148", None, None, required_148, quarters_offered_148, "ODDALTERNATE")

        # MAT150A
        required_150A = {}
        required_150A["LMATBS1"] = True
        required_150A["LMATBS2"] = True
        required_150A["LMATAB1"] = True
        required_150A["LMATAB2"] = True
        required_150A["LAMA"] = True
        required_150A["LMOR"] = True
        required_150A["LMCOMATH"] = True
        required_150A["LMCOBIO"] = True
        quarters_offered_150A = ["Fall", "Winter"]
        MAT150A = Course("MAT150A", None, "MAT150B", required_150A, quarters_offered_150A, "ALWAYS")

        # MAT150B
        required_150B = {}
        required_150B["LMATBS1"] = True
        required_150B["LMATBS2"] = False
        required_150B["LMATAB1"] = False
        required_150B["LMATAB2"] = False
        required_150B["LAMA"] = False
        required_150B["LMOR"] = False
        required_150B["LMCOMATH"] = False
        required_150B["LMCOBIO"] = False
        quarters_offered_150B = ["Winter"]
        interests_150B = ["Abstract"]
        MAT150B = Course("MAT150B", interests_150B, "MAT150C", required_150B, quarters_offered_150B, "ALWAYS")

        # MAT150C
        required_150C = {}
        required_150C["LMATBS1"] = True
        required_150C["LMATBS2"] = False
        required_150C["LMATAB1"] = False
        required_150C["LMATAB2"] = False
        required_150C["LAMA"] = False
        required_150C["LMOR"] = False
        required_150C["LMCOMATH"] = False
        required_150C["LMCOBIO"] = False
        quarters_offered_150C = ["Spring"]
        interests_150C = ["Abstract"]
        MAT150C = Course("MAT150C", interests_150C, None, required_150C, quarters_offered_150C, "ALWAYS")

        # MAT160
        required_160 = {}
        required_160["LMATBS1"] = False
        required_160["LMATBS2"] = False
        required_160["LMATAB1"] = False
        required_160["LMATAB2"] = False
        required_160["LAMA"] = False
        required_160["LMOR"] = True
        required_160["LMCOMATH"] = False
        required_160["LMCOBIO"] = False
        quarters_offered_160 = ["Spring"]
        interests_160 = ["Computers", "Data Analysis"]
        MAT160 = Course("MAT160", interests_160, None, required_160, quarters_offered_160, "ALWAYS")

        # MAT165
        required_165 = {}
        required_165["LMATBS1"] = False
        required_165["LMATBS2"] = False
        required_165["LMATAB1"] = False
        required_165["LMATAB2"] = False
        required_165["LAMA"] = False
        required_165["LMOR"] = False
        required_165["LMCOMATH"] = False
        required_165["LMCOBIO"] = False
        quarters_offered_165 = ["Fall"]
        interests_165 = ["Computers"]
        MAT165 = Course("MAT165", interests_165, None, required_165, quarters_offered_165, "EVENALTERNATE")

        # MAT167
        required_167 = {}
        required_167["LMATBS1"] = False
        required_167["LMATBS2"] = False
        required_167["LMATAB1"] = False
        required_167["LMATAB2"] = False
        required_167["LAMA"] = False
        required_167["LMOR"] = True
        required_167["LMCOMATH"] = False
        required_167["LMCOBIO"] = False
        quarters_offered_167 = ["Fall", "Winter"]
        interests_167 = ["Teaching", "Data Analysis"]
        MAT167 = Course("MAT167", interests_167, None, required_167, quarters_offered_167, "ALWAYS")

        # MAT168
        required_168 = {}
        required_168["LMATBS1"] = False
        required_168["LMATBS2"] = False
        required_168["LMATAB1"] = False
        required_168["LMATAB2"] = False
        required_168["LAMA"] = False
        required_168["LMOR"] = True
        required_168["LMCOMATH"] = True
        required_168["LMCOBIO"] = False
        quarters_offered_168 = ["Fall", "Winter"]
        interests_168 = ["Computers", "Data Analysis"]
        MAT168 = Course("MAT168", interests_168, None, required_168, quarters_offered_168, "ALWAYS")

        # MAT180
        required_180 = {}
        required_180["LMATBS1"] = True
        required_180["LMATBS2"] = True
        required_180["LMATAB1"] = True
        required_180["LMATAB2"] = True
        required_180["LAMA"] = True
        required_180["LMOR"] = True
        required_180["LMCOMATH"] = True
        required_180["LMCOBIO"] = True
        quarters_offered_180 = ["Fall", "Winter", "Spring"]
        MAT180 = Course("MAT180", None, None, required_180, quarters_offered_180, "ALWAYS")

        # MAT185A
        required_185A = {}
        required_185A["LMATBS1"] = True
        required_185A["LMATBS2"] = False
        required_185A["LMATAB1"] = False
        required_185A["LMATAB2"] = False
        required_185A["LAMA"] = True
        required_185A["LMOR"] = False
        required_185A["LMCOMATH"] = False
        required_185A["LMCOBIO"] = False
        quarters_offered_185A = ["Fall", "Spring"]
        MAT185A = Course("MAT185A", None, "MAT185B", required_185A, quarters_offered_185A, "ALWAYS")

        # MAT185B
        required_185B = {}
        required_185B["LMATBS1"] = True
        required_185B["LMATBS2"] = False
        required_185B["LMATAB1"] = False
        required_185B["LMATAB2"] = False
        required_185B["LAMA"] = True
        required_185B["LMOR"] = False
        required_185B["LMCOMATH"] = False
        required_185B["LMCOBIO"] = False
        quarters_offered_185B = ["Spring"]
        MAT185B = Course("MAT185B", None, None, required_185B, quarters_offered_185B, "ODDALTERNATE")

        # MAT189
        required_189 = {}
        required_189["LMATBS1"] = False
        required_189["LMATBS2"] = False
        required_189["LMATAB1"] = False
        required_189["LMATAB2"] = False
        required_189["LAMA"] = False
        required_189["LMOR"] = False
        required_189["LMCOMATH"] = False
        required_189["LMCOBIO"] = False
        quarters_offered_189 = ["Spring"]
        MAT189 = Course("MAT189", None, None, required_189, quarters_offered_189, "ALWAYS")

        # ECS32A
        required_ECS32A = {}
        required_ECS32A["LMATBS1"] = False
        required_ECS32A["LMATBS2"] = False
        required_ECS32A["LMATAB1"] = False
        required_ECS32A["LMATAB2"] = False
        required_ECS32A["LAMA"] = True
        required_ECS32A["LMOR"] = False
        required_ECS32A["LMCOMATH"] = True
        required_ECS32A["LMCOBIO"] = True
        quarters_offered_ECS32A = ["Fall", "Winter", "Spring"]
        ECS32A = Course("ECS32A", None, None, required_ECS32A, quarters_offered_ECS32A, "ALWAYS")

        # PHY7A
        required_PHY7A = {}
        required_PHY7A["LMATBS1"] = False
        required_PHY7A["LMATBS2"] = False
        required_PHY7A["LMATAB1"] = False
        required_PHY7A["LMATAB2"] = False
        required_PHY7A["LAMA"] = False
        required_PHY7A["LMOR"] = False
        required_PHY7A["LMCOMATH"] = False
        required_PHY7A["LMCOBIO"] = False
        quarters_offered_PHY7A = ["Fall", "Winter", "Spring"]
        PHY7A = Course("PHY7A", None, None, required_PHY7A, quarters_offered_PHY7A, "ALWAYS")

        # PHY9A
        required_PHY9A = {}
        required_PHY9A["LMATBS1"] = True
        required_PHY9A["LMATBS2"] = False
        required_PHY9A["LMATAB1"] = False
        required_PHY9A["LMATAB2"] = False
        required_PHY9A["LAMA"] = False
        required_PHY9A["LMOR"] = False
        required_PHY9A["LMCOMATH"] = False
        required_PHY9A["LMCOBIO"] = False
        quarters_offered_PHY9A = ["Fall", "Spring"]
        PHY9A = Course("PHY9A", None, None, required_PHY9A, quarters_offered_PHY9A, "ALWAYS")

        # ECN1A
        required_ECN1A = {}
        required_ECN1A["LMATBS1"] = False
        required_ECN1A["LMATBS2"] = False
        required_ECN1A["LMATAB1"] = False
        required_ECN1A["LMATAB2"] = False
        required_ECN1A["LAMA"] = True  # Default to ECN, eventually want to ask what 2-Quarter series they want to take
        required_ECN1A["LMOR"] = True  # Same as above ^
        required_ECN1A["LMCOMATH"] = False
        required_ECN1A["LMCOBIO"] = False
        quarters_offered_ECN1A = ["Fall", "Winter", "Spring"]
        ECN1A = Course("ECN1A", None, None, required_ECN1A, quarters_offered_ECN1A, "ALWAYS")

        # ECN1B
        required_ECN1B = {}
        required_ECN1B["LMATBS1"] = False
        required_ECN1B["LMATBS2"] = False
        required_ECN1B["LMATAB1"] = False
        required_ECN1B["LMATAB2"] = False
        required_ECN1B["LAMA"] = True  # Default to ECN, eventually want to ask what 2-Quarter series they want to take
        required_ECN1B["LMOR"] = True  # Same as above ^
        required_ECN1B["LMCOMATH"] = False
        required_ECN1B["LMCOBIO"] = False
        quarters_offered_ECN1B = ["Fall", "Winter", "Spring"]
        ECN1B = Course("ECN1B", None, None, required_ECN1B, quarters_offered_ECN1B, "ALWAYS")

        # STA32
        required_STA32 = {}
        required_STA32["LMATBS1"] = False
        required_STA32["LMATBS2"] = False
        required_STA32["LMATAB1"] = False
        required_STA32["LMATAB2"] = False
        required_STA32["LAMA"] = False
        required_STA32["LMOR"] = True
        required_STA32["LMCOMATH"] = False
        required_STA32["LMCOBIO"] = False
        quarters_offered_STA32 = ["Fall", "Winter", "Spring"]
        STA32 = Course("STA32", None, None, required_STA32, quarters_offered_STA32, "ALWAYS")

        # STA100
        required_STA100 = {}
        required_STA100["LMATBS1"] = False
        required_STA100["LMATBS2"] = False
        required_STA100["LMATAB1"] = False
        required_STA100["LMATAB2"] = False
        required_STA100["LAMA"] = False
        required_STA100["LMOR"] = False
        required_STA100["LMCOMATH"] = False
        required_STA100["LMCOBIO"] = False
        quarters_offered_STA100 = ["Fall", "Winter", "Spring"]
        STA100 = Course("STA100", None, None, required_STA100, quarters_offered_STA100, "ALWAYS")

        classes_offered.append(MAT21A)
        classes_offered.append(MAT21B)
        classes_offered.append(MAT21C)
        classes_offered.append(MAT21D)
        classes_offered.append(MAT22A)
        classes_offered.append(MAT22AL)
        classes_offered.append(MAT67)
        classes_offered.append(MAT22B)
        classes_offered.append(MAT108)
        classes_offered.append(MAT111)
        classes_offered.append(MAT114)
        classes_offered.append(MAT115A)
        classes_offered.append(MAT115B)
        classes_offered.append(MAT116)
        classes_offered.append(MAT118A)
        classes_offered.append(MAT118B)
        classes_offered.append(MAT119A)
        classes_offered.append(MAT119B)
        classes_offered.append(MAT124)
        classes_offered.append(MAT127A)
        classes_offered.append(MAT127B)
        classes_offered.append(MAT127C)
        classes_offered.append(MAT128A)
        classes_offered.append(MAT128B)
        classes_offered.append(MAT128C)
        classes_offered.append(MAT129)
        classes_offered.append(MAT133)
        classes_offered.append(MAT135A)
        classes_offered.append(MAT135B)
        classes_offered.append(MAT141)
        classes_offered.append(MAT145)
        classes_offered.append(MAT146)
        classes_offered.append(MAT147)
        classes_offered.append(MAT148)
        classes_offered.append(MAT150A)
        classes_offered.append(MAT150B)
        classes_offered.append(MAT150C)
        classes_offered.append(MAT160)
        classes_offered.append(MAT165)
        classes_offered.append(MAT167)
        classes_offered.append(MAT168)
        classes_offered.append(MAT180)
        classes_offered.append(MAT185A)
        classes_offered.append(MAT185B)
        classes_offered.append(MAT189)
        classes_offered.append(ECS32A)
        classes_offered.append(ENG06)
        classes_offered.append(PHY7A)
        classes_offered.append(PHY9A)
        classes_offered.append(ECN1A)
        classes_offered.append(ECN1B)
        classes_offered.append(STA32)
        classes_offered.append(STA100)
        return classes_offered


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

        col = 0
        row = 1
        count = 0
        cbox_frame = Frame(self)
        cbox_frame.grid(row=3, sticky="nsew")
        self.cbox_list = []
        for course in self.controller.classes_offered:
            checkbox = Checkbutton(cbox_frame, text=course.name)
            checkbox.invoke()  # turns checkbox from default to on
            checkbox.invoke()  # turns checkbox from on to off
            checkbox.grid(row=row, column=col, sticky="nsew", padx=5, in_=cbox_frame)
            self.cbox_list.append(checkbox)
            row += 1
            count+=1
            if count == 10:  # only 10 checkboxes per column
                cbox_frame.grid_columnconfigure(col, weight=1)
                col += 1
                row = 1
                count = 0
        for i in range(10):
            cbox_frame.grid_rowconfigure(i, weight=1)

        button_frame = Frame(self)
        button_frame.grid(row=7, sticky="ew")
        back_button = Button(button_frame, text="Back", command=lambda: controller.show_frame("MajorSelectPage"))
        back_button.grid(row=25, column=0, padx=5, pady=10, sticky="sw", in_=button_frame)
        next_button = Button(button_frame, text="Next", command=lambda: self.goto_interest_select())
        next_button.grid(row=25, column=1, padx=5, pady=10, sticky="se", in_=button_frame)
        for i in range(2):
            button_frame.grid_columnconfigure(i, weight=1)
        col_size, row_size = self.grid_size()
        for i in range(row_size):
            self.grid_rowconfigure(i, minsize=20, weight=1)


    def goto_interest_select(self):
        self.get_info_from_cboxes()
        self.controller.show_frame("InterestSelectPage")

    def get_info_from_cboxes(self):
        self.controller.student.classes_taken.clear()
        for cbox in self.cbox_list:
            if cbox.instate(['selected']):  # https://stackoverflow.com/questions/4236910/getting-tkinter-check-box-state
                self.controller.student.classes_taken[(cbox.cget("text"))] = self.controller.classes_by_name[(cbox.cget("text"))]  # https://stackoverflow.com/questions/33545085/how-to-get-the-text-from-a-checkbutton-in-python-tkinter


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







if __name__ == "__main__":
    app = MultiPageApp()
    app.mainloop()