class Course:

    def __init__(self, name="", interests=[], after="", required={}, quarters_offered=[], years_offered="", enrichment_a=False, enrichment_b=False):
        self.name = name
        self.interests = interests
        self.after = after
        self.required = required
        self.quarters_offered = quarters_offered
        self.years_offered = years_offered
        self.enrichment_a = enrichment_a
        self.enrichment_b = enrichment_b

    def is_offered(self, time):
        offered_in_quarter = False
        offered_in_year = False

        if self.years_offered == "ALWAYS":
            offered_in_year = True
        elif self.years_offered == "EVENALTERNATE":
            if time.quarter == "Fall":  # if it's fall and year is even
                if time.year % 2 == 0:
                    offered_in_year = True
            else:  # else if it's not fall and year is odd
                if time.year % 2 == 1:
                    offered_in_year = True

        else:  # ODDALTERNATE
            if time.quarter == "Fall":  # if it's fall and year is even
                if time.year % 2 == 1:
                    offered_in_year = True
            else:  # else if it's not fall and year is odd
                if time.year % 2 == 0:
                    offered_in_year = True

        # now we have to figure out if it's offered in the quarter
        if time.quarter in self.quarters_offered:
            offered_in_quarter = True

        return offered_in_year and offered_in_quarter





