///File : MainPanel.cpp
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
#include "MainPanel.hpp"

#include "MainFrame.hpp"
#include "strWxStdConv.hpp"

#include <utility>
#include <string>

#include <wx/listctrl.h>
#include <wx/radiobut.h>
#include <wx/progdlg.h>

#include <wx/wupdlock.h>

#include "MyException.hpp"
#include "processManager.hpp"
//------------------------------------------------------------------------------
using namespace std;
//------------------------------------------------------------------------------
MainPanel::MainPanel(wxWindow* parent, wxWindowID id, const wxPoint& pos, const wxSize& size, long style ) : wxPanel( parent, id, pos, size, style )
{
    // Controls
	wxBoxSizer *MainSizer = new wxBoxSizer( wxVERTICAL );

	// Iso / CD
	MainSizer->Add(new wxStaticText(this, wxID_ANY, _("Source :")), 0, wxALL, 3);

    // Iso
	m_isoChoice = new wxRadioButton(this, wxID_ANY, _("From a disk image (iso)"));
	MainSizer->Add(m_isoChoice, 0, wxALL, 3);

	wxBoxSizer *tmpSizer = new wxBoxSizer( wxHORIZONTAL );
	tmpSizer->AddSpacer(20);
	m_isoFile = new wxFilePickerCtrl(this, wxID_ANY, _T(""), _("Please select a disk image"), _T("Iso images (*.iso)|*.iso|All files|*"));
	tmpSizer->Add(m_isoFile, 1, wxLEFT | wxRIGHT | wxBOTTOM, 3);
	MainSizer->Add(tmpSizer, 0, wxEXPAND, 0);

    // DVD
	MainSizer->Add(m_dvdChoice = new wxRadioButton(this, wxID_ANY, _("From a CD/DVD drive")), 0, wxALL, 3);

    // List
	tmpSizer = new wxBoxSizer( wxHORIZONTAL );
	tmpSizer->AddSpacer(20);
    m_dvdDriveList = new wxListBox(this, wxID_ANY);
    tmpSizer->Add(m_dvdDriveList, 1, wxEXPAND | wxLEFT | wxRIGHT | wxBOTTOM, 3);
	MainSizer->Add(tmpSizer, 1, wxEXPAND, 0);

    // Target
    MainSizer->AddSpacer(30);

    MainSizer->Add(new wxStaticText(this, wxID_ANY, _("Target device :")), 0, wxALL, 3);

        // List
    m_usbStickList = new wxListBox(this, wxID_ANY);
    MainSizer->Add(m_usbStickList, 1, wxEXPAND | wxALL, 3);

    // Buttons
    MainSizer->AddSpacer(30);

    wxBoxSizer *BtSizer = new wxBoxSizer( wxHORIZONTAL );
    BtSizer->Add(m_btRefresh = new wxButton(this, wxID_REFRESH), 0, wxALL, 3);
    BtSizer->Add(m_btInstall = new wxButton(this, wxID_ANY, _("Install")), 0, wxALL, 3);

    MainSizer->Add(BtSizer, 0, wxALIGN_RIGHT, 0);

    // Finition
	SetSizer(MainSizer);

    /*m_popupMenu = new wxMenu;
    m_popupMenu->Append(m_menuItemAddManually = MenuAddItem(m_popupMenu, wxString(_("Add Manually")) + _T("\tCtrl+N"), _T("add.png")));
    m_popupMenu->Append(m_menuItemAddAutodetect = MenuAddItem(m_popupMenu, wxString(_("Add with autodection")), _T("add.png")));*/

	// Events
	m_usbStickList->Connect( wxID_ANY, wxEVT_COMMAND_LISTBOX_SELECTED, wxCommandEventHandler(MainPanel::OnListOrFileModified), NULL, this);
	m_dvdDriveList->Connect( wxID_ANY, wxEVT_COMMAND_LISTBOX_SELECTED, wxCommandEventHandler(MainPanel::OnListOrFileModified), NULL, this);
	m_isoFile->Connect( wxID_ANY, wxEVT_COMMAND_FILEPICKER_CHANGED, wxCommandEventHandler(MainPanel::OnListOrFileModified), NULL, this);

	m_btInstall->Connect( wxID_ANY, wxEVT_COMMAND_BUTTON_CLICKED, wxCommandEventHandler(MainPanel::OnInstall), NULL, this);
	m_btRefresh->Connect( wxID_ANY, wxEVT_COMMAND_BUTTON_CLICKED, wxCommandEventHandler(MainPanel::OnRefresh), NULL, this);

	m_isoChoice->Connect( wxID_ANY, wxEVT_COMMAND_RADIOBUTTON_SELECTED, wxCommandEventHandler(MainPanel::OnSourceOptionChanged), NULL, this);
	m_dvdChoice->Connect( wxID_ANY, wxEVT_COMMAND_RADIOBUTTON_SELECTED, wxCommandEventHandler(MainPanel::OnSourceOptionChanged), NULL, this);

	// Content
	RefreshListContent();
	wxCommandEvent tmp;
    OnSourceOptionChanged(tmp);
    m_btInstall->Enable(IsInstallOk());
}

//------------------------------------------------------------------------------
MainPanel::~MainPanel()
{

}
//------------------------------------------------------------------------------
void MainPanel::RefreshListContent()
{
    std::string tmp;
    std::string log;

    // USB
    {
        log = "";
        m_usbStickDevList.clear();
        m_usbStickList->Clear();

        bool showAllChecked = static_cast<MainFrame*>(GetParent())->IsShowAllChecked();

        std::stringstream command;
        command << "\"$(readlink -f '";
        command << StrWxToStd(findFile(_T("data/listUsb")));
        command << "')\" ";
        if(showAllChecked)
        {
            command << "all ";
        }
        command << "2>&1";

        PipeManager pipe(command.str());

        while(! pipe.IsEof())
        {
            tmp = pipe.GetLine();
            if(tmp.empty())
            {
                continue;
            }
            log += tmp;
            m_usbStickDevList.push_back(tmp);
            m_usbStickList->Append(StrStdToWx(pipe.GetLine()));
        }

        if(pipe.Close() != 0)
        {
            m_usbStickDevList.clear();
            m_usbStickList->Clear();

            MY_THROW("Can't read usb list !\n" << log);
        }
    }

    // DVD
    {
        log = "";
        m_dvdDriveDevList.clear();
        m_dvdDriveList->Clear();

        PipeManager pipe(std::string("\"$(readlink -f '") + StrWxToStd(findFile(_T("data/listDvdDrive"))) + "')\" 2>&1");

        while(! pipe.IsEof())
        {

            tmp = pipe.GetLine();
            if(tmp.empty())
            {
                continue;
            }
            log += tmp;
            m_dvdDriveDevList.push_back(tmp);
            m_dvdDriveList->Append(StrStdToWx(pipe.GetLine()));
        }

        if(pipe.Close() != 0)
        {
            m_dvdDriveDevList.clear();
            m_dvdDriveList->Clear();

            MY_THROW("Can't read dvd drive list !\n" << log);
        }
    }

    m_btInstall->Enable(IsInstallOk());
}
//------------------------------------------------------------------------------
void MainPanel::OnSourceOptionChanged(wxCommandEvent& event)
{
    bool isIso = m_isoChoice->GetValue();

    m_isoFile->Enable(isIso);
    m_dvdDriveList->Enable(!isIso);

    m_btInstall->Enable(IsInstallOk());
}
//------------------------------------------------------------------------------
bool MainPanel::IsInstallOk() const
{
    bool isIso = m_isoChoice->GetValue();
    return ((isIso && wxFileExists(m_isoFile->GetPath())) || (!isIso && m_dvdDriveList->GetSelection() != wxNOT_FOUND)) && m_usbStickList->GetSelection() != wxNOT_FOUND;
}
//------------------------------------------------------------------------------
void MainPanel::OnListOrFileModified(wxCommandEvent& event)
{
    if(event.GetEventType() == wxEVT_COMMAND_LISTBOX_SELECTED && !event.IsSelection()) // Prevent segmentation fault : list box deselection send event when the frame is destroying an half the objects are deleted
    {
        return;
    }

    m_btInstall->Enable(IsInstallOk());
}
//------------------------------------------------------------------------------
void MainPanel::OnRefresh(wxCommandEvent& event)
{
    RefreshListContent();
}
//------------------------------------------------------------------------------
void MainPanel::OnInstall(wxCommandEvent& event)
{
    if(IsInstallOk())
    {
        bool isIso = m_isoChoice->GetValue();

        std::string device = m_usbStickDevList.at(m_usbStickList->GetSelection());
        std::string iso;
        if(isIso)
        {
            iso = filenameWxToStd(m_isoFile->GetPath());
        }
        else
        {
            iso = m_dvdDriveDevList.at(m_dvdDriveList->GetSelection());
        }

        PipeManager pipe(std::string("gksudo --description 'WinUSB' -- sh -c 'winusb --noColor --forGui --format \"") + iso + "\" \"" + device + "\" 2>&1'");

        wxProgressDialog *dialog = new wxProgressDialog(_("Installing..."), _("Please wait..."), 100, GetParent(), wxPD_APP_MODAL | wxPD_SMOOTH | wxPD_CAN_ABORT);

        wxString log;
        while(! pipe.IsEof())
        {
            std::string tmp = pipe.GetLine();
            if(!tmp.empty())
            {
                if(*(tmp.end() - 1) == '%')
                {
                    long progress;
                    if(!StrStdToWx(tmp.substr(0, tmp.size() - 1)).ToLong(&progress))
                    {
                        continue;
                    }

                    if(progress > 99) // Maximum is 99 because 100 will stop the ProgressDialog
                    {
                        progress = 99;
                    }

                    if(!dialog->Update(progress))
                    {
                        if(wxMessageBox(_("Are you sure you want to cancel the insatallation ?"), _("Cancel"), wxYES_NO | wxICON_QUESTION, this) == wxNO)
                        {
                            dialog->Resume();
                        }
                        else
                        {
                            exit(1);
                        }
                    }
                }
                else
                {
                    if(tmp == "pulse")
                    {
                        tmp = "";
                    }

                    if(!dialog->Pulse(StrStdToWx(tmp)))
                    {
                        if(wxMessageBox(_("Are you sure you want to cancel the insatallation ?"), _("Cancel"), wxYES_NO | wxICON_QUESTION, this) == wxNO)
                        {
                            dialog->Resume();
                        }
                        else
                        {
                            exit(1);
                        }
                    }

                    if(!tmp.empty())
                    {
                        log << StrStdToWx(tmp + "\n");
                    }
                }
            }
        }

        dialog->Destroy();

        int exitCode = pipe.Close();
        if(exitCode == 0)
        {
            wxMessageBox(_("Installation succeded !"), _("Installation"), wxOK | wxICON_INFORMATION, this);
        }
        else
        {
            wxMessageBox(wxString(_("Installation failed !")) + _T("\nExit code: ") + wxNbToStr(exitCode) + _T("\nLog:\n") + log, _("Installation"), wxOK | wxICON_ERROR, this);
        }
    }
}
//------------------------------------------------------------------------------
void MainPanel::OnShowAllDrive(wxCommandEvent& event)
{
    RefreshListContent();
}
//------------------------------------------------------------------------------
