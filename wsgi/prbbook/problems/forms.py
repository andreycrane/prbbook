# -*- coding: utf-8 -*-
from django import forms
from prbbook.students.models import Group
from prbbook import settings

class ProblemsForm(forms.Form):
	name = forms.CharField(max_length = 255, label = u'Имя группы заданий', 
							required = False, widget = forms.TextInput(attrs={
								'class': 'input-xlarge',
								'placeholder': u'Без названия'
							}))
	groups = forms.ModelMultipleChoiceField(queryset = Group.objects.all(), required = True, 
										label = u"Кому")
	engines = forms.MultipleChoiceField(choices = settings.EngineManager.get_subcat_choices(), required = True, 
									label = u"Задачи", widget = forms.SelectMultiple(attrs = {
											'size': 10,
											'class': 'select-input'
										}))