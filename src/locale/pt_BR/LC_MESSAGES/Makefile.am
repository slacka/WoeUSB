pkgdatadir=$(mypkgdatadir)/locale/pt_BR/LC_MESSAGES

%.mo: %.po
	msgfmt -o $@ $<

dist_pkgdata_DATA = $(srcdir)/woeusb.mo
