#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
	echo "Usage : installDll.sh prefix host" >&2
	exit 1
fi

# Config
	# Le script quitte en cas d'erreur d'une commande
set -o errexit

	# Le script quitte en cas de variables non déclarée
set -o nounset

prefix=$1
host=$2

libPath=""

# build target
dirList=("$host" 'i586-mingw32msvc')
for value in ${dirList[*]}; do # Ubuntu
	if [ -d "/usr/$value/lib" ]; then
		libPath="/usr/$value/lib"
		break
	fi
done

if [ -n "$libPath" ]; then
	## Mingw dll
	if [ -f "/usr/share/doc/mingw32-runtime/mingwm10.dll.gz" ]; then
		gunzip -dc "/usr/share/doc/mingw32-runtime/mingwm10.dll.gz" > "$prefix/mingwm10.dll";
	fi

	cp "$libPath/libgcc_s_dw2-1.dll" "$prefix"
else
	echo "Error: libPath not found !" >&2
	exit 1
fi

exit 0
