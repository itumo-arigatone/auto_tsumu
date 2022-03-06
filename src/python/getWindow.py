import pyautogui
import logging
import sys
import ctypes
from ctypes.wintypes import HWND, DWORD, RECT

args = sys.argv

def GetWindowRectFromName(TargetWindowTitle):
    TargetWindowHandle = ctypes.windll.user32.FindWindowW(0, TargetWindowTitle)
    Rectangle = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(TargetWindowHandle, ctypes.pointer(Rectangle))
    return (Rectangle.left, Rectangle.top, Rectangle.right, Rectangle.bottom)

if __name__ == '__main__':
    GetWindowRectFromName(args[0])
