import re
from itertools import product
from django.conf import settings

INLINESTYLES = False

from pygments.formatters import HtmlFormatter

# The default formatter
DEFAULT = HtmlFormatter(noclasses=INLINESTYLES)

# Add name -> formatter pairs for every variant you want to use
VARIANTS = {
    # 'linenos': HtmlFormatter(noclasses=INLINESTYLES, linenos=True),
}

from docutils import nodes
from docutils.parsers.rst import directives, Directive
from docutils.core import publish_parts
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer

class Pygments(Directive):
    """ Source code syntax hightlighting.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = dict([(key, directives.flag) for key in VARIANTS])
    has_content = True

    def run(self):
        self.assert_has_content()
        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = TextLexer()

        # take an arbitrary option if more than one is given
        formatter = self.options and VARIANTS[self.options.keys()[0]] or DEFAULT
        parsed = highlight(u'\n'.join(self.content), lexer, formatter)
        return [nodes.raw('', parsed, format='html')]

directives.register_directive('sourcecode', Pygments)


def ent_replace(html_input, lang=''):
    REPLACE = (
        ('--'     ,    '&ndash;'                        , '(> ', ')< '),
        ('---'    ,    '&mdash;'                        , '(> ', ')< '),
        ('(c)'    ,    '&copy;'                         , '(> ', ')< '),
        ('(r)'    ,    '&reg;'                          , '(> ', ')< '),
        ('(tm)'   ,    '&trade;'                        , ''   , ')< '),
        ('...'    ,    '&hellip;'                       , ''   , ''   ),
        ('1/2'    ,    '&frac12;'                       , '(> ', ')< '),
        ('1/4'    ,    '&frac14;'                       , '(> ', ')< '),
        ('3/4'    ,    '&frac34;'                       , '(> ', ')< '),
        ('1/3'    ,    '&#8531;'                        , '(> ', ')< '),
        ('2/3'    ,    '&#8532;'                        , '(> ', ')< '),
        ('1/5'    ,    '&#8533;'                        , '(> ', ')< '),
        ('2/5'    ,    '&#8534;'                        , '(> ', ')< '),
        ('3/5'    ,    '&#8535;'                        , '(> ', ')< '),
        ('4/5'    ,    '&#8536;'                        , '(> ', ')< '),
        ('1/6'    ,    '&#8537;'                        , '(> ', ')< '),
        ('5/6'    ,    '&#8538;'                        , '(> ', ')< '),
        ('1/7'    ,    '&#8528;'                        , '(> ', ')< '),
        ('1/8'    ,    '&#8539;'                        , '(> ', ')< '),
        ('3/8'    ,    '&#8540;'                        , '(> ', ')< '),
        ('5/8'    ,    '&#8541;'                        , '(> ', ')< '),
        ('7/8'    ,    '&#8542;'                        , '(> ', ')< '),
        ('1/9'    ,    '&#8529;'                        , '(> ', ')< '),
        ('1/10'   ,    '&#8530;'                        , '(> ', ')< '),
        ('-&gt;'  ,    '&rarr;'                         , '(> ', ')< '),
        ('=&gt;'  ,    '&rArr;'                         , '(> ', ')< '),
        ('&lt;-'  ,    '&larr;'                         , '(> ', ')< '),
        ('&lt;='  ,    '&lArr;'                         , '(> ', ')< '),
        ('>:-)'   ,    "<img src=\"%simages/emoticons/devil.png\" alt=\">:-)\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,  '(> ', ')<.,:;?! '),
        (':-]'    ,    "<img src=\"%simages/emoticons/smile3.png\" alt=\":-]\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,  '(> ', ')<.,:;?! '),
        (':-)'    ,    "<img src=\"%simages/emoticons/smile.png\" alt=\":-)\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,   '(> ', ')<.,:;?! '),
        (';-)'    ,    "<img src=\"%simages/emoticons/smile4.png\" alt=\";-)\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,  '(> ', ')<.,:;?! '),
        ('8-)'    ,    "<img src=\"%simages/emoticons/smile2.png\" alt=\"8-)\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,  '(> ', ')<.,:;?! '),
        (':-P'    ,    "<img src=\"%simages/emoticons/tongue.png\" alt=\":-P\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,  '(> ', ')<.,:;?! '),
        (':\'('   ,    "<img src=\"%simages/emoticons/frown.png\" alt=\":'(\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,   '(> ', ')<.,:;?! '),
        (':-('    ,    "<img src=\"%simages/emoticons/sad.png\" alt=\":-(\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,     '(> ', ')<.,:;?! '),
        (':-/'    ,    "<img src=\"%simages/emoticons/ohwell.png\" alt=\":-/\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,  '(> ', ')<.,:;?! '),
        (':-O'    ,    "<img src=\"%simages/emoticons/redface.png\" alt=\":-O\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH, '(> ', ')<.,:;?! '),
        (':-D'    ,    "<img src=\"%simages/emoticons/biggrin.png\" alt=\":-D\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH, '(> ', ')<.,:;?! '),
        ('X-('    ,    "<img src=\"%simages/emoticons/angry.png\" alt=\"X-(\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,   '(> ', ')<.,:;?! '),
        ('|-)'    ,    "<img src=\"%simages/emoticons/tired.png\" alt=\"|-)\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,   '(> ', ')<.,:;?! '),
        ('{i}'    ,    "<img src=\"%simages/emoticons/info.png\" alt=\"info\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,   '(> ', ')<.,:;?! '),
        ('(!)'    ,    "<img src=\"%simages/emoticons/idea.png\" alt=\"idea\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,   '(> ', ')<.,:;?! '),
        ('{ok}'   ,    "<img src=\"%simages/emoticons/thumbs-up.png\" alt=\"thumbs up\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH, '(> ', ')<.,:;?! '),
        ('{x}'    ,    "<img src=\"%simages/emoticons/error.png\" alt=\"error\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,         '(> ', ')<.,:;?! '),
        ('{*}'    ,    "<img src=\"%simages/emoticons/star_on.png\" alt=\"star (on)\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,   '(> ', ')<.,:;?! '),
        ('{o}'    ,    "<img src=\"%simages/emoticons/star_off.png\" alt=\"star (off)\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH, '(> ', ')<.,:;?! '),
        ('/!\\'   ,    "<img src=\"%simages/emoticons/alert.png\" alt=\"alert\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH,         '(> ', ')<.,:;?! '),
        ('(./)'   ,    "<img src=\"%simages/emoticons/checkmark.png\" alt=\"checkmark\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH, '(> ', ')<.,:;?! '),
        ('&lt;!&gt;',  "<img src=\"%simages/emoticons/attention.png\" alt=\"attention\" style=\"display: inline; vertical-align: bottom;\" />" % settings.ASSETS_PATH, '(> ', ')<.,:;?! '),
    )


    RDICT = {}

    for (key, value, left, right) in REPLACE:
        if (left == '' and right == ''):
            RDICT[re.escape(key)] = value
            
        elif (left == '' and right != ''):
            for r in right:
                RDICT[re.escape(key + r)] = value + r
            RDICT[re.escape(key)+'$'] = value
            
        elif (left != '' and right == ''):
            for l in left:
                RDICT[re.escape(l + key)] = l + value
            RDICT['^'+re.escape(key)] = value
            
        else:
            for (l, r) in product(left, right):
                RDICT[re.escape(l + key + r)] = l + value + r
            for l in left:
                RDICT[re.escape(l + key)+'$'] = l + value
            for r in right:
                RDICT['^'+re.escape(key + r)] = value + r
                
        RDICT['^'+re.escape(key)+'$'] = value
    
    
    def replacer(m):
        try:
            return RDICT[re.escape(m.group(0))]
        except KeyError:
            try:
                return RDICT[re.escape(m.group(0))+'$']
            except KeyError:
                try:
                    return RDICT['^'+re.escape(m.group(0))]
                except KeyError:
                    try:
                        return RDICT['^'+re.escape(m.group(0))+'$']
                    except KeyError:
                        return ''

    rg = re.compile('|'.join(RDICT.keys()))
    content = rg.sub(replacer, html_input)
    content = rg.sub(replacer, content)     # second run is necessary to catch those cases where two replacements are located next to each other


    content = re.sub(r'(\d+)x(\d+)', "\g<1>&times;\g<2>", content)

    if (lang == 'de'):
        content = re.sub(r'&quot;(.*?)&quot;', "&bdquo;\g<1>&ldquo;", content)
    elif (lang == 'fr'):
        content = re.sub(r'&quot;(.*?)&quot;', "&laquo;\g<1>&raquo;", content)
    else:
        content = re.sub(r'&quot;(.*?)&quot;', "&ldquo;\g<1>&rdquo;", content)

    return content


def purify(tag):
    return re.sub(r' align\S+', '', tag)


def render(rst_input, lang=''):
    parts = publish_parts(source=rst_input, writer_name='html')
    content = ''

    # isolate code rendering parts
    frags = parts['fragment'].split('<pre>')
    
    # only work on text not being part of HTML tags
    subparts = re.split('(<.*?>)', frags.pop(0))
    for subsnatch in subparts:
        if len(subsnatch) > 0 and subsnatch[0] != '<':
            content += ent_replace(subsnatch, lang)
        else:
            content += purify(subsnatch)

    for snatch in frags:
        content += "<pre>"
        content += snatch.split('</pre>')[0]
        content += "</pre>"
        subparts = re.split('(<.*?>)', snatch.split('</pre>')[1])
        for subsnatch in subparts:
            if len(subsnatch) > 0 and subsnatch[0] != '<':
                content += ent_replace(subsnatch, lang)
            else:
                content += purify(subsnatch)
        
    #downsize headings
    for i in [5, 4, 3, 2, 1]:
        content = content.replace("<h%d>" % i, "<h%d>" % (i+1))
        content = content.replace("</h%d>" % i, "</h%d>" % (i+1))

    return content