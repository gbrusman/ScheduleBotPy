class AcademicTime:

    def __init__(self, year=0, quarter=""):
        self.quarter = quarter
        self.year = year

    def progress_time(self):
        newtime = AcademicTime(self.year, self.quarter)

        if self.quarter == "Fall":
            newtime.quarter = "Winter";
            newtime.year += 1;
        elif self.quarter == "Winter":
            newtime.quarter = "Spring"
        elif self.quarter == "Spring":
            newtime.quarter = "Fall"

        return newtime

    def reverse_time(self):
        newtime = AcademicTime(self.year, self.quarter)

        if self.quarter == "Fall":
            newtime.quarter = "Spring"
        elif self.quarter == "Winter":
            newtime.quarter = "Fall"
            newtime.year -= 1
        elif self.quarter == "Spring":
            newtime.quarter = "Winter"

        return newtime

    def __eq__(self, o: object) -> bool:
        return super().__eq__(o)

    def __ne__(self, o: object) -> bool:
        return super().__ne__(o)



