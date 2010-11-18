#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import html.parser

class TerraHTMLParser(html.parser.HTMLParser):
    '''A simple parser for http://letras.terra.com.br'''

    def __init__(self, *args, **kwargs):
        html.parser.HTMLParser.__init__(self)
        self.stack = []
        self.data = []
        self.title = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag.lower() == 'div' and 'id' in attrs and attrs['id'] == 'div_letra':
            self.stack.append(tag)
        elif tag.lower() == 'h1' and 'id' in attrs and attrs['id'] == 'identificador_musica':
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if len(self.stack) > 0 and tag.lower() ==  'div':
            self.stack.pop()
        elif len(self.stack) > 0 and tag.lower() == 'p':
           self.data.append('\n')

    def handle_data(self, data):
        if len(self.stack) > 0 and data.strip() != '':
            tag = self.stack[-1]
            if tag == 'div':
                self.data.append(data.strip() + '\n')
            elif tag == 'h1':
                self.stack.pop()
                self.title = data.strip()
                self.data.insert(0, '\n')
                self.data.insert(0, self.title + '\n')

    def run(self, markup):
        self.feed(markup)
        self.close()
        return self.data

    @classmethod
    def list_netlocs(self):
        return ['letras.terra.com.br']

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
    lines = TerraHTMLParser().run(test_string)
    for line in lines:
        print(line, end=' ')
