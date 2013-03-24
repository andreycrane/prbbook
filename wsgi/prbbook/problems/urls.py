from django.conf.urls import patterns, include, url

urlpatterns = patterns('prbbook.problems.views',
	url(r'^$', 'problems_groups', {'page': 1 }),
	url(r'^page/(?P<page>\d+)/$', 'problems_groups'),
	url(r'^group/(?P<group>\d+)/$', 'group_problems_list', name="group_problems_list"),
	url(r'^create/$', 'create_problems'),
	url(r'^problem/(?P<problem_id>\d+)/$', 'show_problem'),
	url(r'^problem/(?P<problem_id>\d+)/img/$', 'problem_img', { 'stage': 1 }),
	url(r'^problem/(?P<problem_id>\d+)/img/(?P<stage>\d+)/$', 'problem_img'),
	url(r'^problem/(?P<problem_id>\d+)/img/(?P<in_params>{(\s*\"[a-zA-Z]+\w*\"\s*:\s*\d+\.*\d*\s*\,\s*)*' 
		+ '(\s*\"[a-zA-Z]+\w*\"\s*:\s*\d+\.*\d*\s*){1}})/$', 'problem_preview_img', {'stage': 1 }),
	url(r'^problem/(?P<problem_id>\d+)/img/(?P<in_params>{(\s*\"[a-zA-Z]+\w*\"\s*:\s*\d+\.*\d*\s*\,\s*)*' 
		+ '(\s*\"[a-zA-Z]+\w*\"\s*:\s*\d+\.*\d*\s*){1}})/stage/(?P<stage>\d+)/$', 'problem_preview_img'),
	url(r'^problem/preview/', 'problem_preview_request'),
	url(r'^problem/(?P<problem_id>\d+)/regenerate/$', 'regenerate_problem'),
	url(r'group/(?P<group_id>\d+)/print/$', 'problems_group_print'),
	url(r'problem/(?P<problem_id>\d+)/student/$', 'student_problem'),
	url(r'problem/(?P<problem_id>\d+)/img/student/$', 'student_problem_img')
)