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
#include "processManager.hpp"


#include "MyException.hpp"

//------------------------------------------------------------------------------
PipeManager::PipeManager(const std::string &command)
{
    m_pipe = popen(command.c_str(), "r");

    if(m_pipe == NULL)
    {
        MY_THROW("Can't open pipe for command '" << command << "' !");
    }
}
//------------------------------------------------------------------------------
PipeManager::~PipeManager()
{
    if(m_pipe != NULL)
    {
        pclose(m_pipe);
    }
}
//------------------------------------------------------------------------------
int PipeManager::Close()
{
    if(m_pipe)
    {
        int exitCode = pclose(m_pipe);
        m_pipe = NULL;
        return exitCode;
    }
    else
    {
        MY_THROW("Pipe not open !");
    }
}
//------------------------------------------------------------------------------
bool PipeManager::GetLine(std::string &line)
{
    line = "";
    char letter = '\0';

    while(not feof(m_pipe))
    {
        letter = fgetc(m_pipe);

        if(letter == '\n' || letter == '\r')
        {
            return 1;
        }
        else if(letter == EOF)
        {
            return 0;
        }
        else
        {
            line += letter;
        }
    }

    return 1;
}
//------------------------------------------------------------------------------
std::string PipeManager::GetLine()
{
    std::string str;
    GetLine(str);
    return str;
}
//------------------------------------------------------------------------------
bool PipeManager::IsEof() const
{
    return feof(m_pipe);
}
//------------------------------------------------------------------------------
int GetProcessOutput(const std::string &command, std::string &str)
{
    str = "";
    PipeManager pipe(command);
    while(! pipe.IsEof())
    {
        str += pipe.GetLine() + "\n";
    }

    if(!str.empty())
    {
        str.erase(str.end() - 1);
    }

    return pipe.Close();
}
//------------------------------------------------------------------------------
