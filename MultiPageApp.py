#!/usr/bin/env python
import tkinter as tk
from operator import attrgetter
from AppliedSeriesChoicePage import AppliedSeriesChoicePage
from Course import Course
from CourseSelectPage import CourseSelectPage
from InterestSelectPage import InterestSelectPage
from MajorSelectPage import MajorSelectPage
from ScheduleDisplayPage import ScheduleDisplayPage
from Student import Student
import psycopg2
import csv
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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
        self.classes_offered = []
        self.classes_by_name = {}

        try:
            self.get_info_from_database()
        except:
            self.get_info_from_csv()

        self.frames = {}
        self.page_names = [MajorSelectPage, CourseSelectPage, InterestSelectPage, ScheduleDisplayPage, AppliedSeriesChoicePage]
        for F in self.page_names:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MajorSelectPage")

    def get_info_from_database(self):
        conn = psycopg2.connect(host="rajje.db.elephantsql.com", database="ytmelfsd", user="ytmelfsd", password="PY2TKJsTJD2cOPlRbwQgVJPHgc4vhWvT")
        cur = conn.cursor()
        # Fill in data from 'courses' table and put it in the dict.
        cur.execute("SELECT * FROM courses ORDER BY display_index ASC;")
        for record in cur:
            new_course = Course(name=record[0], after=record[1], enrichment_a=record[2], enrichment_b=record[3],
                                enrichment=record[4], approved_ud_nonmath=record[5], biology_requirement=record[6],
                                computation_requirement=record[7], prerequisites=record[9])
            self.classes_by_name[record[0]] = new_course

        # Get names of all of the majors currently offered
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'required' AND column_name != 'name';")
        majors = []
        for record in cur:
            majors.append(record[0])

        # Fill in data about major requirements from 'required' table.
        cur.execute("SELECT * FROM required;")
        for record in cur:
            required_dict = {}
            for i in range(1, len(record)):
                required_dict[majors[i - 1]] = record[i]
            self.classes_by_name[record[0]].required = required_dict

        # Get names of all of the majors currently offered
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'course_offerings' AND column_name != 'name';")
        quarters = []
        for record in cur:
            quarters.append(record[0])

        # Fill in data about course offerings from 'course_offerings' table.
        cur.execute("SELECT * FROM course_offerings;")
        for record in cur:
            quarters_offered = []
            for i in range(1, len(record)):
                if record[i]:
                    quarters_offered.append(quarters[i - 1])
            self.classes_by_name[record[0]].quarters_offered = quarters_offered
            self.classes_by_name[record[0]].offered_pattern = record[6]

        # Get names of all of the interests currently supported
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'interests' AND column_name != 'name';")
        interests = []
        num_interests = 0
        for record in cur:
            interests.append(self.convert_interest_format(record[0]))
            num_interests += 1


        # Fill in data about interests from 'interests' table.
        cur.execute("SELECT * FROM interests;")
        for record in cur:
            course_interests = []
            for i in range(1, num_interests + 1):
                if record[i]:
                    course_interests.append(interests[i - 1])
            self.classes_by_name[record[0]].interests = course_interests

        for course in self.classes_by_name:
            self.classes_offered.append(self.classes_by_name[course])
        conn.close()

    def get_info_from_csv(self):
        with open(resource_path('database/courses.csv'), newline='') as courses_csv:
            reader = csv.DictReader(courses_csv)
            # Fill in data from 'courses' CSV file and put it in the dict.
            for row in reader:
                enrichment_a = True if row['enrichment_a'] == 't' else False
                enrichment_b = True if row['enrichment_b'] == 't' else False
                enrichment = True if row['enrichment'] == 't' else False
                approved_ud_nonmath = True if row['approved_ud_nonmath'] == 't' else False
                biology_requirement = True if row['biology_requirement'] == 't' else False
                computation_requirement = True if row['computation_requirement'] == 't' else False
                prerequisites = row['prerequisites']
                new_course = Course(name=row['name'], after=row['after'], enrichment_a=enrichment_a,
                                    enrichment_b=enrichment_b, enrichment=enrichment,
                                    approved_ud_nonmath=approved_ud_nonmath,
                                    biology_requirement=biology_requirement,
                                    computation_requirement=computation_requirement, prerequisites=prerequisites)
                self.classes_by_name[row['name']] = new_course

        with open(resource_path('database/required.csv'), newline='') as required_csv:
            reader = csv.reader(required_csv)
            # Get names of all of the majors currently offered
            majors = next(reader)
            majors.pop(0)

            # Fill in data about major requirements from 'required' table.
            for row in reader:
                required_dict = {}
                for i in range(1,
                               len(row)):  # FIXME: want to make the range not hard-coded, want it to be able to dynamically figure out range.
                    required_dict[majors[i - 1]] = True if row[i] == "t" else False
                self.classes_by_name[row[0]].required = required_dict

        # Get names of all of the quarters currently offered
        with open(resource_path('database/course_offerings.csv'), newline='') as course_offerings_csv:
            reader = csv.reader(course_offerings_csv)
            quarters = next(reader)
            quarters.pop(0)

            # Fill in data about course offerings from 'course_offerings' table.
            for row in reader:
                quarters_offered = []
                for i in range(1, len(row) - 1):
                    if row[i] == 't':
                        quarters_offered.append(quarters[i - 1])
                self.classes_by_name[row[0]].quarters_offered = quarters_offered
                self.classes_by_name[row[0]].offered_pattern = row[len(row) - 1]

        # Get names of all of the interests currently supported
        with open(resource_path('database/interests.csv'), newline='') as interests_csv:
            reader = csv.reader(interests_csv)
            interests = next(reader)
            interests.pop(0)
            for i in range(len(interests)):
                interests[i] = self.convert_interest_format(interests[i])

            # Fill in data about interests from 'interests' table.
            for row in reader:
                course_interests = []
                for i in range(1, len(interests) + 1):
                    if row[i] == 't':
                        course_interests.append(interests[i - 1])
                self.classes_by_name[row[0]].interests = course_interests

        for course in self.classes_by_name:
            self.classes_offered.append(self.classes_by_name[course])


    def convert_interest_format(self, interest):
        interest = interest.replace("_", " ").title()
        return interest


    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    # https://stackoverflow.com/questions/33646605/how-to-access-variables-from-different-classes-in-tkinter
    def get_page(self, page_class):
        return self.frames[page_class]





if __name__ == "__main__":
    app = MultiPageApp()
    app.title("ScheduleBot 0.0.9-alpha")
    app.mainloop()