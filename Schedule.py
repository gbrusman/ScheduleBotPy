from AcademicTime import AcademicTime
from Course import Course
from ScheduleBlock import ScheduleBlock
from Student import Student


class Schedule:

    def __init__(self, student=Student(), classes_offered=[]):
        self.student = student
        self.classes_offered = classes_offered
        self.classes_by_name = {}
        self.schedule = {}
        for course in classes_offered:
            self.classes_by_name[course.name] = course

        #  doing interests a bit different than Java version. Making a dict of interests that map to list of class names
        #  as opposed to hash table of duplicate interests that map to class names
        self.interest_table = {}
        interests = ["Teaching", "Geometry", "Physics", "Biology", "Computers", "Finance", "Abstract", "Data Analysis"]
        for interest in interests:
            cur_interest = []
            for course in classes_offered:
                if course.interests is not None and interest in course.interests:
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
            cur_block = ScheduleBlock(cur_time)
            self.fill_from_after(cur_block, after, cur_time)
            self.try_to_fill_cur_time(cur_block, after, cur_time)
            for course in cur_block.courses:
                self.student.classes_taken[course.name] = course
            self.schedule[cur_time] = cur_block
            cur_time = cur_time.progress_time()
            self.student.cur_time = cur_time

    def add_course_to_block(self, course, block, after, time):
        block.courses.append(course)
        print("Adding ", course.name, " at ", time.quarter,  " ", time.year)
        after.append(course.after)
        self.classes_offered.remove(course)

    def add_course_from_after(self, course, block, after, time, index):
        block.courses.append(course)
        print("Adding ", course.name, " at ", time.quarter, " ", time.year)
        self.classes_offered.remove(course)
        after.pop(index)

    def fill_from_after(self, cur_block, after, cur_time):
        next_after = []
        loop_range = range(len(after))
        for i in loop_range:  # need to recompute this range because len(after) changes in loop
            after_course = self.classes_by_name.get(after[i], None)  # not sure if really what I want (see Schedule.java:120)
            if after_course is not None:
                if after_course.is_offered(cur_time) and after_course.required[self.student.major]:
                    self.add_course_from_after(after_course, cur_block, after, cur_time, i)
                    next_after.append(after_course.after)
                    loop_range = range(len(after))  # FIXME: Still doesn't update properly
                    i -= 1

        for i in range(len(next_after)):
            after.append(next_after(i))

    def try_to_fill_cur_time(self, cur_block, after, cur_time):
        required_or_electives = 0
        placed_interest = False

        while required_or_electives < 2:
            for i in range(len(self.classes_offered)):
                cur_course = self.classes_offered[i]
                if len(cur_block.courses) == 2:
                    break
                if self.class_is_valid(cur_course, cur_time, cur_block):
                    if required_or_electives == 0:
                        if cur_course.required[self.student.major]:
                            self.add_course_to_block(cur_course, cur_block, after, cur_time)
                    else:
                        placed_interest = self.try_to_place_interesting_class(cur_course, cur_block, cur_time, after)
                        if not placed_interest:
                            self.add_course_to_block(cur_course, cur_block, after, cur_time)
                        i -= 1  # to balance index
            required_or_electives += 1

    def is_redundant(self, course, block):
        switcher = {
            "MAT67": self.mat67_redundant,
            "MAT22AL": self.mat22al_redundant,
            "ECS32A": self.ecs32a_redundant,
            "MAT128A": self.mat128a_redundant,
            "MAT128B": self.mat128b_redundant,
            "MAT128C": self.mat128c_redundant
        }
        func = switcher.get(course.name)
        if func is None:
            return False
        if course.name == "MAT22A" or course.name == "MAT22AL":
            return func(block)
        return func()

    def try_to_place_interesting_class(self, cur_course, cur_block, cur_time, after):
        placed_interest = False
        for interest in self.student.interests:  # run through list of student interests
            cur_interest_table = self.interest_table[interest]
            if cur_course in cur_interest_table:  # add course if it coincides with interest
                self.add_course_to_block(cur_course, cur_block, after, cur_time)
                placed_interest = True
                break
            else:  # see if there's an "interesting" class that can be placed here (not very efficient implementation)
                for interest_course in cur_interest_table.values():
                    if self.class_is_valid(interest_course, cur_time, cur_block):
                        self.add_course_to_block(interest_course, cur_block, after, cur_time)
                        placed_interest = True
                        break
        return placed_interest

    def class_is_valid(self, course, time, block):
        return course.is_offered(time) and self.student.has_prereqs(course, block) and not self.student.has_taken(course.name) and self.student.meets_reccommendations(course) and not self.is_redundant(course, block) and not block.contains(course.name)

    def mat67_redundant(self, block):
        return self.student.has_taken("MAT22A") or self.student.has_taken("MAT108") or block.contains("MAT22A") or block.contains("MAT108")

    def mat22al_redundant(self, block):
        return self.student.has_taken("ENG06") or block.contains("ENG06")

    def ecs32a_redundant(self):
        return self.student.major == "LMATAB1" or self.student.major == "LMATBS2"

    def mat128a_redundant(self):
        if self.student.major == "LAMA":
            return self.student.has_taken("MAT128B") and self.student.has_taken("MAT128C")
        if self.student.major == "LMOR" and "Computers" not in self.student.interests:
            return self.student.has_taken("MAT128B") or self.student.has_taken("MAT128C")

    def mat128b_redundant(self):
        if self.student.major == "LAMA" and "Computers" not in self.student.interests:
            return self.student.has_taken("MAT128A") and self.student.has_taken("MAT128C")
        
        if self.student.major == "LMOR" and "Computers" not in self.student.interests:
            return self.student.has_taken("MAT128A") or self.student.has_taken("MAT128C")

    def mat128c_redundant(self):
        if self.student.major == "LAMA" and "Computers" not in self.student.interests:
            return self.student.has_taken("MAT128A") and self.student.has_taken("MAT128B")
        
        if self.student.major == "LMOR" and "Computers" not in self.student.interests:
            return self.student.has_taken("MAT128A") or self.student.has_taken("MAT128B")
        






