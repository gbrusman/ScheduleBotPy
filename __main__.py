from AcademicTime import AcademicTime
from Student import Student
from Course import Course

if __name__ == "__main__":
    time = AcademicTime(2020, "Fall")
    grad_time = AcademicTime(2024, "Spring")
    student = Student(time, grad_time, "LAMA")
    ECS32A = Course("ECS32A", ["Fall", "Winter", "Spring"], "ALWAYS")
    student.meets_reccommendations(ECS32A)