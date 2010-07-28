#!/bin/sh

aclocal
autoconf
automake --add-missing --foreign

if [ -z "$NOCONFIGURE" ]; then
	./configure "$@"
fi
