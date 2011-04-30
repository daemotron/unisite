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
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

link_types = (
    ('unisite.page.views.show', _('Page')),
    ('unisite.blog.views.entry_list', _('Blog')),
)

class Navigation(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'), unique=True)

    def __unicode__(self):
        return self.name


class NavElement(models.Model):
    navigation = models.ForeignKey(Navigation, verbose_name=_('Navigation'))
    position = models.PositiveIntegerField(verbose_name=_('Position'))
    default_target_object = models.CharField(max_length=200, choices=link_types, verbose_name=_('Default Link Target Object Type'))
    default_target_name = models.CharField(max_length=200, blank=True, verbose_name=_('Default Link Target Object Identifier'))
    default_name = models.CharField(max_length=20, verbose_name=_('Default Name'))
    default_regex = models.CharField(max_length=255, verbose_name=_('Default "Is Active" Pattern'))

    def get_id(self):
        return self.default_name.lower()

    def __unicode__(self):
        return self.default_name


class NavElementTranslation(models.Model):
    navelement = models.ForeignKey(NavElement, verbose_name=_('Navigation Element'))
    language = models.CharField(max_length=2, choices=settings.LANGUAGES, verbose_name=_('Language'))
    name = models.CharField(max_length=20, verbose_name=_('Name'))
    target_object = models.CharField(max_length=200, choices=link_types, verbose_name=_('Link Target Object Type'))
    target_name = models.CharField(max_length=200, verbose_name=_('Link Target Object Identifier'))
    regex = models.CharField(max_length=255, verbose_name=_('"Is Active" Pattern'))

    def get_id(self):
        return self.name.lower()

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ("language", "navelement")