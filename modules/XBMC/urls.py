from django.conf.urls.defaults import patterns, include, url

urls = patterns('', 
   url(r'^xbmc/host/(?P<num>\d+)/$', 'XBMC.views.host'),
   url(r'^xbmc/hosts/$', 'XBMC.views.hosts'),
)
