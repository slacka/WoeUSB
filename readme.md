# WinUSB
[![WinUSB Version](https://img.shields.io/badge/winusb-1.0.11-orange.svg)](https://github.com/slacka/WinUSB) 
[![WinUSB License](https://img.shields.io/badge/license-gpl-blue.svg)](https://github.com/slacka/WinUSB/blob/master/COPYING) 

<img src="/doc/WinUSB.png" align="right" />
<br>
_A Linux program to create Windows USB stick installer from a real Windows DVD or an image._

This package contains two programs:

* WinUSB-gui: a simple tool that enable you to create
	 your own usb stick windows installer from iso image
	 or a real DVD.
* winusb: the command line tool.

Supported images:

Windows Vista, Windows 7, Window 8, Windows 10. All languages and any version (home, pro...) and Windows PE are supported.

## Installation:
```
git clone https://github.com/slacka/WinUSB.git
sudo apt install libwxgtk3.0-dev 
./configure
make
sudo make install
```
## Running
```
winusb
```

## License
winusb is sold under [GPL licence](https://github.com/slacka/WinUSB/blob/master/COPYING).
