///File : App.cpp
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
#include "config.hpp"

#if USE_LIBNOTIFY == 1
    #include <libnotify/notify.h>
#endif

#include "strWxStdConv.hpp"

#include "App.hpp"
//------------------------------------------------------------------------------
IMPLEMENT_APP(App)

#ifdef __WXMAC__
    #include <ApplicationServices/ApplicationServices.h>
#endif
//------------------------------------------------------------------------------
bool App::OnInit()
{
    #ifdef __WXMAC__
    ProcessSerialNumber PSN;
    GetCurrentProcess(&PSN);
    TransformProcessType(&PSN,kProcessTransformToForegroundApplication);
    #endif

    // Création du Handler pour les images (permet de les ouvrir)...
    wxInitAllImageHandlers();

    // Gestion de la langue
    // Ajout des préfixes possibles de chemins d'accès aux catalogues
    wxLocale::AddCatalogLookupPathPrefix(findFile(_T("locale")));

    // Mise en place de la langue par défaut du système
    m_locale.Init(wxLANGUAGE_DEFAULT);
    {
       wxLogNull noLog; // Supprime les erreurs si les catalogues n'existent pas
       // Catalogue de l'application
       m_locale.AddCatalog(_T("trad"));
       // Catalogue de wxWidgets
       m_locale.AddCatalog(_T("wxstd"));
    }

    #if USE_LIBNOTIFY == 1
    if(!notify_init(StrWxToStd(PROG_FULL_NAME_GETTEXT).c_str()))
    {
        std::cerr << "Lib notify not initialised !" << std::endl;
        return false;
    }
    #endif

    try
    {
        wxString frameTitle = PROG_FULL_NAME_GETTEXT;
        #if DEBUG == 1
           frameTitle += _T(" - Debug");
        #endif

        m_frame = new MainFrame(frameTitle,  wxDefaultPosition, wxSize(400, 500));
        m_frame->SetMinSize(wxSize(300, 300));
        m_frame->Show(true);
    }
    catch(const std::exception& e) //Rattrape toutes les exceptions
    {
        wxMessageBox(_("Error : ") + wxString(e.what(), wxConvUTF8), _("Error..."),  wxOK | wxICON_ERROR);
        exit(1);
    }

    return true;
}
//------------------------------------------------------------------------------
int App::OnRun()
{
    bool isException = false;
    wxString msg;

    int code = 0;

    try
    {
        code = wxApp::OnRun();
    }
    catch(const std::exception& e) //Rattrape toutes les exceptions
    {
        isException = true;
        msg = wxString(e.what(), wxConvUTF8);
    }
    catch(int errCode)
    {
        msg << _T("Error \"") << errCode << _T("\" has occured !");
        isException = true;
    }
    catch(wxString info)
    {
        msg = info;
        isException = true;
    }
    catch(...)
    {
        msg = _("Unknown error as occured !");
        isException = true;
    }

    if(isException)
    {
        std::cerr << msg << std::endl;
        wxMessageBox(_("Fatal error : ") + wxString(_T("\n")) + msg, _("Error..."),  wxOK | wxICON_ERROR, m_frame);
        return 1;
    }

    return code;
}
//------------------------------------------------------------------------------
