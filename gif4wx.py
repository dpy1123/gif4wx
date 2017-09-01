import os
import sys
import platform
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def on_clipboard_change(clipboard, log=False):
    mine_data = clipboard.mimeData()
    urls = mine_data.urls()
    if len(urls) > 0 and len(urls) == len([url for url in urls if get_file_suffix(url.toString()) == '.gif']):
        if log:
            print(urls)
        clipboard.dataChanged.disconnect(func)
        mimeData = QMimeData()
        mimeData.setUrls(urls)
        clipboard.setMimeData(mimeData)
        clipboard.dataChanged.connect(func)


def get_file_suffix(path):
    return os.path.splitext(path)[1].lower()


def pasteboard_polling_for_mac(log=False):
    import AppKit
    import time
    from urllib.parse import unquote

    count = 0
    while True:  # why polling? see: https://stackoverflow.com/questions/5033266/can-i-receive-a-callback-whenever-an-nspasteboard-is-written-to?answertab=votes#tab-top
        pb = AppKit.NSPasteboard.generalPasteboard()
        url = pb.dataForType_(AppKit.NSURLPboardType)
        if url is not None and pb.changeCount() > count:
            url = url.bytes().tobytes().decode()
            url = url[url.index('<string>') + len('<string>'): url.index('</string>')]
            url = unquote(url)
            if url.startswith('file://') and get_file_suffix(url) == '.gif':
                if log:
                    print(url)
                pb.clearContents()
                nsurl = AppKit.NSURL.fileURLWithPath_isDirectory_(url[len('file://'):], False)
                pb.writeObjects_([nsurl])
                count = pb.changeCount()
        time.sleep(1)


if __name__ == '__main__':
    
    if platform.system() == 'Darwin':
        pasteboard_polling_for_mac()
    else:
        app = QApplication([])
        app.setQuitOnLastWindowClosed(False)

        clipboard = app.clipboard()
        func = lambda: on_clipboard_change(clipboard)
        clipboard.dataChanged.connect(func)

        sys.exit(app.exec())
