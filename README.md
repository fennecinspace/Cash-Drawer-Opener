# USB Opener for POS Cash Drawer

this is a simple python script to open a cash drawer connected by USB (or using a USB adapter)

## Dependencies

```bash
sudo apt install python3 python3-pip
sudo pip3 install PyQt5 pyserial pynput
```

## How to use

```bash
python3 opener.py
```

launch `opener.py` and modify your COM number. <br>
Open Drawer Using <kbd>F12</kbd>

## Different Drawer :
the default codes used for opening the cash drawer are the standard and should work for most drawers.<br>
in case your drawer isn't opening when you're positive that the COM is correct, change CODES in `info.conf` to one of the following :

```python
    [27,112,0,25,250]
    [27,112,0,48,251]
    [27,112,1,49,251]
    [27,118,140]
    [27,112,0,50,250]
    [27,112,48,55,121]
    [27,112,0,64,240]
    [27,112,0,25,255]
    [27,112,0,40,168]
    [27,112,0,48,49]
    [27,112,32,25]
    [27,70,0,50,50]
    [27,112,0,25,251]
    [27,112,48,25,250]
```