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
#if not defined MY_EXCEPTION_HPP_WINUSBGUI
#define MY_EXCEPTION_HPP_WINUSBGUI
//------------------------------------------------------------------------------
#include <exception>
#include <sstream>
#include <string>
#include <iostream>
//------------------------------------------------------------------------------
// FIXME: Retirer la ligne cerr !
#define MY_THROW(what)                                                                                      \
{                                                                                                           \
    std::ostringstream sstring;                                                                             \
    sstring << "Error from '" << __FILE__ << "' at line " << __LINE__ << "\nDescription: " << what;         \
    throw En::MyException(sstring.str());                                                                   \
}                                                                                                           \
//------------------------------------------------------------------------------
#define MY_CATCH_LUA_CERR()                                                                   \
catch(luabind::error &e)                                                                      \
{                                                                                             \
    cerr << "Failed to run lua function !" << endl;                                           \
    cerr << "LUA error (error) :\n" << lua_tostring(Global::GetLuaState(), -1) << endl;       \
    cerr << "What: " << e.what() << endl;                                                     \
}                                                                                             \
catch(luabind::cast_failed &e)                                                                \
{                                                                                             \
    cerr << "Failed to run lua function !" << endl;                                           \
    cerr << "LUA error (cast_failed) :\n" << lua_tostring(Global::GetLuaState(), -1) << endl; \
    cerr << "What: " << e.what() << endl;                                                     \
}                                                                                             \
catch(std::exception &e)                                                                      \
{                                                                                             \
    cerr << "Failed to run lua function (std::exception) !" << endl;                          \
    cerr << "What: " << e.what() << endl;                                                     \
}
//------------------------------------------------------------------------------
namespace En
{
//------------------------------------------------------------------------------
class MyException : public std::exception
{
public:
    MyException(const std::string &info) throw();
    virtual ~MyException() throw();
    virtual const char* what() const throw();

private:
    std::string m_info;
};
//------------------------------------------------------------------------------
} // namespace En
//------------------------------------------------------------------------------
#endif // MY_EXCEPTION_HPP_WINUSBGUI
