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

import hashlib
import os.path
import time
import cPickle
from django import template
from django.conf import settings
import feedparser

register = template.Library()


def get_feed(parser, token):
    # quoted strings do not get split => good test for a single argument
    bits = token.split_contents()
    if len(bits) != 5:
        raise template.TemplateSyntaxError, "%r tag takes exactely four arguments" % token.contents.split()[0]
    if bits[3] != 'as':
        raise template.TemplateSyntaxError, "%r tag's third argument must be 'as'" % token.contents.split()[0]
    if not (bits[1][0] == bits[1][-1] and bits[1][0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's first argument should be in quotes" % token.contents.split()[0]

    return FeedNode(bits[1][1:-1], bits[2], bits[4])


class FeedNode(template.Node):
    
    def __init__(self, feed_url, refresh, var_name):
        self.feed_url = feed_url
        self.var_name = var_name
        self.refresh = int(refresh)
    
    def render(self, context):
        cache_file = settings.CACHE_DIR
        if cache_file[-1] != '/':
            cache_file += "/"
        cache_file += hashlib.sha1(self.feed_url).hexdigest()
        
        d = None
        if os.path.isfile(cache_file):
            if (int(time.time()) - int(os.path.getmtime(cache_file))) < self.refresh:
                ofile = open(cache_file, 'rb')
                d = cPickle.load(ofile)
                ofile.close()
        
        if d == None:
            d = feedparser.parse(self.feed_url)
            ofile = open(cache_file, 'wb')
            cPickle.dump(d, ofile, -1)
            ofile.close()
         
        context[self.var_name] = d
        return ''
        

register.tag('get_feed', get_feed)