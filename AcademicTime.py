class AcademicTime:

    def __init__(self, year=0, quarter=""):
        self.quarter = quarter
        self.year = year

    def progress_time(self, summer_quarters=[]):
        newtime = AcademicTime(self.year, self.quarter)

        if self.quarter == "Fall":
            newtime.quarter = "Winter"
            newtime.year += 1
        elif self.quarter == "Winter":
            newtime.quarter = "Spring"
        elif self.quarter == "Spring" and AcademicTime(self.year, "Summer1") not in summer_quarters and AcademicTime(self.year, "Summer2") not in summer_quarters:
            newtime.quarter = "Fall"
        elif self.quarter == "Spring" and AcademicTime(self.year, "Summer1") in summer_quarters:
            newtime.quarter = "Summer1"
        elif self.quarter == "Summer1" and AcademicTime(self.year, "Summer2") in summer_quarters:
            newtime.quarter = "Summer2"
        elif self.quarter == "Summer1" and AcademicTime(self.year, "Summer2") not in summer_quarters:
            newtime.quarter = "Fall"
        elif self.quarter == "Summer2":
            newtime.quarter = "Fall"


        return newtime

    def reverse_time(self, summer_quarters=[]):
        newtime = AcademicTime(self.year, self.quarter)

        if self.quarter == "Fall" and AcademicTime(self.year, "Summer2") not in summer_quarters:
            newtime.quarter = "Spring"
        elif self.quarter == "Fall" and AcademicTime(self.year, "Summer2") in summer_quarters:
            newtime.quarter = "Summer2"
        elif self.quarter == "Fall" and AcademicTime(self.year, "Summer2") not in summer_quarters and AcademicTime(self.year, "Summer1") in summer_quarters:
            newtime.quarter = "Summer1"
        elif self.quarter == "Summer2" and AcademicTime(self.year, "Summer1") in summer_quarters:
            newtime.quarter = "Summer1"
        elif self.quarter == "Summer2" and AcademicTime(self.year, "Summer1") not in summer_quarters:
            newtime.quarter = "Fall"
        elif self.quarter == "Summer1":
            newtime.quarter = "Fall"
        elif self.quarter == "Winter":
            newtime.quarter = "Fall"
            newtime.year -= 1
        elif self.quarter == "Spring":
            newtime.quarter = "Winter"

        return newtime

    def __eq__(self, o: object) -> bool:
        return self.quarter == o.quarter and self.year == o.year

    def __ne__(self, o: object) -> bool:
        return self.quarter != o.quarter or self.year != o.year

    def __key(self):
        return (self.quarter, self.year)

    def __hash__(self) -> int:
        return hash(self.__key())







