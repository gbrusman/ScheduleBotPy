from AcademicTime import AcademicTime


class ScheduleBlock:
    def __init__(self, time=AcademicTime(), courses=[]):
        self.time = time
        self.courses = courses

    def contains(self, item):
        if item in self.courses:
            return True
        return False

