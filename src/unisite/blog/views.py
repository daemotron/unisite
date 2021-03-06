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
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User

from unisite.util import response
from unisite.blog import models


def get_entry_list(year=0, month=0, day=0, author='', slug='', tagslug=''):
    entries = models.Entry.objects.filter(status__exact='p').filter(publish_date__lte=datetime.now())
    
    if year > 0:
        entries = entries.filter(publish_date__year=year)
        
    if month > 0:
        entries = entries.filter(publish_date__month=month)

    if day > 0:
        entries = entries.filter(publish_date__day=day)

    if author != '':
        entries = entries.filter(entrytranslation__author__username=author)
        
    if slug != '':
        entries = entries.filter(entrytranslation__slug__iexact=slug)
        
    if tagslug != '':
        entries = entries.filter(tags__slug__iexact=tagslug)

    entries = entries.distinct()
    entries = entries.order_by('-publish_date')
    
    return entries


def entry_detail(request, year, month, day, slug):
    entry = get_entry_list(int(year), int(month), int(day), '', slug)
    if entry:
        ctx = {
            'entry': entry[0]
        }
        return response.render(request, 'blog/entry_detail.html', ctx)
    else:
        raise Http404


def entry_list(request, year=0, month=0, day=0, author='', tagslug='', page=1):
    
    # Fetch and paginate the entry list
    entry_list = get_entry_list(int(year), int(month), int(day), author, '', tagslug)
    paginator = Paginator(entry_list, settings.ENTRIES_PER_PAGE)
    
    try:
        entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)
    
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
        'filter': {
            'author': authorUser,
            'date': {'type': dtype, 'value': date},
            'tag': tag,
        }
    }
    
    return response.render(request, 'blog/entry_list.html', ctx)


def feed(request, type):
    pass