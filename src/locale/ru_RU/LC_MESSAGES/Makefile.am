# Il faut mettre les fichiers dans le sous dossier locale/zh_TW/LC_MESSAGES de share...
pkgdatadir=$(mypkgdatadir)/locale/zh_TW/LC_MESSAGES

%.mo: %.po
	msgfmt -o $@ $<

dist_pkgdata_DATA = $(srcdir)/woeusb.mo
