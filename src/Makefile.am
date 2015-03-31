SUBDIRS = data locale win32 linux-menu

bin_PROGRAMS=winusbgui

INCLUDES = $(CFLAGS_ALL)

winusbgui_LDFLAGS = $(EXTRA_LDFLAGS)
	
winusbgui_LDADD = $(LIBS_ALL)

winusbguiSrcBase = AppConfig.hpp	 DialogAbout.hpp  MainPanel.cpp \
	App.cpp		 findFile.cpp	  MainPanel.hpp     processManager.hpp \
	App.hpp		 findFile.hpp	  MyException.cpp   strWxStdConv.cpp \
	MainFrame.cpp	  MyException.hpp   strWxStdConv.hpp \
	DialogAbout.cpp  MainFrame.hpp	  nbStrConvert.hpp \
	processManager.cpp


## --------------- Resources windows ---------------
.rc.o:
	i586-mingw32msvc-windres $^ -o $@ $(EXTRA_WINDRES_ARG)

if HAVE_WINDRES
winusbgui_SOURCES=$(winusbguiSrcBase) rc.rc
else
winusbgui_SOURCES=$(winusbguiSrcBase)
endif
## --------------- Resources windows --------------- 

# Install my_script in $(bindir) and distribute it.
dist_bin_SCRIPTS = winusb

man_MANS = winusbgui.1 winusb.1

if IS_MINGW
install-data-hook:
	## Install Dlls
	"$(srcdir)/installDll.sh" "$(prefix)" "$(host)"
endif

EXTRA_DIST = $(srcdir)/*.cbp $(man_MANS) $(srcdir)/rc.rc $(srcdir)/installDll.sh
