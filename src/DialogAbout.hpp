///File : DialogAbout.hpp
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
#ifndef DIALOG_ABOUT_HPP_WINUSBGUI
#define DIALOG_ABOUT_HPP_WINUSBGUI

#include "wx/wxprec.h"

#ifdef __BORLANDC__
    #pragma hdrstop
#endif

#ifndef WX_PRECOMP
    #include "wx/wx.h"
#endif
//------------------------------------------------------------------------------
#include <wx/stdpaths.h>
//------------------------------------------------------------------------------

#include <wx/intl.h>

#include <wx/hyperlink.h>
#include <wx/gdicmn.h>
#include <wx/settings.h>
#include <wx/notebook.h>
//------------------------------------------------------------------------------
#include "config.hpp"
#include "findFile.hpp"
#include "AppConfig.hpp"
///////////////////////////////////////////////////////////////////////////
#if defined VERSION
    #define NUM_VERSION _(VERSION)
#else
    #define NUM_VERSION _T("1.0.0")
#endif

///////////////////////////////////////////////////////////////////////////////
/// Class PanelNoteBookAutors
///////////////////////////////////////////////////////////////////////////////
class PanelNoteBookAutors : public wxPanel
{
public:
    PanelNoteBookAutors(wxWindow* parent, wxWindowID id = wxID_ANY, const wxString &autherName = _T(""), const wxString &imgName = _T(""), const wxString &siteLink = _T(""), const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxDefaultSize, long style = wxTAB_TRAVERSAL);
};

///////////////////////////////////////////////////////////////////////////////
/// Class about
///////////////////////////////////////////////////////////////////////////////
class DialogAbout : public wxDialog
{
public:
	DialogAbout( wxWindow* parent, wxWindowID id = wxID_ANY, const wxString& title = _("About"), const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxSize( 475,340 ), long style = wxDEFAULT_DIALOG_STYLE );

protected:
    wxStaticBitmap* m_bitmapIcone;
    wxStaticText* m_staticTextTitre;
    wxStaticText* m_staticTextVersion;
    wxNotebook* m_NotebookAutorLicence;
    PanelNoteBookAutors *MyPanelNoteBookAutors;
    wxButton* m_BtOk;
};

#endif //DIALOG_ABOUT_HPP_WINUSBGUI
