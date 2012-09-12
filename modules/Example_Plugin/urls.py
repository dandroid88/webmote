from django.conf.urls.defaults import patterns, include, url

urls = patterns('', 
   url(r'^example/instructions/(?P<num>\d+)/$', 'Example_Plugin.views.instructions'),
   url(r'^example/$', 'Example_Plugin.views.main'),
)
