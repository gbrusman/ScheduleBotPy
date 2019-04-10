from AcademicTime import AcademicTime
from ScheduleBlock import ScheduleBlock
from Course import Course

import copy

class Student:
    def __init__(self, cur_time=AcademicTime(), grad_time=AcademicTime(), major="", interests=[], classes_taken={}):
        self.cur_time = cur_time
        self.grad_time = grad_time
        self.major = major
        self.interests = interests
        self.classes_taken = classes_taken
        self.start_time = copy.deepcopy(cur_time)

    def is_taking(self, course_name, block):
        if block.contains(course_name):
            return True
        return False


    def meets_reccommendations(self, course):
        name = course.name
        # https://jaxenter.com/implement-switch-case-statement-python-138315.html
        switcher = {
            "ECS32A": self.ecs32a_rec,
            "MAT108": self.mat108_rec,
            "MAT22A": self.mat22a_rec,
            "MAT180": self.mat180_rec
        }
        func = switcher.get(name)
        if func is None:
            return True
        return func()

    def has_taken(self, course_name):
        return course_name in self.classes_taken.keys()

    def has_prereqs(self, course, block):
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
            "ECN1A": self.ecn1a_prereq,
            "ECN1B": self.ecn1b_prereq,
            "STA32": self.sta32_prereq,
            "STA100": self.sta100_prereq,
        }
        func = switcher.get(course.name)
        if func is None:
            return False
        if course.name == "ENG06":
            return func(block)  # ENG06 special case, needs block parameter
        return func()

    def ecs32a_rec(self):
        return self.start_time != self.cur_time

    def mat108_rec(self):
        return self.has_taken("MAT21C")

    def mat22a_rec(self):
        return self.has_taken("MAT21C")

    def mat180_rec(self):
        return self.cur_time.year != self.grad_time.year

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

    def ecn1a_prereq(self):
        return True

    def ecn1b_prereq(self):
        return True

    def sta32a_prereq(self):
        return self.has_taken("MAT16B") or self.has_taken("MAT21B") or self.has_taken("MAT17B")

    def sta100_prereq(self):
        return self.has_taken("MAT16B") or self.has_taken("MAT21B") or self.has_taken("MAT17B")






















