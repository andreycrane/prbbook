# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin

class Group(models.Model):
	task_id = models.CharField(max_length = 255, blank = True)
	created = models.BooleanField(default = False, blank = True)
	count = models.IntegerField()

class Member(models.Model):
	group = models.ForeignKey(Group)

admin.site.register(Group)
admin.site.register(Member)