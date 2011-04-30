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
from django.core.urlresolvers import reverse, NoReverseMatch
from unisite.base import models
import re


register = template.Library()


def get_nav_dict(nav, lang, url):
    nv = []
    td = {}
    aflag = False

    try:
        N = models.Navigation.objects.get(name__iexact = nav)
    except models.Navigation.DoesNotExist:
        return []

    try:
        elements = models.NavElement.objects.order_by('position').filter(navigation=N.id)
    except models.NavElement.DoesNotExist:
        return []

    for elem in elements:
        try:
            trans = models.NavElementTranslation.objects.get(navelement=elem.id, language__iexact=lang)
            td = {
                'id': trans.get_id(),
                'name': trans.name,
                'view': trans.target_object,
                'param': trans.target_name,
                'pattern': trans.regex
            }
        except models.NavElementTranslation.DoesNotExist:
            td = {
                'id': elem.get_id(),
                'name': elem.default_name,
                'view': elem.default_target_object,
                'param': elem.default_target_name,
                'pattern': elem.default_regex
            }

        try:
            if td['param'] == "":
                td['link'] = reverse(td['view'],)
            else:
                td['link'] = reverse(td['view'], args=(td['param'],))
        except NoReverseMatch:
            td['link'] = ''

        if (aflag == False):
            if (re.match(td['pattern'], url) != None):
                td['active'] = True
                aflag = True
            else:
                td['active'] = False
        else:
            td['active'] = False

        nv.append(td)
        td = {}

    return nv

def get_nav(parser, token):
    # quoted strings do not get split => good test for a single argument
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError, "%r tag takes exactely three arguments" % token.contents.split()[0]
    if bits[2] != 'as':
        raise template.TemplateSyntaxError, "%r tag's second argument must be 'as'" % token.contents.split()[0]
    if not (bits[1][0] == bits[1][-1] and bits[1][0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's first argument should be in quotes" % token.contents.split()[0]

    return NavNode(bits[1][1:-1], bits[3])


class NavNode(template.Node):
    def __init__(self, nav_name, var_name):
        self.nav_name = nav_name
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = get_nav_dict(self.nav_name, context['LANGUAGE_CODE'], context['request'].path)
        return ''


register.tag('get_nav', get_nav)