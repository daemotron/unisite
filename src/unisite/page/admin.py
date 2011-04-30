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

from unisite.page import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class PageTranslationInline(admin.StackedInline):
    model = models.PageTranslation
    extra = 1


class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('General'), {'fields': ['name', 'default_slug']}),
        (_('Publishing'), {'fields': ['publish_date']}),
    ]
    inlines = [PageTranslationInline]
    list_display = ('name', 'publish_date')


admin.site.register(models.Page, PageAdmin)