from django.conf.urls.defaults import patterns, include, url

urls = patterns('', 
    url(r'^button/(?P<remoteID>\d+)/(?P<y>\d+)/(?P<x>\d+)/$', 'Custom_Remotes.views.newButton'),
    url(r'^button/(?P<buttonID>\d+)/$', 'Custom_Remotes.views.editButton'),
    url(r'^run_button/(?P<buttonID>\d+)/$', 'Custom_Remotes.views.runButton'),
    url(r'^remote/(?P<remoteID>\d+)/$', 'Custom_Remotes.views.remote'),
    url(r'^device_remote/(?P<deviceID>\d+)/$', 'Custom_Remotes.views.deviceRemote'),
    url(r'^remotes/$', 'Custom_Remotes.views.remotes'),
    url(r'^custom_remotes/$', 'Custom_Remotes.views.customRemotes'),
    url(r'^auto_remotes/$', 'Custom_Remotes.views.autoRemotes'),
)
