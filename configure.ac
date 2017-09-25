AC_INIT(woeusb, @@WOEUSB_VERSION@@)
AC_CONFIG_SRCDIR([src])
AM_INIT_AUTOMAKE([foreign])
AC_CONFIG_MACRO_DIR([m4])

MY_PACKAGE_INIT([WoeUSB])

dnl Checks for programs (must be here).
AC_LANG([C++])
AC_PROG_INSTALL
AC_PROG_CXX
AC_PROG_CPP
AC_PROG_LN_S

dnl To compile libs
LT_INIT
AM_PROG_LIBTOOL		dnl indique que l'on utilise Libtool pour la compilation
AC_PROG_MAKE_SET	dnl indique que l'on doit disposer de make qui est utilisé par Libtool

MY_DETECT_OS dnl Detect OS
MY_INIT_DATA_PATH dnl Define data path for unix / win32 depending on the current target system
AM_FIND_WINDRES dnl Find windres is needed

MY_INIT_DEBUG_SWITCH([false]) dnl Allow the user tu build the program in debug mode ; doesn't edit any cpp options ; true to force debug

dnl Libs
MY_FIND_STDCPP
MY_FIND_WXWIDGETS

AC_OUTPUT([Makefile

	src/Makefile
	src/data/Makefile
	src/linux-menu/Makefile
	src/win32/Makefile
	src/locale/Makefile
	src/locale/fr/Makefile
	src/locale/zh_TW/Makefile
	src/locale/fr/LC_MESSAGES/Makefile
	src/locale/zh_TW/LC_MESSAGES/Makefile
	debian/Makefile
	innoSetup/Makefile])

MY_ECHO_BUILD_INFO # Recap
