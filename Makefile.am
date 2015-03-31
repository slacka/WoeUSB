AUTOMAKE_OPTIONS = gnu

SUBDIRS = src innoSetup debian

# M4
ACLOCAL_AMFLAGS = -I m4

## Pour fichier COPYING
pkgdocdir=$(prefix)

if IS_MINGW
pkgdoc_DATA = $(srcdir)/COPYING
endif

EXTRA_DIST = $(srcdir)/os
