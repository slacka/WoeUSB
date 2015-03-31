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
#include "MyException.hpp"
#include <iostream>
//------------------------------------------------------------------------------
namespace En
{
//------------------------------------------------------------------------------
MyException::MyException(const std::string& info) throw() : m_info(info)
{
    //std::cerr << info << std::endl;
}
//------------------------------------------------------------------------------
MyException::~MyException() throw()
{

}
//------------------------------------------------------------------------------
const char* MyException::what() const throw()
{
    return m_info.c_str();
}
//------------------------------------------------------------------------------
} // namespace En
//------------------------------------------------------------------------------
