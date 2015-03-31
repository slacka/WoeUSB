///File : strWxStdConv.hpp
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
#include "math.h"
#include "config.hpp"
//------------------------------------------------------------------------------

#if not defined PACKAGE
    #error "This program should be built with its package !"// #define PACKAGE devismaker
#endif

#include <sstream>
#include "nbStrConvert.hpp"

#if not defined STR_WX_STD_CONV_HPP_WINUSBGUI
#define STR_WX_STD_CONV_HPP_WINUSBGUI
//------------------------------------------------------------------------------
// String
std::string StrWxToStd(const wxString &str);
wxString StrStdToWx(const std::string &str);
wxString wxStrAutoCut(wxString str, const int &maxLen = 60);

// Filename (Pour Windows)
std::string filenameWxToStd(const wxString &str);
wxString filenameStdToWx(const std::string &str);
//------------------------------------------------------------------------------
template < typename T >
bool wxStrToNb(wxString str, T *nb) // Avec verification
{
    // 1 : Remplacement des "." par des ","
    int lang = wxLocale::GetSystemLanguage();

    if(lang == wxLANGUAGE_FRENCH || lang == wxLANGUAGE_FRENCH_BELGIAN || lang == wxLANGUAGE_FRENCH_CANADIAN || lang == wxLANGUAGE_FRENCH_LUXEMBOURG || lang == wxLANGUAGE_FRENCH_MONACO || lang == wxLANGUAGE_FRENCH_SWISS)
    {
        // Si on est en france ==> On remplace les "." du pavé numérique par des ",".
        str.Replace(_T("."), _T(","));
    }

    // On transforme en double ==> Le plus de précision.
    double tempNb;
    bool isOk = str.ToDouble(&tempNb);

    // On cast en "T"

    *nb = T(tempNb);

	return isOk;
}
//------------------------------------------------------------------------------
// Sans verif...
template < typename T >
T wxStrToNb(const wxString &str)
{
    T tempNb;
    wxStrToNb(str, &tempNb);
    return tempNb;
}
//------------------------------------------------------------------------------
template < typename T >
wxString wxNbToStr(const T &nb)
{
    // On doit passer par les std::string pour eviter les nb scientifiques.
	return StrStdToWx(nbToString(nb));
}
//------------------------------------------------------------------------------
template < typename T >
wxString wxNbToHexaStr(const T &nb)
{
    std::stringstream ss;
    std::string str;
    ss << std::hex << nb;

	return StrStdToWx(ss.str());
}
//------------------------------------------------------------------------------
template < typename T >
wxString ArrangeByteSize(const T &size)
{
    // Selection de l'unité...
    const wxString unitList[] = {_("bytes"), _T("Kio"), _T("Mio"), _T("Gio"), _T("Tio") };
    const int unityListSize = sizeof(unitList) / sizeof(wxString);
    int unity = 0;
    unsigned long unityDiv = 1;

    while(1)
    {
        unityDiv = pow(1024, unity);

        if(double(size) / double(unityDiv) < 999)
        {
            break; // Ok : bonne unité
        }

        if(unity >= unityListSize - 1)
        {
            break;
        }

        unity++;
    }

    // On remplie la wxString
    double nb = double(size) / double(unityDiv);
    wxString tempStr = wxNbToStr(nb);

    // Quel est le symole de la virgule ?
    const wxString virguleChar = _T(".");
    //wxString virguleChar = StrStdToWx(cfg->GetString("nb_virguleString"));
    //tempStr.Replace( _T("."), virguleChar);

    const int synifNb = 2;

    // On arrondi
    int virgulePos = tempStr.Find(virguleChar);
    if(virgulePos != wxNOT_FOUND && tempStr.Len() - virgulePos > synifNb + 1) // Trop de chiffres significatifs
    {
        wxChar lastNbChar = tempStr[tempStr.Find(virguleChar) + synifNb + 1];
        // ==> A faire
        if(wxStrToNb<int>(lastNbChar) >= 5) // Si le chiffre avant le dernier chiffre significatif est sup à 5 ==> rajout de 10 ^ -synifNb
        {
            // Utilise le nombre arrondi...
            tempStr = wxNbToStr(nb + pow(10, -synifNb));
            tempStr.Replace( _T("."), virguleChar);
        }

        tempStr = tempStr.Mid(0, tempStr.Find(virguleChar) + synifNb + 1);
    }

    tempStr << _T(" ") << unitList[unity];

    return tempStr;
}
//------------------------------------------------------------------------------

#endif // STR_WX_STD_CONV_HPP_WINUSBGUI
