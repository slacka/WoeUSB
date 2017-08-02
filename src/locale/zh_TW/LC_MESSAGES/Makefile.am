# Il faut mettre les fichiers dans le sous dossier locale/zh_TW/LC_MESSAGES de share...
pkgdatadir=$(mypkgdatadir)/locale/zh_TW/LC_MESSAGES

EXTRA_DIST = $(srcdir)/*.po

all-local:
	msgfmt trad.po -o trad.mo
#	msgfmt wxstd.po -o wxstd.mo
