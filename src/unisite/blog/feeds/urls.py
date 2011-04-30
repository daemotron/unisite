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

from django.conf.urls.defaults import patterns, url
from django.contrib.comments.feeds import LatestCommentFeed

# TODO: add name properties to url patterns
urlpatterns = patterns('my_universe.blog.feeds.views',
    url(r'^$', 'feed_list'),
    url(r'^authors/(?P<author>\w+)/?$', 'feed_list'),
    url(r'^tags/(?P<tagslug>\w+)/?$', 'feed_list'),
    url(r'^(?P<year>\d{4})/?$', 'feed_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/?$', 'feed_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{1,2})/?$', 'feed_list'),
    url(r'^comments/(?P<entry>\d+)/?$', 'comment_list'),
    url(r'^comments/?$', LatestCommentFeed()),
)