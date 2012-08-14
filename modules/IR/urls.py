from django.conf.urls.defaults import patterns, include, url

urls = patterns('', 
    url(r'^ir/addTransceiver/$', 'IR.views.transceivers'),
   url(r'^ir/transceiverSearch/$', 'IR.views.transceiverSearch'),
    url(r'^ir/$', 'IR.views.main'),
)
