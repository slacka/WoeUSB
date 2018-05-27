#!/usr/bin/python3

import os
import re
import time
import threading
import subprocess

import wx
import wx.adv

import woeusb


class MainFrame(wx.Frame):
    __MainPanel = None
    __MenuBar = None

    __menuItemShowAll = None

    def __init__(self, title, pos, size, style=wx.DEFAULT_FRAME_STYLE):
        super(MainFrame, self).__init__(None, -1, title, pos, size, style)

        file_menu = wx.Menu()
        self.__menuItemShowAll = wx.MenuItem(file_menu, wx.ID_ANY, "Show all drives \tCtrl+A",
                                             "Show all drives, even those not detected as USB stick.", wx.ITEM_CHECK)
        file_menu.Append(self.__menuItemShowAll)

        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT)

        help_menu = wx.Menu()
        help_item = help_menu.Append(wx.ID_ABOUT)

        self.__MenuBar = wx.MenuBar()
        self.__MenuBar.Append(file_menu, "&File")
        self.__MenuBar.Append(help_menu, "&Help")

        self.SetMenuBar(self.__MenuBar)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.__MainPanel = MainPanel(self, wx.ID_ANY)
        main_sizer.Add(self.__MainPanel, 1, wx.EXPAND | wx.ALL, 4)

        self.SetSizer(main_sizer)

        # self.Connect(self.__menuItemShowAll.GetId(), wx.EVT_MENU, MainPanel.on_show_all_drive, None, self.__MainPanel)
        self.Bind(wx.EVT_MENU, self.__MainPanel.on_show_all_drive)

        self.Bind(wx.EVT_MENU, self.on_quit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_about, help_item)

    def on_quit(self, _):
        self.Close(True)

    def on_about(self, _):
        my_dialog_about = DialogAbout(self, wx.ID_ANY)
        my_dialog_about.ShowModal()

    def enable_buttons(self, adrSelected):
        pass

    def is_show_all_checked(self):
        return self.__menuItemShowAll.IsChecked()


class MainPanel(wx.Panel):
    __parent = None

    __dvdDriveList = None
    __usbStickList = wx.ListBox

    __dvdDriveDevList = []
    __usbStickDevList = []

    __isoFile = wx.FilePickerCtrl

    __parentFrame = None

    __btInstall = None
    __btRefresh = None

    __isoChoice = None
    __dvdChoice = None

    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL):
        super(MainPanel, self).__init__(parent, ID, pos, size, style)

        self.__parent = parent

        # Controls
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Iso / CD
        main_sizer.Add(wx.StaticText(self, wx.ID_ANY, "Source :"), 0, wx.ALL, 3)

        # Iso
        self.__isoChoice = wx.RadioButton(self, wx.ID_ANY, "From a disk image (iso)")
        main_sizer.Add(self.__isoChoice, 0, wx.ALL, 3)

        tmp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tmp_sizer.AddSpacer(20)
        self.__isoFile = wx.FilePickerCtrl(self, wx.ID_ANY, "", "Please select a disk image",
                                           "Iso images (*.iso)|*.iso;*.ISO|All files|*")
        tmp_sizer.Add(self.__isoFile, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM, 3)
        main_sizer.Add(tmp_sizer, 0, wx.EXPAND, 0)

        # DVD
        self.__dvdChoice = wx.RadioButton(self, wx.ID_ANY, "From a CD/DVD drive")
        main_sizer.Add(self.__dvdChoice, 0, wx.ALL, 3)

        # List
        tmp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tmp_sizer.AddSpacer(20)
        self.__dvdDriveList = wx.ListBox(self, wx.ID_ANY)
        tmp_sizer.Add(self.__dvdDriveList, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 3)
        main_sizer.Add(tmp_sizer, 1, wx.EXPAND, 0)

        # Target
        main_sizer.AddSpacer(20)

        main_sizer.Add(wx.StaticText(self, wx.ID_ANY, "Target device :"), 0, wx.ALL, 3)

        # List
        self.__usbStickList = wx.ListBox(self, wx.ID_ANY)
        main_sizer.Add(self.__usbStickList, 1, wx.EXPAND | wx.ALL, 3)

        '''
        tmp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tmp_sizer.Add(wx.StaticText(self, wx.ID_ANY, "Filesystem: "), 0, wx.CENTER, 2)

        filesystem = wx.Choice(self, choices=["FAT", "NTFS"])
        filesystem.SetSelection(0)
        tmp_sizer.Add(filesystem, 1, wx.RIGHT | wx.LEFT, 1)

        boot_flag = wx.CheckBox(self, label="Toggle boot flag")
        tmp_sizer.Add(boot_flag, 1, wx.CENTER | wx.RIGHT, 1)

        main_sizer.Add(tmp_sizer, 0, wx.Left, 3)

        main_sizer.AddSpacer(20)

        tmp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tmp_sizer.Add(wx.StaticText(self, wx.ID_ANY, "Label: "), 0, wx.CENTER, 2)

        text = wx.TextCtrl(self)
        tmp_sizer.Add(text, 1, wx.EXPAND, 1)

        main_sizer.Add(tmp_sizer, 0, wx.Left, 3)
        '''

        # Buttons
        main_sizer.AddSpacer(30)

        bt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__btRefresh = wx.Button(self, wx.ID_REFRESH)
        bt_sizer.Add(self.__btRefresh, 0, wx.ALL, 3)
        self.__btInstall = wx.Button(self, wx.ID_ANY, "Install")
        bt_sizer.Add(self.__btInstall, 0, wx.ALL, 3)

        main_sizer.Add(bt_sizer, 0, wx.ALIGN_RIGHT, 0)

        # Finalization
        self.SetSizer(main_sizer)

        self.Bind(wx.EVT_LISTBOX, self.on_list_or_file_modified, self.__usbStickList)
        self.Bind(wx.EVT_LISTBOX, self.on_list_or_file_modified, self.__dvdDriveList)
        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_list_or_file_modified, self.__isoFile)

        self.Bind(wx.EVT_BUTTON, self.on_install, self.__btInstall)
        self.Bind(wx.EVT_BUTTON, self.on_refresh, self.__btRefresh)

        self.Bind(wx.EVT_RADIOBUTTON, self.on_source_option_changed, self.__isoChoice)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_source_option_changed, self.__dvdChoice)

        self.refresh_list_content()
        self.on_source_option_changed(wx.CommandEvent)
        self.__btInstall.Enable(self.is_install_ok())

    def refresh_list_content(self):
        # USB
        self.__usbStickDevList = []
        self.__usbStickList.Clear()

        show_all_checked = self.__parent.is_show_all_checked()

        device_list = ListUsb(show_all_checked).list()

        for device in device_list:
            print(device[0])
            self.__usbStickDevList.append(device[0])
            print(device[1])
            self.__usbStickList.Append(device[1])

        # ISO

        self.__dvdDriveDevList = []
        self.__dvdDriveList.Clear()

        readlink = subprocess.run("./data/listDvdDrive",
                                  stdout=subprocess.PIPE).stdout.decode("utf-8").strip().split("\n")

        for device in range(len(readlink)):
            if device % 2 == 0:
                self.__dvdDriveDevList.append(readlink[device])
            else:
                self.__dvdDriveList.Append(readlink[device])

        self.__btInstall.Enable(self.is_install_ok())

    def on_source_option_changed(self, _):
        is_iso = self.__isoChoice.GetValue()

        self.__isoFile.Enable(is_iso)
        self.__dvdDriveList.Enable(not is_iso)

        self.__btInstall.Enable(self.is_install_ok())

    def is_install_ok(self):
        is_iso = self.__isoChoice.GetValue()
        return ((is_iso and os.path.isfile(self.__isoFile.GetPath())) or (
                not is_iso and self.__dvdDriveList.GetSelection() != wx.NOT_FOUND)) and self.__usbStickList.GetSelection() != wx.NOT_FOUND

    def on_list_or_file_modified(self, event):
        if event.GetEventType() == wx.EVT_LISTBOX and not event.IsSelection():
            return

        self.__btInstall.Enable(self.is_install_ok())

    def on_refresh(self, _):
        self.refresh_list_content()

    def on_install(self, _):
        global woe
        if self.is_install_ok():
            is_iso = self.__isoChoice.GetValue()

            device = self.__usbStickDevList[self.__usbStickList.GetSelection()]

            if is_iso:
                iso = self.__isoFile.GetPath()
            else:
                iso = self.__dvdDriveDevList[self.__dvdDriveList.GetSelection()]

            woe.start()

            dialog = wx.ProgressDialog("Installing", "Please wait...", 101, self.GetParent(),
                                       wx.PD_APP_MODAL | wx.PD_SMOOTH | wx.PD_CAN_ABORT)

            while woe.is_alive():
                if not woe.progress:
                    status = dialog.Pulse(woe.state)[0]
                    time.sleep(0.06)
                else:
                    status = dialog.Update(woe.progress, woe.state)[0]

                if not status:
                    if wx.MessageBox("Are you sure you want to cancel the installation?", "Cancel",
                                     wx.YES_NO | wx.ICON_QUESTION, self) == wx.NO:
                        dialog.Resume()
                    else:
                        woe.kill = True
                        break
            dialog.Destroy()

            if woe.error == "":
                wx.MessageBox("Installation succeeded!", "Installation", wx.OK | wx.ICON_INFORMATION, self)
            else:
                wx.MessageBox("Installation failed!" + "\n" + str(woe.error), "Installation", wx.OK | wx.ICON_ERROR,
                              self)

    def on_show_all_drive(self, _):
        self.refresh_list_content()


class DialogAbout(wx.Dialog):
    __bitmapIcone = None
    __staticTextTitre = None
    __staticTextVersion = None
    __NotebookAutorLicence = None
    __MyPanelNoteBookAutors = None
    __BtOk = None

    def __init__(self, parent, ID=wx.ID_ANY, title="About", pos=wx.DefaultPosition, size=wx.Size(570, 590),
                 style=wx.DEFAULT_DIALOG_STYLE):
        super(DialogAbout, self).__init__(parent, ID, title, pos, size, style)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        sizer_all = wx.BoxSizer(wx.VERTICAL)
        sizer_img = wx.BoxSizer(wx.HORIZONTAL)

        img_file_name = "data/icon.png"

        img = wx.Image(img_file_name, wx.BITMAP_TYPE_PNG)
        self.__bitmapIcone = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img), wx.DefaultPosition, wx.Size(48, 48))
        sizer_img.Add(self.__bitmapIcone, 0, wx.ALL, 5)

        sizer_text = wx.BoxSizer(wx.VERTICAL)

        self.__staticTextTitre = wx.StaticText(self, wx.ID_ANY, "app")
        self.__staticTextTitre.SetFont(wx.Font(16, 74, 90, 92, False, "Sans"))
        self.__staticTextTitre.SetForegroundColour(wx.Colour(0, 60, 118))
        sizer_text.Add(self.__staticTextTitre, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        self.__staticTextVersion = wx.StaticText(self, wx.ID_ANY, "Version 0.0.1")
        self.__staticTextVersion.SetFont(wx.Font(10, 74, 90, 92, False, "Sans"))
        self.__staticTextVersion.SetForegroundColour(wx.Colour(69, 141, 196))
        sizer_text.Add(self.__staticTextVersion, 0, wx.LEFT, 5)
        sizer_img.Add(sizer_text, 0, 0, 5)
        sizer_all.Add(sizer_img, 0, wx.EXPAND, 5)

        self.__NotebookAutorLicence = wx.Notebook(self, wx.ID_ANY)

        self.__NotebookAutorLicence.AddPage(
            PanelNoteBookAutors(self.__NotebookAutorLicence, wx.ID_ANY, "slacka et al.", "data/woeusb-logo.png",
                                "github.com/slacka/WoeUSB"), "Authors", True)
        self.__NotebookAutorLicence.AddPage(
            PanelNoteBookAutors(self.__NotebookAutorLicence, wx.ID_ANY, "Colin GILLE / Congelli501",
                                "data/c501-logo.png", "www.congelli.eu"), "Original WinUSB Developer", False)

        licence_str = '''
            %s is free software: you can redistribute it and/or modify
            it under the terms of the GNU General Public License as published by
            the Free Software Foundation, either version 3 of the License, or
            (at your option) any later version.\n
            \n
            %s is distributed in the hope that it will be useful,
            but WITHOUT ANY WARRANTY; without even the implied warranty of
            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
            GNU General Public License for more details.\n
            \n
            You should have received a copy of the GNU General Public License
            along with %s.  If not, see <http://www.gnu.org/licenses/>.
        '''

        licence_txt = wx.TextCtrl(self.__NotebookAutorLicence, wx.ID_ANY, licence_str, wx.DefaultPosition,
                                  wx.DefaultSize, wx.TE_MULTILINE | wx.TE_READONLY)

        self.__NotebookAutorLicence.AddPage(licence_txt, "License")

        sizer_all.Add(self.__NotebookAutorLicence, 1, wx.EXPAND | wx.ALL, 5)

        self.__BtOk = wx.Button(self, wx.ID_OK)
        sizer_all.Add(self.__BtOk, 0, wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, 5)
        self.__BtOk.SetFocus()

        self.SetSizer(sizer_all)
        self.Layout()


class PanelNoteBookAutors(wx.Panel):
    def __init__(self, parent, ID=wx.ID_ANY, autherName="", imgName="", siteLink="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TAB_TRAVERSAL):
        super(PanelNoteBookAutors, self).__init__(parent, ID, pos, size, style)

        sizer_note_book_autors = wx.BoxSizer(wx.VERTICAL)

        auteur_static_text = wx.StaticText(self, wx.ID_ANY, autherName)
        sizer_note_book_autors.Add(auteur_static_text, 0, wx.ALL, 5)

        if siteLink != "":
            autor_link = wx.adv.HyperlinkCtrl(self, wx.ID_ANY, siteLink, siteLink)
            sizer_note_book_autors.Add(autor_link, 0, wx.LEFT | wx.BOTTOM, 5)

        if imgName != "":
            # img_file_name = findFile(imgName)
            img = wx.Image(imgName, wx.BITMAP_TYPE_PNG)
            img_autor_logo = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))
            sizer_note_book_autors.Add(img_autor_logo, 0, wx.LEFT, 5)

        self.SetSizer(sizer_note_book_autors)


class Communication(threading.Thread):
    progress = False
    state = ""
    error = ""
    kill = False

    def __init__(self, source, target):
        threading.Thread.__init__(self)

        woeusb.gui = self
        self.source = source
        self.target = target

    def run(self):
        source_fs_mountpoint, target_fs_mountpoint, temp_directory = woeusb.init(from_cli=False,
                                                                                 install_mode="device",
                                                                                 source_media=self.source,
                                                                                 target_media=self.target)[:3]
        try:
            woeusb.main(source_fs_mountpoint, target_fs_mountpoint, self.source, self.target, "device",
                        temp_directory, "FAT", False)
        except SystemExit:
            pass

        woeusb.cleanup(source_fs_mountpoint, target_fs_mountpoint, temp_directory)

# Packed to class for clarity


class ListUsb:
    def __init__(self, show_all=False):
        self.show_all = show_all

    def list(self):
        devices_list = []

        lsblk = subprocess.run(["lsblk",
                                "--output", "NAME",
                                "--noheadings",
                                "--nodeps"], stdout=subprocess.PIPE).stdout.decode("utf-8")

        devices = re.sub("sr[0-9]", "", lsblk).split()

        for device in devices:
            if self.is_removable_and_writable_device(device):
                if not self.show_all:
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

    def is_removable_and_writable_device(self, block_device_name):
        sysfs_block_device_dir = "/sys/block/" + block_device_name

        # We consider device not removable if the removable sysfs item not exist
        if os.path.isfile(sysfs_block_device_dir + "/removable"):
            removable = open(sysfs_block_device_dir + "/removable")
            removable_content = removable.read()
            removable.close()

            ro = open(sysfs_block_device_dir + "/ro")
            ro_content = ro.read()
            ro.close()

            if removable_content.strip("\n") == "1" and ro_content.strip("\n") == "0":
                return 0
            else:
                return 1
        else:
            return 1



frameTitle = "app"

app = wx.App()

m_frame = MainFrame(frameTitle, wx.DefaultPosition, wx.Size(400, 600))
m_frame.SetMinSize(wx.Size(300, 450))

m_frame.Show(True)
app.MainLoop()
