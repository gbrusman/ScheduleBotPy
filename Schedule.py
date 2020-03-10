from AcademicTime import AcademicTime
from ScheduleBlock import ScheduleBlock
from Student import Student
import psycopg2

MAX_TOT_CLASSES_PER_QUARTER = 3
MAX_MATH_CLASSES_PER_QUARTER = 2
SUMMER_MAX_TOT_CLASSES_PER_QUARTER = 2
SUMMER_MAX_MATH_CLASSES_PER_QUARTER = 1

# FIXME: Pull these from database.
LMOR_ENRICHMENTS_A_NEEDED = 2
LMOR_ENRICHMENTS_B_NEEDED = 2


def convert_interest_format(interest):
    interest = interest.replace("_", " ").title()
    return interest

# Pull interests from database.
conn = psycopg2.connect(host="rajje.db.elephantsql.com", database="ytmelfsd", user="ytmelfsd",
                                password="PY2TKJsTJD2cOPlRbwQgVJPHgc4vhWvT")
cur = conn.cursor()
# Get names of all of the interests currently supported
cur.execute(
    "SELECT column_name FROM information_schema.columns WHERE table_name = 'interests' AND column_name != 'name';")
interests = []
for record in cur:
    interests.append(convert_interest_format(record[0]))

cur.execute("SELECT major, num_enrichments_a_needed, num_enrichments_b_needed, num_enrichments_needed from student_vars;")
# FIXME: make table or something to store number of enrichment_a's, b's, and total for each major.
enrichment_dict = {}
for record in cur:
    enrichment_dict[record[0]] = {"num_enrichments_a_needed": record[1], "num_enrichments_b_needed": record[2], "num_enrichments_needed": record[3]}

conn.close()

class Schedule:
    """
    This is a class that contains all of the data of the schedule, and uses that data to create a schedule.

    Attributes:
        student (Student): The Student object for which the schedule is created.
        classes_offered (list): The list of classes offered by the UC Davis Math Department.
        classes_by_name (dict): The list of classes, but in a map format. Keys are course names, values are Course objects.
        schedule (dict): A map whose keys are objects of type AcademicTime, and whose values are objects of type ScheduleBlock.
        interest_table (dict): A map whose keys are strings (interests), and whose values are lists of classes that fall under the interest.
    """

    def __init__(self, student=Student(), classes_offered=[], elective_classes_offered=[]):
        """The constructor for the Schedule class. Create schedule for student based on student attributes and what classes are offered."""

        self.student = student
        self.classes_offered = classes_offered
        self.elective_classes_offered = elective_classes_offered
        self.classes_by_name = {}
        self.schedule = {}
        self.finish_time = AcademicTime()
        for course in classes_offered:
            self.classes_by_name[course.name] = course


        #  doing interests a bit different than Java version. Making a dict of interests that map to list of class names
        #  as opposed to hash table of duplicate interests that map to class names
        self.interest_table = {}

        for interest in interests:
            cur_interest = []
            for course in classes_offered:
                if course.interests is not None and interest in course.interests:
                    cur_interest.append(course)
            self.interest_table[interest] = cur_interest

        self.fix_21series()  # e.g. if student selected they took 21B, adds 21A to their classes_taken to prevent conflicts
        self.fix_MAT67()  # if student has taken MAT 67 then mark 108 and 22a as not required
        self.student.initialize_enrichment_counts()
        self.student.initialize_128_count()
        self.place_classes()

    def fix_MAT67(self):
        """function that marks 108 and 22A as not required if the student has already taken MAT67"""
        if "MAT67" in self.student.classes_taken:
            for i in range(len(self.classes_offered)):
                if self.classes_offered[i].name == "MAT108" or self.classes_offered[i].name == "MAT22A":
                    self.classes_offered[i].required[self.student.major] = False


    def fix_21series(self):
        """Function to add implicit 21 series prereqs to student's classes_taken list"""
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
        """Function to oversee class placement / creation of the actual schedule."""
        cur_time = self.student.cur_time
        cur_time = cur_time.progress_time(self.student.summer_quarters)  # want to start scheduling on NEXT quarter
        self.student.cur_time = cur_time
        after = []


        while not self.new_is_success():
            cur_block = ScheduleBlock(cur_time)
            self.fill_from_after(cur_block, after, cur_time)
            self.try_to_fill_cur_time(cur_block, after, cur_time)
            for course in cur_block.courses:
                self.student.classes_taken[course.name] = course
            self.schedule[cur_time] = cur_block
            cur_time = cur_time.progress_time(self.student.summer_quarters)
            self.student.cur_time = cur_time
        self.finish_time.quarter = cur_time.quarter
        self.finish_time.year = cur_time.year

    def add_course_to_block(self, course, block, after, time):
        """Function to add a Course object to a ScheduleBlock object"""
        block.courses.append(course)
        print("Adding ", course.name, " at ", time.quarter,  " ", time.year)
        after.append(course.after)
        self.classes_offered.remove(course)
        self.student.update_128_count(course)
        self.update_128_required()
        self.student.update_enrichment_counts(course)


    def add_course_from_after(self, course, block, after, time, index):
        """Function to add a Course object to a ScheduleBlock object from the after list of a previously added class."""
        block.courses.append(course)
        print("Adding ", course.name, " at ", time.quarter, " ", time.year)
        self.classes_offered.remove(course)
        after.pop(index)
        self.student.update_enrichment_counts(course)


    def fill_from_after(self, cur_block, after, cur_time):
        """Function to fill in classes from after list generated in the previous quarter."""
        next_after = []
        i = 0
        while i < len(after):
            after_course = self.classes_by_name.get(after[i], None)
            if after_course is not None:
                if after_course.is_offered(cur_time) and after_course.required[self.student.major] and self.class_is_valid(after_course, cur_time, cur_block):
                    self.add_course_from_after(after_course, cur_block, after, cur_time, i)
                    next_after.append(after_course.after)
                    i -= 1
            i += 1

        for i in range(len(next_after)):
            after.append(next_after[i])


    def try_to_fill_cur_time(self, cur_block, after, cur_time):
        """Function to fill the ScheduleBlock at the current time with classes"""
        required_or_electives = 0
        placed_interest = False
        max_tot_classes_per_quarter = MAX_TOT_CLASSES_PER_QUARTER
        max_math_class_per_quarter = MAX_MATH_CLASSES_PER_QUARTER
        list_to_iterate = self.classes_offered

            # Use normal self.classes_offered for first iteration, use randomly-ordered list only with not-required courses for the 2nd iteration.
        while required_or_electives < 2:
            i = 0
            while i < len(list_to_iterate):
                #cur_course = self.classes_offered[i]
                cur_course = list_to_iterate[i]
                self.fix_ENG06(i)
                if cur_time.quarter == "Summer Session 1" or cur_time.quarter == "Summer Session 2":
                    max_tot_classes_per_quarter = SUMMER_MAX_TOT_CLASSES_PER_QUARTER
                    max_math_class_per_quarter = SUMMER_MAX_MATH_CLASSES_PER_QUARTER
                if len(cur_block.courses) == max_tot_classes_per_quarter:
                    break
                if self.class_is_valid(cur_course, cur_time, cur_block):
                    if self.num_math_classes(cur_block) == max_math_class_per_quarter and cur_course.name[:3] == "MAT":  # don't want to take >2 math courses in one quarter
                        i += 1
                        continue
                    if required_or_electives == 0:
                        if cur_course.required[self.student.major]:
                            self.add_course_to_block(cur_course, cur_block, after, cur_time)
                            i -= 1  # to balance index
                    else:
                        placed_interest = self.try_to_place_interesting_class(cur_course, cur_block, cur_time, after)
                        if not placed_interest:
                            if not (self.num_math_classes(cur_block) == MAX_MATH_CLASSES_PER_QUARTER and cur_course.name[:3] == "MAT"):
                                self.add_course_to_block(cur_course, cur_block, after, cur_time)
                        i -= 1  # to balance index
                i += 1
            required_or_electives += 1
            list_to_iterate = self.elective_classes_offered


    def fix_ENG06(self, i):
        if(self.student.major == "LMOR" and self.classes_offered[i].name == "ENG06" and self.student.has_taken("MAT22AL") and self.student.has_taken("ECS32A")):
            self.classes_offered[i].required["LMOR"] = False

    def is_redundant(self, course, block):
        """Function to test whether or not a class is redundant to take. Returns boolean."""
        switcher = {
            "MAT67": self.mat67_redundant,
            "MAT22AL": self.mat22al_redundant,
            "ECS32A": self.ecs32a_redundant,
            "PHY7A": self.phy7a_redundant,
            "ECS124": self.ecs124_redundant,
            "ECS129": self.ecs129_redundant,
            "ECS170": self.ecs170_redundant,
            "STA141A": self.sta141a_redundant,
            "ENG06": self.eng06_redundant
        }
        if self.is_pointless(course):
            return True
        func = switcher.get(course.name)
        if func is None:
            return False
        if course.name == "MAT22A" or course.name == "MAT22AL" or course.name == "MAT67":
            return func(block)
        return func()

    def update_128_required(self):
        if self.student.num_128s >= self.student.num128s_needed[self.student.major]:
            for name in self.student.not_taken_128s:
                self.classes_by_name[name].required[self.student.major] = False
                self.classes_by_name[name].enrichment_a = True


    def is_pointless(self, course):  # checks to see if we're adding a class that provides absolutely no benefit
        """Function to test whether or not a class is pointless to take. Returns boolean."""
        MAT128s = ["MAT128A", "MAT128B", "MAT128C"]

        if course.name in MAT128s and self.student.num_128s >= self.student.num128s_needed[self.student.major]:

            for name in self.student.not_taken_128s:
                self.classes_by_name[name].required[self.student.major] = False
                self.classes_by_name[name].enrichment_a = True

            return True

        if course.required[self.student.major] or (course.name in MAT128s and self.student.num_128s < self.student.num128s_needed[self.student.major]):
            return False

        if self.student.major == "LMOR":
            if self.student.num_enrichments_b < enrichment_dict["LMOR"]["num_enrichments_b_needed"] and course.enrichment_b:
                return False
            if (self.student.num_enrichments_a >= enrichment_dict["LMOR"]["num_enrichments_a_needed"] and course.enrichment_a) or (self.student.num_enrichments_b >= enrichment_dict["LMOR"]["num_enrichments_b_needed"] and course.enrichment_b):
                return True
        elif self.student.major == "LAMA":
            if (self.student.num_enrichments >= enrichment_dict["LAMA"]["num_enrichments_needed"] and course.enrichment) or (self.student.has_taken_approved_ud_nonmath_req and course.approved_ud_nonmath):
                return True
        elif self.student.major == "LMCOBIO":
            if (self.student.num_enrichments >= enrichment_dict["LMCOBIO"]["num_enrichments_needed"] and course.enrichment) or (self.student.has_taken_biology_req and course.biology_requirement):
                return True
        elif self.student.major == "LMCOMATH":
            if (self.student.num_enrichments >= enrichment_dict["LMCOMATH"]["num_enrichments_needed"] and course.enrichment) or (self.student.has_taken_computation_req and course.computation_requirement):
                return True
        else:
            if (self.student.num_enrichments >= enrichment_dict[self.student.major]["num_enrichments_needed"] and course.enrichment) and (not course.approved_ud_nonmath):
                return True


        if not course.enrichment:
            return True

        departments = ["MAT", "ECS", "STA", "ARE", "CHE", "PHY", "ARE", "ECN", "BIS"]
        if course.name[:3] not in departments:
            return True
        i = 3
        i = 3
        num_str = ""
        while i < len(course.name) and course.name[i].isdigit():
            num_str += course.name[i]
            i += 1
        if not int(num_str) >= 100:
            return True
        return False

    def try_to_place_interesting_class(self, cur_course, cur_block, cur_time, after):
        """Function to try to place a course in the current ScheduleBlock that applies to the student's interests."""
        placed_interest = False
        for interest in self.student.interests:  # run through list of student interests
            cur_interest_table = self.interest_table[interest]
            if cur_course in cur_interest_table:  # add course if it coincides with interest
                if not (self.num_math_classes(cur_block) == MAX_MATH_CLASSES_PER_QUARTER and cur_course.name[:3] == "MAT"):
                    self.add_course_to_block(cur_course, cur_block, after, cur_time)
                    placed_interest = True
                    break
            else:  # see if there's an "interesting" class that can be placed here (not very efficient implementation)
                for interest_course in cur_interest_table:
                    if self.class_is_valid(interest_course, cur_time, cur_block):
                        if not (self.num_math_classes(cur_block) == MAX_MATH_CLASSES_PER_QUARTER and interest_course.name[:3] == "MAT"):
                            self.add_course_to_block(interest_course, cur_block, after, cur_time)
                            placed_interest = True
                            break
        return placed_interest

    def class_is_valid(self, course, time, block):
        """Function to test whether or not the course can be taken."""
        return course.is_offered(time) and self.student.has_prereqs(course, block) and \
               (not self.student.has_taken(course.name)) and self.student.meets_reccommendations(course) and \
               (not self.is_redundant(course, block)) and (not block.contains(course))

    def ecs124_redundant(self):  # might need to check if student is actually LMCO Math/Bio
        redundancies = ["ECS129", "ECS170", "STA141A"]
        for name in redundancies:
            if self.student.has_taken(name):
                return True
        return False

    def ecs129_redundant(self):
        redundancies = ["ECS124", "ECS170", "STA141A"]
        for name in redundancies:
            if self.student.has_taken(name):
                return True
        return False

    def ecs170_redundant(self):
        redundancies = ["ECS129", "ECS124", "STA141A"]
        for name in redundancies:
            if self.student.has_taken(name):
                return True
        return False

    def sta141a_redundant(self):
        redundancies = ["ECS129", "ECS170", "ECS124"]
        for name in redundancies:
            if self.student.has_taken(name):
                return True
        return False

    def mat67_redundant(self, block):
        return self.student.has_taken("MAT22A") or self.student.has_taken("MAT108") or block.contains("MAT22A") or block.contains("MAT108")

    def mat22al_redundant(self, block):
        return self.student.has_taken("ENG06") or block.contains("ENG06")

    def ecs32a_redundant(self):
        return self.student.major == "LMATAB1" or self.student.major == "LMATBS2"

    def eng06_redundant(self):
        major_list = ["LMATAB1", "LMATAB2", "LMATBS1", "LMATBS2"]
        if self.student.major in major_list:
            return self.student.has_taken("ECS32A") and self.student.has_taken("MAT22AL")
        if self.student.major == "LMOR":
            return self.student.has_taken("MAT22AL") and self.student.has_taken("ECS32A")
        return False

    def mat128a_redundant(self):
        if self.student.major == "LAMA":
            return self.student.has_taken("MAT128B") and self.student.has_taken("MAT128C")
        if self.student.major == "LMOR" and "Computers" not in self.student.interests:
            return self.student.has_taken("MAT128B") or self.student.has_taken("MAT128C")
        return False

    def mat128b_redundant(self):
        if self.student.major == "LAMA" and "Computers" not in self.student.interests:
            return self.student.has_taken("MAT128A") and self.student.has_taken("MAT128C")
        
        if self.student.major == "LMOR" and "Computers" not in self.student.interests:
            return self.student.has_taken("MAT128A") or self.student.has_taken("MAT128C")
        return False

    def mat128c_redundant(self):
        if self.student.major == "LAMA" and "Computers" not in self.student.interests:
            return self.student.has_taken("MAT128A") and self.student.has_taken("MAT128B")
        
        if self.student.major == "LMOR" and "Computers" not in self.student.interests:
            return self.student.has_taken("MAT128A") or self.student.has_taken("MAT128B")
        return False

    def phy7a_redundant(self):
        for course in self.classes_offered:
            if course.name == "PHY9B" and course.required["LAMA"]:  #checks if student is applied and chose physics as 2quarter sequence
                return True
        return False

    def new_is_success(self):
        for course_name in self.classes_by_name:
            if self.classes_by_name[course_name].required[self.student.major] and course_name not in self.student.classes_taken.keys():
                return False
        num_needed = enrichment_dict[self.student.major]["num_enrichments_needed"]

        if self.student.num_128s < self.student.num128s_needed[self.student.major]:
            return False
        if self.student.major == "LMOR":
            if self.student.num_enrichments_a < enrichment_dict["LMOR"]["num_enrichments_a_needed"] or self.student.num_enrichments_b < enrichment_dict["LMOR"]["num_enrichments_b_needed"]:
                return False
        elif self.student.num_enrichments < num_needed:
            return False
        return True

    def num_math_classes(self, block):
        num_math_classes = 0
        for course in block.courses:
            if course.name[:3] == "MAT":
                num_math_classes += 1
        return num_math_classes