import psycopg2
from Student import Student
from Course import Course



# FIXME: Goal:     def mat22a_prereq(self): return self.has_taken("MAT21C")  and (self.has_taken("ENG06") or self.has_taken("MAT22AL"))

def find_prereq_string(query_course):
    solution = ""
    conn = psycopg2.connect(host="localhost", database="Math Prerequisite Testing", user="postgres",
                            password="MN~D=bp~+WR2/ppy")
    cur = conn.cursor()

    query_course = "\'MAT22A\'"
    cur.execute("SELECT prerequisite_combination_id FROM courses WHERE name = " + query_course + ";")

    combination_id = cur.fetchone()[0]

    cur.execute("SELECT * FROM combination_courses WHERE combination_id = " + str(combination_id) + ";")

    combination_tuple = cur.fetchone()
    done = False
    while not done:

        course_id = combination_tuple[1]
        sub_combination_id = combination_tuple[2]

        cur.execute("SELECT name FROM courses WHERE display_index = " + str(course_id) + ";")
        solution += "test_student.has_taken(\"" + cur.fetchone()[0] + "\")" + " "

        if combination_id != None:
            cur.execute("SELECT logical_operator FROM prerequisite_logical_operators WHERE combination_id = " + str(combination_id) + ";")
            logical_operator = cur.fetchone()[0]
            solution += logical_operator.lower() + " "

            cur.execute("SELECT * FROM combination_courses WHERE combination_id = " + str(sub_combination_id) + ";")
            combination_tuple = cur.fetchone()
            combination_id = combination_tuple[2]
        else:
            done = True

    print(solution)
    return solution

def convert_interest_format(interest):
        interest = interest.replace("_", " ").title()
        return interest

def get_info_from_database(classes_offered, classes_by_name):
        conn = psycopg2.connect(host="localhost", database="Math Courses", user="postgres", password="MN~D=bp~+WR2/ppy")
        cur = conn.cursor()
        # Fill in data from 'courses' table and put it in the dict.
        cur.execute("SELECT * FROM courses ORDER BY display_index ASC;")
        for record in cur:
            new_course = Course(name=record[0], after=record[1], enrichment_a=record[2], enrichment_b=record[3],
                                enrichment=record[4], approved_ud_nonmath=record[5], biology_requirement=record[6],
                                computation_requirement=record[7])
            classes_by_name[record[0]] = new_course

        # Get names of all of the majors currently offered
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'required' AND column_name != 'name';")
        majors = []
        for record in cur:
            majors.append(record[0])

        # Fill in data about major requirements from 'required' table.
        cur.execute("SELECT * FROM required;")
        for record in cur:
            required_dict = {}
            for i in range(1, 9):
                required_dict[majors[i - 1]] = record[i]
            classes_by_name[record[0]].required = required_dict

        # Get names of all of the majors currently offered
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'course_offerings' AND column_name != 'name';")
        quarters = []
        for record in cur:
            quarters.append(record[0])

        # Fill in data about course offerings from 'course_offerings' table.
        cur.execute("SELECT * FROM course_offerings;")
        for record in cur:
            quarters_offered = []
            for i in range(1, 6):
                if (record[i]):
                    quarters_offered.append(quarters[i - 1])
            classes_by_name[record[0]].quarters_offered = quarters_offered
            classes_by_name[record[0]].offered_pattern = record[6]

        # Get names of all of the interests currently supported
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'interests' AND column_name != 'name';")
        interests = []
        num_interests = 0
        for record in cur:
            interests.append(convert_interest_format(record[0]))
            num_interests += 1


        # Fill in data about interests from 'interests' table.
        cur.execute("SELECT * FROM interests;")
        for record in cur:
            course_interests = []
            for i in range(1, num_interests + 1):
                if record[i]:
                    course_interests.append(interests[i - 1])
            classes_by_name[record[0]].interests = course_interests

        for course in classes_by_name:
            classes_offered.append(classes_by_name[course])

if __name__ == "__main__":
    #def __init__(self, cur_time=AcademicTime(), major="", interests=[], classes_taken={}, num_enrichments=0, num_enrichments_a=0, num_enrichments_b=0, summer_quarters=[]):
    classes_offered = []
    classes_by_name = {}
    get_info_from_database(classes_offered, classes_by_name)

    test_classes_taken = {"MAT21C": classes_by_name["MAT21C"], "MAT22AL": classes_by_name["MAT22AL"]}
    test_student = Student(major="LMOR", classes_taken=test_classes_taken)


    query_course = "\'MAT22A\'"
    prereqs = find_prereq_string(query_course)
    print(eval(prereqs))




