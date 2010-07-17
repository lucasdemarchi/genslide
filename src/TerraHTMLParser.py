#!/usr/bin/env python
# -*- coding: utf-8 -*-

import HTMLParser

class TerraHTMLParser(HTMLParser.HTMLParser):
    '''A simple parser for http://letras.terra.com.br'''

    def __init__(self, *args, **kwargs):
        HTMLParser.HTMLParser.__init__(self)
        self.stack = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag.lower() == 'div' and attrs.has_key('id') and attrs['id'] == 'div_letra':
            self.stack.append(tag)
        elif len(self.stack) > 0 and tag.lower() == 'br':
            print "",

    def handle_startendtag(self, tag, attrs):
        if tag.lower() == 'br':
            print "",

    def handle_endtag(self, tag):
        if len(self.stack) > 0 and tag.lower() == "div":
            self.stack.pop()
        elif len(self.stack) > 0 and tag.lower() == 'p':
           print "\n",

    def handle_data(self, data):
        if len(self.stack) > 0:
            print data.upper(),

    @classmethod
    def run(cls, markup):
        _p = cls()
        _p.feed(markup)
        _p.close()

if __name__ == "__main__":
    test_string = '''
<body>
<p>this is another test</p>
<div id>acsd cas cas <p>acisdcisacs</p></div>
<div id="div_letra" ><p>Oh! Por que duvidar sobre as ondas do mar<br/>
Quando Cristo caminho abriu<br/>
Quando forçado és contra as ondas lutar<br/>
</div>
</body>
'''
    TerraHTMLParser.run(test_string)
