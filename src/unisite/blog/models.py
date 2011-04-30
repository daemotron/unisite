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

stats = (
    ('d', _('Draft')),
    ('p', _('Published')),
    ('w', _('Withdrawn')),
)

class Tag(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('tag name'))
    slug = models.SlugField(max_length=64, verbose_name=_('tag slug'))

    def __unicode__(self):
        return self.name

    # This method makes it possible to use generic views with Entry objects
    def get_translation(self, lang=settings.LANGUAGE_CODE):
        try:
            tt = TagTranslation.objects.get(tag=self, language__iexact=lang)
        except TagTranslation.DoesNotExist:
            try:
                tt = TagTranslation.objects.get(tag=self, language__iexact=settings.LANGUAGE_CODE)
            except TagTranslation.DoesNotExist:
                try:
                    tt = TagTranslation.objects.filter(tag=self)[0]
                except TagTranslation.DoesNotExist:
                    return None
            
        return tt
    
    class Meta:
        verbose_name=_('tag')
        verbose_name_plural=_('tags')
        ordering = ['name']


class TagTranslation(models.Model):
    tag = models.ForeignKey(Tag, verbose_name=_('tag translation'))
    language = models.CharField(max_length=2, choices=settings.LANGUAGES, verbose_name=_('language'))
    label = models.CharField(max_length=64, verbose_name=_('translated tag label'))

    def __unicode__(self):
        return self.label

    class Meta:
        unique_together = ("tag", "language")
        verbose_name=_('tag translation')
        verbose_name_plural=_('tag translations')
        

class Entry(models.Model):
    '''
    An entry in the weblog.
    
    This is only the head of an entry, the actual content is stored
    in related EntryTranslation objects. However, an Entry object can
    return the fitting translation if kindly asked indicating the 
    desired language.
    '''
    
    # Field definitions
    name = models.CharField(max_length=200, verbose_name=_('entry name'), unique=True)
    default_slug = models.SlugField(max_length=64, verbose_name=_('entry default slug'))
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(verbose_name=_('publishing date'))
    status = models.CharField(max_length=2, choices=stats, verbose_name=_('status'))
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), blank=True)

    def __unicode__(self):
        return self.name

    # This method makes it possible to use generic views with Entry objects
    def get_translation(self, lang=settings.LANGUAGE_CODE):
        try:
            et = EntryTranslation.objects.get(entry=self, language__iexact=lang)
        except EntryTranslation.DoesNotExist:
            try:
                et = EntryTranslation.objects.get(entry=self, language__iexact=settings.LANGUAGE_CODE)
            except EntryTranslation.DoesNotExist:
                try:
                    et = EntryTranslation.objects.filter(entry=self)[0]
                except EntryTranslation.DoesNotExist:
                    return None
            
        return et
    
    class Meta:
        verbose_name=_('entry')
        verbose_name_plural=_('entries')


class EntryTranslation(models.Model):
    entry = models.ForeignKey(Entry, verbose_name=_('entry'))
    language = models.CharField(max_length=2, choices=settings.LANGUAGES, verbose_name=_('language'))
    author = models.ForeignKey(User, verbose_name=_('author\'s name'))
    slug = models.SlugField(max_length=64, verbose_name=_('entry slug (URL)'))
    title = models.CharField(max_length=200, verbose_name=_('entry title'))
    heading = models.CharField(max_length=200, verbose_name=_('entry heading'))
    basic_content = models.TextField(verbose_name=_('basic entry content (reStructuredText)'))
    extended_content = models.TextField(verbose_name=_('extended entry content (reStructuredText)'), blank=True, null=True)
    title_html = models.CharField(max_length=255, editable=False, blank=True)
    heading_html = models.CharField(max_length=255, editable=False, blank=True)
    basic_content_html = models.TextField(editable=False, blank=True)
    extended_content_html = models.TextField(editable=False, blank=True, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.entry.name, self.language)
    
    def save(self, *args, **kwargs):
        if self.extended_content:
            self.extended_content_html = render(self.extended_content, self.language)
        self.basic_content_html = render(self.basic_content, self.language)
        self.title_html = ent_replace(self.title, self.language)
        self.heading_html = ent_replace(self.heading, self.language)
        super(EntryTranslation, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("language", "slug")
        verbose_name=_('entry translation')
        verbose_name_plural=_('entry translations')


#class Comment(models.Model):
#    entry = models.ForeignKey(Entry, verbose_name=_('entry'))
#    author = models.CharField(max_length=64, verbose_name=_('author\'s name'))
#    email = models.EmailField(max_length=100, verbose_name=('author\'s email address'))
#    ip = models.IPAddressField(verbose_name=_('author\'s ip address'))
#    parent = models.ForeignKey('self', blank=True, verbose_name=_('comment replies to'))
#    content = models.TextField(verbose_name=_('comment body'))
#    content_html = models.TextField(editable=False, blank=True)
#    create_date = models.DateTimeField(auto_now_add=True)
#    
#    class Meta:
#        verbose_name=_('comment')
#        verbose_name_plural=_('comments')