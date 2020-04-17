# WoeUSB
[![Latest Release](https://img.shields.io/github/release/slacka/WoeUSB.svg)](https://github.com/slacka/WoeUSB/releases)
[![WoeUSB License](https://img.shields.io/badge/license-gpl-blue.svg)](https://github.com/slacka/WoeUSB/blob/master/COPYING)
[![Build Status](https://travis-ci.org/slacka/WoeUSB.svg?branch=master)](https://travis-ci.org/slacka/WoeUSB)

![brand](src/data/woeusb-logo.png)[![thumbnail of GUI wrapper screenshot](dev/woeusbgui-screenshot.thumbnail.png)](dev/woeusbgui-screenshot.png)[![thumbnail of CLI application screenshot](dev/woeusb-screenshot.thumbnail.png)](dev/woeusb-screenshot.png)

_A Linux program to create a Windows USB stick installer from a real Windows DVD or image._

This package contains two programs:

* woeusb: A command-line utility that enables you to create your own bootable Windows installation USB storage device from an existing Windows Installation disc or disk image
* woeusbgui: A GUI wrapper of woeusb based on WxWidgets

Supported images:

Windows Vista, Windows 7, Window 8.x, Windows 10. All languages and any version (home, pro...) and Windows PE are supported.

Supported bootmodes:

* Legacy/MBR-style/IBM PC compatible bootmode
* Native UEFI booting is supported for Windows 7 and later images (limited to the FAT filesystem as the target)

This project is a fork of [Congelli501's WinUSB software](http://en.congelli.eu/prog_info_winusb.html), which has not been maintained since 2012, according to the official website.

## Installation
### Prebuilt Packages
Note that prebuilt packages are not necessarily the latest release and we are NOT responsible for the trustworthiness of these packages.  Regarding any related issues contact its maintainer first.

#### Official Distribution Packages
* [Fedora](https://src.fedoraproject.org/rpms/WoeUSB) packages maintained by mprahl
* [openSUSE](https://software.opensuse.org/package/WoeUSB) packages maintained by [guoyunhe](https://guoyunhe.me/)
* [Gentoo](https://packages.gentoo.org/packages/sys-boot/woeusb) packages maintained by pacho

#### Third-party Distribution Packages
* [Arch Linux](https://aur.archlinux.org/packages/woeusb-git/) packages maintained by darkfm
* [Ubuntu](https://launchpad.net/%7Enilarimogard/+archive/ubuntu/webupd8) packages maintained by [WebUpd8](http://www.webupd8.org/)

### Build from Source
The following are the instructions to install WoeUSB if prebuilt version is not available or too old.

#### Acquire WoeUSB's Source Code
Clone WoeUSB's Git repository to your local machine using `git clone https://github.com/slacka/WoeUSB.git`

NOTE: We no longer support building from source archives provided in the GitHub Releases page as the software version is not set.

#### Setting the Application Version String
This step is required for generating the proper version name based on the Git tags. This step should be repeated if the version is changed.

```shell
$ ./setup-development-environment.bash
```

#### Install WoeUSB's Build Dependencies
```shell
# For Debian-based distributions (NOTE: For your convenience, this package is already provided in the release page)
$ sudo apt-get install devscripts equivs gdebi-core
$ cd <WoeUSB source tree directory, the folder that contains the `src` folder>
$ mk-build-deps # NOTE: Currently, due to Debian Bug #679101, this command will fail if the source path contains spaces.
$ sudo gdebi woeusb-build-deps_<version>_all.deb

# For Fedora > 22
$ sudo dnf install wxGTK3-devel

# For Fedora 22
$ sudo dnf install wxGTK-devel dh-autoreconf.noarch

# For Opensuse
$ sudo zypper in wxGTK3-3_2-devel dh-autoreconf devscripts
```
#### Build & Install WoeUSB
```shell
# For Debian-based distributions
$ dpkg-buildpackage -uc -b # NOTE: Currently, due to a bug in the build system, this command will fail if the source's path contains space or single quotes, refer to issue #84 for details
$ sudo gdebi ../woeusb_<version>_<architecture>.deb

# Generic method
$ autoreconf --force --install # Most non-Debian derived distros will need this
$ ./configure
$ make
$ sudo make install
```

When you go to use the program, if you get an error message with a code of 256, it means you need to format the disk you intend to flash the ISO to, and wipe it with no partition table. You can do this with GParted, or another wonderful tool.

## License
WoeUSB is distributed under the [GPL license](https://github.com/slacka/WoeUSB/blob/master/COPYING).
