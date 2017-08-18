import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def on_clipboard_change(clipboard):
    mine_data = clipboard.mimeData()
    urls = mine_data.urls()
    if len(urls) > 0 and len(urls) == len([url for url in urls if get_file_suffix(url.toString()) == '.gif']):
        clipboard.dataChanged.disconnect()  # disconnect all
        mimeData = QMimeData()
        mimeData.setUrls(urls)
        clipboard.setMimeData(mimeData)
        clipboard.dataChanged.connect(lambda: on_clipboard_change(clipboard))


def get_file_suffix(path):
    return os.path.splitext(path)[1].lower()


if __name__ == '__main__':

    app = QApplication([])
    clipboard = app.clipboard()
    clipboard.dataChanged.connect(lambda: on_clipboard_change(clipboard))
    app.setQuitOnLastWindowClosed(False)

    sys.exit(app.exec())