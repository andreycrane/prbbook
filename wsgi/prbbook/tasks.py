# -*- coding: utf-8 -*-

from celery import task
from time import sleep
from celery import current_task
from prbbook.models import Group, Member

@task(ignore_result = False, track_started = True)
def create_members(group, members):
	# создаем ссылки на объекты логера и запроса
	request = create_members.request

	# присваием груп id задания выполняеющего работу
	group.task_id = request.id
	group.save()

	log = create_members.get_logger()
	for i in xrange(members):
		log.info("Created %d members" % i)
		Member(group = group).save()
		create_members.update_state(state = "PROGRESS", meta = {"current": i, "total": members})
	# обозначаем группу как созданную
	group.created = True
	group.save()
	return True