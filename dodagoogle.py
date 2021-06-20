from PyQt5.QtWidgets import (QListWidget,
                             QListWidgetItem,
                             QMainWindow, QApplication)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
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
        self.googleDriveList.empty_folder_text = "No files in this Google Drive folder"

        # _active_folder is the variable used to keep track
        # of the last selected folder, this is used to go back for example
        self._active_folder = -1
        self._folder_history = []
        self._trashfound = False

    def bind_controls(self):
        self.googleDriveList.itemClicked.connect(self.handle_item_clicked)
        self.googleDriveList.itemDoubleClicked.connect(self.handle_item_doubleclicked)

    def handle_item_doubleclicked(self):
        zen = self.googleDriveList.currentItem()
        if zen.mime_type.endswith(".folder"):
            # Add the selected folder to the history
            self._folder_history.append(zen.fileid)
            self._active_folder = zen.fileid
            self.statusbar.showMessage(self._active_folder)
            self.get_drive_contents(zen.fileid)
        else:
            print("Not a folder")

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
        self.actionUp.triggered.connect(self.handle_back)

    def handle_back(self):
        """
        Go up one folder
        :return:
        """
        print(self._folder_history)
        try:
            # Get the last selected folder and remove it from the array
            # Pop current folder. If this item is not removed first,
            # we don't get the correct parent folder and nothing happens.
            self._folder_history.pop()
            # Get the parent folder
            parent = self._folder_history.pop()
            self.get_drive_contents(folder_id=parent)
        except IndexError as e:
            # If any index error occurs, simply go to the root folder
            self.get_drive_contents(folder_id='')

    def get_drive_contents(self, folder_id):
        """
        Query Google Drive about the files in a directory.
        :param folder_id:  The google id for a file/folder. The format of such
            and id is like this one : 1B9hpSN8OkfIJdgNTU3ApTbXyJfmZnA02
        """

        if folder_id == "root":
            print("ROOT")
            folder_id = ""

        doda = GoogleDrive()
        self.googleDriveList.clear()
        drive_contents = doda.get_files_in_folder(folder_id=folder_id)
        # Sort the returned list on the mime_type.  This way we can group files and folders
        sortedList = sorted(drive_contents, key=lambda k: k['mime_type'])
        self._trashfound = False
        # Font for listitems
        font = QFont()
        font.setBold(False)
        font.setPointSize(12)
        # font.setWeight(75)

        # Put items in the listview
        for folder in sortedList:
            ic = QIcon()
            # Check what type of icon we have to use
            icon_type = folder['mime_type']
            # replace the / into -
            new_icon_type = icon_type.replace("/", "-")

            # Set the icon in case of known files
            if new_icon_type.endswith(".folder"):
                new_icon_type = "Places-folder-green-icon"
            elif new_icon_type.endswith(".presentation"):
                new_icon_type = "application-presentation.png"
            elif new_icon_type.endswith(".doc"):
                new_icon_type = "Word-2-icon.png"
            elif new_icon_type.endswith(".zip"):
                new_icon_type = "application-zip.png"

            ic.addPixmap(QPixmap(f":/icons/{new_icon_type}"))
            # Contruct a new DodaListItem
            dodaListItem = DodaListItem.DodaListItem(owner_name=folder['owner_name'],
                                                     owner_kind=folder['owner_kind'],
                                                     fileid=folder['fileid'],
                                                     filename=folder['filename'],
                                                     file_kind=folder['file_kind'],
                                                     mime_type=folder['mime_type'],
                                                     trashed=folder['trashed'],
                                                     created_time=folder['created_time'])
            dodaListItem.setText(folder['filename'])
            dodaListItem.setFont(font)
            if icon_type.endswith(".folder"):
                dodaListItem.setForeground(QColor('sea green'))
            dodaListItem.setIcon(ic)
            self.googleDriveList.addItem(dodaListItem)
            # Check if an item is marked as trashed
            if folder['trashed']:
                self._trashfound = True

        # Change the trashcan icon here
        if self._trashfound:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/Full-Trash-icon.png"), QIcon.Normal, QIcon.Off)
            self.actionTrash_Can.setIcon(icon)
        else:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/Empty-Trash-icon.png"), QIcon.Normal, QIcon.Off)
            self.actionTrash_Can.setIcon(icon)

    def handle_load_files(self):
        """
        Load the folders from Google Drive, because this is supposed to be the root
        folder, we set an empty folder_id
        """
        zen = self.googleDriveList.currentItem()
        self._folder_history.clear()
        self._folder_history.append("root")
        self.get_drive_contents(folder_id="")

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
