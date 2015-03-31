///File : MainFrame.cpp
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
#include "MainFrame.hpp"

#include <wx/toolbar.h>
//------------------------------------------------------------------------------

MainFrame::MainFrame(const wxString& title, const wxPoint& pos, const wxSize& size, long style) : wxFrame(NULL, -1, title, pos, size, style)
{
    // Presentation général
    wxString ImgFileName;
    #if defined(__WXMSW__)
        SetIcon(wxIcon(_T("win32icon")));
    #elif defined(__UNIX__)
        ImgFileName = findFile(_T("data/icon.png"));
        if(wxFileExists(ImgFileName))
        {
            SetIcon(wxIcon(ImgFileName, wxBITMAP_TYPE_PNG));
        }
    #endif //#ifdef WIN32

        // File menu
    wxMenu *FileMenu = new wxMenu;
    m_menuItemShowAll = new wxMenuItem(FileMenu, wxID_ANY, wxString(_("Show all drive")) + _T("\tCtrl+A"), _("Show all drives, even those not detected as USB stick."), wxITEM_CHECK);
    FileMenu->Append(m_menuItemShowAll);

    FileMenu->AppendSeparator();
    FileMenu->Append(wxID_EXIT);

        // Help Menu
    wxMenu *HelpMenu = new wxMenu;
    HelpMenu->Append(wxID_ABOUT);

        // Menubar
    m_MenuBar = new wxMenuBar();
    m_MenuBar->Append(FileMenu,_("&File"));
    m_MenuBar->Append(HelpMenu,_("&Help"));

    SetMenuBar(m_MenuBar);

    // Body
	wxBoxSizer* MainSizer = new wxBoxSizer( wxVERTICAL );

	m_MainPanel = new MainPanel(this ,wxID_ANY);
    MainSizer->Add(m_MainPanel, 1, wxEXPAND | wxALL, 4);

	SetSizer( MainSizer );

	// Events
    Connect( m_menuItemShowAll->GetId(), wxEVT_COMMAND_MENU_SELECTED, wxCommandEventHandler(MainPanel::OnShowAllDrive), NULL, m_MainPanel);

    Connect( wxID_EXIT, wxEVT_COMMAND_MENU_SELECTED, wxCommandEventHandler(MainFrame::OnQuit));
    Connect( wxID_ABOUT, wxEVT_COMMAND_MENU_SELECTED, wxCommandEventHandler(MainFrame::OnAbout));
}
//------------------------------------------------------------------------------
void MainFrame::OnQuit(wxCommandEvent& event)
{
    Close(true);
}
//------------------------------------------------------------------------------
bool MainFrame::IsShowAllChecked() const
{
    return m_menuItemShowAll->IsChecked();
}
//------------------------------------------------------------------------------
void MainFrame::OnAbout(wxCommandEvent& event)
{
    DialogAbout MyDialogAbout(this, wxID_ANY);
    MyDialogAbout.ShowModal();
}
//------------------------------------------------------------------------------
