#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label = u'Логин', 
                               widget = forms.TextInput(attrs={
                                                  'placeholder': u'Логин'}))
    password = forms.CharField(label = u'Пароль', 
                               widget = forms.PasswordInput(attrs={
                                                  'placeholder': u'Пароль'}))
    remember_me = forms.BooleanField(label = u'Запомнить меня', required = False)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        print cleaned_data
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not authenticate(username = username, password = password):
            msg = u'Неправильный логин или пароль.'
            self._errors['password'] = self.error_class([msg])

        return cleaned_data


class ChangeLoginForm(forms.Form):
    login = forms.CharField(label = u'Логин', required = True, 
                  min_length = 4,
                  widget = forms.TextInput(attrs={
                      'pattern': r'[a-zA-Z0-9+@.-_]+'
                    }))
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeLoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(ChangeLoginForm, self).clean()

        login = self.cleaned_data.get('login')

        if User.objects.filter(username = login) and self.user.username != login:
            msg = u"Пользователь с таким логином уже существует"
            self._errors['login'] = self.error_class([msg])
            self.cleaned_data['login'] = self.user.username

        return self.cleaned_data

class ChangePasswordForm(forms.Form):
    password = forms.CharField(label = u'Текущий пароль', required = True,
                                widget = forms.PasswordInput())
    new_password = forms.CharField(label = u'Новый пароль', required = True,
                                widget = forms.PasswordInput())
    retype_new = forms.CharField(label = u'Повторите пароль', required = True,
                                widget = forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        current_password = cleaned_data.get('password')
        new_password = cleaned_data.get('new_password')
        retype_new = cleaned_data.get('retype_new')

        if not authenticate(username = self.user.username, password = current_password):
            msg = u"Пароль неверный"
            self._errors['password'] = self.error_class([msg])

        if new_password != retype_new:
            msg = u"Пароли не совпадают"
            self._errors['retype_new'] = self.error_class([msg])
        return cleaned_data