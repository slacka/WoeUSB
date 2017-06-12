SUBDIRS = data locale win32 linux-menu

bin_PROGRAMS=woeusbgui

INCLUDES = $(CFLAGS_ALL)

woeusbgui_LDFLAGS = $(EXTRA_LDFLAGS)
	
woeusbgui_LDADD = $(LIBS_ALL)

woeusbguiSrcBase = AppConfig.hpp	 DialogAbout.hpp  MainPanel.cpp \
	App.cpp		 findFile.cpp	  MainPanel.hpp     processManager.hpp \
	App.hpp		 findFile.hpp	  MyException.cpp   strWxStdConv.cpp \
	MainFrame.cpp	  MyException.hpp   strWxStdConv.hpp \
	DialogAbout.cpp  MainFrame.hpp	  nbStrConvert.hpp \
	processManager.cpp


## --------------- Resources windows ---------------
.rc.o:
	i586-mingw32msvc-windres $^ -o $@ $(EXTRA_WINDRES_ARG)

if HAVE_WINDRES
woeusbgui_SOURCES=$(woeusbguiSrcBase) rc.rc
else
woeusbgui_SOURCES=$(woeusbguiSrcBase)
endif
## --------------- Resources windows --------------- 

# Install my_script in $(bindir) and distribute it.
dist_bin_SCRIPTS = woeusb

man_MANS = woeusbgui.1 woeusb.1

if IS_MINGW
install-data-hook:
	## Install Dlls
	"$(srcdir)/installDll.sh" "$(prefix)" "$(host)"
endif

EXTRA_DIST = $(srcdir)/*.cbp $(man_MANS) $(srcdir)/rc.rc $(srcdir)/installDll.sh
