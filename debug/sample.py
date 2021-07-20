import ctypes
from ctypes.wintypes import HWND, DWORD, RECT
import pyautogui

def GetWindowRectFromName(TargetWindowTitle:str)-> tuple:
    TargetWindowHandle = ctypes.windll.user32.FindWindowW(0, TargetWindowTitle)
    Rectangle = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(TargetWindowHandle, ctypes.pointer(Rectangle))
    # top=y left=x
    return (Rectangle.left, Rectangle.top, Rectangle.right, Rectangle.bottom)

if __name__ == "__main__":
    result = GetWindowRectFromName('SCV42')
    sc = pyautogui.screenshot(region=(result[0], result[1], result[2]-result[0], result[3]-result[1]))
    sc.save("./img/window.png")
    print(result)
    pass