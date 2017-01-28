# WinUSB
[![WinUSB Version](https://img.shields.io/badge/winusb-1.0.11-orange.svg)](https://github.com/slacka/WinUSB) 
[![WinUSB License](https://img.shields.io/badge/license-gpl-blue.svg)](https://github.com/slacka/WinUSB/blob/master/COPYING) 

<img src="winusb.jpg" align="right" />
<br>
_A Linux program to create Windows USB stick installer from a real Windows DVD or an image._

This package contains two programs:

* WinUSB-gui: a simple tool that enable you to create
	 your own usb stick windows installer from iso image
	 or a real DVD.
* winusb: the command line tool.

Supported images:

Windows Vista, Windows 7, Window 8, Windows 10. All languages and any version (home, pro...) and Windows PE are supported.

## Installation
### Acquire WinUSB's source code
Choose one of the following method:

* Download and extract source code archive from GitHub
* Cloning WinUSB's Git repository to local machine using `git clone https://github.com/slacka/WinUSB.git`

### Install WinUSB's build dependencies
```shell
# For Ubuntu
$ sudo apt-get install devscripts equivs gdebi-core
$ cd <WinUSB source code directory>
$ mk-build-deps debian/control # NOTE: Currently due to Debian Bug #679101 this command will fail if source path contains spaces.
$ sudo gdebi winusb-build-deps_<version>_all.deb

# For Fedora
$ sudo dnf install wxGTK3-devel
```
### Build and then install WinUSB
```
# For Ubuntu
$ dpkg-buildpackage -uc -b
$ sudo gdebi ../winusb_<version>_<architecture>.deb

# Generic
./configure
make
sudo make install
```

## License
winusb is sold under [GPL licence](https://github.com/slacka/WinUSB/blob/master/COPYING).
