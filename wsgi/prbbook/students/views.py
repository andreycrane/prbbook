# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from models import Group, UserProfile
from prbbook.decorators import admin_only
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from prbbook.students.forms import GroupForm, StudentForm
from prbbook.problems.models import Problem
from parser import HtmlStudentsParser, CsvStudentsParser

# вывод списка студентов
@login_required(login_url='/login/')
@admin_only
def students(request, page):
    students_list = User.objects.filter(is_superuser = False)
    # создаем обьект разбивателя на страницы
    paginator = Paginator(students_list, 25)
    students = []
    # пытаемся вытащить запрошенную страницу из списка страниц
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # если обьект номера страницы не сисло 
        # извелкаем первую
        students = paginator.page(1)
    except EmptyPage:
        # если страница по запрошенному номеру не существует
        # извлекаем последнюю
        students = paginator.page(paginator.num_pages)
    return render_to_response("students_all.html", { 'students': students })

@login_required(login_url = '/login/')
@admin_only
def register(request):
    student = False
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if not form.is_valid():
            return render_to_response("register_student.html", {'form': form })
        name = form.cleaned_data['name']
        login = form.cleaned_data['login']
        password = form.cleaned_data['password']
        group = form.cleaned_data['group']
        # создаем новый объект пользователя
        user = User.objects.create_user(username = login, password = password)
        user.first_name = name
        user.save()

        profile = UserProfile.objects.create(user = user, group = group)
        profile.save()
        student = user
    return render_to_response("register_student.html", {'form': StudentForm(), 'student': student })

@login_required(login_url = '/login/')
@admin_only
def groups(request, page):
    groups_list = Group.objects.all()
    paginator = Paginator(groups_list, 25)
    groups = []
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)
    return render_to_response("groups_all.html", { 'groups': groups })

@login_required(login_url = '/login/')
@admin_only
def add_group(request):
    group = False
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if not form.is_valid():
            return render_to_response("add_group.html", {'form': form })
        group = form.save()
    return render_to_response("add_group.html", { 'group': group })


@login_required(login_url = '/login/')
@admin_only
def student_problems_list(request, student_id):
    student = get_object_or_404(User, pk = student_id)
    problems = Problem.objects.filter(user = student)
    return render_to_response("lecturer_student_problems.html", locals())

@login_required(login_url = '/login/')
@admin_only
def students_of_group(request, group_id):
    group = get_object_or_404(Group, pk = group_id)
    students_list = User.objects.filter(userprofile__group = group)
    return render_to_response("students_of_group.html",  locals())

@login_required(login_url = '/login/')
@admin_only
def register_from_html(request):
    created = False
    if request.method == 'POST':
        reg_file = request.FILES['file']
        content = reg_file.read()
        try:
            parser = HtmlStudentsParser(unicode(content.decode('cp1251')))
            repeated = 0
            for group_name, lst_name, first_name, login in parser.get_list():
                # ищем в базе данную группу или создаем ее
                try:
                    group = Group.objects.get(name = group_name)
                except ObjectDoesNotExist:
                    group = Group(name = group_name)
                    group.save()
                # ищем в базе пользователя с даным логином
                try:
                    user = User.objects.get(username = login)
                except ObjectDoesNotExist:
                    # если пользователь не существует создаем его

                    user = User(username = login, first_name = first_name, last_name = lst_name, password = login) 
                    user.save()
                else:
                    # если пользователь существует пропускаем итерацию
                    repeated += 1
                    continue
                # ищем в базе студента с аккаунтом и группой
                try:
                    student = UserProfile.objects.get(user = user, group = group)
                except ObjectDoesNotExist:
                    # если не существует создаем его
                    student = UserProfile(user = user, group = group)
                    student.save()
            created = True
        except Exception as e:
            error = str(e)
    return render_to_response("register_from_html.html", locals())

@login_required(login_url = '/login/')
@admin_only
def register_from_csv(request):
    created = False
    if request.method == 'POST':
        reg_file = request.FILES['file']
        content = reg_file.read()
        try:
            parser = CsvStudentsParser(content.decode('cp1251'))
            repeated = 0
            for login, lst_name, first_name, group_name in parser.get_list():
                # ищем в базе данную группу или создаем ее
                try:
                    group = Group.objects.get(name = group_name)
                except ObjectDoesNotExist:
                    group = Group(name = group_name)
                    group.save()
                # ищем в базе пользователя с даным логином
                try:
                    user = User.objects.get(username = login)
                except ObjectDoesNotExist:
                    # если пользователь не существует создаем его

                    user = User(username = login, first_name = first_name, last_name = lst_name, password = login) 
                    user.save()
                else:
                    # если пользователь существует пропускаем итерацию
                    repeated += 1
                    continue
                # ищем в базе студента с аккаунтом и группой
                try:
                    student = UserProfile.objects.get(user = user, group = group)
                except ObjectDoesNotExist:
                    # если не существует создаем его
                    student = UserProfile(user = user, group = group)
                    student.save()
            created = True
        except Exception as e:
            error = str(e)
    return render_to_response("register_from_csv.html", locals())