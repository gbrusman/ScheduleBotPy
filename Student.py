from AcademicTime import AcademicTime
from ScheduleBlock import ScheduleBlock
from Course import Course

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
    def __init__(self, cur_time=AcademicTime(), major="", interests=[], classes_taken={}, num_enrichments=0, num_enrichments_a=0, num_enrichments_b=0, num_128s = 0):
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
        self.num_128s = num_128s

        self.num128s_needed = {"LMATAB1": 0, "LMATAB2": 0, "LMATBS1": 0, "LMATBS2": 0, "LAMA": 2, "LMCOBIO": 3, "LMCOMATH": 3,
                       "LMOR": 1}


    def update_128_count(self, course):
        if course.name == "MAT128A" or course.name == "MAT128B" or course.name == "MAT128C":
            self.num_128s += 1

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
        if course.enrichment_a:
            self.num_enrichments_a += 1
            if self.major == "LMOR":
                self.num_enrichments += 1
        if course.enrichment_b:
            self.num_enrichments_b += 1
            if self.major == "LMOR":
                self.num_enrichments += 1
        if course.enrichment and not course.required[self.major]:
            self.num_enrichments += 1

    def is_taking(self, course_name, block):
        """Function to test whether a student is currently taking a Course (in cur_time). Returns boolean."""
        if block.contains(course_name):
            return True
        return False


    def meets_reccommendations(self, course):
        """Function to test whether a student meets the recommendations to take a course. Returns boolean.

        Extra Info:
            These recommendations are not mandated by course requirements, but are recipes for success from the advising team.
        """
        name = course.name
        # https://jaxenter.com/implement-switch-case-statement-python-138315.html
        switcher = {
            "ECS32A": self.ecs32a_rec,
            "MAT108": self.mat108_rec,
            "MAT22A": self.mat22a_rec,
            "MAT180": self.mat180_rec,
            "MAT150A": self.mat150a_rec,
            "MAT185A": self.mat185a_rec,
            "MAT128B": self.mat128b_rec,
            "MAT128C": self.mat128c_rec
        }
        func = switcher.get(name)
        if func is None:
            return True
        return func()

    def has_taken(self, course_name):
        """Function to test whether a student has already taken a course in a previous quarter. Returns boolean."""
        return course_name in self.classes_taken.keys()

    def has_prereqs(self, course, block):
        """Function to test whether a student has the prereqs necessary to take a course. Returns boolean."""
        switcher = {
            "MAT21A": self.mat21a_prereq,
            "MAT21B": self.mat21b_prereq,
            "MAT21C": self.mat21c_prereq,
            "MAT21D": self.mat21d_prereq,
            "MAT22A": self.mat22a_prereq,
            "MAT22AL": self.mat22al_prereq,
            "MAT22B": self.mat22b_prereq,
            "MAT67": self.mat67_prereq,
            "MAT108": self.mat108_prereq,
            "MAT111": self.mat111_prereq,
            "MAT114": self.mat114_prereq,
            "MAT115A": self.mat115a_prereq,
            "MAT115B": self.mat115b_prereq,
            "MAT116": self.mat116_prereq,
            "MAT118A": self.mat118a_prereq,
            "MAT118B": self.mat118b_prereq,
            "MAT119A": self.mat119a_prereq,
            "MAT119B": self.mat119b_prereq,
            "MAT124": self.mat124_prereq,
            "MAT127A": self.mat127a_prereq,
            "MAT127B": self.mat127b_prereq,
            "MAT127C": self.mat127c_prereq,
            "MAT128A": self.mat128a_prereq,
            "MAT128B": self.mat128b_prereq,
            "MAT128C": self.mat128c_prereq,
            "MAT129": self.mat129_prereq,
            "MAT133": self.mat133_prereq,
            "MAT135A": self.mat135a_prereq,
            "MAT135B": self.mat135b_prereq,
            "MAT141": self.mat141_prereq,
            "MAT145": self.mat145_prereq,
            "MAT146": self.mat146_prereq,
            "MAT147": self.mat147_prereq,
            "MAT148": self.mat148_prereq,
            "MAT150A": self.mat150a_prereq,
            "MAT150B": self.mat150b_prereq,
            "MAT150C": self.mat150c_prereq,
            "MAT160": self.mat160_prereq,
            "MAT165": self.mat165_prereq,
            "MAT167": self.mat167_prereq,
            "MAT168": self.mat168_prereq,
            "MAT180": self.mat180_prereq,
            "MAT185A": self.mat185a_prereq,
            "MAT185B": self.mat185b_prereq,
            "MAT189": self.mat189_prereq,
            "ECS32A": self.ecs32a_prereq,
            "ENG06": self.eng06_prereq,
            "PHY7A": self.phy7a_prereq,
            "PHY9A": self.phy9a_prereq,
            "PHY9B": self.phy9b_prereq,
            "ECN1A": self.ecn1a_prereq,
            "ECN1B": self.ecn1b_prereq,
            "ECN100A": self.ecn100a_prereq,
            "ECN100B": self.ecn100b_prereq,
            "ECN121A": self.ecn121a_prereq,
            "ECN121B": self.ecn121b_prereq,
            "ECN122": self.ecn122_prereq,
            "ECN134": self.ecn134_prereq,
            "ARE100A": self.are100a_prereq,
            "ARE100B": self.are100b_prereq,
            "ARE155": self.are155_prereq,
            "ARE156": self.are156_prereq,
            "ARE157": self.are157_prereq,
            "STA32": self.sta32_prereq,
            "STA100": self.sta100_prereq,
            "STA131A": self.sta131a_prereq,
            "STA131B": self.sta131b_prereq,
            "STA131C": self.sta131c_prereq,
            "STA137": self.sta137_prereq,
            "STA141A": self.sta141a_prereq,
            "STA141B": self.sta141b_prereq,
            "STA141C": self.sta141c_prereq,
            "BIS2A": self.bis2a_prereq,
            "BIS2B": self.bis2b_prereq,
            "CHE2A": self.che2a_prereq,
            "CHE2B": self.che2b_prereq,
            "ECS124": self.ecs124_prereq,
            "ECS129": self.ecs129_prereq,
            "ECS170": self.ecs170_prereq,
            "Approved Upper Division Non-Math": self.APPROVED_UD_NONMATH_prereq,
            "Biology Requirement": self.BIOLOGY_REQUIREMENT_prereq,
            "Computation Requirement": self.COMPUTATION_REQUIREMENT_prereq,
        }
        func = switcher.get(course.name)
        if func is None:
            return False
        if course.name == "ENG06" or course.name == "PHY9B":
            return func(block)  # ENG06/PHY9B special case b/c concurrency, needs block parameter
        return func()

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
        return self.num_enrichments >= 1 # will help push it back to senior year

    def mat180_rec(self):
        #return self.cur_time.year == self.grad_time.year  # and self.cur_time.quarter == self.grad_time.quarter
        #return self.can_graduate("MAT180")
        return self.num_enrichments >= 2

    def mat21a_prereq(self):
        return True

    def mat21b_prereq(self):
        return self.has_taken("MAT21A") or self.has_taken("MAT17A")

    def mat21c_prereq(self):
        return self.has_taken("MAT21B") or self.has_taken("MAT16C") or self.has_taken("MAT17C") or self.has_taken("MAT17B")

    def mat21d_prereq(self):
        return self.has_taken("MAT21C") or self.has_taken("MAT17C")

    def mat22a_prereq(self):
        return (self.has_taken("MAT21C") or self.has_taken("MAT16C") or self.has_taken("MAT17C")) and (self.has_taken("ENG06") or self.has_taken("MAT22AL"))

    def mat22al_prereq(self):
        return self.has_taken("MAT21C") or self.has_taken("MAT17C")

    def mat67_prereq(self):
        return self.has_taken("MAT21C")

    def mat22b_prereq(self):
        return self.has_taken("MAT22A") or self.has_taken("MAT67")

    def mat108_prereq(self):
        return self.has_taken("MAT21B")

    def mat111_prereq(self):
        return self.has_taken("MAT67") or self.has_taken("MAT67") or self.has_taken("MAT108") or self.has_taken("MAT114") or self.has_taken("MAT115A") or self.has_taken("MAT141") or self.has_taken("MAT145")

    def mat114_prereq(self):
        return self.has_taken("MAT21C") and (self.has_taken("MAT22A") or self.has_taken("MAT67"))

    def mat115a_prereq(self):
        return self.has_taken("MAT21B")

    def mat115b_prereq(self):
        return self.has_taken("MAT115A") and (self.has_taken("MAT22A") or self.has_taken("MAT67"))

    def mat116_prereq(self):
        return self.has_taken("MAT21D") and self.has_taken("MAT22B") and (self.has_taken("MAT22A") or self.has_taken("MAT67"))

    def mat118a_prereq(self):
        return self.has_taken("MAT21D") and self.has_taken("MAT22B") and (self.has_taken("MAT22A") or self.has_taken("MAT67"))

    def mat118b_prereq(self):
        return self.has_taken("MAT118A")

    def mat119a_prereq(self):
        return self.has_taken("MAT21D") and self.has_taken("MAT22B") and (self.has_taken("MAT22A") or self.has_taken("MAT67"))

    def mat119b_prereq(self):
        return self.has_taken("MAT119A")

    def mat124_prereq(self):
        return self.has_taken("MAT22B") and (self.has_taken("MAT22A") or self.has_taken("MAT67"))

    def mat127a_prereq(self):
        return self.has_taken("MAT21C") and (self.has_taken("MAT67") or (self.has_taken("MAT22A") and self.has_taken("MAT108")))

    def mat127b_prereq(self):
        return self.has_taken("MAT127A")

    def mat127c_prereq(self):
        return self.has_taken("MAT127B")

    def mat128a_prereq(self):
        return self.has_taken("MAT21C") and (self.has_taken("ECS32A") or self.has_taken("ENG06") or self.has_taken("EME05") or self.has_taken("ECS30"))

    def mat128b_prereq(self):
        return (self.has_taken("MAT22A") or self.has_taken("MAT67")) and (self.has_taken("ECS32A") or self.has_taken("ENG06") or self.has_taken("EME005") or self.has_taken("ECS30"))

    def mat128c_prereq(self):
        return (self.has_taken("MAT22A") or self.has_taken("MAT67")) and self.has_taken("MAT22B") and (self.has_taken("ECS32A") or self.has_taken("ENG06") or self.has_taken("EME05") or self.has_taken("ECS30"))

    def mat129_prereq(self):
        return self.has_taken("MAT21D") and self.has_taken("MAT22B") and (self.has_taken("MAT22A") or self.has_taken("MAT67")) and self.has_taken("MAT127A")

    def mat133_prereq(self):
        return (self.has_taken("MAT67") or (self.has_taken("MAT22A") and self.has_taken("MAT108"))) and self.has_taken("MAT135A")

    def mat135a_prereq(self):
        return self.has_taken("MAT21C") and (self.has_taken("MAT108") or self.has_taken("MAT127A"))

    def mat135b_prereq(self):
        return self.has_taken("MAT135A") and (self.has_taken("MAT22A") or self.has_taken("MAT67"))

    def mat141_prereq(self):
        return self.has_taken("MAT21B") and (self.has_taken("MAT22A") or self.has_taken("MAT67"))

    def mat145_prereq(self):
        return self.has_taken("MAT21C")

    def mat146_prereq(self):
        return self.has_taken("MAT145") and self.has_taken("MAT127A") and (self.has_taken("MAT22A") or self.has_taken("MAT67"))

    def mat147_prereq(self):
        return self.has_taken("MAT127A")

    def mat148_prereq(self):
        return self.has_taken("MAT67") or (self.has_taken("MAT22A") and self.has_taken("MAT108"))

    def mat150a_prereq(self):
        return self.has_taken("MAT67") or (self.has_taken("MAT22A") and self.has_taken("MAT108"))

    def mat150b_prereq(self):
        return self.has_taken("MAT150A")

    def mat150c_prereq(self):
        return self.has_taken("MAT150B")

    def mat160_prereq(self):
        return self.has_taken("MAT167")

    def mat165_prereq(self):
        return self.has_taken("MAT22A") or self.has_taken("MAT67") and (self.has_taken("MAT127A") or self.has_taken("MAT108") or self.has_taken("MAT114") or self.has_taken("MAT115A") or self.has_taken("MAT145"))

    def mat167_prereq(self):
        return self.has_taken("MAT22A") or self.has_taken("MAT67")

    def mat168_prereq(self):
        return self.has_taken("MAT21C") and ((self.has_taken("MAT22A") and self.has_taken("MAT108")) or self.has_taken("MAT67"))

    def mat180_prereq(self):
        return self.has_taken("MAT127A") and (self.has_taken("MAT67") or (self.has_taken("MAT22A") and self.has_taken("MAT108")))

    def mat185a_prereq(self):
        return (self.has_taken("MAT67") or (self.has_taken("MAT22A") and self.has_taken("MAT108"))) and self.has_taken("MAT127B")

    def mat185b_prereq(self):
        return self.has_taken("MAT185A")

    def mat189_prereq(self):
        return self.has_taken("MAT127A") and ((self.has_taken("MAT22A") and self.has_taken("MAT108")) or self.has_taken("MAT67"))

    def ecs32a_prereq(self):
        return True

    def eng06_prereq(self, block):
        return (self.has_taken("MAT16A") or self.has_taken("MAT17A") or self.has_taken("MAT21A")) and (self.has_taken("MAT16B") or self.has_taken("MAT17B") or (self.has_taken("MAT21B") or self.is_taking("MAT21B", block)))

    def phy7a_prereq(self):
        return True

    def phy9a_prereq(self):
        return self.has_taken("MAT21B")

    def phy9b_prereq(self, block):
        return self.has_taken("PHY9A") and self.has_taken("MAT21C") and (self.has_taken("MAT21D") or self.is_taking("MAT21D", block))

    def bis2a_prereq(self):
        return True

    def bis2b_prereq(self):
        return True

    def che2a_prereq(self):
        return True

    def che2b_prereq(self):
        return self.has_taken("CHE2A")

    def ecn1a_prereq(self):
        return True

    def ecn1b_prereq(self):
        return True

    def sta32_prereq(self):
        return self.has_taken("MAT16B") or self.has_taken("MAT21B") or self.has_taken("MAT17B")

    def sta100_prereq(self):
        return self.has_taken("MAT16B") or self.has_taken("MAT21B") or self.has_taken("MAT17B")

    def sta131a_prereq(self):
        return self.has_taken("MAT21D") and (self.has_taken("MAT22A") or self.has_taken("MAT67"))

    def sta131b_prereq(self):
        return self.has_taken("STA131A") or self.has_taken("MAT135A")

    def sta131c_prereq(self):
        return self.has_taken("STA131B")

    def sta137_prereq(self):
        return self.has_taken("STA108")

    def sta141a_prereq(self):
        return self.has_taken("STA108") or self.has_taken("STA106")

    def sta141b_prereq(self):
        return self.has_taken("STA141A")

    def sta141c_prereq(self):
        return self.has_taken("STA141B")

    def ecn100a_prereq(self):
        return self.has_taken("ECN1A") and self.has_taken("ECN1B") and self.has_taken("MAT21B")

    def ecn100b_prereq(self):
        return self.has_taken("ECN100A")

    def ecn121a_prereq(self):
        return (self.has_taken("ECN100A") or self.has_taken("ARE100A")) and (self.has_taken("ECN100B") or self.has_taken("ARE100B"))

    def ecn121b_prereq(self):
        return (self.has_taken("ECN100A") or self.has_taken("ARE100A")) and (self.has_taken("ECN100B") or self.has_taken("ARE100B"))

    def ecn122_prereq(self):
        return self.has_taken("MAT21A") and self.has_taken("MAT21B")

    def ecn134_prereq(self):
        return (self.has_taken("ECN100A") or self.has_taken("ARE100A")) and self.has_taken("ECN100B") and \
        (self.has_taken("ECN102") or self.has_taken("ECN140") or self.has_taken("STA108") or self.has_taken("ARE106"))

    def are100a_prereq(self):
        return self.has_taken("ECN1A") and self.has_taken("ECN1B") and self.has_taken("MAT21A") and self.has_taken("MAT21B")

    def are100b_prereq(self):
        return self.has_taken("ARE100A")

    def are155_prereq(self):
        return self.has_taken("ARE100A") and self.has_taken("STA103") and self.has_taken("STA13")

    def are156_prereq(self):
        return self.has_taken("ARE100B") and self.has_taken("ARE100A") and self.has_taken("ARE155")

    def are157_prereq(self):
        return self.has_taken("ARE155") and self.has_taken("ARE100A")

    def ecs124_prereq(self):
        return (self.has_taken("ECS32A") or self.has_taken("ECS36A") or self.has_taken("ENG06")) and \
               (self.has_taken("STA13") or self.has_taken("STA32") or self.has_taken("STA100") or self.has_taken("MAT135A") or self.has_taken("STA131A")) and \
               (self.has_taken("BIS2A") or self.has_taken("MCB10"))

    def ecs129_prereq(self):
        return (self.has_taken("BIS2A") or self.has_taken("MCB10")) and (self.has_taken("ECS32A") or self.has_taken("ECS36A"))

    def ecs170_prereq(self):
        return self.has_taken("ECS60") or self.has_taken("ECS32B") or self.has_taken("ECS36C")

    def APPROVED_UD_NONMATH_prereq(self):
        return self.has_taken("MAT108") and self.has_taken("MAT128A") #randomly came up with these prereqs. Wanted this class to be hopefully junior year-ish?

    def BIOLOGY_REQUIREMENT_prereq(self):
        return self.has_taken("MAT124") and self.has_taken("MAT128A") #randomly came up with these as above

    def COMPUTATION_REQUIREMENT_prereq(self):
        return self.has_taken("MAT128A") #randomly came up with this as above



























