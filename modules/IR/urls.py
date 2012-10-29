from django.conf.urls.defaults import patterns, include, url

urls = patterns('', 
   url(r'^ir/transceivers/$', 'IR.views.transceivers'),
   url(r'^ir/devices/$', 'IR.views.devices'),
   url(r'^ir/device/(?P<num>\d+)/$', 'IR.views.device'),
   url(r'^ir/recordAction/$', 'IR.views.recordAction'),
   url(r'^ir/searchLIRC/(?P<deviceID>\d+)/$', 'IR.views.searchLIRC'),
   url(r'^ir/addFromLIRC/(?P<deviceID>\d+)/$', 'IR.views.addFromLIRC'),
   url(r'^ir/help/$', 'IR.views.help'),
   url(r'^ir/$', 'IR.views.main'),
)
