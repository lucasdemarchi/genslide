#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) 2010 Lucas De Marchi <lucas.de.marchi@gmail.com>
"""

import sys
import os
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
            'file': Schemes.LOCAL,
            'http': Schemes.EXTERN,
            'ftp': Schemes.EXTERN,
            'https': Schemes.EXTERN
            }
    ret = schemes.get(scheme, Schemes.UNKNOWN)
    if ret == Schemes.UNKNOWN:
        raise Exception("Unknown address")

    return ret

def parse_options():
    usage = "%prog [options] <address|file>"
    parser = OptionParser(usage=usage)
    parser.add_option('-c', '--max-cols',
                      action='store', type='int', dest='max_cols',
                      help='Max number of cols per slide. If a certain row ' \
                              'is larger than this number, it will be split ' \
                              'in the best possible manner. [NOT IMPLEMENTED YET]')
    parser.add_option('-r', '--max-rows',
                      action='store', type='int', dest='max_rows',
                      help='Max number of rows per slide. If a verse conttains ' \
                              'more rows than this number, it will be split in ' \
                              'slides. [NOT IMPLEMENTED YET]')
    parser.add_option('-o', '--output-dir',
                      action='store', type='string', dest='output_dir', default=os.getcwd(),
                      help='Directory in which the generated pdf or latex file will be let. ' \
                              'Default is the current working directory. [ NOT USED YET]')
    parser.add_option('-l', '--latex',
                      action='store_true', dest='let_latex', default=False,
                      help='Let the generated latex file on output directory. ' \
                              '[NOT USED YET]')
    parser.add_option('-L', '--latex-only',
                      action='store_true',  dest='let_latex_only', default=False,
                      help='Do not generate the pdf file, let only the latex file' \
                              'on output directory. [NOT USED YET]')
    parser.add_option('-T', '--template-dir',
                      action='store', type='string', dest='template_dir',
                      help='Use TEMPLATE_DIR in as a directory containing templates. ' \
                              'It will be put in precedence to other default directories. ' \
                              '[NOT USED YET]')
    parser.add_option('-t', '--template',
                      action='store', type='string', dest='template',
                      help='Use TEMPLATE instead of the default one. [NOT USED YET]')
    (options, args) = parser.parse_args()
    if len(args) != 1:
        print 'ERROR: you must specify a file or internet address'
        parser.print_help()
        sys.exit(1)

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
        with open(addr_parse_result.path, 'r') as f:
            parsed_text = f.readlines()

    slidefmt = SlideFormatter('/tmp/', '/tmp/')
    parsed_text = slidefmt.format(parsed_text)
    for line in parsed_text:
        print line.encode('utf-8'),

if __name__ == "__main__":
    sys.exit(main(*sys.argv))

