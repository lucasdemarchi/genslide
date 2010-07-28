#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) 2010 Lucas De Marchi <lucas.de.marchi@gmail.com>
"""

import sys
import os
import urlparse
import codecs
from optparse import OptionParser

from url_opener import URLOpener
from terra_html_parser import TerraHTMLParser
from slide_formatter import SlideFormatter
import sysconfig

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
                              'in the best possible manner.')
    parser.add_option('-r', '--max-rows',
                      action='store', type='int', dest='max_rows',
                      help='Max number of rows per slide. If a verse conttains ' \
                              'more rows than this number, it will be split in ' \
                              'slides.')
    parser.add_option('-o', '--output-dir',
                      action='store', type='string', dest='output_dir',
                      help='Directory in which the generated latex file will be let. ' \
                              'Default is to output to stdout. If a directory is ' \
                              'specified, it will have the same name as input file')
    parser.add_option('-T', '--template-dir',
                      action='store', type='string', dest='template_dir',
                      help='Use TEMPLATE_DIR in as a directory containing templates. ' \
                              'It will be put in precedence to other default '
                              'directories.')
    parser.add_option('-t', '--template',
                      action='store', type='string', dest='template',
                      help='Use TEMPLATE instead of the default one.')
    parser.add_option('-u', '--no-upper',
                      action='store_false', dest='toupper', default=True,
                      help='Do not convert input text to uppercase letters')
    (options, args) = parser.parse_args()
    if len(args) != 1:
        print 'ERROR: you must specify a file or internet address'
        parser.print_help()
        sys.exit(1)

    return options, args

def main(*args):
    (options, args) = parse_options()
    sysconfig.option_parser = options
    sysconfig.initialize()

    addr = args[0]
    parsed_text = []
    addr_parse_result = urlparse.urlparse(addr)
    if find_method(addr_parse_result.scheme) != Schemes.LOCAL:
        html = URLOpener.open(addr)
        parser = find_parser(addr_parse_result.netloc)
        parsed_text = parser.run(html)
    else:
        with codecs.open(addr_parse_result.path, encoding='utf-8', mode='r') as f:
            parsed_text = f.readlines()

    slidefmt = SlideFormatter()
    parsed_text = slidefmt.format(parsed_text)
    if sysconfig.option_parser.output_dir:
        (tmp, outfile) = os.path.split(addr_parse_result.path)
        (outfile, root) = os.path.splitext(outfile)
        outfile += '.tex'
        with codecs.open(os.path.join(sysconfig.option_parser.output_dir,
                  outfile), mode='w', encoding='utf-8') as f:
            f.writelines([l for l in parsed_text])
    else:
        for line in parsed_text:
            print line,

if __name__ == "__main__":
    sys.exit(main(*sys.argv))

