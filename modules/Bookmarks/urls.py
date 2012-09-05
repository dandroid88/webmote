from django.conf.urls.defaults import patterns, include, url

urls = patterns('', 
    url(r'^bookmark/(?P<actionID>\d+)/$', 'Bookmarks.views.bookmark'),
    url(r'^bookmark_actions/$', 'Bookmarks.views.bookmarkActions'),
)
