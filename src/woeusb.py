#!/usr/bin/python3

# A Linux program to create bootable Windows USB stick from a real Windows DVD or an image
# Copyright © 2013 Colin GILLE / congelli501
# Copyright © 2017 slacka et. al.
# Python port - WaxyMocha
#
# This file is part of WoeUSB.
#
# WoeUSB is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WoeUSB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WoeUSB  If not, see <http://www.gnu.org/licenses/>.

import os
import time
import lzma
import shutil
import argparse
import tempfile
import traceback
import threading
import subprocess
import urllib.request
from datetime import datetime

import utils

application_name = 'WoeUSB'
application_version = '@@WOEUSB_VERSION@@'
DEFAULT_NEW_FS_LABEL = 'Windows USB'

application_site_url = 'https://github.com/slacka/WoeUSB'
application_copyright_declaration = "Copyright © Colin GILLE / congelli501 2013\\nCopyright © slacka et.al. 2017"
application_copyright_notice = application_name + " is free software licensed under the GNU General Public License version 3(or any later version of your preference) that gives you THE 4 ESSENTIAL FREEDOMS\\nhttps://www.gnu.org/philosophy/"

'''
Global Parameters
Only set parameters global when there's no other way around(like passing in function as a function argument), usually when the variable is directly or indirectly referenced by traps
Even when the parameter is set global, you should pass it in as function argument when it's possible for better code reusability.
TODO: Global parameter cleanup
Doing GUI-specific stuff when set to 1, set by --only-for-gui
Requires to be set to global due to indirectly referenced by trap
'''

# Increase verboseness, provide more information when required
verbose = False

debug = False

# NOTE: Need to pass to traps, so need to be global
# source_fs_mountpoint = ""
# target_fs_mountpoint = ""

# source_media may be a optical disk drive or a disk image
# target_media may be an entire usb storage device or just a partition
# source_media = ""
# target_media = ""

target_device = ""

CopyFiles_handle = threading.Thread()

# Execution state for cleanup functions to determine if clean up is required
# NOTE: Need to pass to traps, so need to be global
current_state = 'pre-init'

# temp_directory = b""
# install_mode = ""
gui = None


def init(from_cli=True, install_mode=None, source_media=None, target_media=None, workaround_bios_boot_flag=False,
         target_filesystem_type="FAT", filesystem_label=DEFAULT_NEW_FS_LABEL):
    source_fs_mountpoint = "/media/woeusb_source_" + str(
        round((datetime.today() - datetime.fromtimestamp(0)).total_seconds())) + "_" + str(os.getpid())
    target_fs_mountpoint = "/media/woeusb_target_" + str(
        round((datetime.today() - datetime.fromtimestamp(0)).total_seconds())) + "_" + str(os.getpid())

    temp_directory = tempfile.mkdtemp(prefix="WoeUSB.")

    verbose = False

    no_color = True

    debug = False

    parser = None

    if from_cli:
        parser = setup_arguments()
        args = parser.parse_args()

        if args.about:
            print_application_info()
            return 0

        if args.device:
            install_mode = "device"
        elif args.partition:
            install_mode = "partition"
        else:
            utils.print_with_color("You need to specify instalation type (--device or --partition")
            return 1

        # source_media may be a optical disk drive or a disk image
        # target_media may be an entire usb storage device or just a partition
        source_media = args.source
        target_media = args.target

        workaround_bios_boot_flag = args.workaround_bios_boot_flag

        target_filesystem_type = args.target_filesystem

        # Parameters that needs to be determined in runtime
        # due to different names in distributions

        filesystem_label = args.label

        verbose = args.verbose

        no_color = args.no_color

        debug = args.debug

    utils.no_color = no_color
    utils.gui = gui

    return [source_fs_mountpoint, target_fs_mountpoint, temp_directory, install_mode, source_media, target_media,
            workaround_bios_boot_flag, target_filesystem_type, filesystem_label, verbose, debug, parser]


def main(source_fs_mountpoint, target_fs_mountpoint, source_media, target_media, install_mode, temp_directory,
         target_filesystem_type, workaround_bios_boot_flag):
    global debug
    global verbose
    global no_color
    global current_state
    global target_device

    current_state = 'enter-init'

    command_mkdosfs, command_mkntfs, command_grubinstall = utils.check_runtime_dependencies(application_name)
    if command_grubinstall == "grub-install":
        name_grub_prefix = "grub"
    else:
        name_grub_prefix = "grub2"

    utils.print_with_color(application_name + " v" + application_version)
    utils.print_with_color("==============================")

    if os.getuid() != 0:
        utils.print_with_color("Warning: You are not running " + application_name + " as root!", "yellow")
        utils.print_with_color("Warning: This might be the reason of the following failure.", "yellow")

    if utils.check_runtime_parameters(install_mode, source_media, target_media):
        parser.print_help()
        return 1

    target_device, target_partition = utils.determine_target_parameters(install_mode, target_media)

    if utils.check_source_and_target_not_busy(install_mode, source_media, target_device, target_partition):
        return 1

    if install_mode == "device":
        wipe_existing_partition_table_and_filesystem_signatures(target_device)
        create_target_partition_table(target_device, "legacy")
        create_target_partition(target_device, target_partition, target_filesystem_type, target_filesystem_type,
                                command_mkdosfs,
                                command_mkntfs)

        if target_filesystem_type == "NTFS":
            create_uefi_ntfs_support_partition(target_device)
            install_uefi_ntfs_support_partition(target_device + "2", temp_directory)

    if install_mode == "partition":
        utils.check_target_partition(target_partition, install_mode, target_device)

    current_state = "start-mounting"

    if mount_source_filesystem(source_media, source_fs_mountpoint):
        utils.print_with_color("Error: Unable to mount source filesystem", "red")
        return 1

    if target_filesystem_type == "FAT":
        if utils.check_fat32_filesize_limitation(source_fs_mountpoint):
            return 1

    if mount_target_filesystem(target_partition, target_fs_mountpoint, target_filesystem_type):
        utils.print_with_color("Error: Unable to mount target filesystem", "red")
        return 1

    if utils.check_target_filesystem_free_space(target_fs_mountpoint, source_fs_mountpoint, target_partition):
        return 1

    current_state = "copying-filesystem"

    workaround_linux_make_writeback_buffering_not_suck(True)

    copy_filesystem_files(source_fs_mountpoint, target_fs_mountpoint)

    # workaround_support_windows_7_uefi_boot(source_fs_mountpoint, target_fs_mountpoint)

    install_legacy_pc_bootloader_grub(target_fs_mountpoint, target_device, command_grubinstall)

    install_legacy_pc_bootloader_grub_config(target_fs_mountpoint, target_device, command_grubinstall, name_grub_prefix)

    if workaround_bios_boot_flag:
        workaround_buggy_motherboards_that_ignore_disks_without_boot_flag_toggled(target_device)

    current_state = "finished"

    return 0


def print_application_info():
    print(application_name + " " + application_version)
    print(application_site_url)
    print(application_copyright_declaration)
    print(application_copyright_notice)


def wipe_existing_partition_table_and_filesystem_signatures(target_device):
    utils.print_with_color("Wiping all existing partition table and filesystem signatures in " + target_device, "green")
    subprocess.run(["wipefs", "--all", target_device])
    check_if_the_drive_is_really_wiped(target_device)


# Some broken locked-down flash drive will appears to be successfully wiped but actually nothing is written into it and will shown previous partition scheme afterwards.  This is the detection of the case and will bail out if such things happened
# target_device: The target device file to be checked


def check_if_the_drive_is_really_wiped(target_device):
    check_kill_signal()

    utils.print_with_color("Ensure that " + target_device + " is really wiped...")

    lsblk = subprocess.run(["lsblk", "--pairs", "--output", "NAME,TYPE", target_device], stdout=subprocess.PIPE).stdout

    grep = subprocess.Popen(["grep", "--count", "TYPE=\"part\""], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    if grep.communicate(input=lsblk)[0].decode("utf-8").strip() != "0":
        utils.print_with_color(
            "Error: Partition is still detected after wiping all signatures, this indicates that the drive might be locked into readonly mode due to end of lifespan.")
        return 1
    return 0


def create_target_partition_table(target_device, partition_table_type):
    check_kill_signal()

    utils.print_with_color("Creating new partition table on " + target_device + "...", "green")

    parted_partiton_table_argument = ""

    if partition_table_type in ["legacy", "msdos", "mbr", "pc"]:
        parted_partiton_table_argument = "msdos"
    elif partition_table_type in ["gpt", "guid"]:
        parted_partiton_table_argument = "gpt"
        utils.print_with_color("Error: Currently GUID partition table is not supported.", "red")
        return 2
    else:
        utils.print_with_color("Error: Partition table not supported.", "red")
        return 2

    # Create partition table(and overwrite the old one, whatever it was)
    subprocess.run(["parted", "--script", target_device, "mklabel", parted_partiton_table_argument])


def workaround_make_system_realize_partition_table_changed(target_device):
    utils.print_with_color("Making system realize that partition table has changed...")

    subprocess.run(["blockdev", "--rereadpt", target_device])
    utils.print_with_color("Wait 3 seconds for block device nodes to populate...")

    time.sleep(3)
    check_kill_signal()


def create_target_partition(target_device, target_partition, filesystem_type, filesystem_label, command_mkdosfs,
                            command_mkntfs):
    check_kill_signal()

    if filesystem_type in ["FAT", "vfat"]:
        parted_mkpart_fs_type = "fat32"
    elif filesystem_type in ["NTFS", "ntfs"]:
        parted_mkpart_fs_type = "ntfs"
    else:
        utils.print_with_color("Error: Filesystem not supported", "red")
        return 2

    utils.print_with_color("Creating target partition...", "green")

    # Create target partition
    # We start at 4MiB for grub (it needs a post-mbr gap for its code) and alignment of flash memery block erase segment in general, for details see http://www.gnu.org/software/grub/manual/grub.html#BIOS-installation and http://lwn.net/Articles/428584/
    # If NTFS filesystem is used we leave a 512KiB partition at the end for installing UEFI:NTFS partition for NTFS support
    if parted_mkpart_fs_type == "fat32":
        subprocess.run(["parted",
                        "--script",
                        target_device,
                        "mkpart",
                        "primary",
                        parted_mkpart_fs_type,
                        "4MiB",
                        "100%"])  # last sector of the disk
    elif parted_mkpart_fs_type == "ntfs":
        # Major partition for storing user files
        # NOTE: Microsoft Windows has a bug that only recognize the first partition for removable storage devices, that's why this partition should always be the first one
        subprocess.run(["parted",
                        "--script",
                        target_device,
                        "mkpart",
                        "primary",
                        parted_mkpart_fs_type,
                        "4MiB",
                        "--",
                        "-1025s"])  # Leave 512KiB==1024sector in traditional 512bytes/sector disk, disks with sector with more than 512bytes only result in partition size greater than 512KiB and is intentionally let-it-be.
    # FIXME: Leave exact 512KiB in all circumstances is better, but the algorithm to do so is quite brainkilling.
    else:
        utils.print_with_color("FATAL: Illegal parted_mkpart_fs_type, please report bug.", "green")

    check_kill_signal()

    workaround_make_system_realize_partition_table_changed(target_device)

    # Format target partition's filesystem
    if filesystem_type in ["FAT", "vfat"]:
        subprocess.run([command_mkdosfs, "-F", "32", target_partition])
    elif filesystem_type in ["NTFS", "ntfs"]:
        subprocess.run([command_mkntfs, "--quick", "--label", filesystem_label, target_partition])
    else:
        utils.print_with_color("FATAL: Shouldn't be here")
        return 1


def create_uefi_ntfs_support_partition(target_device):
    check_kill_signal()

    # FIXME: The partition type should be `fat12` but `fat12` isn't recognized by Parted...
    # NOTE: The --align is set to none because this partition is indeed misaligned, but ignored due to it's small size

    subprocess.run(["parted",
                    "--align", "none",
                    "--script",
                    target_device,
                    "mkpart",
                    "primary",
                    "fat16",
                    "--", "-1024s", "-1s"])


# Install UEFI:NTFS partition by writing the partition image into the created partition
# FIXME: Currently this requires internet access to download the image from GitHub directly, it should be replaced by including the image in our datadir
# uefi_ntfs_partition: The previously allocated partition for installing UEFI:NTFS, requires at least 512KiB
# download_directory: The temporary directory for downloading UEFI:NTFS image from GitHub
# target_device: For workaround_make_system_realize_partition_table_changed


def install_uefi_ntfs_support_partition(uefi_ntfs_partition, download_directory):
    check_kill_signal()

    try:
        file = urllib.request.urlretrieve("https://github.com/pbatard/rufus/raw/master/res/uefi/", "uefi-ntfs.img")[0]
    except urllib.request.ContentTooShortError:
        utils.print_with_color(
            "Warning: Unable to download UEFI:NTFS partition image from GitHub, installation skipped.  Target device might not be bootable if the UEFI firmware doesn't support NTFS filesystem.")
        return 1

    shutil.move(file, download_directory.decode("utf-8").strip() + "/" + file)  # move file to download_directory

    shutil.copy2(download_directory.decode("utf-8").strip() + "/uefi-ntfs.img", uefi_ntfs_partition)


# Some buggy BIOSes won't put detected device with valid MBR but no partitions with boot flag toggled into the boot menu, workaround this by setting the first partition's boot flag(which partition doesn't matter as GNU GRUB doesn't depend on it anyway


def workaround_buggy_motherboards_that_ignore_disks_without_boot_flag_toggled(target_device):
    check_kill_signal()

    utils.print_with_color(
        "Applying workaround for buggy motherboards that will ignore disks with no partitions with the boot flag toggled")

    subprocess.run(["parted", "--script",
                    target_device,
                    "set", "1", "boot", "on"])


def mount_source_filesystem(source_media, source_fs_mountpoint):
    check_kill_signal()

    utils.print_with_color("Mounting source filesystem...", "green")

    # os.makedirs(source_fs_mountpoint, exist_ok=True)

    if subprocess.run(["mkdir", "--parents", source_fs_mountpoint]).returncode != 0:
        utils.print_with_color("Error: Unable to create " + source_fs_mountpoint + " mountpoint directory", "red")
        return 1

    if os.path.isfile(source_media):
        if subprocess.run(["mount",
                           "--options", "loop,ro",
                           "--types", "udf,iso9660",
                           source_media,
                           source_fs_mountpoint]).returncode != 0:
            utils.print_with_color("Error: Unable to mount source media", "red")
            return 1
    else:
        if subprocess.run(["mount",
                           "--options", "ro",
                           source_media,
                           source_fs_mountpoint]).returncode != 0:
            utils.print_with_color("Error: Unable to mount source media", "red")
            return 1


# Mount target filesystem to existing path as mountpoint
# target_partition: The partition device file target filesystem resides, for example /dev/sdX1
# target_fs_mountpoint: The existing directory used as the target filesystem's mountpoint, for example /mnt/target_filesystem
# target_fs_type: The filesystem of the target filesystem currently supports: FAT, NTFS


def mount_target_filesystem(target_partition, target_fs_mountpoint, target_fs_type):
    check_kill_signal()

    utils.print_with_color("Mounting target filesystem...", "green")

    # os.makedirs(target_fs_mountpoint, exist_ok=True)

    if subprocess.run(["mkdir", "--parents", target_fs_mountpoint]).returncode != 0:
        utils.print_with_color("Error: Unable to create " + target_fs_mountpoint + " mountpoint directory", "red")
        return 1

    # Determine proper mount options according to filesystem type
    if target_fs_type == "FAT":
        mount_options = "utf8=1"
    elif target_fs_type == "NTFS":
        pass
    else:
        utils.print_with_color("Fatal: Unsupported target_fs_type, please report bug.", "red")

    if subprocess.run(["mount",
                       target_partition,
                       target_fs_mountpoint]).returncode != 0:
        utils.print_with_color("Error: Unable to mount target media", "red")
        return 1


# Copying all files from one filesystem to another, with progress reporting


def copy_filesystem_files(source_fs_mountpoint, target_fs_mountpoint):
    global CopyFiles_handle

    check_kill_signal()

    total_size = 0
    for dirpath, dirnames, filenames in os.walk(source_fs_mountpoint):
        for file in filenames:
            path = os.path.join(dirpath, file)
            total_size += os.path.getsize(path)

    utils.print_with_color("Copying files from source media...", "green")

    CopyFiles_handle = CopyFiles(source_fs_mountpoint, target_fs_mountpoint)
    CopyFiles_handle.start()

    for dirpath, _, filenames in os.walk(source_fs_mountpoint):
        check_kill_signal()
        if not os.path.isdir(target_fs_mountpoint + dirpath.replace(source_fs_mountpoint, "")):
            os.mkdir(target_fs_mountpoint + dirpath.replace(source_fs_mountpoint, ""))
        for file in filenames:
            path = os.path.join(dirpath, file)
            CopyFiles_handle.file = path
            shutil.copy2(path, target_fs_mountpoint + path.replace(source_fs_mountpoint, ""))

    CopyFiles_handle.stop = True


# As Windows 7's installation media doesn't place the required EFI
# bootloaders in the right location, we extract them from the
# system image manually
# TODO: Functionize Windows 7 checking


def workaround_support_windows_7_uefi_boot(source_fs_mountpoint, target_fs_mountpoint):
    global verbose

    check_kill_signal()

    grep = subprocess.run(["grep", "--extended-regexp", "--quiet", "^MinServer=7[0-9]{3}\.[0-9]",
                           source_fs_mountpoint + "/sources/cversion.ini"],
                          stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
    if grep == "" and not os.path.isfile(source_fs_mountpoint + "/bootmgr.efi"):
        return 0

    utils.print_with_color(
        "Source media seems to be Windows 7-based with EFI support, applying workaround to make it support UEFI booting",
        "yellow")

    efi_directory = ""
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

    efi_boot_directory = ""
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


def workaround_linux_make_writeback_buffering_not_suck(mode):
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


def install_legacy_pc_bootloader_grub(target_fs_mountpoint, target_device, command_grubinstall):
    check_kill_signal()

    utils.print_with_color("Installing GRUB bootloader for legacy PC booting support...", "green")

    subprocess.run([command_grubinstall,
                    "--target=i386-pc",
                    "--boot-directory=" + target_fs_mountpoint,
                    "--force", target_device])


# Install a GRUB config file to chainload Microsoft Windows's bootloader in Legacy PC bootmode
# target_fs_mountpoint: Target filesystem's mountpoint(where GRUB is installed)
# name_grub_prefix: May be different between distributions, so need to be specified (grub/grub2)


def install_legacy_pc_bootloader_grub_config(target_fs_mountpoint, target_device, command_grubinstall,
                                             name_grub_prefix):
    check_kill_signal()

    utils.print_with_color("Installing custom GRUB config for legacy PC booting...", "green")

    grub_cfg = target_fs_mountpoint + "/" + name_grub_prefix + "/grub.cfg"

    os.makedirs(target_fs_mountpoint + "/" + name_grub_prefix, exist_ok=True)

    cfg = open(grub_cfg, "w")
    cfg.write("ntldr /bootmgr\n")
    cfg.write("boot")
    cfg.close()


# Unmount mounted filesystems and clean-up mountpoints before exiting program
# exit status:
#     unclean(2): Not fully clean, target device can be safely detach from host
#     unsafe(3): Target device cannot be safely detach from host


def cleanup_mountpoint(fs_mountpoint):
    if os.path.ismount(fs_mountpoint):  # os.path.ismount() checks if path is a mount point
        utils.print_with_color("Unmounting and removing " + fs_mountpoint + "...", "green")
        if subprocess.run(["umount", fs_mountpoint]).returncode:
            utils.print_with_color("Warning: Unable to unmount filesystem.", "yellow")
            return 1

        try:
            os.rmdir(fs_mountpoint)
        except OSError:
            utils.print_with_color("Warning: Unable to remove source mountpoint", "yellow")
            return 2

    return 0


def cleanup(source_fs_mountpoint, target_fs_mountpoint, temp_directory):
    if CopyFiles_handle.is_alive():
        CopyFiles_handle.stop = True

    if current_state in ["copying-filesystem", "finished"]:
        workaround_linux_make_writeback_buffering_not_suck(False)

    flag_unclean = False
    flag_unsafe = False

    cleanup_result = cleanup_mountpoint(source_fs_mountpoint)

    if cleanup_result == 2:
        flag_unclean = True

    cleanup_result = cleanup_mountpoint(target_fs_mountpoint)

    if cleanup_result == 1:
        flag_unsafe = True
    elif cleanup_result == 2:
        flag_unclean = True

    if flag_unclean:
        utils.print_with_color("Some mountpoints are not unmount/cleaned successfully and must be done manually",
                               "yellow")

    if flag_unsafe:
        utils.print_with_color(
            "We unable to unmount target filesystem for you, please make sure target filesystem is unmounted before detaching to prevent data corruption",
            "yellow")
        utils.print_with_color("Some mountpoints are not unmount/cleaned successfully and must be done manually",
                               "yellow")

    if utils.check_is_target_device_busy(target_device):
        utils.print_with_color(
            "Target device is busy, please make sure you unmount all filesystems on target device or shutdown the computer before detaching it.",
            "yellow")
    else:
        utils.print_with_color("You may now safely detach the target device", "green")

    shutil.rmtree(temp_directory)

    if current_state == "finished":
        utils.print_with_color("Done :)", "green")
        utils.print_with_color("The target device should be bootable now", "green")


# Ok, you may asking yourself, what the f**k is this, and why is it called everywhere. Let me explain
# In python you can't just stop or kill thread, it must end its execution,
# or recognize moment where you want it to stop and politely perform euthanasia on itself.
# So, here, if gui is set, we throw exception which is going to be (hopefully) catch by GUI,
# simultaneously ending whatever script was doing meantime!
# Everyone goes to home happy and user is left with wrecked pendrive (just joking, next thing called by gui is cleanup)
# TODO: Put here more descriptive error

def check_kill_signal():
    if gui is not None:
        if gui.kill:
            raise KeyboardInterrupt


def setup_arguments():
    parser = argparse.ArgumentParser(
        description="WoeUSB can create a bootable Microsoft Windows(R) USB storage device from an existing Windows optical disk or an ISO disk image.")
    parser.add_argument("source", help="Source")
    parser.add_argument("target", help="Target")
    parser.add_argument("--device", "-d", action="store_true",
                        help="Completely WIPE the entire USB storage  device, then build a bootable Windows USB device from scratch.")
    parser.add_argument("--partition", "-p", action="store_true",
                        help="Copy Windows files to an existing partition of a USB storage device and make it bootable.  This allows files to coexist as long as no filename conflict exists.")

    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose mode")
    parser.add_argument("--version", "-V", action="version", version=application_version,
                        help="Print application version")
    parser.add_argument("--about", "-ab", action="store_true", help="Show info about this application")
    parser.add_argument("--no-color", action="store_true", help="Disable message coloring")
    parser.add_argument("--debug", action="store_true", help="Enable script debugging")
    parser.add_argument("--label", "-l", default="Windows USB",
                        help="Specify label for the newly created file system in --device creation method")
    parser.add_argument("--workaround-bios-boot-flag", action="store_true",
                        help="Workaround BIOS bug that won't include the device in boot menu if non of the partition's boot flag is toggled")
    parser.add_argument("--debugging-internal-function-call", metavar="<function>", default="",
                        help="Development option for developers to test certain function without running the entire build")
    parser.add_argument("--target-filesystem", "--tgt-fs", choices=["FAT", "NTFS"], default="FAT",
                        help="Specify the filesystem to use as the target partition's filesystem.")
    parser.add_argument('--for-gui', action="store_true", help=argparse.SUPPRESS)

    return parser


# Classes for threading module


class CopyFiles(threading.Thread):
    file = ""
    stop = False

    def __init__(self, source, target):
        threading.Thread.__init__(self)
        self.source = source
        self.target = target

    def run(self):
        source_size = utils.get_size(self.source)
        len_ = 0
        file_old = None

        while not self.stop:
            target_size = utils.get_size(self.target)

            if len_ != 0 and __name__ == "__main__":
                print('\033[3A')
                print(" " * len_)
                print(" " * 4)
                print('\033[3A')

            # Prevent printing same filenames
            if self.file != file_old:
                file_old = self.file
                utils.print_with_color(self.file.replace(self.source, ""))

            string = "Copied " + utils.convert_to_human_readable_format(
                target_size) + " from a total of " + utils.convert_to_human_readable_format(source_size)
            len_ = len(string)
            percentage = (target_size * 100) // source_size

            if __name__ != "__main__":
                gui.state = string
                gui.progress = percentage
            else:
                print(string)
                print(str(percentage) + "%")

            time.sleep(0.05)

        return 0


if __name__ == "__main__":
    source_fs_mountpoint, target_fs_mountpoint, temp_directory, \
        install_mode, source_media, target_media, \
        workaround_bios_boot_flag, target_filesystem_type, new_file_system_label, \
        verbose, debug, parser = init()
    try:
        main(source_fs_mountpoint, target_fs_mountpoint, source_media, target_media, install_mode, temp_directory,
             target_filesystem_type, workaround_bios_boot_flag)
    except KeyboardInterrupt:
        pass
    except Exception as error:
        utils.print_with_color(error, "red")
        if debug:
            traceback.print_exc()

    cleanup(source_fs_mountpoint, target_fs_mountpoint, temp_directory)
