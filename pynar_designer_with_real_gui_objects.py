from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QLineEdit,QComboBox,QGroupBox,QLabel
from PyQt5.QtCore import Qt,QRect

class PLabel(QLabel):
    
    def __init__(self, parent = None):
        super(PLabel, self).__init__(parent)
        self.name = ""
        #self.setMinimumSize(75,60)


    
    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        #super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos

        #super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        pos=self.pos() #debug için pozisyon bilgisi
        print(pos.x(), pos.y()) #debug için pozisyon bilgisi
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        #super(DragButton, self).mouseReleaseEvent(event)

class PComboBox(QComboBox):
    
    def __init__(self, parent = None):
        super(PComboBox, self).__init__(parent)
        self.name = ""
        #self.setMinimumSize(75,60)


    
    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        #super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos

        #super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        pos=self.pos() #debug için pozisyon bilgisi
        print(pos.x(), pos.y()) #debug için pozisyon bilgisi
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        #super(DragButton, self).mouseReleaseEvent(event)

class PLineEdit(QLineEdit):
    
    def __init__(self, parent = None):
        super(PLineEdit, self).__init__(parent)
        self.name = ""
        #self.setMinimumSize(75,60)


    
    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        #super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos

        #super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        pos=self.pos() #debug için pozisyon bilgisi
        print(pos.x(), pos.y()) #debug için pozisyon bilgisi
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        #super(DragButton, self).mouseReleaseEvent(event)



class PPushButton(QPushButton):
    
    def __init__(self, parent = None):
        super(PPushButton, self).__init__(parent)
        self.name = ""
        #self.setMinimumSize(75,60)

    
    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        #super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos

        #super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        pos=self.pos() #debug için pozisyon bilgisi
        print(pos.x(), pos.y()) #debug için pozisyon bilgisi
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        #super(DragButton, self).mouseReleaseEvent(event)

class PGroupBox(QGroupBox):
    
    def __init__(self, parent = None):
        super(PGroupBox, self).__init__(parent)
        self.name = ""
        #self.setMinimumSize(150,100)

    
    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        #super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos

        #super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        pos=self.pos() #debug için pozisyon bilgisi
        print(pos.x(), pos.y()) #debug için pozisyon bilgisi
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        #super(DragButton, self).mouseReleaseEvent(event)




def clicked():
    print ("click as normal!")


if __name__ == "__main__":
    app = QApplication([])
    w   = QWidget()
    w.resize(800,600)




    # Pencere oluştur
    window = PGroupBox(w)
    window.setTitle(u"Pencere Başlığı")
    window.setGeometry(QRect(180, 70, 271, 281))
    window.setStyleSheet(
    """
    QGroupBox  {
        border: 1px solid gray;
        border-color: #FF17365D;
        margin-top: 27px;
        font-size: 12px;
        background-color: white;

    }
    QGroupBox::title  {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 8px 8000px 5px 1px;
        background-color: #FF17365D;
        color: rgb(255, 255, 255);
    }
    """
    )
    
    # toolbox'da Combobox oluştur
    toolbox_pcombobox  = PComboBox(w)
    toolbox_pcombobox.setGeometry(0, 30, 100, 20)
    toolbox_pcombobox.addItem('Açılan Kutu')


    
    # toolbox'da 3 PushButton oluştur
    for i in range(3):
        toolbox_ppushbutton  = PPushButton(w)
        toolbox_ppushbutton.setGeometry(0, 60, 100, 20)
        toolbox_ppushbutton.setText('Buton')

    # toolbox'da LineEdit oluştur
    toolbox_plineedit  = PLineEdit(w)
    toolbox_plineedit.setGeometry(0, 90, 100, 20)
    toolbox_plineedit.setText('Metin Kutusu')

    # toolbox'da Label oluştur
    toolbox_plabel  = PLabel(w)
    toolbox_plabel.setGeometry(0, 120, 100, 20)
    toolbox_plabel.setText('Etiket')

    w.show()
    app.exec_() 

