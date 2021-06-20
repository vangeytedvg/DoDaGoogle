
from PyQt5 import QtCore, QtGui, QtWidgets


class DenkaListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # The text that will appear in the widget when there are no items
        self._empty_folder_text = ""

    @property
    def empty_folder_text(self):
        return self._placeholder_text

    @empty_folder_text.setter
    def empty_folder_text(self, text):
        self._empty_folder_text = text
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        # We have nothing in the list?
        if self.count() == 0:
            painter = QtGui.QPainter(self.viewport())
            painter.save()
            # col = self.palette().placeholderText().color()
            text_color = QtGui.QColor("sea green")
            painter.setPen(text_color)
            font_met = self.fontMetrics()
            elided_text = font_met.elidedText(
                self._empty_folder_text, QtCore.Qt.ElideRight, self.viewport().width()
            )
            painter.drawText(self.viewport().rect(), QtCore.Qt.AlignHCenter, elided_text)
            painter.restore()
