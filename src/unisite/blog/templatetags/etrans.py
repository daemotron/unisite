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

from django import template
from unisite.blog import models

register = template.Library()


def local__get_entry_trans(entry_id, lang):
    ent = models.Entry.objects.get(id=entry_id)
    return ent.get_translation(lang)


def local__get_tag_trans(tag_id, lang):
    tg = models.Tag.objects.get(id=tag_id)
    return tg.get_translation(lang)


def get_entry_trans(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError, "%r tag takes exactely three arguments" % token.contents.split()[0]
    if bits[2] != 'as':
        raise template.TemplateSyntaxError, "%r tag's third argument must be 'as'" % token.contents.split()[0]

    return EntryNode(bits[1], bits[3])


def get_tag_trans(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError, "%r tag takes exactely three arguments" % token.contents.split()[0]
    if bits[2] != 'as':
        raise template.TemplateSyntaxError, "%r tag's third argument must be 'as'" % token.contents.split()[0]

    return TagNode(bits[1], bits[3])


class EntryNode(template.Node):
    def __init__(self, entry_id, var_name):
        self.entry_id = template.Variable(entry_id)
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = local__get_entry_trans(self.entry_id.resolve(context), context['LANGUAGE_CODE'])
        return ''


class TagNode(template.Node):
    def __init__(self, tag_id, var_name):
        self.tag_id = template.Variable(tag_id)
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = local__get_tag_trans(self.tag_id.resolve(context), context['LANGUAGE_CODE'])
        return ''    
    
    
register.tag('get_entry_trans', get_entry_trans)
register.tag('get_tag_trans', get_tag_trans)