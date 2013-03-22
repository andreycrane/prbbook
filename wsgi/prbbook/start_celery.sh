#!/usr/bin/env bash

function start {
    echo "Выполняю \"nohup ./manage.py celery worker --loglevel=INFO --logfile=./celery.log --pidfile=./celery.pid --quiet >> /dev/null & > /dev/null\""
    nohup ./manage.py celery worker --loglevel=INFO --logfile=./celery.log --pidfile=./celery.pid --quiet >> /dev/null & > /dev/null
} 

if [[ -e "./celery.pid" ]] 
then
    echo "Файл ./celery.pid присутствует"
    pid=`cat ./celery.pid`
    if [[ `ps -A | grep $pid` ]]
    then
       echo "Процесс указанный в файле ./celery.pid существует"
       echo "Выполняю \"kill -s HUP $pid\""
       kill -s HUP $pid
    else
       echo "Процесс указанный в файле ./celery.pid не существует"
       echo "Выполняю \"rm ./celery.pid\""
       rm ./celery.pid
       echo "Проверяю не запущены ли в системе веркеры celery"
       if [[ `ps -Af | grep "celery worker"` ]]
       then
          echo "В системе запущены процессы веркеров"
       else
          echo "В системе не запущены процессы веркеров"
          start
       fi
    fi
else
    echo "Файл ./celery.pid отсутствует"
    start
fi
