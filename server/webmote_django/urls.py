from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     #url(r'^$', 'webmote.views.home', name='home'),
    url(r'^$', 'webmote_django.webmote.views.index'),
    # url(r'^webmote/', include('webmote_django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Pages
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$','webmote_django.webmote.views.logout_view'),
    url(r'^help/$', 'webmote_django.webmote.views.help'),
    url(r'^logout/$', 'webmote_django.webmote.views.logout_view'),
    url(r'^identification/$', 'webmote_django.webmote.views.identification'),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += staticfiles_urlpatterns()
