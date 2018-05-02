#!/bin/python3

import subprocess
import os
from datetime import datetime

## Global Parameters
## Only set parameters global when there's no other way around(like passing in function as a function argument), usually when the variable is directly or indirectly referenced by traps
## Even when the parameter is set global, you should pass it in as function argument when it's possible for better code reusability.
## TODO: Global parameter cleanup
## TODO: Use Y/N or true/false instead 1(true)/0(false) as boolean value so it won't confuse with the regular bash intepretation of 0(true)/non-zero(false)
### Doing GUI-specific stuff when set to 1, set by --only-for-gui
### Requires to be set to global due to indirectly referenced by trap
global_only_for_gui = False

### Increase verboseness, provide more information when required
verbose = False

### Disable message coloring when set to 1, set by --no-color
no_color = False

DD_BLOCK_SIZE = 4 * 1024 * 1024 # 4MiB

## NOTE: Need to pass to traps, so need to be global
source_fs_mountpoint = "/media/woeusb_source_" + str(round((datetime.today() - datetime.fromtimestamp(0)).total_seconds())) + "_" + str(os.getpid())
target_fs_mountpoint = "/media/woeusb_target_" + str(round((datetime.today() - datetime.fromtimestamp(0)).total_seconds())) + "_" + str(os.getpid())
target_device = ""

## FIXME: No documentation for this non-trivial parameter
pulse_current_pid = 0

## Execution state for cleanup functions to determine if clean up is required
## NOTE: Need to pass to traps, so need to be global
current_state = 'pre-init'

## For some reason alias won't be recognized in function if it's definition's LINENO is greater then it's reference in function, so we define it here:
''' Needed in python ?
alias\
	echo_with_color=util_echo_with_color\
	switch_terminal_text_color=util_switch_terminal_text_color\
	shift_array=util_shift_array\
	is_target_busy=check_is_target_device_busy\
	printf_with_color=util_printf_with_color
'''
temp_directory = subprocess.run(["mktemp", "--tmpdir", "--directory", " WoeUSB.XXXXXX.tempdir"], stdout=subprocess.PIPE).stdout

def init(runtime_executable_name, only_for_gui_ref):
	global current_state

	application_name='WoeUSB'
	application_version='@@WOEUSB_VERSION@@'
	DEFAULT_NEW_FS_LABEL='Windows USB'

	current_state='enter-init'

	flag_print_help = "N"
	flag_print_version = "N"
	flag_print_about = "N"

	application_site_url = 'https://github.com/slacka/WoeUSB'
	application_copyright_declaration = "Copyright © Colin GILLE / congelli501 2013\\nCopyright © slacka et.al. 2017"
	application_copyright_notice = application_name + " is free software licensed under the GNU General Public License version 3(or any later version of your preference) that gives you THE 4 ESSENTIAL FREEDOMS\\nhttps://www.gnu.org/philosophy/"

	install_mode = ""

	# source_media may be a optical disk drive or a disk image
	# target_media may be an entire usb storage device or just a partition
	source_media = ""
	target_media = ""

	target_partition = ""

	workaround_bios_boot_flag = "N"


def print_help():
	pass
def print_version():
	pass
def print_application_info():
	pass
def process_commandline_parameters():
	pass
def process_miscellaneous_requests():
	pass
def check_runtime_dependencies():
	pass
def check_permission():
	pass
def check_runtime_parameters():
	pass
def determine_target_parameters():
	pass
def check_is_target_device_busy():
	pass
def check_source_and_target_not_busy():
	pass
def wipe_existing_partition_table_and_filesystem_signatures():
	pass
def check_if_the_drive_is_really_wiped():
	pass
def create_target_partition_table():
	pass
def workaround_make_system_realize_partition_table_changed():
	pass
def create_target_partition():
	pass
def create_uefi_ntfs_support_partition():
	pass
def install_uefi_ntfs_support_partition():
	pass
def workaround_buggy_motherboards_that_ignore_disks_without_boot_flag_toggled():
	pass
def check_target_partition():
	pass
def check_uefi_ntfs_support_partition():
	pass
def mount_source_filesystem():
	pass
def mount_target_filesystem():
	pass
def check_target_filesystem_free_space():
	pass
def copy_filesystem_files():
	pass
def copy_large_file():
	pass
def workaround_support_windows_7_uefi_boot():
	pass
def workaround_linux_make_writeback_buffering_not_suck():
	pass
def install_legacy_pc_bootloader_grub():
	pass
def install_legacy_pc_bootloader_grub_config():
	pass
def cleanup_mountpoints():
	pass
def trigger_wxGenericProgressDialog_pulse():
	pass
def trap_errexit():
	pass
def trap_exit():
	pass
def trap_interrupt():
	pass
def trap_return():
	pass
def trap_debug():
	pass
def util_call_external_command():
	pass
def util_switch_terminal_text_color():
	pass
def util_echo_with_color():
	pass
def util_printf_with_color():
	pass
def util_shift_array():
	pass
def util_is_parameter_set_and_not_empty():
	pass
def util_check_function_parameters_quantity():
	pass
def check_for_big_files():
	pass