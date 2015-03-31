dnl ---------------------------------------------------------------------------
dnl MY_FIND_SFML()
dnl Find SFML lib
dnl ---------------------------------------------------------------------------

AC_DEFUN([MY_FIND_SFML],
[
	dnl OpenGL header
	AM_CHECK_LIB_HEADER([GL], [gl], [GL/gl.h], [], [], AC_MSG_ERROR([	/!\ This programme requires OpenGL headers !]))

	dnl SFML
	if test "$IS_MAC" = 'true'; then
		CHECK_FRAMEWORK_LIST([SFML], [SFML sfml-graphics sfml-window sfml-system sfml-audio])
	else
		AM_CHECK_LIB_HEADER([SFML], [sfml], [SFML/Graphics.hpp SFML/Window.hpp SFML/Audio.hpp SFML/System.hpp], [sfml-graphics sfml-window sfml-system sfml-audio], [], AC_MSG_ERROR([	/!\ This programme requires SFML !]))
	fi
])

dnl ---------------------------------------------------------------------------
dnl MY_FIND_LIBNOTIFY()
dnl Find LIBNOTIFY lib
dnl ---------------------------------------------------------------------------

AC_DEFUN([MY_FIND_LIBNOTIFY],
[
	dnl Pkg Config (cf man pkg-config => AUTOCONF MACROS)
	PKG_PROG_PKG_CONFIG dnl Check is 'pkg-config' is installed
	AH_TEMPLATE([USE_LIBNOTIFY], [Define if libnotify can be used.])
	AH_TEMPLATE([USE_LIBNOTIFY_NEW], [Define if libnotify version is more than 0.7.3 because Gnome decided to change the API.])

	if test "$IS_MINGW" = 'true'; then
		AC_DEFINE([USE_LIBNOTIFY], [0])
	else
		PKG_CHECK_MODULES([LIBNOTIFY], [libnotify >= 0.4], AC_DEFINE([USE_LIBNOTIFY], [1]), AC_DEFINE([USE_LIBNOTIFY], [0]))

		PKG_CHECK_MODULES([LIBNOTIFY_NEW], [libnotify >= 0.7.3], AC_DEFINE([USE_LIBNOTIFY_NEW], [1]), AC_DEFINE([USE_LIBNOTIFY_NEW], [0]))
		
		LIBS_ALL="$LIBS_ALL ${LIBNOTIFY_LIBS}"
		AC_SUBST([LIBS_ALL], [$LIBS_ALL])
		CFLAGS_ALL="$CFLAGS_ALL ${LIBNOTIFY_CFLAGS}"
		AC_SUBST([CFLAGS_ALL], [$CFLAGS_ALL])
	fi
])

dnl ---------------------------------------------------------------------------
dnl MY_FIND_WXWIDGETS()
dnl Find WXWIDGETS lib
dnl ---------------------------------------------------------------------------

AC_DEFUN([MY_FIND_WXWIDGETS],
[
	AM_OPTIONS_WXCONFIG
	AM_PATH_WXCONFIG(2.8.4, wxWin=1, , [xrc,std])
		    if test "$wxWin" != 1; then
		    AC_MSG_ERROR([
		            wxWidgets must be installed on your system.

		            Please check that wx-config is in path, the directory
		            where wxWidgets libraries are installed (returned by
		            'wx-config --libs' or 'wx-config --static --libs' command)
		            is in LD_LIBRARY_PATH or equivalent variable and
		            wxWidgets version is 2.8.4 or above.
		            ])
		fi
		
	dnl All lib options
	LIBS_ALL="$LIBS_ALL ${WX_LIBS}"
	AC_SUBST([LIBS_ALL], [$LIBS_ALL])
	CFLAGS_ALL="$CFLAGS_ALL ${WX_CXXFLAGS}"
	AC_SUBST([CFLAGS_ALL], [$CFLAGS_ALL])
	
	if test "$IS_MINGW" = 'true'; then
		EXTRA_WINDRES_ARG="$EXTRA_WINDRES_ARG $(echo "$WX_CXXFLAGS" | cut -d " " -f 1-2)" ## Pour n'avoir que les deux premiers chanps (inclue).'
		AC_SUBST([EXTRA_WINDRES_ARG])
	fi
])

dnl ---------------------------------------------------------------------------
dnl MY_FIND_BOOST()
dnl Find BOOST lib
dnl ---------------------------------------------------------------------------

AC_DEFUN([MY_FIND_BOOST],
[
	dnl Boost
	AM_CHECK_LIB_HEADER([BOOST], [boost], [boost/config.hpp], [], [], AC_MSG_ERROR([	/!\ This programme requires boost !]))
])

dnl ---------------------------------------------------------------------------
dnl MY_FIND_GTK2()
dnl Find BOOST lib
dnl ---------------------------------------------------------------------------

AC_DEFUN([MY_FIND_GTK2],
[
	dnl gtk+2
	if test "$IS_MINGW" = 'false'; then
		AM_CHECK_LIB_HEADER([GTK2], [gtk+-2.0], [gdk/gdkx.h gtk/gtk.h], [gtk-x11-2.0], [], AC_MSG_ERROR([	/!\ This programme requires gtk+ 2 !]))
	fi
])

dnl ---------------------------------------------------------------------------
dnl MY_FIND_LUA()
dnl Find LUA lib
dnl ---------------------------------------------------------------------------

AC_DEFUN([MY_FIND_LUA],
[
	dnl LUA
	LUA_VERSION="5.1" dnl Sous windows, la lib s'appelle lua, et pas lua5.1, Sous Ubunut, la lib s'appelle lua !
	AM_CHECK_LIB_HEADER([LUA], [lua${LUA_VERSION}], [lua.hpp], [lua @ lua${LUA_VERSION}], [], [AC_MSG_ERROR([	/!\ This programme requires LUA !])])
])

dnl ---------------------------------------------------------------------------
dnl MY_FIND_OPENGL()
dnl Find OPENGL lib
dnl ---------------------------------------------------------------------------

AC_DEFUN([MY_FIND_OPENGL],
[
	dnl OpenGL header
	AM_CHECK_LIB_HEADER([GL], [gl], [GL/gl.h], [], [], AC_MSG_ERROR([	/!\ This programme requires OpenGL headers !]))

	dnl OpenGL WIN32 & MAC
	if test "$IS_MINGW" = 'true'; then
			dnl intl (gettext)
		AM_CHECK_LIB_HEADER([OGLWIN], [], [], [opengl32 glu32], [], [AC_MSG_ERROR([	/!\ This programme requires intl (gettext) !])])
	elif test "$IS_MAC" = 'true'; then
		CHECK_FRAMEWORK_LIST([SFML], [OpenGL GLUT])
	fi
])

dnl ---------------------------------------------------------------------------
dnl MY_FIND_INTL()
dnl Find INTL lib
dnl ---------------------------------------------------------------------------

AC_DEFUN([MY_FIND_INTL],
[
	dnl intl (gettext)
	if test "$IS_LINUX" = 'false'; then
		AM_CHECK_LIB_HEADER([INTL], [intl], [libintl.h locale.h], [intl], [], [AC_MSG_ERROR([	/!\ This programme requires intl (gettext) !])])
	fi
])

dnl ---------------------------------------------------------------------------
dnl MY_FIND_STDCPP()
dnl Find stdc++ lib
dnl ---------------------------------------------------------------------------

AC_DEFUN([MY_FIND_STDCPP],
[
	dnl STL, pas sous windows comme on passe en stdc++ static
	if test "$IS_MINGW" = 'false'; then
		AC_CHECK_LIB(stdc++, main,,AC_MSG_ERROR([	/!\ This programme requires libstdc++ !]))
	fi
])

dnl ---------------------------------------------------------------------------
dnl MY_PACKAGE_INIT(package full name)
dnl
dnl Init the source package
dnl
dnl ---------------------------------------------------------------------------

AC_DEFUN([MY_PACKAGE_INIT],
[
	AM_CONFIG_HEADER(src/config.hpp)

	AC_SUBST(VERSION)

	ISODATE=`date +%Y-%m-%d`
	AC_SUBST([ISODATE])
	PACKAGE_NAME="$1"
	AC_SUBST([PACKAGE_NAME])
	AC_DEFINE_UNQUOTED([PACKAGE_NAME], ["$PACKAGE_NAME"])
])

dnl ---------------------------------------------------------------------------
dnl MY_INIT_CPP_PROGS()
dnl
dnl Init programs for C++ sources
dnl
dnl ---------------------------------------------------------------------------

dnl AC_DEFUN([MY_INIT_CPP_PROGS],
dnl [
dnl 	dnl Checks for programs.
dnl 	AC_PROG_INSTALL
dnl 	#AC_PROG_CC
dnl 	AC_PROG_CXX
dnl 	AC_PROG_CPP
dnl 	AC_PROG_LN_S
dnl ])

dnl ---------------------------------------------------------------------------
dnl MY_ECHO_BUILD_INFO()
dnl
dnl Init programs for C++ sources
dnl
dnl ---------------------------------------------------------------------------

AC_DEFUN([MY_ECHO_BUILD_INFO],
[
	# Autre
	INFO_LINE="####################################"

	# Recap
	MSG="The package is now configured. You should type make !"

	MSG="$MSG\n    DEBUG MODE          : "
	if test "$DEBUG" = 1; then
		debugModeStr="enable"
	else
		debugModeStr="disable"
	fi
	MSG="${MSG}${debugModeStr}."
	
	
	MSG="$MSG\n    TARGET PLATFORM     : "
	MSG="${MSG}${MY_TARGET_OS}."
	MSG="$MSG\n    INSTALLATION PREFIX : "
	MSG="${MSG}${prefix}."

	echo -e "\n${INFO_LINE}\n\n${MSG}\n\n${INFO_LINE}\n"
])

dnl ---------------------------------------------------------------------------
dnl MY_INIT_LIBTOOL
dnl
dnl Init libtool
dnl
dnl ---------------------------------------------------------------------------

dnl AC_DEFUN([MY_INIT_LIBTOOL],
dnl [
dnl 	dnl To compile libs
dnl 	AM_PROG_LIBTOOL		dnl indique que l'on utilise Libtool pour la compilation
dnl 	AC_PROG_MAKE_SET	dnl indique que l'on doit disposer de make qui est utilisé par Libtool
dnl ])

dnl ---------------------------------------------------------------------------
dnl MY_INIT_DEBUG_SWITCH([Force debug])
dnl
dnl Allow the user tu build the program in debug mode ; doesn't edit any cpp options !
dnl
dnl ---------------------------------------------------------------------------

AC_DEFUN([MY_INIT_DEBUG_SWITCH],
[
	dnl debug
	DEBUG=0
	AC_ARG_ENABLE([debug], [  --enable-debug          Chose if the package should be built in debug mode], [DEBUG=1])

	dnl Force debug
	if test "$1" = "true" || test "$1" = "1"; then
		DEBUG=1
	fi

	AC_MSG_CHECKING([if debug is enabled])			

	AH_TEMPLATE([DEBUG], [Define is a debug version sould be build])
	AM_CONDITIONAL([IS_DEBUG], [test "$DEBUG" -eq 1])
	AC_DEFINE_UNQUOTED([DEBUG], [$DEBUG])
	
	if test "$DEBUG" -eq 1; then
		AC_MSG_RESULT([yes])
	else
		AC_MSG_RESULT([no])
	fi
])

dnl ---------------------------------------------------------------------------
dnl MY_INIT_BUILD_OPTION(Debug option, no debug option)
dnl
dnl Init CXXFLAGS and CPPFLAGS
dnl
dnl ---------------------------------------------------------------------------

AC_DEFUN([MY_INIT_BUILD_OPTION],
[
	dnl Basic
	warningOptions=' -Wall -Wclobbered -Wempty-body -Wmissing-field-initializers -Wsign-compare -Wtype-limits -Wuninitialized' # -Wignored-qualifiers
	if test "$IS_MAC" = 'true'; then
		warningOptions=' -Wall'
	fi

	if test "$DEBUG" -eq 1; then
		CXXFLAGS="$1 $warningOptions"
	else
		CXXFLAGS="$2 $warningOptions"
	fi

	CPPFLAGS=${CXXFLAGS}
	AC_SUBST([CXXFLAGS])
	AC_SUBST([CPPFLAGS])
	
	dnl Extra LDFLAGS (for win32)
	EXTRA_LDFLAGS=''
	
	if test "$IS_MINGW" = "true"; then
		true
		EXTRA_LDFLAGS="$EXTRA_LDFLAGS -static-libgcc -static-libstdc++" dnl Static stdc++
		
		if test "$DEBUG" -eq 0; then
			EXTRA_LDFLAGS="$EXTRA_LDFLAGS -mwindows"
			dnl -mwindows : Pour cacher la console sous windows.
		fi
	fi

	AC_SUBST([EXTRA_LDFLAGS])
	
	dnl EXTRA_WINDRES_ARG
	EXTRA_WINDRES_ARG="$EXTRA_WINDRES_ARG"
	AC_SUBST([EXTRA_WINDRES_ARG])
])

dnl ---------------------------------------------------------------------------
dnl MY_INIT_DATA_PATH
dnl
dnl Define data path for unix / win32 depending on the current target system
dnl
dnl ---------------------------------------------------------------------------

AC_DEFUN([MY_INIT_DATA_PATH],
[
	if test "$IS_MINGW" = true; then	
		mypkgdatadir="$prefix"
		bindir="$prefix"
		AC_SUBST([mypkgdatadir])
		AC_SUBST([prefix])
	else
		mypkgdatadir="$datadir/$PACKAGE"
		AC_SUBST([mypkgdatadir])
	fi
])

dnl ---------------------------------------------------------------------------
dnl AM_CHECK_LIB_HEADER(LIBNAME-MAJ, NAME, HEADERS, LIBS, [ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND]])
dnl
dnl My lib & header check
dnl
dnl Example use:
dnl   AM_CHECK_LIB_HEADER([LUA], [lua], [lua.hpp], [lua5.1], [], [Error])
dnl ---------------------------------------------------------------------------

AC_DEFUN([AM_CHECK_LIB_HEADER],
[
	declare $1_CFLAGS=''
	declare $1_LIBS=''

	dnl Headers	
	dnl We try with check-headers
	headerOk=1
	for headerName in $3; do
		AC_CHECK_HEADERS([$headerName],[],[headerOk=0])
	done
	
	dnl Libs
	backLibs="$LIBS"
	
	libsOk=1
	libsList=''
	
	isLastField=0
	fieldId=1
	while test "$isLastField" -eq 0; do
		toTestLibsList=''

		if ! echo "$4" | grep '@' > '/dev/null'; then
			dnl Only on field
			isLastField=1
			toTestLibsList="$4"
		else
			toTestLibsList="$(echo $4 | cut -d'@' -f$fieldId)"
		fi
		
		if test -n "$toTestLibsList"; then
			libsList=''
			libsOk=1
		
			for libName in $toTestLibsList; do
				AC_CHECK_LIB([$libName], [main], [], [libsOk=0])
				libsList="$libsList -l$libName"
			done
		else
			isLastField=1 dnl Fin
			libsList=''
			
			if test -n "$4"; then
				dnl Liste se finie par "|" => pas ok !
				libsOk=0
			else
				dnl Liste vide => ok !
				libsOk=1
			fi
		fi
		
		if test "$libsOk" -eq 1; then
			dnl On a trouvé une liste qui marche => on arrète !
			isLastField=1
		fi
		
		let fieldId=fieldId+1
	done
	
	AC_SUBST([LIBS], [$backLibs])
	
	dnl pkg-config
	if test "$headerOk" -eq 0 || test "$libsOk" -eq 0; then
		if test -n "$2"; then
			dnl We try with pkg-config
			PKG_PROG_PKG_CONFIG
			PKG_CHECK_MODULES([$1], [$2], [headerOk=1; libsOk=1], [])
		
			if test "$headerOk" -eq 0 || test "$libsOk" -eq 0; then
				dnl Still not found
				$6
				true # We need a command if $6 is empty
			else
				dnl All si Ok
				$5
				true # We need a command if $5 is empty
			fi
		else
			dnl Not found
			$6
			true # We need a command if $6 is empty
		fi
	else
		dnl All is Ok
		AC_SUBST([$1_LIBS], [$libsList])
		AC_SUBST([$1_CFLAGS], [''])
		$5
	fi
	
	dnl All lib options
	LIBS_ALL="$LIBS_ALL ${$1_LIBS}"
	AC_SUBST([LIBS_ALL], [$LIBS_ALL])
	CFLAGS_ALL="$CFLAGS_ALL ${$1_CFLAGS}"
	AC_SUBST([CFLAGS_ALL], [$CFLAGS_ALL])
])

dnl ---------------------------------------------------------------------------
dnl CHECK_FRAMEWORK_LIST(libNameMaj, framework list)
dnl
dnl Check for windows ressources compiler (windres)
dnl
dnl Example use:
dnl   CHECK_FRAMEWORK_LIST([SFML], [SFML sfml-graphics sfml-window sfml-system sfml-audio])
dnl ---------------------------------------------------------------------------

AC_DEFUN([CHECK_FRAMEWORK_LIST],
[
	frameworkPathList="/System/Library/Frameworks /Library/Frameworks"

	declare $1_CFLAGS=''
	declare $1_LIBS=''

	frameworksOk=1
	frameworksList=''
	
	isLastField=0
	fieldId=1
	while test "$isLastField" -eq 0; do
		toTestframeworksList=''

		if ! echo "$2" | grep '@' > '/dev/null'; then
			dnl Only on field
			isLastField=1
			toTestframeworksList="$2"
		else
			toTestframeworksList="$(echo $2 | cut -d'@' -f$fieldId)"
		fi
		
		if test -n "$toTestframeworksList"; then
			frameworksList=''
			frameworksOk=1
		
			for frameworkName in $toTestframeworksList; do
				AC_MSG_CHECKING([for framework $frameworkName])
				isThisFrameworkOk=0

				for frameworkPath in $frameworkPathList; do
					dir="$frameworkPath/$frameworkName.framework/Versions/Current"
					if test -d "$dir"; then
						isThisFrameworkOk=1
						
						frameworksList="$frameworksList -framework $frameworkName"
						
						AC_MSG_RESULT([yes : $dir])
						break
					fi
				done
				
				AC_MSG_RESULT([no])
			done
		else
			isLastField=1 dnl Fin
			frameworksList=''
			
			if test -n "$2"; then
				dnl Liste se finie par "|" => pas ok !
				frameworksOk=0
			else
				dnl Liste vide => ok !
				frameworksOk=1
			fi
		fi
		
		if test "$frameworksOk" -eq 1; then
			dnl On a trouvé une liste qui marche => on arrète !
			isLastField=1
		fi
		
		let fieldId=fieldId+1
	done
	
	dnl Save
	if test "$frameworksOk" -eq 1; then
		AC_SUBST([$1_LIBS], [$frameworksList])
		AC_SUBST([$1_CFLAGS], [$frameworksList])
	
		dnl All lib options
		LIBS_ALL="$LIBS_ALL ${$1_LIBS}"
		AC_SUBST([LIBS_ALL], [$LIBS_ALL])
		CFLAGS_ALL="$CFLAGS_ALL ${$1_CFLAGS}"
		AC_SUBST([CFLAGS_ALL], [$CFLAGS_ALL])
	else
		AC_MSG_ERROR([	/!\ This programme requires the folowing frameworks : $2 !])
	fi
])


dnl ---------------------------------------------------------------------------
dnl AM_FIND_WINDRES()
dnl
dnl Check for windows ressources compiler (windres)
dnl
dnl Example use:
dnl   AM_FIND_WINDRES()
dnl ---------------------------------------------------------------------------

AC_DEFUN([AM_FIND_WINDRES],
[
	WINDRES=''
		
	if test "$IS_MINGW" = 'true'; then
		AC_MSG_CHECKING([for windres])
		for name in 'windres' 'i586-pc-mingw32msvc'; do
			if which "$name" > /dev/null; then
				WINDRES="$name"
				AM_CONDITIONAL([IS_MINGW], [true])
				AC_MSG_RESULT(["yes : $WINDRES"])
				break
			fi
		done
	
		if test -z "$WINDRES"; then
			AC_MSG_RESULT(["no"])
		fi
	fi
	
	AM_CONDITIONAL([HAVE_WINDRES], [test -n "$WINDRES"])
	AC_SUBST([WINDRES])
])

dnl ---------------------------------------------------------------------------
dnl MY_DETECT_OS()
dnl
dnl Check for the target operation system
dnl
dnl Set: IS_MINGW (true or false)
dnl Set: IS_LINUX (true or false)
dnl Set: IS_MAC   (true or false)
dnl Set: MY_TARGET_OS   (mingw, linux or mac)
dnl Example use:
dnl   AM_FIND_WINDRES()
dnl ---------------------------------------------------------------------------

AC_DEFUN([MY_DETECT_OS],
[
	if echo $host | grep "linux" > /dev/null; then
		MY_TARGET_OS="linux"
		IS_MINGW="false"
		IS_LINUX="true"
		IS_MAC="false"
	elif echo $host | grep "mingw" > /dev/null; then
		MY_TARGET_OS="mingw"
		IS_MINGW="true"
		IS_LINUX="false"
		IS_MAC="false"
	elif echo $host | grep "darwin" > /dev/null; then
		MY_TARGET_OS="darwin"
		IS_MINGW="false"
		IS_LINUX="false"
		IS_MAC="true"
	else
		MY_TARGET_OS="unknown"
		IS_MINGW="false"
		IS_LINUX="false"
		IS_MAC="false"
	
		AC_MSG_ERROR([	/!\ Unknown OS !])
	fi

	AC_SUBST([MY_TARGET_OS])
	AM_CONDITIONAL([IS_MINGW], [$IS_MINGW])
	AM_CONDITIONAL([IS_LINUX], [$IS_LINUX])
	AM_CONDITIONAL([IS_MAC], [$IS_MAC])
])

dnl ---------------------------------------------------------------------------
dnl Macros for wxWidgets detection. Typically used in configure.in as:
dnl
dnl     AC_ARG_ENABLE(...)
dnl     AC_ARG_WITH(...)
dnl        ...
dnl     AM_OPTIONS_WXCONFIG
dnl        ...
dnl        ...
dnl     AM_PATH_WXCONFIG(2.6.0, wxWin=1)
dnl     if test "$wxWin" != 1; then
dnl        AC_MSG_ERROR([
dnl                wxWidgets must be installed on your system
dnl                but wx-config script couldn't be found.
dnl
dnl                Please check that wx-config is in path, the directory
dnl                where wxWidgets libraries are installed (returned by
dnl                'wx-config --libs' command) is in LD_LIBRARY_PATH or
dnl                equivalent variable and wxWidgets version is 2.3.4 or above.
dnl        ])
dnl     fi
dnl     CPPFLAGS="$CPPFLAGS $WX_CPPFLAGS"
dnl     CXXFLAGS="$CXXFLAGS $WX_CXXFLAGS_ONLY"
dnl     CFLAGS="$CFLAGS $WX_CFLAGS_ONLY"
dnl
dnl     LIBS="$LIBS $WX_LIBS"
dnl ---------------------------------------------------------------------------

dnl ---------------------------------------------------------------------------
dnl AM_OPTIONS_WXCONFIG
dnl
dnl adds support for --wx-prefix, --wx-exec-prefix, --with-wxdir and
dnl --wx-config command line options
dnl ---------------------------------------------------------------------------

AC_DEFUN([AM_OPTIONS_WXCONFIG],
[
    AC_ARG_WITH(wxdir,
                [  --with-wxdir=PATH       Use uninstalled version of wxWidgets in PATH],
                [ wx_config_name="$withval/wx-config"
                  wx_config_args="--inplace"])
    AC_ARG_WITH(wx-config,
                [  --with-wx-config=CONFIG wx-config script to use (optional)],
                wx_config_name="$withval" )
    AC_ARG_WITH(wx-prefix,
                [  --with-wx-prefix=PREFIX Prefix where wxWidgets is installed (optional)],
                wx_config_prefix="$withval", wx_config_prefix="")
    AC_ARG_WITH(wx-exec-prefix,
                [  --with-wx-exec-prefix=PREFIX
                          Exec prefix where wxWidgets is installed (optional)],
                wx_config_exec_prefix="$withval", wx_config_exec_prefix="")
])

dnl Helper macro for checking if wx version is at least $1.$2.$3, set's
dnl wx_ver_ok=yes if it is:
AC_DEFUN([_WX_PRIVATE_CHECK_VERSION],
[
    wx_ver_ok=""
    if test "x$WX_VERSION" != x ; then
      if test $wx_config_major_version -gt $1; then
        wx_ver_ok=yes
      else
        if test $wx_config_major_version -eq $1; then
           if test $wx_config_minor_version -gt $2; then
              wx_ver_ok=yes
           else
              if test $wx_config_minor_version -eq $2; then
                 if test $wx_config_micro_version -ge $3; then
                    wx_ver_ok=yes
                 fi
              fi
           fi
        fi
      fi
    fi
])

dnl ---------------------------------------------------------------------------
dnl AM_PATH_WXCONFIG(VERSION, [ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND
dnl                  [, WX-LIBS [, ADDITIONAL-WX-CONFIG-FLAGS]]]])
dnl
dnl Test for wxWidgets, and define WX_C*FLAGS, WX_LIBS and WX_LIBS_STATIC
dnl (the latter is for static linking against wxWidgets). Set WX_CONFIG_NAME
dnl environment variable to override the default name of the wx-config script
dnl to use. Set WX_CONFIG_PATH to specify the full path to wx-config - in this
dnl case the macro won't even waste time on tests for its existence.
dnl
dnl Optional WX-LIBS argument contains comma- or space-separated list of
dnl wxWidgets libraries to link against (it may include contrib libraries). If
dnl it is not specified then WX_LIBS and WX_LIBS_STATIC will contain flags to
dnl link with all of the core wxWidgets libraries.
dnl
dnl Optional ADDITIONAL-WX-CONFIG-FLAGS argument is appended to wx-config
dnl invocation command in present. It can be used to fine-tune lookup of
dnl best wxWidgets build available.
dnl
dnl Example use:
dnl   AM_PATH_WXCONFIG([2.6.0], [wxWin=1], [wxWin=0], [html,core,net]
dnl                    [--unicode --debug])
dnl ---------------------------------------------------------------------------

dnl
dnl Get the cflags and libraries from the wx-config script
dnl
AC_DEFUN([AM_PATH_WXCONFIG],
[
  dnl do we have wx-config name: it can be wx-config or wxd-config or ...
  if test x${WX_CONFIG_NAME+set} != xset ; then
     WX_CONFIG_NAME=wx-config
  fi

  if test "x$wx_config_name" != x ; then
     WX_CONFIG_NAME="$wx_config_name"
  fi

  dnl deal with optional prefixes
  if test x$wx_config_exec_prefix != x ; then
     wx_config_args="$wx_config_args --exec-prefix=$wx_config_exec_prefix"
     WX_LOOKUP_PATH="$wx_config_exec_prefix/bin"
  fi
  if test x$wx_config_prefix != x ; then
     wx_config_args="$wx_config_args --prefix=$wx_config_prefix"
     WX_LOOKUP_PATH="$WX_LOOKUP_PATH:$wx_config_prefix/bin"
  fi
  if test "$cross_compiling" = "yes"; then
     wx_config_args="$wx_config_args --host=$host_alias"
  fi

  dnl don't search the PATH if WX_CONFIG_NAME is absolute filename
  if test -x "$WX_CONFIG_NAME" ; then
     AC_MSG_CHECKING(for wx-config)
     WX_CONFIG_PATH="$WX_CONFIG_NAME"
     AC_MSG_RESULT($WX_CONFIG_PATH)
  else
     AC_PATH_PROG(WX_CONFIG_PATH, $WX_CONFIG_NAME, no, "$WX_LOOKUP_PATH:$PATH")
  fi

  if test "$WX_CONFIG_PATH" != "no" ; then
    WX_VERSION=""

    min_wx_version=ifelse([$1], ,2.2.1,$1)
    if test -z "$5" ; then
      AC_MSG_CHECKING([for wxWidgets version >= $min_wx_version])
    else
      AC_MSG_CHECKING([for wxWidgets version >= $min_wx_version ($5)])
    fi

    WX_CONFIG_WITH_ARGS="$WX_CONFIG_PATH $wx_config_args $5 $4"

    WX_VERSION=`$WX_CONFIG_WITH_ARGS --version 2>/dev/null`
    wx_config_major_version=`echo $WX_VERSION | \
           sed 's/\([[0-9]]*\).\([[0-9]]*\).\([[0-9]]*\)/\1/'`
    wx_config_minor_version=`echo $WX_VERSION | \
           sed 's/\([[0-9]]*\).\([[0-9]]*\).\([[0-9]]*\)/\2/'`
    wx_config_micro_version=`echo $WX_VERSION | \
           sed 's/\([[0-9]]*\).\([[0-9]]*\).\([[0-9]]*\)/\3/'`

    wx_requested_major_version=`echo $min_wx_version | \
           sed 's/\([[0-9]]*\).\([[0-9]]*\).\([[0-9]]*\)/\1/'`
    wx_requested_minor_version=`echo $min_wx_version | \
           sed 's/\([[0-9]]*\).\([[0-9]]*\).\([[0-9]]*\)/\2/'`
    wx_requested_micro_version=`echo $min_wx_version | \
           sed 's/\([[0-9]]*\).\([[0-9]]*\).\([[0-9]]*\)/\3/'`

    _WX_PRIVATE_CHECK_VERSION([$wx_requested_major_version],
                              [$wx_requested_minor_version],
                              [$wx_requested_micro_version])

    if test -n "$wx_ver_ok"; then

      AC_MSG_RESULT(yes (version $WX_VERSION))
      WX_LIBS=`$WX_CONFIG_WITH_ARGS --libs`

      dnl is this even still appropriate?  --static is a real option now
      dnl and WX_CONFIG_WITH_ARGS is likely to contain it if that is
      dnl what the user actually wants, making this redundant at best.
      dnl For now keep it in case anyone actually used it in the past.
      AC_MSG_CHECKING([for wxWidgets static library])
      WX_LIBS_STATIC=`$WX_CONFIG_WITH_ARGS --static --libs 2>/dev/null`
      if test "x$WX_LIBS_STATIC" = "x"; then
        AC_MSG_RESULT(no)
      else
        AC_MSG_RESULT(yes)
      fi

      dnl starting with version 2.2.6 wx-config has --cppflags argument
      wx_has_cppflags=""
      if test $wx_config_major_version -gt 2; then
        wx_has_cppflags=yes
      else
        if test $wx_config_major_version -eq 2; then
           if test $wx_config_minor_version -gt 2; then
              wx_has_cppflags=yes
           else
              if test $wx_config_minor_version -eq 2; then
                 if test $wx_config_micro_version -ge 6; then
                    wx_has_cppflags=yes
                 fi
              fi
           fi
        fi
      fi

      dnl starting with version 2.7.0 wx-config has --rescomp option
      wx_has_rescomp=""
      if test $wx_config_major_version -gt 2; then
        wx_has_rescomp=yes
      else
        if test $wx_config_major_version -eq 2; then
           if test $wx_config_minor_version -ge 7; then
              wx_has_rescomp=yes
           fi
        fi
      fi
      if test "x$wx_has_rescomp" = x ; then
         dnl cannot give any useful info for resource compiler
         WX_RESCOMP=
      else
         WX_RESCOMP=`$WX_CONFIG_WITH_ARGS --rescomp`
      fi

      if test "x$wx_has_cppflags" = x ; then
         dnl no choice but to define all flags like CFLAGS
         WX_CFLAGS=`$WX_CONFIG_WITH_ARGS --cflags`
         WX_CPPFLAGS=$WX_CFLAGS
         WX_CXXFLAGS=$WX_CFLAGS

         WX_CFLAGS_ONLY=$WX_CFLAGS
         WX_CXXFLAGS_ONLY=$WX_CFLAGS
      else
         dnl we have CPPFLAGS included in CFLAGS included in CXXFLAGS
         WX_CPPFLAGS=`$WX_CONFIG_WITH_ARGS --cppflags`
         WX_CXXFLAGS=`$WX_CONFIG_WITH_ARGS --cxxflags`
         WX_CFLAGS=`$WX_CONFIG_WITH_ARGS --cflags`

         WX_CFLAGS_ONLY=`echo $WX_CFLAGS | sed "s@^$WX_CPPFLAGS *@@"`
         WX_CXXFLAGS_ONLY=`echo $WX_CXXFLAGS | sed "s@^$WX_CFLAGS *@@"`
      fi

      ifelse([$2], , :, [$2])

    else

       if test "x$WX_VERSION" = x; then
          dnl no wx-config at all
          AC_MSG_RESULT(no)
       else
          AC_MSG_RESULT(no (version $WX_VERSION is not new enough))
       fi

       WX_CFLAGS=""
       WX_CPPFLAGS=""
       WX_CXXFLAGS=""
       WX_LIBS=""
       WX_LIBS_STATIC=""
       WX_RESCOMP=""
       ifelse([$3], , :, [$3])

    fi
  else

    WX_CFLAGS=""
    WX_CPPFLAGS=""
    WX_CXXFLAGS=""
    WX_LIBS=""
    WX_LIBS_STATIC=""
    WX_RESCOMP=""

    ifelse([$3], , :, [$3])

  fi

  AC_SUBST(WX_CPPFLAGS)
  AC_SUBST(WX_CFLAGS)
  AC_SUBST(WX_CXXFLAGS)
  AC_SUBST(WX_CFLAGS_ONLY)
  AC_SUBST(WX_CXXFLAGS_ONLY)
  AC_SUBST(WX_LIBS)
  AC_SUBST(WX_LIBS_STATIC)
  AC_SUBST(WX_VERSION)
  AC_SUBST(WX_RESCOMP)
])
