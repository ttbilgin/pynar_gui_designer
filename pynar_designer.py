from PyQt5.QtCore import (QByteArray, QDataStream, QIODevice, QMimeData,
        QPoint, Qt)
from PyQt5.QtGui import QColor, QDrag, QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QMainWindow, QPushButton, QLineEdit
import sys, json

GRID_SIZE = 100


class QLabelCustom(QLabel):

    def __init__(self, parent = None):
        super(QLabelCustom, self).__init__(parent)
        self.name = ""
        self.setMinimumSize(75,30)
        self.setScaledContents(True)
        
class CustomSource(QFrame):
    def __init__(self, parent = None):
        
        super(CustomSource, self).__init__(parent)

        self.setMinimumSize(300,500)
        self.setFrameStyle(QFrame.Box)
        
    def add(self, address):
        lab = QLabelCustom(self)
        lab.setPixmap(QPixmap("components/{}".format(address)))
        lab.setToolTip(address)
        lab.adjustSize()
        lab.setAttribute(Qt.WA_DeleteOnClose)
        lab.name = address
        
        return lab
        
    def mouseMoveEvent(self, e):
        child = self.childAt(e.pos())
        if not child: 
            return
        mimeData = QMimeData()
        mimeData.setImageData(QPixmap(child.pixmap()).toImage())
        mimeData.setText(child.toolTip())
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(QPixmap(child.pixmap()))
        offset = QPoint()
        offset.setX(child.width()//2)
        offset.setY(child.height()//2)
        drag.setHotSpot(offset)
        drag.exec_()
        try:
            drag.target().chosen.name = child.name
            self.parent().parent().nametextedit.setText(child.name)
        except:
            pass

class CustomTarget(QFrame):

    def __init__(self, parent = None):
        
        super(CustomTarget, self).__init__(parent)
        
        self.setMinimumSize(700,500)
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet("QWidget {background-color: #d9d9d9;}")
        
        self.setAcceptDrops(True)
        
        self.childlist = []
        self.chosen = None
        self.grabbed = False
    
    def dragEnterEvent(self,e):
        e.accept()
    
    def mousePressEvent(self,e):
        child = self.childAt(e.pos())
        if not child: 
            return
        self.chosen = child
        self.parent().parent().nametextedit.setText(child.name)
    
    #Kendi içinde yer değiştirme istenmiyorsa bu fonksiyonu silin
    def mouseMoveEvent(self, e):
        if(self.grabbed):
            new_x = e.x() - self.chosen.x()
            new_y = e.y() - self.chosen.y()
            self.chosen.resize(new_x, new_y)
            return
        child = self.childAt(e.pos())
        if not child: 
            return
        self.chosen = child
        if(child.x() + child.width() - e.x() < child.width()//4 and child.y() + child.height() - e.y() < child.height()//4):
            self.grabbed = True
            new_x = e.x() - child.x()
            new_y = e.y() - child.y()
            child.resize(new_x, new_y)
        else:
            mimeData = QMimeData()
            mimeData.setImageData(QPixmap(child.pixmap()).toImage())
            mimeData.setText(child.toolTip())
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setPixmap(QPixmap(child.pixmap()).scaled(child.size()))
            offset = QPoint()
            offset.setX(child.width()//2)
            offset.setY(child.height()//2)
            print(offset)
            drag.setHotSpot(offset)
            drag.exec_()
            target = drag.target()
            try:
                target.chosen.name = child.name
                target.chosen.resize(child.size())
                target.parent().parent().nametextedit.setText(child.name)
            except Exception as e:
                print(e)
            if isinstance(target, CustomTarget):
                try:
                    self.childlist.remove(child)
                except:
                    pass
                child.close()

    def mouseReleaseEvent(self, e):
        self.grabbed = False
                
    def dropEvent(self, e):
        if not (isinstance(e.source(), CustomSource) or self):
            return
        e.accept()
        lab = QLabelCustom(self)
        lab.setPixmap(QPixmap(e.mimeData().imageData()))
        lab.setToolTip(e.mimeData().text())
        lab.adjustSize()
        lab.setAttribute(Qt.WA_DeleteOnClose)
        if e.source() == self:
            lab.move(e.pos().x() - (self.chosen.width()//2), e.pos().y() - (self.chosen.height()//2))
        else:
            lab.move(e.pos().x() - (lab.width()//2), e.pos().y() - (lab.height()//2))
        self.childlist.append(lab)
        self.chosen = lab
        lab.show()
        
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.setMinimumSize(800,500)
        side_layout = QHBoxLayout()
        main_layout = QVBoxLayout()
        
        self.custom1 = CustomSource()
        self.custom2 = CustomTarget()
        side_layout.addWidget(self.custom1)
        side_layout.addWidget(self.custom2)
        
        label1 = self.custom1.add("entry.png")
        label2 = self.custom1.add("button.png")
        label2.move(0,200)
        
        self.nametextedit = QLineEdit()
        self.nametextedit.textChanged.connect(self.namechange)
        
        self.button1 = QPushButton("Kaydet")
        self.button1.clicked.connect(self.save)
        
        side_layout.addWidget(self.nametextedit)
        
        main_layout.addLayout(side_layout)
        main_layout.addWidget(self.button1)
        
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def namechange(self):
        self.custom2.chosen.name = self.nametextedit.text()
    
    def save(self):
        dict = {}
        for i in self.custom2.childlist:
            data = []
            x = i.x() + i.width()//2
            x = x // GRID_SIZE
            y = i.y() + i.height()//2
            y = y // GRID_SIZE
            val = {'Row':y , 'Column':x}
            name = i.name
            if name:
                val["Name"] = name
            tt = i.toolTip()
            if(tt in dict):
                tt = tt + "1"
                while(tt in dict):
                    identifier = int(tt[-1])
                    tt = tt[:-1]
                    identifier += 1
                    tt += str(identifier)
            dict[tt] = val
        with open("position.json", "w") as file:
            json.dump(dict, file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
