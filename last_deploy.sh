#!/usr/bin/env bash

commits=`git log --pretty="%s" | grep Deploy`
number=`expr match "$commits" 'Deploy #\([0-9]*\)'`
echo "Номер последнего деплоя $number"