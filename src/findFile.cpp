///File : findFile.cpp
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
#include "findFile.hpp"
//------------------------------------------------------------------------------

wxString findFile(const wxString &str)
{
    wxString testPath;

    testPath = wxGetCwd() + _T("/") + str;
    if(wxFileExists(testPath) || wxDirExists(testPath)) // Si c'est dans le dossier ./
    {
        return testPath;
    }

    testPath = _T("../") + str;
    if(wxFileExists(testPath) || wxDirExists(testPath)) // Si c'est dans le dossier ../
    {
        return testPath;
    }

    #if defined(__UNIX__)
    testPath = wxString(wxStandardPaths::Get().GetInstallPrefix() + _T("/share/") + _T(PACKAGE) + _T("/") + str);
    if(wxFileExists(testPath) || wxDirExists(testPath)) // Si c'est dans le dossier /usr/.../share/nomprog
    {
        return testPath;
    }
    #endif // defined(__UNIX__)

    testPath = wxString(wxStandardPaths::Get().GetDataDir() + _T("/") + str);
    if(wxFileExists(testPath) || wxDirExists(testPath)) // Si c'est dans le dossier /usr/.../share/nomPaquet
    {
        return testPath;
    }

    // Si non
    wxMessageBox(_("File not Found : ") + str, _("Error"), wxICON_ERROR);
    return _T("");
}
