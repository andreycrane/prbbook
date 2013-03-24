#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import logout as auth_logout
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from forms import *
import settings
from decorators import *
from problems.models import Problem

def login(request):
    if request.method == 'POST':
        form  = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            
            user = authenticate(username = username, password = password)
            auth_login(request, user)

            if remember_me:
                request.session.set_expiry(0)
            
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render_to_response('login.html', { 'form': form })

@login_required(login_url = '/login/')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url = '/login/')
def home(request):
    user = request.user
    if user.is_superuser:
        return render_to_response("lecturer_engines.html", { 'engines': settings.EngineManager.engines })
    else:
        return render_to_response("student_panel.html", { 'problems': Problem.objects.filter(user = user) })

@login_required(login_url = '/login/')
@admin_only
def engine_preview(request, engine_id):
    user = request.user
    if not user.is_superuser:
        return HttpResponseRedirect("/")

    prbcls = settings.EngineManager.get_engine(engine_id)

    problem = prbcls()
    problem.load_preview_params()
    in_params = problem.get_in_params()
    problem.calculate()
    out_params = problem.get_out_params()

    return render_to_response("engine_preview.html", { 'prb': prbcls, 
                                                        'in_params': in_params,
                                                        'out_params': out_params })

@login_required(login_url = '/login/')
@admin_only
def engine_preview_image(request, engine_id, stage):
    ProblemEngine = settings.EngineManager.get_engine(engine_id)

    engine = ProblemEngine()
    engine.load_preview_params()
    engine.calculate()
    img = engine.get_image(stage = int(stage))
    # пишем содержимое изображения в тело ответа
    response = HttpResponse(mimetype="image/png")
    img.save(response, "PNG")
    return response


@login_required(login_url = '/login/')
def profile(request):
    user = request.user
    template = "lecturer_profile_page.html" if user.is_superuser else "student_profile_page.html"
    changes_saved = False
    if request.method == 'POST':
        action = request.POST.get('action', None)
        if action == 'login':
            change_login_form = ChangeLoginForm(user, request.POST)
            if not change_login_form.is_valid():
                return render_to_response(template, { 'login_form': change_login_form, 'password_form': ChangePasswordForm(user) })
            user.username = change_login_form.cleaned_data['login']
            user.save()
            changes_saved = True
        elif action == 'password':
            change_password_form = ChangePasswordForm(user, request.POST)
            if not change_password_form.is_valid():
                return render_to_response(template, { 'password_form': change_password_form, 
                                                    'login_form': ChangeLoginForm(user, { 'login': user.username}) })
            new_password = change_password_form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            changes_saved = True
        else:
            return HttpResponseNotFound()
    return render_to_response(template, { 'login_form': ChangeLoginForm(user, { 'login': user.username}), 
                                          'password_form': ChangePasswordForm(user), 'changes_saved': changes_saved })