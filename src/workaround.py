#!/usr/bin/python3

import os
import lzma
import subprocess
import time

import utils

def make_system_realize_partition_table_changed(target_device):
    utils.print_with_color("Making system realize that partition table has changed...")

    subprocess.run(["blockdev", "--rereadpt", target_device])
    utils.print_with_color("Wait 3 seconds for block device nodes to populate...")

    time.sleep(3)


# Some buggy BIOSes won't put detected device with valid MBR but no partitions with boot flag toggled into the boot menu, workaround this by setting the first partition's boot flag(which partition doesn't matter as GNU GRUB doesn't depend on it anyway


def buggy_motherboards_that_ignore_disks_without_boot_flag_toggled(target_device):
    utils.print_with_color(
        "Applying workaround for buggy motherboards that will ignore disks with no partitions with the boot flag toggled")

    subprocess.run(["parted", "--script",
                    target_device,
                    "set", "1", "boot", "on"])


# As Windows 7's installation media doesn't place the required EFI
# bootloaders in the right location, we extract them from the
# system image manually
# TODO: Functionize Windows 7 checking


def support_windows_7_uefi_boot(source_fs_mountpoint, target_fs_mountpoint):
    global verbose

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
        if verbose:
            print("DEBUG: Can't find efi directory, use " + efi_directory)
    else:
        efi_directory = test_efi_directory
        if verbose:
            print("DEBUG: " + efi_directory + " detected.")

    test_efi_boot_directory = subprocess.run(["find", target_fs_mountpoint, "-ipath", target_fs_mountpoint + "/boot"],
                                             stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

    if test_efi_boot_directory == "":
        efi_boot_directory = target_fs_mountpoint + "/boot"
        if verbose:
            print("DEBUG: Can't find efi/boot directory, use " + efi_boot_directory)
    else:
        efi_boot_directory = test_efi_boot_directory
        if verbose:
            print("DEBUG: " + efi_boot_directory + " detected.")

    # If there's already an EFI bootloader existed, skip the workaround
    test_efi_bootloader = subprocess.run(
        ["find", target_fs_mountpoint, "-ipath", target_fs_mountpoint + "/efi/boot/boot*.efi"],
        stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

    if test_efi_bootloader != "":
        print("INFO: Detected existing EFI bootloader, workaround skipped.")
        return 0

    os.makedirs(efi_boot_directory)

    wim = lzma.open(source_fs_mountpoint + "/sources/install.wim", mode="rb").read()

    file = open(efi_boot_directory + "/bootx64.efi", mode="wb")
    file.write(wim)
    file.close()


def linux_make_writeback_buffering_not_suck(mode):
    VM_DIRTY_BACKGROUND_BYTES = str(16 * 1024 * 1024)  # 16MiB
    VM_DIRTY_BYTES = str(48 * 1024 * 1024)  # 48MiB

    if mode:
        utils.print_with_color(
            "Applying workaround to prevent 64-bit systems with big primary memory from being unresponsive during copying files.",
            "yellow")

        dirty_background_bytes = open("/proc/sys/vm/dirty_background_bytes", "w")
        dirty_background_bytes.write(VM_DIRTY_BACKGROUND_BYTES)
        dirty_background_bytes.close()

        dirty_bytes = open("/proc/sys/vm/dirty_bytes", "w")
        dirty_bytes.write(VM_DIRTY_BYTES)
        dirty_bytes.close()
    else:
        utils.print_with_color(
            "Resetting workaround to prevent 64-bit systems with big primary memory from being unresponsive during copying files.",
            "yellow")

        dirty_background_bytes = open("/proc/sys/vm/dirty_background_bytes", "w")
        dirty_background_bytes.write("0")
        dirty_background_bytes.close()

        dirty_bytes = open("/proc/sys/vm/dirty_bytes", "w")
        dirty_bytes.write("0")
        dirty_bytes.close()
