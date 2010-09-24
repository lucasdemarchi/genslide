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
    parser.add_option('-d', '--no-line-smart',
                      action='store_false', dest='smart_line', default=True,
                      help='Turn off the smart line wrapping')
    parser.add_option('-e', '--no-verse-smart',
                      action='store_false', dest='smart_verse', default=True,
                      help='Turn off the smart verse wrapping')
    parser.add_option('-o', '--output-dir',
                      action='store', type='string', dest='output_dir',
                      help='Directory in which the generated latex file will be let. ' \
                              'Default is to output to stdout. If a directory is ' \
                              'specified, it will have the same name as input file')
    parser.add_option('-s', '--save-txt',
                      action='store_true', dest='save_txt',
                      help='Save a copy of the text to output dir.')
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

    if not options.output_dir and options.save_txt:
        print 'ERROR: --save-txt options demands that an output directory is given'
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
    outfile = None
    outfiletxt = None
    if find_method(addr_parse_result.scheme) != Schemes.LOCAL:
        html = URLOpener.open(addr)
        parser = find_parser(addr_parse_result.netloc)
        parsed_text = parser.run(html)
        if sysconfig.option_parser.output_dir:
            outfile = parser.title.replace(' ', '-').lower() + '.tex'
            outfiletxt = outfile[0:-4] + '.txt'
    else:
        if sysconfig.option_parser.output_dir:
            (tmp, outfile) = os.path.split(addr_parse_result.path)
            (outfile, root) = os.path.splitext(outfile)
            outfile += '.tex'
        with codecs.open(addr_parse_result.path, encoding='utf-8', mode='r') as f:
            parsed_text = f.readlines()

    slidefmt = SlideFormatter()
    fmt_text = slidefmt.format(parsed_text)
    if outfile:
        with codecs.open(os.path.join(sysconfig.option_parser.output_dir,
                  outfile), mode='w', encoding='utf-8') as f:
            f.writelines([l for l in fmt_text])
    else:
        for line in fmt_text:
            print line,

    if outfiletxt:
        with codecs.open(os.path.join(sysconfig.option_parser.output_dir,
                outfiletxt), mode='w', encoding='utf-8') as f:
            f.writelines([l for l in parsed_text])

if __name__ == "__main__":
    sys.exit(main(*sys.argv))

