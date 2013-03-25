# -*- coding: utf-8 -*-

from celery import task
from prbbook import settings
from models import Problem
from itertools import cycle, islice, imap

@task(ignore_result = False, track_started = True)
def create_problems(problem_group, engines, groups):
    # создаем ссылки на объекты логера и запроса
    request = create_problems.request
    log = create_problems.get_logger()
    # присваием группе id задания выполняеющего работу
    problem_group.task_id = request.id
    problem_group.save()
    # формируем список студентов по указанным в форме группам
    users = [profile.user for group in groups for profile in group.userprofile_set.all()]
    # равномерно расределяем задачи между студентами
    engine_names = [engine for engine in islice(cycle(engines), None, len(users))]
    for i, (user, engine_name) in enumerate(imap(None, users, engine_names)):
        # извлекаем заданный движок задачи и инстанцируем его
        ProblemEngine = settings.EngineManager.get_engine(engine_name)
        engine = ProblemEngine()
        # генерируем исходные данные задачи и выполняем их корректировку
        while True:
            try:
                engine.randomize_in_params()
                engine.adjust()
                engine.calculate()
            except Exception:
                pass
            else:
                break
        # создаем объект задания и передаем ему все необходимые данные
        problem = Problem(user = user, problem_engine = engine_name,
            problem_in_params = engine.get_store_str(), # передаем в задание исходные данные 
            group = problem_group)
        problem.save()
        # обновляем состояние задания
        create_problems.update_state(state = "PROGRESS", meta = {"current": i, "total": len(users) })
    problem_group.created = True
    problem_group.save()
    return True