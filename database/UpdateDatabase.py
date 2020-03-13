#!/usr/bin/env python
import psycopg2



if __name__ == "__main__":
    conn = psycopg2.connect(host="rajje.db.elephantsql.com", database="ytmelfsd", user="ytmelfsd",
                            password="PY2TKJsTJD2cOPlRbwQgVJPHgc4vhWvT")
    cur = conn.cursor()

    try:
        f = open("course_offerings.csv")
        next(f)
        cur.execute("TRUNCATE TABLE course_offerings;")
        cur.copy_from(f, 'course_offerings', sep=",")
        print("Updated 'course_offerings' successfully!")
    except Exception as e:
        print("Failed to update from course_offerings.csv:")
        print(e)

    try:
        f = open("courses.csv")
        next(f)
        cur.execute("TRUNCATE TABLE courses;")
        cur.copy_from(f, 'courses', sep=",")
        print("Updated 'courses' successfully!")
    except Exception as e:
        print("Failed to update from courses.csv:")
        print(e)

    try:
        f = open("interests.csv")
        next(f)
        cur.execute("TRUNCATE TABLE interests;")
        cur.copy_from(f, 'interests', sep=",")
        print("Updated 'interests' successfully!")
    except Exception as e:
        print("Failed to update from interests.csv:")
        print(e)

    try:
        f = open("required.csv")
        next(f)
        cur.execute("TRUNCATE TABLE required;")
        cur.copy_from(f, 'required', sep=",")
        print("Updated 'required' successfully!")
    except Exception as e:
        print("Failed to update from required.csv:")
        print(e)

    try:
        f = open("student_vars.csv")
        next(f)
        cur.execute("TRUNCATE TABLE student_vars;")
        cur.copy_from(f, 'student_vars', sep=",")
        print("Updated 'student_vars' successfully!")
    except Exception as e:
        print("Failed to update from student_vars.csv:")
        print(e)



    conn.commit()


