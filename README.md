# send gif in wechat

![](usage.gif)

## env
tested on:  
* win10 + py3.5.4
* macOS + py3.6.2

## setup
```bash
pip3 install -U pyqt5 pyobjc
```

## run
1. run `python3 gif4wx.py` in shell
2. copy on source gif
3. paste wherever you want

## change log
[09-01]  
 Use AppKit on macOS, avoid activate python window for Qt to get clipboard change event.