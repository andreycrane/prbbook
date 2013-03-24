#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from prbbook.students.models import UserProfile
from prbbook.students.models import Group
from problems.models import Problem, ProblemGroup

admin.site.register(Problem)
admin.site.register(ProblemGroup)
admin.site.register(Group)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)