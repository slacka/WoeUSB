# Contributing Guidelines
This document explains how to contribute to this project in many aspects. Please make sure to read this thoroughly before making any contributions.

## Reporting Issues
The so-called "issue" includes but is not limited to software bugs and suggestions

### Always Search for Duplicates Before Filing a New Issue
There is a possibility that your issue has already been filed, so please search the issue tracker before filing a new one

When searching, use keywords instead of full sentences. For example, search "crash unbounded variable" instead of "The program crashes with 'unbounded variable' message printed on screen".

### Report Software Bugs Effectively
How you report software bugs greatly affects how fast it can be processed and fixed, refer to [How to Report Bugs Effectively](http://www.chiark.greenend.org.uk/~sgtatham/bugs.html) for more information

## Localize (Translate) the Software
If you are fluent in a language other than English, you may help this project by translating it to your language. This is called localization or L10N for short.  This software has already been internationalized so that it is capable of displaying different languages.

Also, please consider translating our documentation to the language that you are fluent in.

## Improving Documentation
The documentation of this project may be outdated through time, and needs help to keep it up to date.

### Manual Pages (manpages)
Refer to the following articles for reference on writing manpages:

* [Linux Man Page Howto](http://www.schweikhardt.net/man_page_howto.html)
* [The GNU Troff Manual: Macro Packages » man » Usage](https://www.gnu.org/software/groff/manual/html_node/Man-usage.html#Man-usage)

## Improving Code
There are so many aspects of the code that can be improved, however, please consider the following topics while doing so.

### Coding Style
It is required to mimic the coding style of the current code

#### Indentation
This project uses tab characters for indentation as it's width can be flexibly configured in many text editors

#### Padding Spaces
* Padding is required for operators
* Padding is avoided for the outer curly braces

#### Word Separating Method
NOTE: This currently only applies to the GNU Bash shell scripts.

* Underscore for variable names
* Underscore for function names

### Defensive Bash Programming
* All parameters that are assigned a value should be treated as read-only and remain unchanged throughout the code
* All parameters that are confirmed to not be used should be UNSET
* Function parameters should be caught by `local` parameters instead of directly referenced using positional parameter syntax

### Character Encoding of Files
We use UTF-8 encoding for all of our files

## Promote This Project to Others
It is appreciated if you share this project with others.  Also, if you write an article about this project, plese share it with us, we'd love to hear about it!

## Design Artwork/Logos for This Software
All current artwork is stored under src/data.  Please only use materials that are under a free license.

## Hints on Using the Git VCS
### Create commits based on minimal independent changes
Avoid creating commits that do multiple things at once as this will help other developers understand the change history.

### Write Comprehensible Commit Messages
Use concrete language on what the commit does in the commit message.

### Avoid Changing History That Has Been Pushed to Remote Repository
