from django.conf.urls.defaults import patterns, include, url

urls = patterns('', 
   url(r'^x10/devices/$', 'X10.views.devices'),
   url(r'^x10/device/(?P<num>\d+)/$', 'X10.views.device'),
#   url(r'^x10/state/$', 'X10.views.state'),
#   url(r'^/help/$', 'X10.views.help'),
   url(r'^x10/$', 'X10.views.main'),
)
