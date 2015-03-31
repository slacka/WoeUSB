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
#include <iostream>
#include <string>

#include <stdio.h>
#include <stdlib.h>
//------------------------------------------------------------------------------
class PipeManager
{
public:
    PipeManager(const std::string &command);
    ~PipeManager();

    std::string GetLine();
    bool GetLine(std::string &line);
    bool IsEof() const;
    int Close();

private:
    FILE *m_pipe;
};
//------------------------------------------------------------------------------
int GetProcessOutput(const std::string &command, std::string &str);
//------------------------------------------------------------------------------
