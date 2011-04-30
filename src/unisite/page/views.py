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

from django.http import Http404
from unisite.util import response

from unisite.page import models


def get_page(slug='index', lang='en'):
    try:
        pg = models.PageTranslation.objects.get(slug__iexact=slug, language__iexact=lang)
    except models.PageTranslation.DoesNotExist:
        try:
            pg = models.PageTranslation.objects.get(slug__iexact=slug)
        except models.PageTranslation.DoesNotExist:
            try:
                p = models.Page.objects.get(default_slug__iexact=slug)
            except models.Page.DoesNotExist:
                return False

            try:
                pg = models.PageTranslation.objects.get(page=p.id)
            except models.PageTranslation.DoesNotExist:
                return False

    return(pg)


def index(request):
    return(show(request, 'index'))


def show(request, page_name):
    pg = get_page(page_name, request.LANGUAGE_CODE)
    if (pg):
        ctx = {
            'language': pg.language,
            'title': pg.title_html,
            'heading': pg.heading_html,
            'content': pg.content_html,
        }
        return response.render(request, 'page/show.html', ctx)
    else:
        raise Http404