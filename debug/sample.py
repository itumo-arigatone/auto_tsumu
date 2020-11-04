from pywinauto import application
from time import sleep

# app = application.Application().connect(path="/Users/souma/Documents/Vysor.exe")
app = application.Application().connect(title_re="Vysor", visible_only="True")

app[u'SCV42'].CaptureAsImage().save('./img/window.png')