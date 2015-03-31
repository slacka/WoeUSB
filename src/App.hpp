///File : App.hpp
//------------------------------------------------------------------------------
/*
    This file is part of WinUSBgui.

    WinUSBgui is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    WinUSBgui is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with WinUSBgui.  If not, see <http://www.gnu.org/licenses/>.
*/
//------------------------------------------------------------------------------
#include "wx/wxprec.h"

#ifdef __BORLANDC__
    #pragma hdrstop
#endif

#ifndef WX_PRECOMP
    #include "wx/wx.h"
#endif
//------------------------------------------------------------------------------
#include <wx/intl.h>
#include <wx/splash.h>
#include <wx/stdpaths.h>
#include <wx/textfile.h>
//------------------------------------------------------------------------------
#include "config.hpp"
#include "findFile.hpp"
#include "MainFrame.hpp"
#include "AppConfig.hpp"
//------------------------------------------------------------------------------

#if not defined APP_HPP_WINUSBGUI
#define APP_HPP_WINUSBGUI

class App : public wxApp
{
public:
    virtual bool OnInit();
    virtual int OnRun();

private:
    wxLocale m_locale;
    MainFrame *m_frame;
};
//------------------------------------------------------------------------------

#endif //APP_HPP_WINUSBGUI
