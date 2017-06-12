# Contributing Guidelines
This documents explains how to contribute this project in many aspects, make sure to read them thoroughly before making any contributions

## Reporting Issues
The so-called "issue" includes but not limited to software bugs and suggestions

### Always search for duplicates before filing a new one
There is possibility that your issue is already been filed on the issue tracker, please search it before considering filing a new one

Use keywords instead of full sentences as search query, for example search "crash unbounded variable" instead of "The program crashes with 'unbounded variable' message printed on screen"

### Report Software Bugs Effectively
How you report software bugs greatly effects how fast it has been processed and fixed, refer [How to Report Bugs Effectively](http://www.chiark.greenend.org.uk/~sgtatham/bugs.html) for more information

## Improving Code
There's so many aspects of the code that can be improved, however please consider the following topics while doing so.

### Coding Style
It is required to mimic the coding style of the current code

#### Indentation
This project uses tab characters as indentation character as it's width can be flexibly configured in any modern text editors

#### Padding Spaces
* Padding are required for operators
* Padding are avoided for the outer of the curly braces

#### Word Separating Method
NOTE: Currently this only applies to the GNU Bash shell scripts.

* Underscore for variable names
* Underscore for function names

### Defensive Bash Programming
* READONLY all parameters that is assigned a value and is not changed in the rest of the code
* All parameters that is confirmed to not be used should be UNSET
* Function parameters should be catched by `local` paramters instead of directly referenced using positional parameter syntax

### Character Encoding of File
We use UTF-8 for all of our files

## Promote This Project to Others
It is welcomed to share this project to others so that they can try it.  Also if you write an article about this project plese share with us, we'd love to hear!

## Design Artwork/Logos for This Software
All current artworks are under src/data.  Please only use materials that are under a free license.