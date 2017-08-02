# Il faut mettre les fichiers dans le sous dossier locale/zh_TW/LC_MESSAGES de share...
pkgdatadir=$(mypkgdatadir)/locale/zh_TW/LC_MESSAGES
dist_pkgdata_DATA = $(srcdir)/trad.mo
EXTRA_DIST = $(srcdir)/*.po

# Lin-Buo-Ren: FIXME: This line is made to prevent the following make failure:
# make[6]: Entering directory '/src/locale/zh_TW/LC_MESSAGES'
# make[6]: *** No rule to make target 'trad.mo', needed by 'all-am'.  Stop.
trad.mo: all-local

all-local:
	msgfmt trad.po -o trad.mo
#	msgfmt wxstd.po -o wxstd.mo
