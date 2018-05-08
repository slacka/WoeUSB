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
import sys
import argparse
import subprocess
import pathlib
import time
import urllib.request
import shutil
import re
import traceback
import tempfile
from datetime import datetime

# Disable message coloring when set to 1, set by --no-color
no_color = False

# External tools
try:
    import termcolor
except ImportError:
    print("Module termcolor is not installed, text coloring disabled")
    no_color = True

# import parted  # Unused for now

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
TODO: Use Y/N or true/false instead 1(true)/0(false) as boolean value so it won't confuse with the regular bash intepretation of 0(true)/non-zero(false)
Doing GUI-specific stuff when set to 1, set by --only-for-gui
Requires to be set to global due to indirectly referenced by trap
'''
global_only_for_gui = False

# Increase verboseness, provide more information when required
verbose = False

debug = False

# NOTE: Need to pass to traps, so need to be global
source_fs_mountpoint = "/media/woeusb_source_" + str(
    round((datetime.today() - datetime.fromtimestamp(0)).total_seconds())) + "_" + str(os.getpid())
target_fs_mountpoint = "/media/woeusb_target_" + str(
    round((datetime.today() - datetime.fromtimestamp(0)).total_seconds())) + "_" + str(os.getpid())

target_device = ""

# FIXME: No documentation for this non-trivial parameter
pulse_current_pid = 0

# Execution state for cleanup functions to determine if clean up is required
# NOTE: Need to pass to traps, so need to be global
current_state = 'pre-init'

temp_directory = tempfile.mkdtemp(prefix="WoeUSB.")


def main(only_for_gui_ref):
    global current_state
    global verbose
    global no_color
    global target_device
    global debug

    parser = setup_arguments()
    args = parser.parse_args()

    if args.about:
        print_application_info()
        return 0

    current_state = 'enter-init'

    if args.device:
        install_mode = "device"
    elif args.partition:
        install_mode = "partition"
    else:
        print_with_color("You need to specify instalation type (--device or --partition")
        return 1

    # source_media may be a optical disk drive or a disk image
    # target_media may be an entire usb storage device or just a partition
    source_media = args.source
    target_media = args.target

    workaround_bios_boot_flag = args.workaround_bios_boot_flag

    target_filesystem_type = args.target_filesystem

    # Parameters that needs to be determined in runtime
    # due to different names in distributions

    new_file_system_label = args.label

    verbose = args.verbose

    if not no_color:
        no_color = args.no_color

    debug = args.debug

    command_mkdosfs, command_mkntfs, command_grubinstall = check_runtime_dependencies(application_name)
    if command_grubinstall == "grub-install":
        name_grub_prefix = "grub"
    else:
        name_grub_prefix = "grub2"

    print_with_color(application_name + " v" + application_version)
    print_with_color("==============================")

    if os.getuid() != 0:
        print_with_color("Warning: You are not running " + application_name + " as root!", "yellow")
        print_with_color("Warning: This might be the reason of the following failure.", "yellow")

    if check_runtime_parameters(install_mode, source_media, target_media):
        parser.print_help()
        return 1

    trigger_wxGenericProgressDialog_pulse("on", only_for_gui_ref)

    target_device, target_partition = determine_target_parameters(install_mode, target_media)

    if check_source_and_target_not_busy(install_mode, source_media, target_device, target_partition):
        return 1

    if install_mode == "device":
        wipe_existing_partition_table_and_filesystem_signatures(target_device)
        create_target_partition_table(target_device, "legacy")
        create_target_partition(target_partition, target_filesystem_type, new_file_system_label, command_mkdosfs,
                                command_mkntfs)

        if target_filesystem_type == "NTFS":
            create_uefi_ntfs_support_partition(target_device)
            install_uefi_ntfs_support_partition(target_device + "2", temp_directory)

    if install_mode == "partition":
        check_target_partition(target_partition, install_mode, target_device)

    current_state = "start-mounting"

    if mount_source_filesystem(source_media, source_fs_mountpoint):
        print_with_color("Error: Unable to mount source filesystem", "red")
        return 1

    if target_filesystem_type == "FAT":
        if check_for_big_files(source_fs_mountpoint):
            return 1

    if mount_target_filesystem(target_partition, target_fs_mountpoint, "vfat"):
        print_with_color("Error: Unable to mount target filesystem", "red")
        return 1

    if check_target_filesystem_free_space(target_fs_mountpoint, source_fs_mountpoint, target_partition):
        return 1

    current_state = "copying-filesystem"

    workaround_linux_make_writeback_buffering_not_suck(True)

    copy_filesystem_files(source_fs_mountpoint, target_fs_mountpoint, only_for_gui_ref)

    workaround_support_windows_7_uefi_boot(source_fs_mountpoint, target_fs_mountpoint)

    install_legacy_pc_bootloader_grub(target_fs_mountpoint, target_device, command_grubinstall)

    install_legacy_pc_bootloader_grub_config(target_fs_mountpoint, target_device, command_grubinstall, name_grub_prefix)

    if workaround_bios_boot_flag == "Y":
        workaround_buggy_motherboards_that_ignore_disks_without_boot_flag_toggled(target_device)

    current_state = "finished"

    trigger_wxGenericProgressDialog_pulse("off", only_for_gui_ref)

    return 0


def print_application_info():
    print(application_name + " " + application_version)
    print(application_site_url)
    print(application_copyright_declaration)
    print(application_copyright_notice)


def check_runtime_dependencies(application_name):
    result = "success"

    system_commands = ["mount", "wipefs", "lsblk", "blockdev", "df", "parted"]
    for command in system_commands:
        if shutil.which(command) == "":
            print_with_color(
                "Error: " + application_name + " requires " + command + " command in the executable search path, but it is not found.",
                "red")
            result = "failed"

    fat = ["mkdosfs", "mkfs.msdos", "mkfs.vfat", "mkfs.fat"]
    for command in fat:
        if shutil.which(command) != "":
            fat = command
            break

    if isinstance(fat, list):
        print_with_color("Error: mkdosfs/mkfs.msdos/mkfs.vfat/mkfs.fat command not found!", "red")
        print_with_color("Error: Please make sure that dosfstools is properly installed!", "red")
        result = "failed"

    ntfs = "mkntfs"
    if shutil.which("mkntfs") == "":
        print_with_color("Error: mkntfs command not found!", "red")
        print_with_color("Error: Please make sure that ntfs-3g is properly installed!", "red")
        result = "failed"

    grub = ["grub-install", "grub2-install"]
    for command in grub:
        if shutil.which(command) != "":
            grub = command
            break

    if isinstance(grub, list):
        print_with_color("Error: grub-install or grub2-install command not found!", "red")
        print_with_color("Error: Please make sure that GNU GRUB is properly installed!", "red")
        result = "failed"

    if result != "success":
        raise RuntimeError("Dependencies are not met")
    else:
        return [fat, ntfs, grub]


def check_runtime_parameters(install_mode, source_media, target_media):
    if not os.path.isfile(source_media) and not pathlib.Path(source_media).is_block_device():
        print_with_color(
            "Error: source media \"" + source_media + "\" not found or not a regular file or a block device file!",
            "red")
        return 1

    if not pathlib.Path(target_media).is_block_device():
        print_with_color("Error: Target media \"" + target_media + "\" is not a block device file!", "red")
        return 1

    if install_mode == "device" and target_media[-1].isdigit():
        print_with_color("Error: Target media \"" + target_media + "\" is not an entire storage device!", "red")
        return 1

    if install_mode == "partition" and not target_media[-1].isdigit():
        print_with_color("Error: Target media \"" + target_media + "\" is not an partition!", "red")
        return 1
    return 0


def determine_target_parameters(install_mode, target_media):
    if install_mode == "partition":
        target_partition = target_media

        while target_media[-1].isdigit():
            target_media = target_media[:-1]
        target_device = target_media
    else:
        target_device = target_media
        target_partition = target_media + str(1)

    if verbose:
        print_with_color("Info: Target device is " + target_device)
        print_with_color("Info: Target partition is " + target_partition)

    return [target_device, target_partition]


def check_is_target_device_busy(device):
    mount = subprocess.run("mount", stdout=subprocess.PIPE).stdout
    if re.findall(device, str(mount)) != []:
        return 1
    return 0


def check_source_and_target_not_busy(install_mode, source_media, target_device, target_partition):
    if check_is_target_device_busy(source_media):
        print_with_color("Error: Source media is currently mounted, unmount the partition then try again", "red")
        return 1

    if install_mode == "partition":
        if check_is_target_device_busy(target_partition):
            print_with_color("Error: Target partition is currently mounted, unmount the partition then try again",
                             "red")
            return 1
    else:
        if check_is_target_device_busy(target_device):
            print_with_color(
                "Error: Target device is currently busy, unmount all mounted partitions in target device then try again",
                "red")
            return 1


def wipe_existing_partition_table_and_filesystem_signatures(target_device):
    print_with_color("Wiping all existing partition table and filesystem signatures in " + target_device, "green")
    subprocess.run(["wipefs", "--all", target_device])
    check_if_the_drive_is_really_wiped(target_device)


# Some broken locked-down flash drive will appears to be successfully wiped but actually nothing is written into it and will shown previous partition scheme afterwards.  This is the detection of the case and will bail out if such things happened
# target_device: The target device file to be checked


def check_if_the_drive_is_really_wiped(target_device):
    print_with_color("Ensure that " + target_device + " is really wiped...")

    lsblk = subprocess.run(["lsblk", "--pairs", "--output", "NAME,TYPE", target_device], stdout=subprocess.PIPE).stdout

    grep = subprocess.Popen(["grep", "--count", "TYPE=\"part\""], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    if grep.communicate(input=lsblk)[0].decode("utf-8").strip() != "0":
        print_with_color(
            "Error: Partition is still detected after wiping all signatures, this indicates that the drive might be locked into readonly mode due to end of lifespan.")
        return 1
    return 0


def create_target_partition_table(target_device, partition_table_type):
    print_with_color("Creating new partition table on " + target_device + "...", "green")

    parted_partiton_table_argument = ""

    if partition_table_type in ["legacy", "msdos", "mbr", "pc"]:
        parted_partiton_table_argument = "msdos"
    elif partition_table_type in ["gpt", "guid"]:
        parted_partiton_table_argument = "gpt"
        print_with_color("Error: Currently GUID partition table is not supported.", "red")
        return 2
    else:
        print_with_color("Error: Partition table not supported.", "red")
        return 2

    # Create partition table(and overwrite the old one, whatever it was)
    subprocess.run(["parted", "--script", target_device, "mklabel", parted_partiton_table_argument])


def workaround_make_system_realize_partition_table_changed(target_device):
    print_with_color("Making system realize that partition table has changed...")

    subprocess.run(["blockdev", "--rereadpt", target_device])
    print_with_color("Wait 3 seconds for block device nodes to populate...")

    time.sleep(3)


def create_target_partition(target_partition, filesystem_type, filesystem_label, command_mkdosfs, command_mkntfs):
    parted_mkpart_fs_type = ""

    if filesystem_type in ["FAT", "vfat"]:
        parted_mkpart_fs_type = "fat32"
    elif filesystem_type in ["NTFS", "ntfs"]:
        parted_mkpart_fs_type = "ntfs"
    else:
        print_with_color("Error: Filesystem not supported", "red")
        return 2

    print_with_color("Creating target partition...", "green")

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
        print_with_color("FATAL: Illegal parted_mkpart_fs_type, please report bug.", "green")

    workaround_make_system_realize_partition_table_changed(target_device)

    # Format target partition's filesystem
    if filesystem_type in ["FAT", "vfat"]:
        subprocess.run([command_mkdosfs, "-F", "32", target_partition])
    elif filesystem_type in ["NTFS", "ntfs"]:
        subprocess.run([command_mkntfs, "--quick", "--label", filesystem_label, target_partition])
    else:
        print_with_color("FATAL: Shouldn't be here")
        return 1


def create_uefi_ntfs_support_partition(target_device):
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
    try:
        file = urllib.request.urlretrieve("https://github.com/pbatard/rufus/raw/master/res/uefi/", "uefi-ntfs.img")[0]
    except urllib.request.ContentTooShortError:
        print_with_color(
            "Warning: Unable to download UEFI:NTFS partition image from GitHub, installation skipped.  Target device might not be bootable if the UEFI firmware doesn't support NTFS filesystem.")
        return 1

    shutil.move(file, download_directory.decode("utf-8").strip() + "/" + file)  # move file to download_directory

    shutil.copy2(download_directory.decode("utf-8").strip() + "/uefi-ntfs.img", uefi_ntfs_partition)


# Some buggy BIOSes won't put detected device with valid MBR but no partitions with boot flag toggled into the boot menu, workaround this by setting the first partition's boot flag(which partition doesn't matter as GNU GRUB doesn't depend on it anyway


def workaround_buggy_motherboards_that_ignore_disks_without_boot_flag_toggled(target_device):
    print_with_color(
        "Applying workaround for buggy motherboards that will ignore disks with no partitions with the boot flag toggled")

    subprocess.run(["parted", "--script",
                    target_device,
                    "set", "1", "boot", "on"])


# Check target partition for potential problems before mounting them for --partition creation mode as we don't know about the existing partition
# target_partition: The target partition to check
# install_mode: The usb storage creation method to be used
# target_device: The parent device of the target partition, this is passed in to check UEFI:NTFS filesystem's existence on check_uefi_ntfs_support_partition


def check_target_partition(target_partition, install_mode, target_device):
    target_filesystem = subprocess.run(["lsblk",
                                        "--output", "FSTYPE",
                                        "--noheadings",
                                        target_partition], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

    if target_filesystem == "vfat":
        pass  # supported
    elif target_filesystem == "ntfs":
        check_uefi_ntfs_support_partition(target_device)
    else:
        print_with_color("Error: Target filesystem not supported, currently supported filesystem: FAT, NTFS.", "red")
        return 1

    return 0


# Check if the UEFI:NTFS support partition exists
# Currently it depends on the fact that this partition has a label of "UEFI_NTFS"
# target_device: The UEFI:NTFS partition residing entier device file


def check_uefi_ntfs_support_partition(target_device):
    lsblk = subprocess.run(["lsblk",
                            "--output", "LABEL",
                            "--noheadings",
                            target_device], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

    if re.findall("UEFI_NTFS", lsblk) != []:
        print_with_color(
            "Warning: Your device doesn't seems to have an UEFI:NTFS partition, UEFI booting will fail if the motherboard firmware itself doesn't support NTFS filesystem!")
        print_with_color(
            "Info: You may recreate disk with an UEFI:NTFS partition by using the --device creation method")


def mount_source_filesystem(source_media, source_fs_mountpoint):
    print_with_color("Mounting source filesystem...", "green")

    # os.makedirs(source_fs_mountpoint, exist_ok=True)

    if subprocess.run(["mkdir", "--parents", source_fs_mountpoint]).returncode != 0:
        print_with_color("Error: Unable to create " + source_fs_mountpoint + " mountpoint directory", "red")
        return 1

    if os.path.isfile(source_media):
        if subprocess.run(["mount",
                           "--options", "loop,ro",
                           "--types", "udf,iso9660",
                           source_media,
                           source_fs_mountpoint]).returncode != 0:
            print_with_color("Error: Unable to mount source media", "red")
            return 1
    else:
        if subprocess.run(["mount",
                           "--options", "ro",
                           source_media,
                           source_fs_mountpoint]).returncode != 0:
            print_with_color("Error: Unable to mount source media", "red")
            return 1


# Mount target filesystem to existing path as mountpoint
# target_partition: The partition device file target filesystem resides, for example /dev/sdX1
# target_fs_mountpoint: The existing directory used as the target filesystem's mountpoint, for example /mnt/target_filesystem
# target_fs_type: The filesystem of the target filesystem, this is same as the --types argument of mount(8), currently supports: vfat


def mount_target_filesystem(target_partition, target_fs_mountpoint, target_fs_type):
    mount_options = "defaults"

    print_with_color("Mounting target filesystem...", "green")

    # os.makedirs(target_fs_mountpoint, exist_ok=True)

    if subprocess.run(["mkdir", "--parents", target_fs_mountpoint]).returncode != 0:
        print_with_color("Error: Unable to create " + target_fs_mountpoint + " mountpoint directory", "red")
        return 1

    # Determine proper mount options according to filesystem type
    if target_fs_type == "vfat":
        mount_options = "utf8=1"
    else:
        print_with_color("Fatal: Unsupported target_fs_type, please report bug.", "red")

    if subprocess.run(["mount",
                       target_partition,
                       target_fs_mountpoint]).returncode != 0:
        print_with_color("Error: Unable to mount target media", "red")
        return 1


# TODO: add free_space_human_readable and needed_space_human_readable
def check_target_filesystem_free_space(target_fs_mountpoint, source_fs_mountpoint, target_partition):
    df = subprocess.run(["df",
                         "--block-size=1",
                         target_fs_mountpoint], stdout=subprocess.PIPE).stdout
    # free_space = int(df.strip().split()[4])

    awk = subprocess.Popen(["awk", "{print $4}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    free_space = awk.communicate(input=df)[0]
    free_space = free_space.decode("utf-8").strip()
    free_space = re.sub("[^0-9]", "", free_space)
    free_space = int(free_space)

    needed_space = 0
    for dirpath, dirnames, filenames in os.walk(source_fs_mountpoint):
        for file in filenames:
            path = os.path.join(dirpath, file)
            needed_space += os.path.getsize(path)

    additional_space_required_for_grub_installation = 1000 * 1000 * 10  # 10MiB

    needed_space += additional_space_required_for_grub_installation

    if needed_space > free_space:
        print_with_color("Error: Not enough free space on target partition!")
        print_with_color(
            "Error: We required ${needed_space_human_readable}(" + needed_space + " bytes) but '" + target_partition + "' only has ${free_space_human_readable}(" + free_space + " bytes).")
        return 1


# Copying all files from one filesystem to another, with progress reporting


def copy_filesystem_files(source_fs_mountpoint, target_fs_mountpoint, only_for_gui):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(source_fs_mountpoint):
        for file in filenames:
            path = os.path.join(dirpath, file)
            total_size += os.path.getsize(path)

    # FIXME: Why do we `trigger_wxGenericProgressDialog_pulse off` and on here?
    trigger_wxGenericProgressDialog_pulse("off", only_for_gui)

    print_with_color("Copying files from source media...", "green")

    for item in os.listdir(source_fs_mountpoint):
        source = os.path.join(source_fs_mountpoint, item)
        target = os.path.join(target_fs_mountpoint, item)

        if os.path.islink(source):  # Do not copy links
            continue
        elif os.path.isdir(source):
            if os.path.exists(target):  # if target dir exists, remove it
                shutil.rmtree(target)

            shutil.copytree(source, target)
        else:
            if os.path.exists(target):  # if target file exists, remove it
                os.remove(target)

            shutil.copy2(source, target)


def workaround_support_windows_7_uefi_boot(source_fs_mountpoint, target_fs_mountpoint):
    pass


def workaround_linux_make_writeback_buffering_not_suck(mode):
    VM_DIRTY_BACKGROUND_BYTES = str(16 * 1024 * 1024)  # 16MiB
    VM_DIRTY_BYTES = str(48 * 1024 * 1024)  # 48MiB

    if mode:
        print_with_color(
            "Applying workaround to prevent 64-bit systems with big primary memory from being unresponsive during copying files.",
            "yellow")

        dirty_background_bytes = open("/proc/sys/vm/dirty_background_bytes", "w")
        dirty_background_bytes.write(VM_DIRTY_BACKGROUND_BYTES)
        dirty_background_bytes.close()

        dirty_bytes = open("/proc/sys/vm/dirty_bytes", "w")
        dirty_bytes.write(VM_DIRTY_BYTES)
        dirty_bytes.close()
    else:
        print_with_color(
            "Resetting workaround to prevent 64-bit systems with big primary memory from being unresponsive during copying files.",
            "yellow")

        dirty_background_bytes = open("/proc/sys/vm/dirty_background_bytes", "w")
        dirty_background_bytes.write("0")
        dirty_background_bytes.close()

        dirty_bytes = open("/proc/sys/vm/dirty_bytes", "w")
        dirty_bytes.write("0")
        dirty_bytes.close()


def install_legacy_pc_bootloader_grub(target_fs_mountpoint, target_device, command_grubinstall):
    print_with_color("Installing GRUB bootloader for legacy PC booting support...", "green")

    subprocess.run([command_grubinstall,
                    "--target=i386-pc",
                    "--boot-directory=" + target_fs_mountpoint,
                    "--force", target_device])


# Install a GRUB config file to chainload Microsoft Windows's bootloader in Legacy PC bootmode
# target_fs_mountpoint: Target filesystem's mountpoint(where GRUB is installed)
# name_grub_prefix: May be different between distributions, so need to be specified (grub/grub2)


def install_legacy_pc_bootloader_grub_config(target_fs_mountpoint, target_device, command_grubinstall,
                                             name_grub_prefix):
    print_with_color("Installing custom GRUB config for legacy PC booting...", "green")

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


def cleanup_mountpoints(source_fs_mountpoint, target_fs_mountpoint, only_for_gui):
    clean_result = "unknown"

    trigger_wxGenericProgressDialog_pulse("off", only_for_gui)

    if os.path.ismount(source_fs_mountpoint):  # os.path.ismount() checks if path is a mount point
        print_with_color("Unmounting and removing " + source_fs_mountpoint + "...", "green")
        if not subprocess.run(["umount", source_fs_mountpoint]).returncode:
            try:
                os.rmdir(source_fs_mountpoint)
            except OSError:
                print_with_color("Warning: Unable to remove source mountpoint", "yellow")
                clean_result = "unclean"
        else:
            print_with_color("Warning: Unable to unmount source filesystem.", "yellow")
            clean_result = "unclean"

    if os.path.ismount(target_fs_mountpoint):  # os.path.ismount() checks if path is a mount point
        print_with_color("Unmounting and removing " + target_fs_mountpoint + "...", "green")
        if not subprocess.run(["umount", target_fs_mountpoint]).returncode:
            try:
                os.rmdir(target_fs_mountpoint)
            except OSError:
                print_with_color("Warning: Unable to remove target mountpoint", "yellow")
                clean_result = "unclean"
        else:
            print_with_color("Warning: Unable to unmount target filesystem.", "yellow")
            clean_result = "unsafe"

    if clean_result == "unclean":
        return 2
    elif clean_result == "unsafe":
        return 3
    else:
        return 0


def trigger_wxGenericProgressDialog_pulse(swich, only_for_gui):
    pass


def check_for_big_files(source_fs_mountpoint):
    for dirpath, dirnames, filenames in os.walk(source_fs_mountpoint):
        for file in filenames:
            path = os.path.join(dirpath, file)
            if os.path.getsize(path) > (2 ** 32) - 1:  # Max fat32 file size
                print_with_color(
                    "Error: File $file is larger than that supported by the fat32 filesystem. Use NTFS (--target-filesystem NTFS).",
                    "red")
                return 1
    return 0


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
    parser.add_argument("--no_color", action="store_true", help="Disable message coloring")
    parser.add_argument("--debug", action="store_true", help="Enable script debugging")
    parser.add_argument("--label", "-l", default="Windows USB",
                        help="Specify label for the newly created file system in --device creation method")
    parser.add_argument("--workaround_bios_boot_flag", action="store_true",
                        help="Workaround BIOS bug that won't include the device in boot menu if non of the partition's boot flag is toggled")
    parser.add_argument("--debugging_internal_function_call", metavar="<function>", default="",
                        help="Development option for developers to test certain function without running the entire build")
    parser.add_argument("--target_filesystem", "--tgt-fs", choices=["FAT", "NTFS"], default="FAT",
                        help="Specify the filesystem to use as the target partition's filesystem.")

    return parser


# Print function
# This function takes into account no_color flag
# Second parameter take color of text, default is no color


def print_with_color(text, color=""):
    if no_color or color == "":
        sys.stdout.write(text + "\n")
    else:
        termcolor.cprint(text, color)


try:
    main(global_only_for_gui)
except KeyboardInterrupt:
    pass
except Exception as error:
    print_with_color(error, "red")
    if debug:
        traceback.print_exc()

if current_state in ["copying-filesystem", "finished"]:
    workaround_linux_make_writeback_buffering_not_suck(False)

cleanup_result = cleanup_mountpoints(source_fs_mountpoint, target_fs_mountpoint, global_only_for_gui)
if cleanup_result == 2:
    print_with_color("Some mountpoints are not unmount/cleaned successfully and must be done manually", "yellow")
elif cleanup_result == 3:
    print_with_color("We unable to unmount target filesystem for you, please make sure target filesystem is unmounted before detaching to prevent data corruption", "yellow")
    print_with_color("Some mountpoints are not unmount/cleaned successfully and must be done manually", "yellow")

if check_is_target_device_busy(target_device):
    print_with_color("Target device is busy, please make sure you unmount all filesystems on target device or shutdown the computer before detaching it.", "yellow")
else:
    print_with_color("You may now safely detach the target device", "green")

shutil.rmtree(temp_directory)

if current_state == "finished":
    print_with_color("Done :)", "green")
    print_with_color("The target device should be bootable now", "green")
