///File : MainPanel.hpp
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
#include <wx/vscroll.h>
#include <wx/event.h>
#include <wx/stdpaths.h>
#include <wx/statline.h>
#include <wx/listctrl.h>

#include <vector>
//------------------------------------------------------------------------------
#include "config.hpp"
#include "findFile.hpp"
#include "AppConfig.hpp"
#include <wx/filepicker.h>

//------------------------------------------------------------------------------

#if not defined MAIN_PANEL_HPP_WINUSBGUI
#define MAIN_PANEL_HPP_WINUSBGUI
//------------------------------------------------------------------------------
class MainFrame;
//------------------------------------------------------------------------------
void SendNotification(const wxString &title, const wxString &text = _T(""), wxString iconFilename = _T(""));
//------------------------------------------------------------------------------
class MainPanel : public wxPanel
{
public:
    MainPanel(wxWindow* parent, wxWindowID id, const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxDefaultSize, long style = wxTAB_TRAVERSAL );
    ~MainPanel();

    void OnSourceOptionChanged(wxCommandEvent& event);
    void OnListOrFileModified(wxCommandEvent& event);
    void OnRefresh(wxCommandEvent& event);
    void OnInstall(wxCommandEvent& event);
    void OnShowAllDrive(wxCommandEvent& event);

    void RefreshListContent();

    bool IsInstallOk() const;

private:
    wxListBox *m_dvdDriveList, *m_usbStickList;
    std::vector<std::string> m_dvdDriveDevList, m_usbStickDevList;
    wxFilePickerCtrl *m_isoFile;

    MainFrame *m_parentFrame;

    wxButton *m_btInstall, *m_btRefresh;

    wxRadioButton *m_isoChoice, *m_dvdChoice;

    //std::vector<std::pair<std::string, std::string> > m_list;
};

#endif //MAIN_PANEL_HPP_WINUSBGUI
