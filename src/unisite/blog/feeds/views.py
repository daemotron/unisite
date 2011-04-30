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

from datetime import datetime

from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.conf import settings
#from django.contrib.comments.feeds import LatestCommentFeed
#from django.contrib.syndication.views import Feed

from unisite.util import response
from unisite.blog import models
from unisite.blog.views import get_entry_list


#def generic_comments(request):
#    fdict = { 'latest': LatestCommentFeed, }
#    return feed(request, 'latest', fdict)


def feed_list(request, year=0, month=0, day=0, author='', tagslug=''):
    
    entries = get_entry_list(int(year), int(month), int(day), author, '', tagslug)
    
    if entries.count() >= settings.ENTRIES_PER_FEED:
        entries = entries[:settings.ENTRIES_PER_FEED]
    
    if entries:
        pdate = entries[0].publish_date
    else:
        pdate = None
    
    # If month and day have not been set, assign 1 (so they don't block the date() function)
    if (year != 0 and month == 0 and day == 0):
        month = 1
        day = 1
        dtype = 'Y'
    elif (year != 0 and month != 0 and day == 0):
        day = 1
        dtype = 'F Y'
    else:
        dtype = None
    
    try:
        date = datetime(int(year), int(month), int(day))
    except ValueError:
        date = None
        
    try:
        tag = models.Tag.objects.get(slug__iexact=tagslug)
    except models.Tag.DoesNotExist:
        tag = None
        
    try:
        authorUser = User.objects.get(username__iexact=author)
    except User.DoesNotExist:
        authorUser = None
        
    ctx = {
        'entries': entries,
        'pubdate': pdate,
        'host': request.get_host(),
        'secure': request.is_secure(),
        'filter': {
            'author': authorUser,
            'date': {'type': dtype, 'value': date},
            'tag': tag,
        }
    }
    
    return response.render(request, 'blog/feeds/rss_entries.html', ctx, mimetype="application/rss+xml")


def comment_list(request, entry=0):
    
    if entry > 0:
        try:
            ent = models.Entry.objects.get(id=entry)
        except models.Entry.DoesNotExist:
            raise Http404
    else:
        ent = None
    
    try:
        clist = Comment.objects.filter(content_type__model='entry').filter(is_public=True).filter(is_removed=False)
    except Comment.DoesNotExist:
        clist = None
        
    pdate = None
    if clist != None:
        clist = clist.order_by('-submit_date')
        try:
            pdate = clist[0].submit_date
        except IndexError:
            pdate = None
    
    ctx = {
        'pubdate': pdate,
        'entry': ent,
        'host': request.get_host(),
        'secure': request.is_secure(),
    }
    
    return response.render(request, 'blog/feeds/rss_comments.html', ctx, mimetype="application/rss+xml")