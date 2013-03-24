# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from prbbook import settings
from models import ProblemGroup, Problem
from prbbook.decorators import admin_only
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from forms import ProblemsForm
from itertools import cycle, islice, imap, groupby
from json import dumps
from django.template.loader import render_to_string

@login_required(login_url = '/login/')
@admin_only
def problems_groups(request, page):
    groups_list = ProblemGroup.objects.all()
    paginator = Paginator(groups_list, 25)
    groups = []
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)
    return render_to_response("problems.html", {'groups': groups })

@login_required(login_url = '/login/')
@admin_only
def group_problems_list(request, group):
    group = get_object_or_404(ProblemGroup, pk = group)
    # извлекаем список заданий и сортируем по задачам
    problems = sorted(Problem.objects.filter(group = group), key=lambda problem: problem.problem_engine)
    # группируем задания по задаче исходным данным к ней
    problems_groups = []
    for engine, problems_by_engine in groupby(problems, key=lambda x: x.problem_engine):
        for params, problems_by_params in groupby(sorted(problems_by_engine, key=lambda x: x.problem_in_params), key=lambda x: x.problem_in_params):
            problems_groups.append(list(problems_by_params))
    return render_to_response("group_problems_list.html", locals())


@login_required(login_url = '/login/')
@admin_only
def create_problems(request):
    group = False
    if request.method == 'POST':
        # загружаем данные POST из запроса в объект формы
        form = ProblemsForm(request.POST)
        # проверяем правильность загруженных данных
        if not form.is_valid(): # если данные не верны возвращаем форму с сообщением об ошибке
            return render_to_response("create_problems.html", { 'form': form })
        # извлекаем из формы данные в объекты
        name = form.cleaned_data["name"]
        engines = form.cleaned_data["engines"]
        groups = form.cleaned_data["groups"]
        # формируем список студентов по указанным в форме группам
        users = [profile.user for group in groups for profile in group.userprofile_set.all()]
        # равномерно расределяем задачи между студентами
        engine_names = [engine for engine in islice(cycle(engines), None, len(users))]
        # если имя группы заданий не задано, то будет использовано значение по умолчанию
        if not name: name = u"Без названия"
        # создаем объект группы и сохраняем его
        problems_group = ProblemGroup(name = name)
        problems_group.save()
        print users
        for user, engine_name in imap(None, users, engine_names):
            print user, engine_name
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
                group = problems_group)
            problem.save()
        group = problems_group
    return render_to_response("create_problems.html", {'form': ProblemsForm(), 'group': group })

@login_required(login_url = '/login/')
@admin_only
def show_problem(request, problem_id):
    saved = False
    # находим объект задания или отдаем ошибку 404
    problem = get_object_or_404(Problem, pk = problem_id)
    # если это POST запрос
    if request.method == 'POST':
        in_params = {}
        # извлекаем ключи из POST запроса
        # и формируем новый объект для сериализации
        for key in request.POST.keys():
            in_params[key] = float(request.POST[key].replace(",", "."))
        # сериализуем объект в строку
        store_str = dumps(in_params)
        # сохраняем новые исходные данные в задание
        problem.problem_in_params = store_str
        problem.save()
        saved = True
    # извлекаем класс движка задачи для данного задания и интстанцируем его
    ProblemEngine = settings.EngineManager.get_engine(problem.problem_engine)
    engine = ProblemEngine()
    # загружаем данные задачи в движок из задания, производим расчет
    # и извлекаем входные и выходные данные
    engine.load_store_str(problem.problem_in_params)
    in_params = engine.get_in_params()
    engine.calculate()
    out_params = engine.get_out_params()
    return render_to_response("lecturer_problem_page.html", locals())

# контроллер для генерирования изображения
# по заданным заданию и уровню отрисовки
@login_required(login_url = '/login/')
@admin_only
def problem_img(request, problem_id, stage):
    # находим объект задания или отдаем ошибку 404
    problem = get_object_or_404(Problem, pk = problem_id)
    # извлекаем класс движка задачи для данного задания и интстанцируем его
    ProblemEngine = settings.EngineManager.get_engine(problem.problem_engine)
    engine = ProblemEngine()
    # загружаем данные задачи в движок из задания, производим расчет
    # и извлекаем входные и выходные данные
    engine.load_store_str(problem.problem_in_params)
    engine.calculate()
    img = engine.get_image(stage = int(stage))
    # выполняем сериализацию изображения в объект ответа
    response = HttpResponse(mimetype = 'image/png')
    img.save(response, 'PNG')
    return response

# контроллер для генерирования изображений 
# для предосмотра по заданным в url запроса параметрам
@login_required(login_url = '/login/')
@admin_only
def problem_preview_img(request, problem_id, in_params, stage):
    # находим объект задания или отдаем ошибку 404
    problem = get_object_or_404(Problem, pk = problem_id)
    # извлекаем класс движка задачи для данного задания и интстанцируем его
    ProblemEngine = settings.EngineManager.get_engine(problem.problem_engine)
    engine = ProblemEngine()
    # загружаем данные задачи в движок из задания, производим расчет
    # и извлекаем входные и выходные данные
    response = None
    try:
        engine.load_store_str(in_params)
        engine.calculate()
        img = engine.get_image(stage = int(stage))
        # выполняем сериализацию изображения в объект ответа
        response = HttpResponse(mimetype = 'image/png')
        img.save(response, 'PNG')
    except Exception as e:
        response = HttpResponse(mimetype = 'text/html', status = 500)
    return response

@login_required(login_url = '/login/')
@admin_only
def problem_preview_request(request):
    # извлекаем необходимые параметры из запросы
    try:
        in_params = request.GET["in_params"]
        problem = request.GET["problem"]
    except:
        return HttpResponseNotFound() # если параметры отсутсвуют -> 404
    problem = get_object_or_404(Problem, pk = problem) # если объект отсутствует -> 404
     # извлекаем класс движка задачи для данного задания и интстанцируем его
    ProblemEngine = settings.EngineManager.get_engine(problem.problem_engine)
    engine = ProblemEngine()
    # создаем JSON объект ответа
    resp = { 'status': 'success', 'body': '' }
    try:
         # загружаем данные задачи в движок из запроса
        engine.load_store_str(in_params)
        # производит валидацию данных
        engine.validate()
        # производим расчет
        engine.calculate()
        # рендерим выходные данные задачи в шаблон
        resp['body'] = render_to_string("out_params.html", { 'out_params': engine.get_out_params() })
    except Exception as e:
        # в случае ошибки при загрузки данных в движок
        resp['status'] = 'error'
        resp['body'] = e.message
    print problem, in_params
    return HttpResponse(dumps(resp), status = 200, mimetype="application/json")

@login_required(login_url = '/login/')
@admin_only
def regenerate_problem(request, problem_id):
    problem = get_object_or_404(Problem, pk = problem_id)
    # извлекаем заданный движок задачи и инстанцируем его
    ProblemEngine = settings.EngineManager.get_engine(problem.problem_engine)
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
    problem.problem_in_params = engine.get_store_str()
    problem.save()
    redirect_url = "/problems/group/%d/" % problem.group.id
    return HttpResponseRedirect(redirect_url)

@login_required(login_url = '/login/')
@admin_only
def problems_group_print(request, group_id):
    group = get_object_or_404(ProblemGroup, pk = group_id)
    problems = Problem.objects.filter(group = group.id)
    # создаем список заданий
    problems_list = []
    for problem in problems:
        # создаем хэш-объект задания
        problem_dict = {}
        problem_dict["object"] = problem
        # извлекаем движок
        ProblemEngine = settings.EngineManager.get_engine(problem.problem_engine)
        problem_dict["engine"] = ProblemEngine
        # инстанцируем движок и загружаем в него данные
        engine = ProblemEngine()
        engine.load_store_str(problem.problem_in_params)
        # получаем исходные данные к задаче
        problem_dict["in_params"] = engine.get_in_params()
        # расчитываем задачу и получаем данные решения
        engine.calculate()
        problem_dict["out_params"] = engine.get_out_params()
        # добавляем хэш задания в список
        problems_list.append(problem_dict)
    return render_to_response("problems_print.html", locals())


@login_required(login_url = '/login/')
def student_problem(request, problem_id):
    # излекаем задание с заданным id и принадлежащие данному студенту 
    problem = get_object_or_404(Problem, pk = problem_id, user = request.user)
    # извлекаем класс движка задачи для данного задания и интстанцируем его
    ProblemEngine = settings.EngineManager.get_engine(problem.problem_engine)
    engine = ProblemEngine()
    # загружаем данные задачи в движок из задания, производим расчет
    # и извлекаем входные и выходные данные
    engine.load_store_str(problem.problem_in_params)
    in_params = engine.get_in_params()
    return render_to_response("student_problem.html", locals())

@login_required(login_url = '/login/')
def student_problem_img(request, problem_id):
    # находим объект задания или отдаем ошибку 404
    problem = get_object_or_404(Problem, pk = problem_id, user = request.user)
    # извлекаем класс движка задачи для данного задания и интстанцируем его
    ProblemEngine = settings.EngineManager.get_engine(problem.problem_engine)
    engine = ProblemEngine()
    # загружаем данные задачи в движок из задания, производим расчет
    # и извлекаем входные и выходные данные
    engine.load_store_str(problem.problem_in_params)
    engine.calculate()
    img = engine.get_image(stage = int(1))
    # выполняем сериализацию изображения в объект ответа
    response = HttpResponse(mimetype = 'image/png')
    img.save(response, 'PNG')
    return response