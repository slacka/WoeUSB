# WoeUSB
[![Latest Release](https://img.shields.io/github/release/slacka/WoeUSB.svg)](https://github.com/slacka/WoeUSB/releases)
[![WoeUSB License](https://img.shields.io/badge/license-gpl-blue.svg)](https://github.com/slacka/WoeUSB/blob/master/COPYING)
[![Build Status](https://travis-ci.org/slacka/WoeUSB.svg?branch=master)](https://travis-ci.org/slacka/WoeUSB)

<img src="src/data/woeusb-logo.png" align="right" />
_A Linux program to create Windows USB stick installer from a real Windows DVD or an image._

This package contains two programs:

* woeusbgui: a simple tool that enable you to create
	 your own usb stick windows installer from iso image
	 or a real DVD.
* woeusb: the command line tool.

Supported images:

Windows Vista, Windows 7, Window 8, Windows 10. All languages and any version (home, pro...) and Windows PE are supported.

Supported bootmodes:

* Legacy/MBR-style/IBM PC compatible bootmode
* Native UEFI booting is supported for Windows 7 and later images(with a limitation of only FAT filesystem can be used as target filesystem)

This project is a fork of [Congelli501's WinUSB software](http://en.congelli.eu/prog_info_winusb.html), which is not maintained since 2012, according to the official website.

## Installation
Following is the instructions to install WoeUSB if your Linux distro's packaged version is not available or too old.

### Acquire WoeUSB's source code
Clone WoeUSB's Git repository to local machine using `git clone https://github.com/slacka/WoeUSB.git`

NOTE: We no longer support building from source archive provided in the GitHub Releases page as the software version is not set.

### Setting application version string
This step is required for generating proper version name from Git tags, it should be redone if the version is changed

```shell
$ ./setup-development-environment.bash
```

### Install WoeUSB's build dependencies
```shell
# For Ubuntu
$ sudo apt-get install devscripts equivs gdebi-core
$ cd <WoeUSB source code directory>
$ mk-build-deps # NOTE: Currently due to Debian Bug #679101 this command will fail if source path contains spaces.
$ sudo gdebi woeusb-build-deps_<version>_all.deb

# For Fedora
$ sudo dnf install wxGTK3-devel
```
### Build & install WoeUSB
```shell
# For Ubuntu
$ dpkg-buildpackage -uc -b # NOTE: Currently due to bug in the build system this command will fail if source's path contains space or single quotes, refer issue #84 for details
$ sudo gdebi ../woeusb_<version>_<architecture>.deb

# Generic method
$ ./configure
$ make
$ sudo make install
```

## License
WoeUSB is sold under the [GPL license](https://github.com/slacka/WoeUSB/blob/master/COPYING).
