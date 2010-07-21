#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) 2010 Lucas De Marchi <lucas.de.marchi@gmail.com>
"""

import sys
import urlparse
from optparse import OptionParser

from URLOpener import URLOpener
from TerraHTMLParser import TerraHTMLParser
from SlideFormatter import SlideFormatter

def find_parser(netloc):
    netlocs = []

    # put all parsers here
    netlocs.extend(TerraHTMLParser.list_netlocs())

    # FIXME: iterate trough parsers and find right parser
    return TerraHTMLParser()

def main(*args):
    usage = "%prog [options] address"
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    if len(args) != 1:
        raise Exception('Wrong number of args')
    addr = args[0]

    html = URLOpener.open(addr)

    url_parse_result = urlparse.urlparse(addr)
    parser = find_parser(url_parse_result.netloc)
    parsed_text = parser.run(html)

    slidefmt = SlideFormatter('/tmp/', '/tmp/')
    parsed_text = slidefmt.format(parsed_text)
    for line in parsed_text:
        print line.encode('utf-8'),

if __name__ == "__main__":
    sys.exit(main(*sys.argv))

