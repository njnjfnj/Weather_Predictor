import windows.main_window
from PySide6.QtCore import qDebug

@windows.main_window.a()
def a():
    qDebug("b")
