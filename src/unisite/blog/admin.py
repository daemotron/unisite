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

from unisite.blog import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class EntryTranslationInline(admin.StackedInline):
    model = models.EntryTranslation
    prepopulated_fields = {'slug': ('heading',)}
    extra = 1
#    fieldsets = [
#        (_('general'), {
#            'fields': ('language', 'author')
#        }),
#        (_('header settings'), {
#            'fields': ('title', 'slug')
#        }),
#        (_('content'), {
#            'fields': ('heading', 'basic_content')
#        }),
#        (_('extended content'), {
#            'classes': ('collapse',),
#            'fields': ('extended_content')
#        }),
#    ]

def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = _('Mark selected entries as published')

def make_withdrawn(modeladmin, request, queryset):
    queryset.update(status='w')
make_withdrawn.short_description = _('Mark selected entries as withdrawn')

class EntryAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('General'), {'fields': ['name', 'default_slug']}),
        (_('Publishing'), {'fields': ['status', 'publish_date']}),
        (_('Meta information'), {'fields': ['tags']}),
    ]
    prepopulated_fields = {'default_slug': ('name',)}
    inlines = [EntryTranslationInline]
    date_hierarchy = 'publish_date'
    list_display = ('name', 'publish_date', 'is_published')
    ordering = ('-publish_date',)
    list_per_page = 25
    filter_horizontal = ('tags',)
    
    def is_published(self, obj):
        if obj.status == 'p':
            return True
        else:
            return False
        
    is_published.short_description = _('Published')
    is_published.boolean = True
    
    actions = [make_published, make_withdrawn]


class TagTranslationInline(admin.TabularInline):
    model = models.TagTranslation
    extra = 3


class TagAdmin(admin.ModelAdmin):
    inlines = [TagTranslationInline]
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(models.Entry, EntryAdmin)
admin.site.register(models.Tag, TagAdmin)
#admin.site.register(models.Comment)