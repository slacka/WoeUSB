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
import re
import subprocess


# Packed to class for clarity


def usb_drive(show_all=False):
    devices_list = []

    lsblk = subprocess.run(["lsblk",
                            "--output", "NAME",
                            "--noheadings",
                            "--nodeps"], stdout=subprocess.PIPE).stdout.decode("utf-8")

    devices = re.sub("sr[0-9]|cdrom[0-9]", "", lsblk).split()

    for device in devices:
        if is_removable_and_writable_device(device):
            if not show_all:
                continue

        # FIXME: Needs a more reliable detection mechanism instead of simply assuming it is under /dev
        block_device = "/dev/" + device

        device_capacity = subprocess.run(["lsblk",
                                          "--output", "SIZE",
                                          "--noheadings",
                                          "--nodeps",
                                          block_device], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

        device_model = subprocess.run(["lsblk",
                                       "--output", "MODEL",
                                       "--noheadings",
                                       "--nodeps",
                                       block_device], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

        if device_model != "":
            devices_list.append([block_device, block_device + "(" + device_model + ", " + device_capacity + ")"])
        else:
            devices_list.append([block_device, block_device + "(" + device_capacity + ")"])

    return devices_list


def is_removable_and_writable_device(block_device_name):
    sysfs_block_device_dir = "/sys/block/" + block_device_name

    # We consider device not removable if the removable sysfs item not exist
    if os.path.isfile(sysfs_block_device_dir + "/removable"):
        with open(sysfs_block_device_dir + "/removable") as removable:
            removable_content = removable.read()

        with open(sysfs_block_device_dir + "/ro") as ro:
            ro_content = ro.read()

        if removable_content.strip("\n") == "1" and ro_content.strip("\n") == "0":
            return 0
        else:
            return 1
    else:
        return 1


def dvd_drive():
    devices_list = []
    find = subprocess.run(["find", "/sys/block",
                           "-maxdepth", "1",
                           "-mindepth", "1"], stdout=subprocess.PIPE).stdout.decode("utf-8").split()
    devices = []
    for device in find:
        tmp = re.findall("sr[0-9]", device)

        if tmp == []:
            continue

        devices.append([device, tmp[0]])

    for device in devices:
        optical_disk_drive_devfs_path = "/dev/" + device[1]

        with open(device[0] + "/device/model", "r") as model:
            model_content = model.read().strip()

        devices_list.append([optical_disk_drive_devfs_path, optical_disk_drive_devfs_path + " - " + model_content])

    return devices_list
