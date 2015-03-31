///File : DialogAbout.cpp
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
#include "DialogAbout.hpp"
//------------------------------------------------------------------------------

DialogAbout::DialogAbout( wxWindow* parent, wxWindowID id, const wxString& title, const wxPoint& pos, const wxSize& size, long style ) : wxDialog( parent, id, title, pos, size, style )
{
	this->SetSizeHints( wxDefaultSize, wxDefaultSize );

	wxBoxSizer* sizerAll = new wxBoxSizer( wxVERTICAL );
	wxBoxSizer* sizerImg = new wxBoxSizer( wxHORIZONTAL );

    wxString ImgFileName = findFile(_T("data/icon.png"));
    if(wxFileExists(ImgFileName))
    {
        wxImage img(ImgFileName, wxBITMAP_TYPE_PNG);
        m_bitmapIcone = new wxStaticBitmap( this, wxID_ANY, wxBitmap(img), wxDefaultPosition, wxSize(48,48));
        sizerImg->Add( m_bitmapIcone, 0, wxALL, 5 );
    }

	wxBoxSizer* sizerTxt;
	sizerTxt = new wxBoxSizer( wxVERTICAL );

	m_staticTextTitre = new wxStaticText( this, wxID_ANY, PROG_FULL_NAME_GETTEXT);
	m_staticTextTitre->SetFont( wxFont( 16, 74, 90, 92, false, wxT("Sans")));
	m_staticTextTitre->SetForegroundColour( wxColour( 0, 60, 118 ) );
	sizerTxt->Add( m_staticTextTitre, 0, wxEXPAND|wxLEFT|wxRIGHT|wxTOP, 5 );

	m_staticTextVersion = new wxStaticText( this, wxID_ANY, wxString::Format(_("Version %s"), NUM_VERSION));
	m_staticTextVersion->SetFont( wxFont( 10, 74, 90, 92, false, wxT("Sans") ) );
	m_staticTextVersion->SetForegroundColour( wxColour( 69, 141, 196 ) );
	sizerTxt->Add( m_staticTextVersion, 0, wxLEFT, 50 );
	sizerImg->Add( sizerTxt, 0, 0, 5 );
	sizerAll->Add( sizerImg, 0, wxEXPAND, 5 );

	m_NotebookAutorLicence = new wxNotebook( this, wxID_ANY);

	m_NotebookAutorLicence->AddPage(new PanelNoteBookAutors(m_NotebookAutorLicence, wxID_ANY, _T("Colin GILLE / Congelli501"), _T("data/c501-logo.png"), _T("www.congelli.eu")), _("Developer"), true);

	wxString licenceStr = wxString::Format(_(
    "%s is free software: you can redistribute it and/or modify"
    "it under the terms of the GNU General Public License as published by"
    "the Free Software Foundation, either version 3 of the License, or"
    "(at your option) any later version.\n"
    "\n"
    "%s is distributed in the hope that it will be useful,"
    "but WITHOUT ANY WARRANTY; without even the implied warranty of"
    "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
    "GNU General Public License for more details.\n"
    "\n"
    "You should have received a copy of the GNU General Public License"
    "along with %s.  If not, see <http://www.gnu.org/licenses/>."), PROG_FULL_NAME_GETTEXT, PROG_FULL_NAME_GETTEXT, PROG_FULL_NAME_GETTEXT);

	wxTextCtrl *LicenceTxt = new wxTextCtrl(m_NotebookAutorLicence, wxID_ANY, licenceStr, wxDefaultPosition, wxDefaultSize, wxTE_MULTILINE | wxTE_READONLY);

	m_NotebookAutorLicence->AddPage(LicenceTxt, _("License"));

	sizerAll->Add( m_NotebookAutorLicence, 1, wxEXPAND | wxALL, 5 );

	m_BtOk = new wxButton(this, wxID_OK);
	sizerAll->Add( m_BtOk, 0, wxALIGN_RIGHT | wxBOTTOM | wxRIGHT, 5 );
	m_BtOk->SetFocus();

	this->SetSizer( sizerAll );
	this->Layout();
}

//------------------------------------------------------------------------------
PanelNoteBookAutors::PanelNoteBookAutors( wxWindow* parent, wxWindowID id, const wxString &autherName, const wxString &imgName, const wxString &siteLink, const wxPoint& pos, const wxSize& size, long style ) : wxPanel( parent, id, pos, size, style )
{
	wxBoxSizer *sizerNoteBookAutors = new wxBoxSizer( wxVERTICAL );

	wxStaticText *AuteurStaticText = new wxStaticText(this, wxID_ANY, autherName);
	sizerNoteBookAutors->Add(AuteurStaticText, 0, wxALL, 5);

    if(siteLink != _T(""))
    {
        wxHyperlinkCtrl *AuteurLink = new wxHyperlinkCtrl(this, wxID_ANY, siteLink, siteLink);
        sizerNoteBookAutors->Add(AuteurLink, 0, wxLEFT | wxBOTTOM, 5);
    }

    if(imgName != _T(""))
    {
        wxString ImgFileName = findFile(imgName);
        if(wxFileExists(ImgFileName))
        {
            wxImage img(ImgFileName, wxBITMAP_TYPE_PNG);
            wxStaticBitmap *ImgAutherLogo = new wxStaticBitmap( this, wxID_ANY, wxBitmap(img));
            sizerNoteBookAutors->Add(ImgAutherLogo, 0, wxLEFT, 5);
        }
    }

	this->SetSizer(sizerNoteBookAutors);
}
