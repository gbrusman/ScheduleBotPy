from AcademicTime import AcademicTime
from Course import Course
from ScheduleBlock import ScheduleBlock
from Student import Student

class Schedule:

    def __init__(self, student = Student(), classes_offered = []):
        self.student = student
        self.classes_offered = classes_offered
        self.classes_by_name = {}
        for course in classes_offered:
            self.classes_by_name[course.name] = course

        #  doing interests a bit different than Java version. Making a dict of interests that map to list of class names
        #  as opposed to hash table of duplicate interests that map to class names
        self.interest_table = {}
        interests = ["Teaching", "Geometry", "Physics", "Biology", "Computers", "Finance", "Abstract", "Data Analysis"]
        for interest in interests:
            cur_interest = []
            for course in classes_offered:
                if course.interests != [] and interest in course.interests:
                    cur_interest.append(course.name)
            self.interest_table[interest] = cur_interest

        self.place_classes()

    def place_classes(self):
        grad_time = self.student.grad_time
        cur_time = self.student.cur_time
        cur_time = cur_time.progress_time()  # want to start scheduling on NEXT quarter
        after = []
        finish_time = self.student.grad_time.progress_time()  # due to semantics we want to stop taking classes the quarter AFTER they graduate

        while cur_time != finish_time:  # need to override __eq__ in AcademicTime
            print("Line 77 in Schedule.Java ^")

