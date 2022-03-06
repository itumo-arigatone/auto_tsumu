import pyautogui
import logging
import ctypes
from ctypes.wintypes import HWND, DWORD, RECT

def GetWindowRectFromName(TargetWindowTitle):
    TargetWindowHandle = ctypes.windll.user32.FindWindowW(0, TargetWindowTitle)
    Rectangle = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(TargetWindowHandle, ctypes.pointer(Rectangle))
    return (Rectangle.left, Rectangle.top, Rectangle.right, Rectangle.bottom)

def getCursolePosition():
    pyautogui.position()
