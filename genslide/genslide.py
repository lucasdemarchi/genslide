#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) 2010 Lucas De Marchi <lucas.de.marchi@gmail.com>
"""

import sys
import urlparse
from optparse import OptionParser

from url_opener import URLOpener
from terra_html_parser import TerraHTMLParser
from slide_formatter import SlideFormatter

def find_parser(netloc):
    netlocs = []

    # put all parsers here
    netlocs.extend(TerraHTMLParser.list_netlocs())

    # FIXME: iterate trough parsers and find right parser
    return TerraHTMLParser()

class Schemes:
    LOCAL = 0
    EXTERN = 1
    UNKNOWN = 2

def find_method(scheme):
    schemes = {
            '': Schemes.LOCAL,
            'http': Schemes.EXTERN,
            'ftp': Schemes.EXTERN,
            'https': Schemes.EXTERN
            }
    ret = schemes.get(scheme, Schemes.UNKNOWN)
    if ret == Schemes.UNKNOWN:
        raise Exception("Unknown address")

    return ret

def parse_options():
    usage = "%prog [options] address"
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    if len(args) != 1:
        raise Exception('Wrong number of args')
    return options, args

def main(*args):
    (options, args) = parse_options()
    addr = args[0]
    parsed_text = []
    addr_parse_result = urlparse.urlparse(addr)
    if find_method(addr_parse_result.scheme) != Schemes.LOCAL:
        html = URLOpener.open(addr)
        parser = find_parser(addr_parse_result.netloc)
        parsed_text = parser.run(html)
    else:
        with open(addr, 'r') as f:
            parsed_text = f.readlines()

    slidefmt = SlideFormatter('/tmp/', '/tmp/')
    parsed_text = slidefmt.format(parsed_text)
    for line in parsed_text:
        print line.encode('utf-8'),

if __name__ == "__main__":
    sys.exit(main(*sys.argv))

