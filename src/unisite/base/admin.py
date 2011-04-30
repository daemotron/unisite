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

from unisite.base import models
from django.contrib import admin

class NavElementTranslationInline(admin.TabularInline):
    model = models.NavElementTranslation
    extra = 3

class NavElementInline(admin.StackedInline):
    model = models.NavElement
    extra = 1

class NavElementAdmin(admin.ModelAdmin):
    inlines = [NavElementTranslationInline]

class NavigationAdmin(admin.ModelAdmin):
    inlines = [NavElementInline]

admin.site.register(models.Navigation, NavigationAdmin)
admin.site.register(models.NavElement, NavElementAdmin)
