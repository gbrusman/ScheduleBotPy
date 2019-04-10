from AcademicTime import AcademicTime

if __name__ == "__main__":
    time = AcademicTime(2020, "Fall")
    print(time.quarter)
    print(time.year)

    progress = time.progress_time()
    reverse = time.reverse_time()

    print(progress.quarter, progress.year)
    print(reverse.quarter, reverse.year)