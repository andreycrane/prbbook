#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from prbbook.students.models import Group
from django.contrib.auth.models import User

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group

class StudentForm(forms.Form):
    name = forms.CharField(max_length = 30, min_length = 3, 
                            required = True, label = u'ФИО',
                            widget = forms.TextInput(attrs={
                                'placeholder': u'Фамилия Имя Отчество',
                                'style': 'margin-bottom: 5px;',
                                'class': 'input-xlarge'}))
    login = forms.CharField(max_length = 30, min_length = 3, 
                            required = True, label = u'Логин',
                            widget = forms.TextInput(attrs={
                                                  'placeholder': u'Логин'}))
    password = forms.CharField(min_length = 6, required =True, 
                            label = u'Пароль', 
                            widget = forms.PasswordInput(attrs={
                                'placeholder': u'Пароль'}))
    retype = forms.CharField(min_length = 6, required = True,
                             label = u'Пароль', 
                             widget = forms.PasswordInput(attrs={
                                'placeholder': u'Повторить'
                            }))
    group = forms.ModelChoiceField(queryset = Group.objects.all(), empty_label = u'Не выбрана', required = True, label = u'Группа')

    def clean(self):
        cleaned_data = super(StudentForm, self).clean()
        
        password = cleaned_data.get("password")
        retype = cleaned_data.get("retype")
        login = cleaned_data.get('login')

        if User.objects.filter(username = login):
            msg = u'Пользователь с таким логином уже существует.'
            self._errors['login'] = self.error_class([msg])

        if password and retype and (password != retype):
            msg = u'Пароли не совпадают.'
            self._errors['retype'] = self.error_class([msg])
          
        return cleaned_data