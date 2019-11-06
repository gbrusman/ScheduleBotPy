 param (
    [switch]$f = $false
 )


$scripts = "AcademicTime.py", "AppliedSeriesChoicePage.py", "Course.py", "CourseSelectPage.py", "InterestSelectPage.py", "MajorSelectPage.py", "MultiPageApp.py", "ScheduleBlock.py", "ScheduleDisplayPage.py", "Schedule.py", "Student.py"

$options = "-n", "ScheduleBotWINDOWS"

if($f) {
    $options += "--onefile", "--windowed"
}

pyinstaller $options $scripts