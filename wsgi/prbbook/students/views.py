# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import Group, UserProfile
from prbbook.decorators import admin_only
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from prbbook.students.forms import GroupForm, StudentForm
from prbbook.problems.models import Problem

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