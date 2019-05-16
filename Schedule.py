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
                    cur_interest.append(course)
            self.interest_table[interest] = cur_interest

        self.fix_21series()  # e.g. if student selected they took 21B, adds 21A to their classes_taken to prevent conflicts
        self.place_classes()
        if self.is_success():
            print("SUCCESS! :D")
        else:
            print("FAILURE! ;(")

    def fix_21series(self):
        if "MAT21D" in self.student.classes_taken:
            if "MAT21C" not in self.student.classes_taken:
                self.student.classes_taken["MAT21C"] = self.classes_by_name["MAT21C"]
            if "MAT21B" not in self.student.classes_taken:
                self.student.classes_taken["MAT21B"] = self.classes_by_name["MAT21B"]
            if "MAT21A" not in self.student.classes_taken:
                self.student.classes_taken["MAT21A"] = self.classes_by_name["MAT21A"]
        if "MAT21C" in self.student.classes_taken:
            if "MAT21B" not in self.student.classes_taken:
                self.student.classes_taken["MAT21B"] = self.classes_by_name["MAT21B"]
            if "MAT21A" not in self.student.classes_taken:
                self.student.classes_taken["MAT21A"] = self.classes_by_name["MAT21A"]
        if "MAT21B" in self.student.classes_taken:
            if "MAT21A" not in self.student.classes_taken:
                self.student.classes_taken["MAT21A"] = self.classes_by_name["MAT21A"]

    def place_classes(self):
        grad_time = self.student.grad_time
        cur_time = self.student.cur_time
        cur_time = cur_time.progress_time()  # want to start scheduling on NEXT quarter
        self.student.cur_time = cur_time
        after = []
        finish_time = grad_time.progress_time()  # due to semantics we want to stop taking classes the quarter AFTER they graduate

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
        if not course.required[self.student.major]:
            self.student.num_enrichments += 1

    def add_course_from_after(self, course, block, after, time, index):
        block.courses.append(course)
        print("Adding ", course.name, " at ", time.quarter, " ", time.year)
        self.classes_offered.remove(course)
        after.pop(index)
        if not course.required[self.student.major]:
            self.student.num_enrichments += 1

    def fill_from_after(self, cur_block, after, cur_time):
        next_after = []
        i = 0
        while i < len(after):  # need to recompute this range because len(after) changes in loop
            after_course = self.classes_by_name.get(after[i], None)  # not sure if really what I want (see Schedule.java:120)
            if after_course is not None:
                if after_course.is_offered(cur_time) and after_course.required[self.student.major]:
                    self.add_course_from_after(after_course, cur_block, after, cur_time, i)
                    next_after.append(after_course.after)
                    i -= 1
            i += 1

        for i in range(len(next_after)):
            after.append(next_after[i])

    def try_to_fill_cur_time(self, cur_block, after, cur_time):
        required_or_electives = 0
        placed_interest = False

        while required_or_electives < 2:
            i = 0
            while i < len(self.classes_offered):
                cur_course = self.classes_offered[i]
                if len(cur_block.courses) == 2:
                    break
                if self.class_is_valid(cur_course, cur_time, cur_block):
                    if required_or_electives == 0:
                        if cur_course.required[self.student.major]:
                            self.add_course_to_block(cur_course, cur_block, after, cur_time)
                            i -= 1  # to balance index
                    else:
                        placed_interest = self.try_to_place_interesting_class(cur_course, cur_block, cur_time, after)
                        if not placed_interest:
                            self.add_course_to_block(cur_course, cur_block, after, cur_time)
                        i -= 1  # to balance index
                i += 1
            required_or_electives += 1

    def is_redundant(self, course, block):
        switcher = {
            "MAT67": self.mat67_redundant,
            "MAT22AL": self.mat22al_redundant,
            "ECS32A": self.ecs32a_redundant,
            "MAT128A": self.mat128a_redundant,
            "MAT128B": self.mat128b_redundant,
            "MAT128C": self.mat128c_redundant,
            "PHY7A": self.phy7a_redundant
        }
        if self.is_pointless(course):
            return True
        func = switcher.get(course.name)
        if func is None:
            return False
        if course.name == "MAT22A" or course.name == "MAT22AL" or course.name == "MAT67":
            return func(block)
        return func()

    def is_pointless(self, course):  # checks to see if we're adding a class that provides absolutely no benefit
        if course.required[self.student.major]:
            return False
        departments = ["MAT", "ECS", "STA", "ARE", "CHE", "PHY", "ARE", "ECN", "BIS"]
        if course.name[:3] not in departments:
            return True
        i = 3
        num_str = ""
        while course.name[i].isdigit() and i < len(course.name) - 1:
            num_str += course.name[i]
            i += 1
        if not int(num_str) >= 100:
            return True

    def try_to_place_interesting_class(self, cur_course, cur_block, cur_time, after):
        placed_interest = False
        for interest in self.student.interests:  # run through list of student interests
            cur_interest_table = self.interest_table[interest]
            if cur_course in cur_interest_table:  # add course if it coincides with interest
                self.add_course_to_block(cur_course, cur_block, after, cur_time)
                placed_interest = True
                break
            else:  # see if there's an "interesting" class that can be placed here (not very efficient implementation)
                for interest_course in cur_interest_table:
                    if self.class_is_valid(interest_course, cur_time, cur_block):
                        self.add_course_to_block(interest_course, cur_block, after, cur_time)
                        placed_interest = True
                        break
        return placed_interest

    def class_is_valid(self, course, time, block):
        return course.is_offered(time) and self.student.has_prereqs(course, block) and (not self.student.has_taken(course.name)) and self.student.meets_reccommendations(course) and (not self.is_redundant(course, block)) and (not block.contains(course))

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

    def phy7a_redundant(self):
        for course in self.classes_offered:
            if course.name == "PHY9B" and course.required["LAMA"]:  #checks if student is applied and chose physics as 2quarter sequence
                return True
        return False

    def is_success(self):
        major = self.student.major
        switcher = {
            "LAMA": self.is_success_LAMA,
            "LMOR": self.is_success_LMOR,
            "LMATBS1": self.is_success_LMATBS1,
            "LMATBS2": self.is_success_LMATBS2,
            "LMATAB1": self.is_success_LMATAB1,
            "LMATAB2": self.is_success_LMATAB2,
            "LMCOBIO": self.is_success_LMCOBIO,
            "LMCOMATH": self.is_success_LMCOMATH

        }
        func = switcher.get(major)
        return func()

    def is_success_LAMA(self):
        requirements = ["MAT21A", "MAT21B", "MAT21C", "MAT21D", "MAT22A", "MAT22B", "MAT108", "ENG06", "ECS32A", "MAT127A", "MAT127B", "MAT127C", "MAT135A", "MAT150A", "MAT119A", "MAT185A"]
        two_quarter_series = ["PHY9A", "PHY9B", "CHE2A", "CHE2B", "BIS2A", "BIS2B", "STA32", "STA100", "ECN1A", "ECN1B"]
        num_two_quarter_courses = 0
        for course_name in requirements:
            if course_name not in self.student.classes_taken.keys():
                return False
        if self.student.num_enrichments < 2:
            return False
        for course in two_quarter_series:
            if self.student.has_taken(course):
                num_two_quarter_courses += 1
        if num_two_quarter_courses < 2:
            return False
        return True

    def is_success_LMOR(self):
        requirements = ["MAT21A", "MAT21B", "MAT21C", "MAT21D", "MAT22A", "MAT22B", "MAT108", "ENG06", "ECN1A", "ECN1B", "STA32", "MAT127A", "MAT127B", "MAT127C", "MAT135A", "MAT135B", "MAT150A", "MAT160", "MAT168"]
        for course_name in requirements:
            if course_name not in self.student.classes_taken.keys():
                return False
        if self.student.num_enrichments < 4:  #Enrichment A and B, current system doesn't work here
            return False
        return True

    def is_success_LMATBS1(self):
        requirements = ["MAT21A", "MAT21B", "MAT21C", "MAT21D", "MAT22A", "MAT22B", "MAT108", "ENG06", "PHY9A", "MAT127A",
                        "MAT127B", "MAT127C", "MAT135A", "MAT150A", "MAT150B", "MAT150C", "MAT185A"]
        for course_name in requirements:
            if course_name not in self.student.classes_taken.keys():
                return False
        if self.student.num_enrichments < 4:
            return False
        return True

    def is_success_LMATBS2(self):
        requirements = ["MAT21A", "MAT21B", "MAT21C", "MAT21D", "MAT22A", "MAT22B", "MAT108", "ENG06", "MAT127A",
                        "MAT127B", "MAT127C", "MAT135A", "MAT150A", "MAT111", "MAT115A", "MAT141"]
        for course_name in requirements:
            if course_name not in self.student.classes_taken.keys():
                return False
        if self.student.num_enrichments < 4:
            return False
        return True

    def is_success_LMATAB1(self):
        requirements = ["MAT21A", "MAT21B", "MAT21C", "MAT21D", "MAT22A", "MAT22B", "MAT108", "ENG06", "MAT127A",
                        "MAT127B", "MAT127C", "MAT135A", "MAT150A"]
        for course_name in requirements:
            if course_name not in self.student.classes_taken.keys():
                return False
        if self.student.num_enrichments < 4:
            return False
        return True

    def is_success_LMATAB2(self):
        requirements = ["MAT21A", "MAT21B", "MAT21C", "MAT21D", "MAT22A", "MAT108", "MAT22B", "ENG06", "MAT127A",
                        "MAT127B", "MAT127C", "MAT135A", "MAT150A", "MAT111", "MAT115A", "MAT141"]
        for course_name in requirements:
            if course_name not in self.student.classes_taken.keys():
                return False
        if self.student.num_enrichments < 4:
            return False
        return True

    def is_success_LMCOBIO(self):
        requirements = ["MAT21A", "MAT21B", "MAT21C", "MAT21D", "MAT22A", "MAT22B", "ENG06", "MAT108", "ECS32A", "MAT127A",
                        "MAT127B", "MAT127C", "MAT128A", "MAT128B", "MAT128C", "MAT135A", "MAT150A", "MAT124"]
        for course_name in requirements:
            if course_name not in self.student.classes_taken.keys():
                return False
        if self.student.num_enrichments < 2:
            return False
        return True

    def is_success_LMCOMATH(self):
        requirements = ["MAT21A", "MAT21B", "MAT21C", "MAT21D", "MAT22A", "MAT22B", "ENG06", "MAT108", "ECS32A", "MAT127A",
                        "MAT127B", "MAT127C", "MAT128A", "MAT128B", "MAT128C", "MAT135A", "MAT150A", "MAT168"]
        for course_name in requirements:
            if course_name not in self.student.classes_taken.keys():
                return False
        if self.student.num_enrichments < 2:
            return False
        return True