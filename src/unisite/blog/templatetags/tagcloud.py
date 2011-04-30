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
from django import template
from django.conf import settings
from unisite.blog import models
from unisite.blog.templatetags.etrans import local__get_tag_trans

register = template.Library()


def t_part(t):
    return t[1].label.lower()


def local__get_tag_cloud(lang):
    tlist = []
    tags = models.Tag.objects.all()
    mcount = 0
    
    for tag in tags:
        tcount = models.Entry.objects.filter(status__exact='p').filter(publish_date__lte=datetime.now()).filter(tags__id=tag.id).distinct().count()
        if tcount > mcount:
            mcount = tcount
        if tcount >= settings.TAGCLOUD_THRESHOLD:
            trans = local__get_tag_trans(tag.id, lang)
            tlist.append([tag, trans, 1, tcount])

    mapdict = {}
    rlist = range(settings.TAGCLOUD_THRESHOLD, mcount + 1)
    
    bsize = int(len(rlist) / settings.TAGCLOUD_STAGES)
    rsize = int(len(rlist) % settings.TAGCLOUD_STAGES)
    start = 0
    
    for i in xrange(1, settings.TAGCLOUD_STAGES + 1, 1):
        if i <= rsize:
            mapdict[i] = rlist[start:start+bsize+1]
            start += (bsize + 1)
        else:
            mapdict[i] = rlist[start:start+bsize]
            start += bsize
        
    for i in tlist:
        for j in xrange(1, settings.TAGCLOUD_STAGES + 1, 1):
            if i[3] in mapdict[j]:
                i[2] = j
                break

    tlist.sort(key=t_part)
    return tlist


def get_tag_cloud(parser, token):
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "%r tag takes exactely two arguments" % token.contents.split()[0]
    if bits[1] != 'as':
        raise template.TemplateSyntaxError, "%r tag's first argument must be 'as'" % token.contents.split()[0]
    
    return CloudNode(bits[2])
    
    
class CloudNode(template.Node):
    
    def __init__(self, var_name):
        self.var_name = var_name
        
    def render(self, context):
        context[self.var_name] = local__get_tag_cloud(context['LANGUAGE_CODE'])
        return ''
    
    
register.tag('get_tag_cloud', get_tag_cloud)