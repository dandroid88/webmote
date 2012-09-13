from django.conf.urls.defaults import patterns, include, url

urls = patterns('', 
   url(r'^macros/macro/(?P<num>\d+)/$', 'Macros.views.macro'),
   url(r'^macros/$', 'Macros.views.macros'),
)
