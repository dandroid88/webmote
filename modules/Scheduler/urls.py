from django.conf.urls.defaults import patterns, include, url

urls = patterns('', 
    url(r'^scheduler/schedule/(?P<id>\d+)/$', 'Scheduler.views.schedule'),
    url(r'^scheduler/editActive/(?P<id>\d+)/$', 'Scheduler.views.editActive'),
    url(r'^scheduler/runSchedlet/(?P<id>\d+)/$', 'Scheduler.views.runSchedlet'),
    url(r'^scheduler/$', 'Scheduler.views.schedules'),
)
