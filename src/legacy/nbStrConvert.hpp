///File : nbConvert.hpp
//------------------------------------------------------------------------------
/*
    Copyright (C) 2009 Colin GILLE / congelli501

    This file is part of Devis Maker.
    Devis Maker is sold under Devis Maker license (read COPYING file).
*/
//------------------------------------------------------------------------------
#include <string>
#include <iostream>
#include <sstream>
//------------------------------------------------------------------------------
#if not defined NB_STR_CONVERT_HPP
#define NB_STR_CONVERT_HPP
//------------------------------------------------------------------------------
template < typename T >
std::string nbToString(const T &nb)
{
    std::stringstream ss;
    std::string str;
    if(sizeof(T) != 1) // Pas char
    {
        ss << std::fixed << nb; // fixed : pas de nb scientifique. Par contre, plein de zero...
    }
    else
    {
        // Type char ==> on le tranforme en int
        ss << std::fixed << int(nb); // fixed : pas de nb scientifique. Par contre, plein de zero...
    }
    ss >> str;

    // On enléve les 0 et . innutils
    std::string::iterator it = str.end() - 1;
    if(str.find('.') != std::string::npos) // On ne racourci pas le nb si pas de virgule
    {
        while(str.size() > 1 && *it == '0')
        {
            str.erase(it);
            it = str.end() - 1;
        }

        if(*it == '.') // Si on arrive à la virgule ==> suppression.
        {
            str.erase(it);
        }
    }

    return str;
}

//------------------------------------------------------------------------------
template < typename T >
T stringToNb(std::string nbStr)
{
    std::stringstream ss;
    T nb;
    ss << nbStr;
    if(sizeof(T) != 1) // Pas char
    {
        ss >> nb;
    }
    else
    {
        // Type char ==> on le tranforme en int
        int tmp;
        ss >> tmp;
        nb = char(tmp);
    }

    return nb;
}
//------------------------------------------------------------------------------
#endif // NB_STR_CONVERT_HPP
