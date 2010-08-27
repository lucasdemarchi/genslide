SUBDIRS = genslide data

MAINTAINERCLEANFILES = \
Makefile.in \
aclocal.m4 \
config.guess \
config.h.in \
config.h.in~ \
config.sub \
configure \
depcomp \
install-sh \
ltconfig \
ltmain.sh \
missing \
py-compile

dist_bin_SCRIPTS = genslide-bin

dist-hook:
	rm -rf `find $(distdir) -name '*.am'`
	rm -rf `find $(distdir) -name '*.in'`
	rm -rf `find $(distdir) -name 'configure.ac'`
