#!/usr/bin/env bash

commits=`git log --pretty="%s" | grep Deploy`
echo "$commits"
number=`expr match "$commits" 'Deploy #\([0-9]*\)'`
number=`expr $number + 1`
echo "$number"

git add .
git commit -m "Deploy #$number"
git push origin master