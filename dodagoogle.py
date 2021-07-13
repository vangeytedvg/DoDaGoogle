from PyQt5.QtWidgets import (QMainWindow, QApplication, QFrame, QLabel,
                             QLineEdit, QToolBar, QSlider)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtCore import QByteArray, QSettings, Qt

from frmMain_ui import Ui_MainWindow
from utilities.setting import Settings
from GoogleDrive import GoogleDrive
from CustomWidgets import DodaListItem


class DodaGoogle(QMainWindow, Ui_MainWindow):
    """
    DoDaGoogle class, mimics Google Drive
    """

    def __init__(self):
        """
        Ctor
        """
        super(DodaGoogle, self).__init__()
        # These are the widgets that will be placed on the statusbar
        self.slide = QSlider(parent=self, orientation=Qt.Horizontal)
        self.lbl_google_folderid = QLineEdit("none")
        self.lbl_google_folderid_info = QLabel("Google folder id")
        self.lbl_trashed = QLabel("no")
        self.lbl_trashed_info = QLabel("Trashed")
        self.lbl_filename = QLineEdit("none")
        self.lbl_filename_info = QLabel("Selected file/folder")
        self.lbl_parent = QLineEdit("none")
        self.lbl_parent_info = QLabel("Selected file/folder")
        # House keeping...
        self.setupUi(self)
        self.loadsettings()
        self.setup_statusbar()
        self.setup_toolbar(self.toolbar_Dynamic)
        self.bind_actions()
        self.bind_controls()
        self.googleDriveList.empty_folder_text = "No files in this Google Drive folder"

        # _active_folder is the variable used to keep track
        # of the last selected folder, this is used to go back for example
        self._active_folder = -1
        self._folder_history = []
        self._trashfound = False

    def setup_toolbar(self, toolbar: QToolBar):
        """
        Setup additional widget for a toolbar
        :param toolbar: The toolbar to host the widgets
        :return:
        """
        self.slide.setTickPosition(QSlider.TicksBothSides)
        self.slide.setMaximumWidth(100)
        self.slide.setMinimum(25)
        self.slide.setMaximum(64)
        toolbar.addWidget(self.slide)

    def setup_statusbar(self):
        """
        Add additional widgets to the statusbar.
        """
        # Filename
        self.lbl_filename_info.setStyleSheet("color: rgb(171, 171, 171);")
        self.lbl_filename.setReadOnly(True)
        self.statusbar.addPermanentWidget(self.lbl_filename_info)
        self.statusbar.addPermanentWidget(self.lbl_filename)
        # Trashcan info
        self.lbl_trashed_info.setStyleSheet("color: rgb(171, 171, 171);")
        self.lbl_trashed.setFrameShadow(QFrame.Raised)
        self.lbl_trashed.setFrameShape(QFrame.Panel)
        self.statusbar.addPermanentWidget(self.lbl_trashed_info)
        self.statusbar.addPermanentWidget(self.lbl_trashed)
        # Google folder/file id
        self.lbl_google_folderid_info.setStyleSheet("color: rgb(171, 171, 171);")
        self.lbl_google_folderid.setReadOnly(True)
        self.statusbar.addPermanentWidget(self.lbl_google_folderid_info)
        self.statusbar.addPermanentWidget(self.lbl_google_folderid)

    def bind_controls(self):
        """
        Bind signals for normal Widgets
        :return:
        """
        self.googleDriveList.itemClicked.connect(self.handle_item_clicked)
        self.googleDriveList.itemDoubleClicked.connect(self.handle_item_doubleclicked)

    def handle_item_doubleclicked(self):
        """
        When the user double-clicks a folder or file
        """
        zen = self.googleDriveList.currentItem()
        if zen.mime_type.endswith(".folder"):
            # Add the selected folder to the history
            self._folder_history.append(zen.fileid)
            self._active_folder = zen.fileid
            self.get_drive_contents(zen.fileid)

    def handle_item_clicked(self):
        """
        When te user clicks on a folder/file
        """
        zen = self.googleDriveList.currentItem()
        # If it is an instance of DodaListItem, we can get the enriched
        # information from it.
        if type(zen).__name__ == "DodaListItem":
            if zen.mime_type.endswith(".folder"):
                self.lbl_filename_info.setText("Selected Folder")
            else:
                self.lbl_filename_info.setText("Selected File")
            self.lbl_filename.setText(zen.filename)
            print(zen.trashed)
            if zen.trashed:
                self.lbl_trashed.setStyleSheet("color: red;")
                self.lbl_trashed.setText("Marked as trash")
            else:
                self.lbl_trashed.setStyleSheet("color: white;")
                self.lbl_trashed.setText("no")
            self.lbl_google_folderid.setText(zen.fileid)

    def bind_actions(self):
        """
        Bind menu/toolbar actions
        :return:
        """
        self.actionE_xit.triggered.connect(self.close)
        self.actionLoad_Files.triggered.connect(self.handle_load_files)
        self.actionUp.triggered.connect(self.handle_back)
        self.actionUpload_files.triggered.connect(self.handle_upload_files)

    def handle_back(self):
        """
        Go up one folder
        """
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
            # Disable the back button
            self.actionUp.setEnabled(False)

    def handle_upload_files(self):
        """
        Upload a file or folder to GoogleDrive
        """
        pass

    def get_drive_contents(self, folder_id):
        """
        Query Google Drive about the files in a directory.
        :param folder_id:  The google id for a file/folder. The format of such
            and id is like this one : 1B9hpSN8OkfIJdgNTU3ApTbXyJfmZnA02
        """

        if folder_id == "root":
            folder_id = ""

        doda = GoogleDrive()
        self.googleDriveList.clear()
        drive_contents = doda.get_files_in_folder(folder_id=folder_id)
        self.lbl_google_folderid.setText(folder_id)

        # If we have contents, enable the back button
        if drive_contents:
            self.actionUp.setEnabled(True)

        # Sort the returned list on the mime_type.  This way we can group files and folders
        sortedList = sorted(drive_contents, key=lambda k: k['mime_type'])
        self._trashfound = False

        # Font for listitems
        font = QFont()
        font.setBold(False)
        font.setPointSize(10)

        # Put items in the listview
        for folder in sortedList:
            ic = QIcon()
            # Check what type of icon we have to use
            icon_type = folder['mime_type']
            # replace the / into -
            new_icon_type = icon_type.replace("/", "-")
            new_icon_type = new_icon_type.replace("+", "-")
            print("ICT : ", f":/icons/{new_icon_type}")
            ic.addPixmap(QPixmap(f":/icons/{new_icon_type}.png"))
            # Contruct a new DodaListItem
            dodaListItem = DodaListItem.DodaListItem(owner_name=folder['owner_name'],
                                                     owner_kind=folder['owner_kind'],
                                                     fileid=folder['fileid'],
                                                     filename=folder['filename'],
                                                     file_kind=folder['file_kind'],
                                                     mime_type=folder['mime_type'],
                                                     trashed=folder['trashed'],
                                                     created_time=folder['created_time'],
                                                     parents=folder['parents'])

            dodaListItem.setText(folder['filename'])
            dodaListItem.setFont(font)
            # A folder?
            if icon_type.endswith(".folder"):
                dodaListItem.setForeground(QColor('sea green'))
            dodaListItem.setIcon(ic)
            self.googleDriveList.addItem(dodaListItem)
            # Check if an item is marked as trashed
            if folder['trashed']:
                self._trashfound = True
                dodaListItem.setForeground(QColor('red'))

        # Change the trashcan icon here
        if self._trashfound:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/action_icons/Full-Trash-icon.png"), QIcon.Normal, QIcon.Off)
            self.actionTrash_Can.setIcon(icon)
        else:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/action_icons/Empty-Trash-icon.png"), QIcon.Normal, QIcon.Off)
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
