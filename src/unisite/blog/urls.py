'''
Copyright (c) 2011 Daemotron <mail@daemotron.net>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''

from django.conf.urls.defaults import patterns, include, url

# TODO: add name properties to url patterns
urlpatterns = patterns('my_universe.blog.views',
    url(r'^$', 'entry_list'),
    url(r'^page/(?P<page>\d+)/?$', 'entry_list'),
    url(r'^authors/(?P<author>\w+)/?$', 'entry_list'),
    url(r'^authors/(?P<author>\w+)/page/(?P<page>\d+)/?$', 'entry_list'),
    url(r'^tags/(?P<tagslug>\w+)/?$', 'entry_list'),
    url(r'^tags/(?P<tagslug>\w+)/page/(?P<page>\d+)/?$', 'entry_list'),
    url(r'^(?P<year>\d{4})/?$', 'entry_list'),
    url(r'^(?P<year>\d{4})/page/(?P<page>\d+)/?$', 'entry_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/?$', 'entry_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/page/(?P<page>\d+)/?$', 'entry_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{1,2})/?$', 'entry_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{1,2})/page/(?P<page>\d+)/?$', 'entry_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/?$', 'entry_detail'),
    url(r'^feeds/', include('my_universe.blog.feeds.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
)