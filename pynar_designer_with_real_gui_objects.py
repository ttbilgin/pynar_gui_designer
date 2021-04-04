from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QLineEdit,QComboBox,QTabWidget
from PyQt5.QtCore import Qt,QRect

class DragButton(QComboBox):

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos

        super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        super(DragButton, self).mouseReleaseEvent(event)


class DragButton2(QPushButton):
    
    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        super(DragButton2, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos

        super(DragButton2, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        super(DragButton2, self).mouseReleaseEvent(event)

'''
def clicked():
    print ("click as normal!")
'''
if __name__ == "__main__":
    app = QApplication([])
    w   = QWidget()
    w.resize(800,600)



    tabWidget = QTabWidget(w)
    tabWidget.setObjectName(u"tabWidget")
    tabWidget.setStyleSheet("QTabBar::tab { width: 270px; align:left;}");
    tabWidget.setGeometry(QRect(180, 70, 271, 181))
    tab = QWidget()
    tab.setObjectName(u"tab")
    tabWidget.addTab(tab, "Pencere Başlığı")

    button = DragButton(w)
    #button.clicked.connect(clicked)
    button2 = DragButton2("tikla",w)
    button2.setGeometry(0, 30, 100, 20)
    
    w.show()
    app.exec_() 
