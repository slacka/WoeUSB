#!/usr/bin/python3

"""
This file is part of WoeUSB.

WoeUSB is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

WoeUSB is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with WoeUSB.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import subprocess
import time

import utils


def make_system_realize_partition_table_changed(target_device):
    """
    :param target_device:
    :return:
    """
    utils.print_with_color("Making system realize that partition table has changed...")

    subprocess.run(["blockdev", "--rereadpt", target_device])
    utils.print_with_color("Wait 3 seconds for block device nodes to populate...")

    time.sleep(3)


def buggy_motherboards_that_ignore_disks_without_boot_flag_toggled(target_device):
    """
    Some buggy BIOSes won't put detected device with valid MBR but no partitions with boot flag toggled into the boot menu, workaround this by setting the first partition's boot flag(which partition doesn't matter as GNU GRUB doesn't depend on it anyway

    :param target_device:
    :return:
    """
    utils.print_with_color(
        "Applying workaround for buggy motherboards that will ignore disks with no partitions with the boot flag toggled")

    subprocess.run(["parted", "--script",
                    target_device,
                    "set", "1", "boot", "on"])


def support_windows_7_uefi_boot(source_fs_mountpoint, target_fs_mountpoint):
    """
    As Windows 7's installation media doesn't place the required EFI
    bootloaders in the right location, we extract them from the
    system image manually

    :TODO: Functionize Windows 7 checking

    :param source_fs_mountpoint:
    :param target_fs_mountpoint:
    :return:
    """
    grep = subprocess.run(["grep", "--extended-regexp", "--quiet", "^MinServer=7[0-9]{3}\.[0-9]",
                           source_fs_mountpoint + "/sources/cversion.ini"],
                          stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
    if grep == "" and not os.path.isfile(source_fs_mountpoint + "/bootmgr.efi"):
        return 0

    utils.print_with_color(
        "Source media seems to be Windows 7-based with EFI support, applying workaround to make it support UEFI booting",
        "yellow")

    test_efi_directory = subprocess.run(["find", target_fs_mountpoint, "-ipath", target_fs_mountpoint + "/efi"],
                                        stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

    if test_efi_directory == "":
        efi_directory = target_fs_mountpoint + "/efi"
        if utils.verbose:
            print("DEBUG: Can't find efi directory, use " + efi_directory)
    else:
        efi_directory = test_efi_directory
        if utils.verbose:
            print("DEBUG: " + efi_directory + " detected.")

    test_efi_boot_directory = subprocess.run(["find", target_fs_mountpoint, "-ipath", target_fs_mountpoint + "/boot"],
                                             stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

    if test_efi_boot_directory == "":
        efi_boot_directory = target_fs_mountpoint + "/boot"
        if utils.verbose:
            print("DEBUG: Can't find efi/boot directory, use " + efi_boot_directory)
    else:
        efi_boot_directory = test_efi_boot_directory
        if utils.verbose:
            print("DEBUG: " + efi_boot_directory + " detected.")

    # If there's already an EFI bootloader existed, skip the workaround
    test_efi_bootloader = subprocess.run(
        ["find", target_fs_mountpoint, "-ipath", target_fs_mountpoint + "/efi/boot/boot*.efi"],
        stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

    if test_efi_bootloader != "":
        print("INFO: Detected existing EFI bootloader, workaround skipped.")
        return 0

    os.makedirs(efi_boot_directory, exist_ok=True)

    bootloader = subprocess.run(["7z",
                                 "e",
                                 "-so",
                                 source_fs_mountpoint + "/sources/install.wim",
                                 "Windows/Boot/EFI/bootmgfw.efi"], stdout=subprocess.PIPE).stdout

    with open(efi_boot_directory + "/bootx64.efi", "wb") as target_bootloader:
        target_bootloader.write(bootloader)


def linux_make_writeback_buffering_not_suck(mode):
    """
    :param mode: True - enable; False - disable
    """
    if mode:
        utils.print_with_color(
            "Applying workaround to prevent 64-bit systems with big primary memory from being unresponsive during copying files.",
            "yellow")

        vm_dirty_background_bytes = str(16 * 1024 * 1024)  # 16MiB
        vm_dirty_bytes = str(48 * 1024 * 1024)  # 48MiB
    else:
        utils.print_with_color(
            "Resetting workaround to prevent 64-bit systems with big primary memory from being unresponsive during copying files.",
            "yellow")

        vm_dirty_background_bytes = "0"
        vm_dirty_bytes = "0"

    with open("/proc/sys/vm/dirty_background_bytes", "w") as dirty_background_bytes:
        dirty_background_bytes.write(vm_dirty_background_bytes)

    with open("/proc/sys/vm/dirty_bytes", "w") as dirty_bytes:
        dirty_bytes.write(vm_dirty_bytes)
