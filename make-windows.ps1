 param (
    [switch]$f = $false
 )


$scripts = "AcademicTime.py", "AppliedSeriesChoicePage.py", "Course.py", "CourseSelectPage.py", "InterestSelectPage.py", "MajorSelectPage.py", "MultiPageApp.py", "ScheduleBlock.py", "ScheduleDisplayPage.py", "Schedule.py", "Student.py"

$options = "-p", "C:\Users\gabri\PycharmProjects\ScheduleBotPy\venv\Lib\site-packages", "-n", "ScheduleBotWINDOWS", "--debug", "all"

$spec = "ScheduleBotWINDOWS.spec"

if($f) {
    $options += "--onefile", "--windowed"
}

pyinstaller $options $spec