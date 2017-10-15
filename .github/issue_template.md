## Good Habit Checklist for Issue Reporting
Checkout [Mastering Markdown · GitHub Guides](https://guides.github.com/features/mastering-markdown/#GitHub-flavored-markdown) if you needs help on the GitHub-flavored Markdown syntax.  You may remove sections and content that doesn't apply.

* [ ] I've searched the issue tracker and is pretty sure that there's no duplicate issue already filed.
* [ ] I've built the latest development snapshot using the instructions in README and verified that the issue can still be reproduced (for bug reports)

## Issue Reproduce Instructions
> 1. Launch WoeUSB by running `<command>`
> 2. <Do blablabla...>

## Expected Behavior
> No error

## Current Behavior
> WoeUSB errors with message "blablabla"

## Info of My Environment
### WoeUSB Version
> For build from source code, run `git describe --tags --always --dirty` under the source tree, for releases launch WoeUSB from the application menu then go to Help >> About and check the version line.

### GNU Bash Version
> WoeUSB exploits several advanced features of the Bash scripting language and requires a relatively-recent Bash intepreter.  Run `bash --version` in a terminal to acquire the information.

### Operating System Distribution Name and Version
> Different OS distributions provides different characteristics and may influence the result of running WoeUSB.  Run `lsb_release --description` or `lsb_release -d` in a terminal to acquire the information.

### Information about the Target Device
> Transcend JetFlash® 790K 64GB (USB 3.1 variant) 

### WoeUSB Commandline(if run with CLI(`woeusb`))
> sudo woeusb --device Windows9.iso /dev/sdx

### Source Media Info
> "Windows 9 Professional Edition" downloaded from <https://microsoft.com/download/windows-9>
