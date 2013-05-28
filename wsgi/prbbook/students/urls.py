from django.conf.urls import patterns, include, url

urlpatterns = patterns('prbbook.students.views',
	url(r'^$', 'students', {'page': 1}, name="students"),
	url(r'^page/(?P<page>\d+)/$', 'students', name='students_page'),
	url(r'^register/$', 'register', name="register_student"),
	url(r'^groups/$', 'groups', {'page': 1}, name="students_groups"),
	url(r'^group/(?P<group_id>\d+)/delete/$', 'delete_students_group', name='delete_students_group'),
	url(r'^groups/page/(?P<page>\d+)/$', 'groups', name="students_groups_page"),
	url(r'^groups/add/$', 'add_group', name="add_group"),
	url(r'^student/(?P<student_id>\d+)/problems/', 'student_problems_list', name="students_problems_list"),
	url(r'^groups/group/(?P<group_id>\d+)/$', 'students_of_group', name="students_of_group"),
	url(r'register/html/$', 'register_from_html', name='register_from_html'),
	url(r'register/csv/$', 'register_from_csv', name='register_from_csv')
)