# Il faut mettre les fichiers dans le sous dossier locale de share...
SUBDIRS = fr zh_TW

EXTRA_DIST = $(srcdir)/*.mo $(srcdir)/*.po

all-local:
	msgfmt default.po -o default.mo
