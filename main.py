"""
    主程序
"""

from CallMainWindow import *
import qdarkstyle  # 深色调护眼高逼格

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    myWin = MyMainWindow()
    myWin.show()
    toolbar = myWin.findChild(QToolBar)
    toolbar.setVisible(False)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()