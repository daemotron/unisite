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

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from unisite.util.rst import render
from unisite.util.rst import ent_replace 

#from my_universe.base.models import Language

# The page class represents a pseudo-static page
class Page(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('page name'), unique=True)
    default_slug = models.SlugField(max_length=64, verbose_name=_('page default slug'))
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(verbose_name=_('publishing date'))

    def __unicode__(self):
        return self.name


class PageTranslation(models.Model):
    page = models.ForeignKey(Page, verbose_name=_('page'))
    language = models.CharField(max_length=2, choices=settings.LANGUAGES, verbose_name=_('language'))
    slug = models.SlugField(max_length=64, verbose_name=_('page slug (URL)'))
    title = models.CharField(max_length=200, verbose_name=_('page title'))
    heading = models.CharField(max_length=200, verbose_name=_('page heading'))
    content = models.TextField(verbose_name=_('page content (reStructuredText)'))
    author = models.ForeignKey(User, verbose_name=_('author\'s name'))
    content_html = models.TextField(editable=False, blank=True)
    title_html = models.CharField(max_length=255, editable=False, blank=True)
    heading_html = models.CharField(max_length=255, editable=False, blank=True)

    class Meta:
        unique_together = ("language", "slug")
        
    def save(self, *args, **kwargs):
        self.content_html = render(self.content, self.language)
        self.title_html = ent_replace(self.title, self.language)
        self.heading_html = ent_replace(self.heading, self.language)
        super(PageTranslation, self).save(*args, **kwargs)