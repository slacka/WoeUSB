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
#include "strWxStdConv.hpp"
//------------------------------------------------------------------------------
wxString wxStrAutoCut(wxString str, const unsigned int &maxLen)
{
    if(str.Len() > maxLen)
    {
        str = str.Mid(0, maxLen - 3);
        str << _T("...");
    }

    return str;
}
//------------------------------------------------------------------------------
std::string StrWxToStd(const wxString &str)
{
	return std::string(str.mb_str(wxConvUTF8));
}
//------------------------------------------------------------------------------
wxString StrStdToWx(const std::string &str)
{
	return wxString(str.c_str(), wxConvUTF8);
}
//------------------------------------------------------------------------------
// Filename
std::string filenameWxToStd(const wxString &str)
{
	return std::string(str.mb_str(wxConvFile));
}
//------------------------------------------------------------------------------
wxString filenameStdToWx(const std::string &str)
{
	return wxString(str.c_str(), wxConvFile);
}
//------------------------------------------------------------------------------
