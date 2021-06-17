from PyQt5.QtWidgets import (QListWidget,
                             QListWidgetItem,
                             QMainWindow, QApplication)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QByteArray, QSettings

from frmMain_ui import Ui_MainWindow
from utilities.setting import Settings
from GoogleDrive import GoogleDrive
from CustomWidgets import DodaListItem


class DodaGoogle(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(DodaGoogle, self).__init__()
        self.setupUi(self)
        self.loadsettings()
        self.bind_actions()
        self.bind_controls()
        self._folders = []

    def bind_controls(self):
        self.googleDriveList.itemClicked.connect(self.handle_item_clicked)
        self.googleDriveList.itemDoubleClicked.connect(self.handle_item_doubleclicked)

    def handle_item_doubleclicked(self):
        zen = self.googleDriveList.currentItem()
        self.get_drive_contents(zen.fileid)

    def handle_item_clicked(self):
        zen = self.googleDriveList.currentItem()
        # If it is an instance of DodaListItem, we can get the enriched
        # information from it.
        if type(zen).__name__ == "DodaListItem":
            print(zen.owner_name)
            print(zen.owner_kind)
            print(zen.filename)
            print(zen.trashed)
            print(zen.fileid)
            print(zen.mime_type)

    def bind_actions(self):
        """
        Bind menu/toolbar actions
        :return:
        """
        self.actionE_xit.triggered.connect(self.close)
        self.actionLoad_Files.triggered.connect(self.handle_load_files)

    def get_drive_contents(self, folder_id):
        doda = GoogleDrive()
        self.googleDriveList.clear()
        self._folders = doda.get_files_in_folder(folder_id=folder_id)
        for folder in self._folders:
            ic = QIcon()
            # Check what type of icon we have to use
            icon_type = folder['mime_type']

            # replace the / into -
            new_icon_type = icon_type.replace("/", "-")
            print("ICON", new_icon_type)
            if new_icon_type == "application-vnd.google-apps.folder":
                print("ZWABBER")
                new_icon_type = "Places-folder-green-icon"

            ic.addPixmap(QPixmap(f":/icons/{new_icon_type}"))

            ploink = DodaListItem.DodaListItem(owner_name=folder['owner_name'],
                                               owner_kind=folder['owner_kind'],
                                               fileid=folder['fileid'],
                                               filename=folder['filename'],
                                               file_kind=folder['file_kind'],
                                               mime_type=folder['mime_type'],
                                               trashed=folder['trashed'],
                                               created_time=folder['created_time'])
            ploink.setText(folder['filename'])
            ploink.setIcon(ic)
            self.googleDriveList.addItem(ploink)

    def handle_load_files(self):
        """
        Slot
        Load the folders from Google Drive
        """
        zen = self.googleDriveList.currentItem()
        self.get_drive_contents(folder_id="")

    def load_folder_contents(self, folder_id=''):
        self.handle_load_files()

    """------------------ Settings Section ------------------"""

    def closeEvent(self, event):
        """
          Overrides the base close event
        :param event: event to override
        :return: nothing
        """
        mySettings = Settings(self, "DenkaTech", "DodaGoogle")
        mySettings.save_form_settings("mainwindow", "frm_main/geometry")
        self.savesettings()

    def savesettings(self):
        """
          Save settings to the registry (windows) or setting file (linux)
        """
        settings = QSettings("DenkaTech", "DodaGoogle")
        settings.beginGroup("mainwindow")
        settings.setValue("frm_main/geometry", self.saveGeometry())
        settings.setValue("frm_main/state", self.saveState())
        settings.endGroup()

    def loadsettings(self):
        """
          Load the settings from the registry (windows) or settings file (linux)
        """
        # --> this part needs to be migrated to the Settings class
        settings = QSettings("DenkaTech", "DodaGoogle")
        settings.beginGroup("mainwindow")
        self.restoreState(settings.value("frm_main/state", QByteArray()))
        self.restoreGeometry(settings.value("frm_main/geometry", QByteArray()))
        settings.endGroup()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    main_form = DodaGoogle()
    main_form.show()
    sys.exit(app.exec_())
