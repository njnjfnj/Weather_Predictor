# This Python file uses the following encoding: utf-8
import sys
import windows.main_window
from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication([])
    window = windows.main_window.Main_window(app.primaryScreen())
    screen = app.primaryScreen().geometry()
    w = screen.width()*0.6
    h = screen.height()*0.6
    x = screen.width() * 0.5-w/2
    y = screen.height()*0.5-h/2
    window.setGeometry(x, y, w, h)
    window.show()

    #file = .open("style.css")
    with open('style.css', 'r') as file:
        app.setStyleSheet(file.read())

    sys.exit(app.exec())
