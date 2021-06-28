"""
Class responsible for saving and restoring the state of a form
"""
from PyQt5.QtCore import QSettings, QByteArray


class Settings:
    def __init__(self, parent=None, company="", section=""):
        self._parent = parent
        self._company = company
        self._section = section

    def save_form_settings(self, group, item):
        """
        Form state and geometry saving
        """
        settings = QSettings(self._company, self._section)
        settings.beginGroup(group)
        settings.setValue(item, self._parent.saveGeometry())
        settings.setValue(item, self._parent.saveState())
        settings.endGroup()

    def save_setting(self, group, item, data):
        """
        Save generic data
        """
        settings = QSettings(self._company, self._section)
        settings.beginGroup(group)
        settings.setValue(item, data)
        settings.endGroup()

    def load_setting(self, group, item):
        """
        Load generic data
        """
        settings = QSettings(self._company, self._section)
        settings.beginGroup(group)
        setting = settings.value(item, "Nothing")
        settings.endGroup()
        return setting

    def load_setting_from_byte_array(self, group, item):
        """
        Load generic data
        """
        settings = QSettings(self._company, self._section)
        settings.beginGroup(group)
        setting = settings.value(item, QByteArray())
        settings.endGroup()
        return setting

