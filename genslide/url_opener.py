#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request, urllib.parse, urllib.error
import sys

class URLOpener:
    def __init__(self):
        pass

    @classmethod
    def open(self, url):
        sock = urllib.request.urlopen(url)
        html_source = sock.read()
        sock.close()
        return str(html_source, 'iso8859-1')


def main(*args):
    print("%s" % (URLOpener.open('http://letras.terra.com.br/harpa-crista/357602/')))

if __name__ == "__main__":
    sys.exit(main(*sys.argv))
