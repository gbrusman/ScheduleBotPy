#!/usr/bin/env python
import psycopg2



if __name__ == "__main__":
    conn = psycopg2.connect(host="rajje.db.elephantsql.com", database="ytmelfsd", user="ytmelfsd",
                            password="PY2TKJsTJD2cOPlRbwQgVJPHgc4vhWvT")
    cur = conn.cursor()

    f = open("database/course_offerings.csv")
    next(f)
    cur.execute("TRUNCATE TABLE course_offerings;")
    cur.copy_from(f, 'course_offerings', sep=",")

    f = open("database/courses.csv")
    next(f)
    cur.execute("TRUNCATE TABLE courses;")
    cur.copy_from(f, 'courses', sep=",")

    f = open("database/interests.csv")
    next(f)
    cur.execute("TRUNCATE TABLE interests;")
    cur.copy_from(f, 'interests', sep=",")

    f = open("database/required.csv")
    next(f)
    cur.execute("TRUNCATE TABLE required;")
    cur.copy_from(f, 'required', sep=",")

    f = open("database/student_vars.csv")
    next(f)
    cur.execute("TRUNCATE TABLE student_vars;")
    cur.copy_from(f, 'student_vars', sep=",")


    conn.commit()



