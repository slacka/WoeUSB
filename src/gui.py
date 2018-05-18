#!/usr/bin/python3

import wx
import time


class MainFrame(wx.Frame):
    __MainPanel = None
    __MenuBar = None

    __menuItemShowAll = None

    def __init__(self, title, pos, size, style = wx.DEFAULT_FRAME_STYLE):
        super(MainFrame, self).__init__(None, -1, title, pos, size, style)

        file_menu = wx.Menu()
        self.__menuItemShowAll = wx.MenuItem(file_menu, wx.ID_ANY, "Show all drives Ctrl+A", "Show all drives, even those not detected as USB stick.", wx.ITEM_CHECK)
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

        #self.Connect(self.__menuItemShowAll.GetId(), wx.EVT_MENU, MainPanel.on_show_all_drive, None, self.__MainPanel)

        self.Bind(wx.EVT_MENU, self.on_quit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_about, help_item)

    def on_quit(self, event):
        self.Close(True)

    def on_about(self, event):
        pass

    def enable_buttons(self, adrSelected):
        pass

    def is_show_all_checked(self):
        return self.__menuItemShowAll.IsChecked()


class MainPanel(wx.Panel):
    __dvdDriveList = None
    __usbStickList = None

    __dvdDriveDevList = None
    __usbStickDevList = None

    __isoFile = None

    __parentFrame = None

    __btInstall = None
    __btRefresh = None

    __isoChoice = None
    __dvdChoice = None

    def __init__(self, parent, id, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.TAB_TRAVERSAL):
        super(MainPanel, self).__init__(parent, id, pos, size, style)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(wx.StaticText(self, wx.ID_ANY, "Source :"), 0, wx.ALL, 3)

        self.__isoChoice = wx.RadioButton(self, wx.ID_ANY, "From a disk image (iso)")
        main_sizer.Add(self.__isoChoice, 0, wx.ALL, 3)

        tmpSizer = wx.BoxSizer(wx.HORIZONTAL)
        tmpSizer.AddSpacer(20)
        self.__isoFile = wx.FilePickerCtrl(self, wx.ID_ANY, "", "Please select a disk image", "Iso images (*.iso)|*.iso;*.ISO|All files|*")
        tmpSizer.Add(self.__isoFile, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM, 3)
        main_sizer.Add(tmpSizer, 0, wx.EXPAND, 0)

    def on_source_option_changed(self, event):
        pass

    def on_list_or_file_modified(self, event):
        pass

    def on_refresh(self, event):
        pass

    def on_install(self, event):
        pass

    def on_show_all_drive(self, event):
        pass

    def refresh_list_content(self):
        pass

    def is_install_ok(self):
        pass

frameTitle = "app"

app = wx.App()

m_frame = MainFrame(frameTitle,  wx.DefaultPosition, wx.Size(400, 500))
m_frame.SetMinSize(wx.Size(300, 300))
m_frame.Show(True)
app.MainLoop()

time.sleep(5)
