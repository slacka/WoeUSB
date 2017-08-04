# Il faut mettre les fichiers dans le sous dossier locale/fr/LC_MESSAGES de share...
pkgdatadir=$(mypkgdatadir)/locale/fr/LC_MESSAGES

%.mo: %.po
	msgfmt -o $@ $<

dist_pkgdata_DATA = \
	$(srcdir)/woeusb.mo\
	$(srcdir)/wxstd.mo
