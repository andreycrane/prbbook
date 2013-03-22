#!/usr/bin/env bash
if [[ -e "./celery.pid" ]]
then
    pid=`cat ./celery.pid`
    if [[ `ps -A | grep $pid` ]]
    then
        echo "Процесс указанный в файле ./celery.pid существует"
        echo "Выполняю \"kill -s QUIT $pid\""
        kill -s QUIT $pid
    else
        echo "Процесс указанный в файле ./celery.pid не существует"
        echo "Выполняю \"rm ./celery.pid\""
        rm ./celery.pid
    fi
else
    echo "Файл ./celery.pid не существует."
fi
