# ScheduleBotPy
Goal of this program is to be used to help undergraduate math students with basic scheduling, thus avoiding trivial advising appointments.


## How to Run:
There are separate executables for Windows, Mac, and Linux. Double click on the correct executable for your operating system (and agree to whatever warnings pop up) and the program should run after a few seconds.

## Database:
The database is a PostgreSQL database that is hosted on a free ElephantSQL server. The free version allows up to 20MB of storage (we are way under that), and up to 5 simultaneous connections. The program only accesses the database right at the beginning of execution, and should only be connected to the database for <1sec, so statistically, only being able to have 5 simultaneous connections should be fine.

### Structure of Database:
There are 5 tables in the database.
#### courses:
The courses table contains the names of the courses that are offered, what course a student should take directly after taking a specific course, whether a course counts as an enrichment A or an enrichment B (for the LMOR major), whether a course counts as an enrichment course at all (for every major), whether a course counts for the computation requirement or the biology requirement (for the LMCO majors), a display index to make the order of the courses more natural when displaying them in the program, and the prerequisites for the course **which may not match exactly with the general catalog** for reasons explained later.

##### Updating the Prerequisites:
If you would like to update a classes prerequisites, you must ensure that the proper format is maintained so that the program can parse the data correctly.
- Course names must match the names given under the "name" column **exactly**. 
- To specify course A and course B, you simply write **A and B**.
- To specify course C or D, you simply write **A or B**.
- You can use parentheses "()", but they must match up. 
    - For example, **(A and B) or (C and D)** is acceptable. 
    - **(A and B) or (C and D** will cause an error, since there needs to be another ")" after "D".

##### More about the Prerequisites:
Some of the prerequisites in the database are not exactly what the prerequisites are officially. There are instances where I added artificial prerequisites to a class in order to push it further back in the schedule. This is because there are some classes that can be taken relatively early on, but it is recommended to take them closer to graduation.

### Updating the Database:
I made scripts to update the database. The steps for updating the database are as follows:
1. Go to the copy of the database directory that you have locally on your computer.
2. Make the changes you want in the CSV files located in the database directory.
3. Open a terminal in this directory. On Windows, you can use a cmd prompt. Run the python script titled "UpdateDatabase.py", which runs on Python3, or "UpdateDatabasePython2.py", which runs on Python2. 

The command to type into the terminal prompt is: 
  <pre><code>python UpdateDatabase.py </code></pre>
  or 
  <pre><code>python UpdateDatabasePython2.py </code></pre>
 
 The scripts will replace the data in the database with the data in the CSV files.
 It is highly recommended to keep a master copy of the most up to date versions of all of the CSV's somewhere for staff, since the scripts will update from **all** of the CSV's in the directory, not just some of them.
  

