#!/urs/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response

def admin_only(function):
	def wrapper(*args, **kwargs):
		request = args[0]
		if request.user.is_superuser:
			return function(*args, **kwargs)
		else:
			return render_to_response("no_access.html")
	return wrapper