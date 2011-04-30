from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Index is index...
    url(r'^$', 'my_universe.page.views.index', name="index-page"),

    # Page module
    url(r'^page/', include('unisite.page.urls')),
    
    # Blog module
    url(r'^blog/', include('unisite.blog.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
