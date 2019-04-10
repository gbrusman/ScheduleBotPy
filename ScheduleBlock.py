from AcademicTime import AcademicTime


class ScheduleBlock:
    def __init__(self, time=AcademicTime(), courses=[]):
        self.time = time
        self.courses = courses
        
