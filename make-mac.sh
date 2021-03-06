#!/bin/bash

scripts="AcademicTime.py AppliedSeriesChoicePage.py Course.py CourseSelectPage.py InterestSelectPage.py MajorSelectPage.py MultiPageApp.py ScheduleBlock.py ScheduleDisplayPage.py Schedule.py Student.py"

spec="ScheduleBotMAC.spec"

name="ScheduleBotMAC"

options="-n ${name} " 

O=${1:-0}

if [ -f dist/$name ] 
then
echo "Removing file {$name}"
rm dist/$name
fi

if [ -d dist/$name ] 
then
echo "Removing directory {$name}"
rm -r dist/$name
fi


if [ $O -eq 1 ]
then
echo "Making as one file."
options+="--onefile --windowed"
fi

echo "$options"

pyinstaller $options $spec

