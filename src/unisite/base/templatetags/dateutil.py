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
from datetime import datetime

register = template.Library()

def get_datetime(parser, token):
    bits = token.split_contents()
    if len(bits) != 6 and len(bits) != 9:
        raise template.TemplateSyntaxError, "%r tag takes exactely six or nine arguments" % token.contents.split()[0]
    if bits[4] != 'as' and bits[7] != 'as':
        raise template.TemplateSyntaxError, "%r tag's fifth resp. eighth argument must be 'as'" % token.contents.split()[0]
    
    if len(bits) == 6:
        return DateNode(bits[5], bits[1], bits[2], bits[3])
    else:
        return DateNode(bits[8], bits[1], bits[2], bits[3], bits[4], bits[5], bits[6])


class DateNode(template.Node):
    
    def __init__(self, var_name, year, month, day, hour=0, minute=0, second=0):
        self.var_name = var_name
        self.year = template.Variable(year)
        self.month = template.Variable(month)
        self.day = template.Variable(day)
        self.hour = template.Variable(hour)
        self.minute = template.Variable(minute)
        self.second = template.Variable(second)
        
    def render(self, context):
        year = int(self.year.resolve(context))
        month = int(self.month.resolve(context))
        day = int(self.day.resolve(context))
        hour = int(self.hour.resolve(context))
        minute = int(self.minute.resolve(context))
        second = int(self.second.resolve(context))
        try:
            if int(hour) == 0 or int(minute) == 0 or int(second) == 0:
                self.date = datetime(int(year), int(month), int(day))
            else:
                self.date = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        except ValueError:
            self.date = None

        context[self.var_name] = self.date
        return ''
    
    
register.tag('get_datetime', get_datetime)