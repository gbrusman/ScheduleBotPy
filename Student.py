from AcademicTime import AcademicTime
import csv
import os
import sys


arr_128s = ["MAT128A", "MAT128B", "MAT128C"]
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Student:
    """
    This is a class to represent the student for which the schedule is being created.

    Attributes:
        cur_time (AcademicTime): The current time (Quarter, Year).
        major (string): The major the student is pursuing.
        interests (list): The students interests within mathematics. Each interest is a string.
        classes_taken (dict): The classes the student has already taken up until cur_time. Keys are course names, values are Course objects.
        start_time (AcademicTime): The AcademicTime that represents the student's first quarter at UC Davis.
        num_enrichments (int): The number of enrichment courses the student has taken up until cur_time.
    """
    def __init__(self, cur_time=AcademicTime(), major="", interests=[], classes_taken={}, num_enrichments=0, num_enrichments_a=0, num_enrichments_b=0, summer_quarters=[]):
        """The constructor for the Student class."""
        self.cur_time = cur_time
        self.major = major
        self.interests = interests
        self.classes_taken = classes_taken
        self.start_time = AcademicTime(cur_time.year, cur_time.quarter)
        self.num_enrichments = num_enrichments
        self.num_enrichments_a = num_enrichments_a
        self.num_enrichments_b = num_enrichments_b
        self.has_taken_approved_ud_nonmath_req = False
        self.has_taken_biology_req = False
        self.has_taken_computation_req = False
        self.num_128s = 0
        self.not_taken_128s = arr_128s
        self.summer_quarters = summer_quarters

        self.num128s_needed = {"LMATAB1": 0, "LMATAB2": 0, "LMATBS1": 0, "LMATBS2": 0, "LAMA": 2, "LMCOBIO": 3, "LMCOMATH": 3,
                       "LMOR": 1}

    def update_128_count(self, course):
        if course.name in arr_128s:
            self.num_128s += 1
            self.not_taken_128s.remove(course.name)


    def initialize_128_count(self):
        for course_name in self.classes_taken:
            if course_name in arr_128s:
                self.num_128s += 1
                self.not_taken_128s.remove(course_name)
                if self.num_128s > self.num128s_needed[self.major]:
                    self.num_enrichments += 1




    def check_major_specific_requirements(self):
        for course in self.classes_taken:
            if self.classes_taken[course].approved_ud_non_math:
                self.has_taken_approved_ud_nonmath_req = True
            if self.classes_taken[course].biology_requirement:
                self.has_taken_biology_req = True
            if self.classes_taken[course].computation_requirement:
                self.has_taken_computation_req = True

    def initialize_enrichment_counts(self):
        for course in self.classes_taken:
            enrichment_counted = False
            if self.classes_taken[course].enrichment and not self.classes_taken[course].required[self.major]:
                self.num_enrichments += 1
                enrichment_counted = True
            if self.classes_taken[course].enrichment_a:
                self.num_enrichments_a += 1
                if not enrichment_counted:
                    self.num_enrichments += 1
                    enrichment_counted = True
            if self.classes_taken[course].enrichment_b:
                self.num_enrichments_b += 1
                if not enrichment_counted:
                    self.num_enrichments += 1


    def update_enrichment_counts(self, course):
        # only really need enrichment a/b checks for LMOR but it won't hurt the other cases
        mat128s = ["MAT128A", "MAT128B", "MAT128C"]
        if course.enrichment_a:
            self.num_enrichments_a += 1
            if self.major == "LMOR":
                self.num_enrichments += 1
        if course.enrichment_b:
            self.num_enrichments_b += 1
            if self.major == "LMOR":
                self.num_enrichments += 1
        if course.enrichment and not course.required[self.major]:
            if course.name in mat128s:
                if self.num_128s > self.num128s_needed[self.major]:
                    self.num_enrichments += 1
            else:
                self.num_enrichments += 1

    def is_taking(self, course_name, block):
        """Function to test whether a student is currently taking a Course (in cur_time). Returns boolean."""
        if block.contains(course_name):
            return True
        return False


    def meets_reccommendations(self, course): #FIXME: Need to deprecate this and just include anything necessary into the prereqs DB.
        """Function to test whether a student meets the recommendations to take a course. Returns boolean.

        Extra Info:
            These recommendations are not mandated by course requirements, but are recipes for success from the advising team.
        """
        name = course.name
        # https://jaxenter.com/implement-switch-case-statement-python-138315.html
        switcher = {
            "ECN1B": self.ecn1b_rec,
            "ECS32A": self.ecs32a_rec,
            "MAT108": self.mat108_rec,
            "MAT22A": self.mat22a_rec,
            "MAT180": self.mat180_rec,
            "MAT150A": self.mat150a_rec,
            "MAT185A": self.mat185a_rec,
            # FIXME: Add these two back and revert database changes and revert other 128 changes I made in Schedule.py?
            #"MAT128B": self.mat128b_rec,
            #"MAT128C": self.mat128c_rec
        }
        func = switcher.get(name)
        if func is None:
            return True
        return func()

    def has_taken(self, course_name):
        """Function to test whether a student has already taken a course in a previous quarter. Returns boolean."""
        return course_name in self.classes_taken.keys()

    def find_prereq_string(self, query_course):
        solution = ""


        unformatted_prereqs = query_course.prerequisites
        if unformatted_prereqs == None:
            return "True"

        split_prereqs = unformatted_prereqs.split()

        for word in split_prereqs:
            if word not in ['or', 'and']:  # If word is a classname and not a logical operator
                if word[0] == '(':
                    num_left_parens = 1
                    while word[num_left_parens] == '(':
                        num_left_parens += 1
                    new_word = ("(" * num_left_parens) + "self.has_taken" + "(\'" + word[
                                                                                            num_left_parens:] + "\')"
                else:
                    new_word = "self.has_taken(\'" + word + "\')"
                # Properly place end quote before right paren on words with right paren.
                if word[len(word) - 1] == ')':
                    num_right_parens = 1
                    while word[len(word) - num_right_parens] == ')':
                        num_right_parens += 1
                    new_word = new_word[0:len(new_word) - (1 + num_right_parens)] + "\'" + (")" * num_right_parens)
                solution += new_word + " "

            else:
                solution += word + " "
        return solution

    def find_prereq_string_from_csv(self, query_course):
        solution = ""
        with open(resource_path('database/courses.csv'), newline='') as courses_csv:
            reader = csv.DictReader(courses_csv)
            target_row = []
            for row in reader:
                if row['name'] == query_course:
                    target_row = row
                    break
            if not target_row:
                return "True"

            split_prereqs = target_row['prerequisites'].split()
            if not split_prereqs:
                return "True"

            for word in split_prereqs:
                if word not in ['or', 'and']:  # If word is a classname and not a logical operator
                    if word[0] == '(':
                        num_left_parens = 1
                        while word[num_left_parens] == '(':
                            num_left_parens += 1
                        new_word = ("(" * num_left_parens) + "self.has_taken" + "(\'" + word[
                                                                                                num_left_parens:] + "\')"
                    else:
                        new_word = "self.has_taken(\'" + word + "\')"
                    # Properly place end quote before right paren on words with right paren.
                    if word[len(word) - 1] == ')':
                        num_right_parens = 1
                        while word[len(word) - num_right_parens] == ')':
                            num_right_parens += 1
                        new_word = new_word[0:len(new_word) - (1 + num_right_parens)] + "\'" + (")" * num_right_parens)
                    solution += new_word + " "

                else:
                    solution += word + " "
            return solution

    def has_prereqs(self, course, block):
        """Function to test whether a student has the prereqs necessary to take a course. Returns boolean."""
        try:
            prereq_string = self.find_prereq_string(course)
        except:
            prereq_string = self.find_prereq_string_from_csv(course)
        # prereq_string = self.find_prereq_string_from_csv(course.name)

        if prereq_string == "":
            return True
        return eval(prereq_string)


    def ecn1b_rec(self):
        return self.has_taken("ECN1A")

    def ecs32a_rec(self):
        return self.start_time != self.cur_time

    def mat108_rec(self):
        return self.has_taken("MAT21C")

    def mat22a_rec(self):
        return self.has_taken("MAT21C")

    def mat128b_rec(self):
        return self.has_taken("MAT128A")

    def mat128c_rec(self):
        return self.has_taken("MAT128A")

    def mat150a_rec(self):
        return self.num_enrichments >= 1  # will help push it back to senior year

    def mat185a_rec(self):
        return self.num_enrichments >= 1  # will help push it back to senior year

    def mat180_rec(self):
        return self.num_enrichments >= 2




















