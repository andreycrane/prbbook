from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('prbbook.views',
	url(r'^$', 'home', name="home"),
	url(r'^login/$', 'login', name="login"),
	url(r'^logout/$', 'logout', name="logout"),
	url(r'^profile/$', 'profile', name="profile"),
	url(r'^engine/preview/(?P<engine_id>[a-zA-z0-9._]+)/$', 'engine_preview', name="engine_preview"),
	url(r'^engine/preview/(?P<engine_id>[a-zA-z0-9._]+)/img/(?P<stage>\d+)/$', 'engine_preview_image', name="engine_preview_image"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^students/', include('prbbook.students.urls')),
    url(r'^problems/', include('prbbook.problems.urls'))
)

urlpatterns += staticfiles_urlpatterns()