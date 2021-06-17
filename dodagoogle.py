from PyQt5.QtWidgets import (QListWidget,
                             QListWidgetItem,
                             QMainWindow, QApplication)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QByteArray, QSettings

from frmMain_ui import Ui_MainWindow
from utilities.setting import Settings
from GoogleDrive import GoogleDrive


class DodaListItem(QListWidgetItem):
    """
    Sublassing QListWidgetItem so we can add some properties
    we need.
    'owner_name': zen[0]['displayName'],
                    'owner_kind': zen[0]['kind'],
                    'fileid': item['id'],
                    'filename': item['name'],
                    'file_kind': item['kind'],
                    'mimeType': item['mimeType'],
                    'trashed': item['trashed'],
                    'createdTime': item['createdTime']
    """
    def __init__(self, owner_name, owner_kind, fileid, filename, file_kind, mimeType, trashed, createdTime):
        super(DodaListItem, self).__init__()
        self.owner_name = ownername
        self.filename = filename


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

    def handle_item_clicked(self):
        zen = self.googleDriveList.currentItem()
        if type(zen).__name__ == "DodaListItem":
            print(zen.filename)

    def bind_actions(self):
        """
        Bind menu/toolbar actions
        :return:
        """
        self.actionE_xit.triggered.connect(self.close)
        self.actionLoad_Files.triggered.connect(self.handle_load_files)

    def handle_load_files(self):
        """
        Slot
        Load the folders from Google Drive
        """
        doda = GoogleDrive()
        self._folders = doda.get_drive_folders(500)
        # Retrieve the folders in the root for the moment
        for folder in self._folders:
            ic = QIcon()
            ic.addPixmap(QPixmap(':/icons/Places-folder-blue-icon'))
            ploink = DodaListItem(folder['filename'])
            ploink.setText(folder['filename'])
            ploink.setIcon(ic)
            self.googleDriveList.addItem(ploink)

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
