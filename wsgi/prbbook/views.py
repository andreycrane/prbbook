from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import View
from prbbook.tasks import create_members
fromprbbook.models import Group, Member
from django.http import HttpResponseRedirect, HttpResponse
from json import dumps
from termcolor import colored, cprint
from pprint import pprint

class HomeView(View):
    def get(self, request):
        groups = Group.objects.filter(created = False)
        print groups
        return render_to_response("index.html", locals())

    def post(self, request):
        group = Group(count = 200)
        group.save()
        create_members.delay(group, 200)
        return HttpResponseRedirect("/")

def group_status(request, group_id):
    group = get_object_or_404(Group, pk = int(group_id))
    print colored("Group object..", "red")
    task = create_members.AsyncResult(group.task_id)
    status = task.status
    # Response object
    task_status = { 'status': status }
    # special
    if status == "PROGRESS":
        task_status['current'] = task.info['current']
        task_status['total'] = task.info['total']
        task_status['process'] = (100.0 / task_status['total']) * task_status['current']
    if True:
        print "%s" % colored("Action: group_status", "red")
        print "Task status: %s" % colored(task.status, "green")
        print colored("Response object: ", "red"),
        pprint(task_status)
    return HttpResponse(dumps(task_status), mimetype = 'application/json',)