import psycopg2
from Student import Student
from Course import Course

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



def find_prereq_string(query_course):
    solution = ""
    conn = psycopg2.connect(host="localhost", database="Math Prerequisite Testing String", user="postgres",
                            password="MN~D=bp~+WR2/ppy")
    cur = conn.cursor()

    cur.execute("SELECT prerequisites FROM courses WHERE name = " + query_course + ";")

    unformatted_prereqs = cur.fetchone()[0]
    if unformatted_prereqs == None:
        return "True"

    split_prereqs = unformatted_prereqs.split()
    #print(split_prereqs)

    for word in split_prereqs:
        if word not in ['or', 'and']: # If word is a classname and not a logical operator
            if word[0] == '(':
                num_left_parens = 1
                while word[num_left_parens] == '(':
                    num_left_parens += 1
                new_word = ("(" * num_left_parens) + "test_student.has_taken" + "(\'" + word[num_left_parens:] + "\')"
            else:
                new_word = "test_student.has_taken(\'" + word + "\')"
            # Properly place end quote before right paren on words with right paren.
            if word[len(word) - 1] == ')':
                num_right_parens = 1
                while word[len(word) - num_right_parens] == ')':
                    num_right_parens += 1
                new_word = new_word[0:len(new_word) - (1 + num_right_parens)] + "\'" + (")" * num_right_parens)
            solution += new_word + " "

        else:
            solution += word + " "
    print(solution)
    return solution

if __name__ == "__main__":
    classes_offered = []
    classes_by_name = {}
    get_info_from_database(classes_offered, classes_by_name)

    test_classes_taken = {"MAT21C": classes_by_name["MAT21C"], "MAT108": classes_by_name["MAT108"]}
    test_student = Student(major="LMOR", classes_taken=test_classes_taken)


    # for key in classes_by_name:
    #     try:
    #         query_course = "\'" + key + "\'"
    #         prereqs = find_prereq_string(query_course)
    #         eval(prereqs)
    #     except:
    #         print("Issue with course: " + key)

    query_course = "\'MAT168\'"
    prereqs = find_prereq_string(query_course)
    print(eval(prereqs))