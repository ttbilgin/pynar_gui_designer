from PyQt5 import QtWidgets,QtGui, QtCore
from PyQt5.QtCore import QDir, QFile, QUrl, Qt, QSize, QRect
from PyQt5.QtGui import QGuiApplication, QFont, QTextCursor, QIcon
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import (QMenu, QAbstractItemView, QGridLayout, qApp, QAction, QMainWindow, QToolBar,
QWidget,QApplication, QTextEdit, QPushButton, QLabel, QDesktopWidget, QCheckBox, QListWidget, QRadioButton, 
QScrollBar, QSpinBox, QPushButton,QLineEdit,QComboBox,QGroupBox,QPlainTextEdit, QMessageBox, QMdiSubWindow, QMdiArea)
from tkinter import *

mainwindow_p = None

class MdiWindow(QtWidgets.QMdiSubWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowSystemMenuHint)
        self.setWindowTitle("Başlık")
        self.props = ["title"]	
        #self.setFixedSize(400, 80)

    def closeEvent(self, event):
        # do stuff
        event.ignore()		

    def mouseMoveEvent(self, event):
        self.move(QtCore.QPoint(10,10))
        super().mouseMoveEvent(event)
    
    def mousePressEvent(self, event):
        event.accept()
        mainwindow_p.createobjectprops(self)
        super().mousePressEvent(event)
    
    #Pencere boyutunu sabitleme.
    def readjustSize(self):
        # print(corner_x)
        # print(corner_y)
        max_width = 0
        max_length = 0
        for i in mainwindow_p.penceredeki_itemler:
            max_width = max(max_width, i.geometry().right() - mainwindow_p.AracKutusu.geometry().right())
            max_length = max(max_length, i.geometry().bottom() - mainwindow_p.AracKutusu.geometry().top())
        # currentSize = mainwindow_p.pencere.geometry().size()
        self.setMinimumSize(max_width, max_length)
        # mainwindow_p.pencere.geometry().setSize(currentSize)


class MainClass(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setUI()
    
    def setUI(self):
    
        #Pointer
        global mainwindow_p
        mainwindow_p = self
        self.setFixedSize(800,600)
        
        #Pencere içinde kalan itemleri saklamak için set
        self.penceredeki_itemler = set()
        
        #Seçili obje için değişken
        self.selected = None
        
        self.w   = QWidget()
        #self.w.resize(1000,800)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.w)
        self.toolbar = QToolBar(self.w)
        self.verticalLayout.addWidget(self.toolbar)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.w)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AracKutusu = QtWidgets.QGroupBox(self.w)
        self.AracKutusu.setMinimumSize(QtCore.QSize(170, 0))
        self.AracKutusu.setObjectName("AracKutusu")
        self.AracKutusu.setTitle("Araç Kutusu")
        self.horizontalLayout.addWidget(self.AracKutusu)
        self.frame = QtWidgets.QFrame(self.w)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout2.setObjectName("verticalLayout2")
        self.pencere = MdiWindow() 
        self.mdiarea = QMdiArea()
        self.mdiarea.addSubWindow(self.pencere)
        self.verticalLayout2.addWidget(self.mdiarea)
        self.copAlani = QtWidgets.QGroupBox(self.frame)
        self.copAlani.setMinimumSize(QtCore.QSize(300, 75))
        self.copAlani.setTitle("")
        self.copAlani.setObjectName("copAlani")
        self.copButonu = QPushButton(self.copAlani)
        self.copButonu.setGeometry(QtCore.QRect(10, 10, 51, 51))
        self.copButonu.setObjectName("copButonu")
        self.copButonu.setIconSize(QSize(45, 45))
        self.copButonu.setStyleSheet("border: none")
        self.copButonu.setIcon(QIcon("assets/delete.png"))
        self.verticalLayout2.addWidget(self.copAlani)
        self.verticalLayout2.setStretch(0, 8)
        self.verticalLayout2.setStretch(1, 1)
        self.horizontalLayout.addWidget(self.frame, 1)
        self.groupBox = QtWidgets.QGroupBox(self.w)
        self.groupBox.setMinimumSize(QtCore.QSize(170, 0))
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle("Özellikler")
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        # self.horizontalLayout.setStretch(0, 2)
        # self.horizontalLayout.setStretch(1, 10)
        # self.horizontalLayout.setStretch(2, 2)

        self.pencere.setStyleSheet(
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

        self.kodaDonustur = QAction(QIcon('assets/headerLogo1.png'), 'Tasarımınızı PyNar Editörüne Aktarın', self)
        self.kodaDonustur.setShortcut('Ctrl+Q')
        self.kodaDonustur.triggered.connect(self.kodaDonusturFonksiyonu)
        self.toolbar.addAction(self.kodaDonustur)
        
        for k in range(5,0,-1):
            # toolbox'da Combobox oluştur
            exec(f'self.comboBox{k} = PComboBox(self.w)')
            exec(f'self.comboBox{k}.setGeometry(45, 80, 100, 20)')
            exec(f"self.comboBox{k}.setObjectName('comboBox{k}')")
            exec(f"self.comboBox{k}.installEventFilter(self)")
            exec(f'self.comboBox{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.comboBox{k}.customContextMenuRequested.connect(self.myListWidgetContext)')
            exec(f"self.comboBox{k}.addItem('Açılan Kutu')")

            # toolbox'da 3 PushButton oluştur
            exec(f'self.buton{k} = PPushButton(self.w)')
            exec(f'self.buton{k}.setGeometry(45, 110, 100, 20)')
            exec(f"self.buton{k}.setObjectName('buton{k}')")
            exec(f"self.buton{k}.installEventFilter(self)")
            exec(f"self.buton{k}.setText('Buton')")
            exec(f'self.buton{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.buton{k}.customContextMenuRequested.connect(self.myListWidgetContext)')

            # toolbox'da LineEdit oluştur
            exec(f'self.lineEdit{k} = PLineEdit(self.w)')
            exec(f'self.lineEdit{k}.setGeometry(45, 140, 100, 20)')
            exec(f"self.lineEdit{k}.setObjectName('lineEdit{k}')")
            exec(f"self.lineEdit{k}.installEventFilter(self)")
            exec(f"self.lineEdit{k}.setText('Metin Kutusu')")
            exec(f'self.lineEdit{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.lineEdit{k}.customContextMenuRequested.connect(self.myListWidgetContext)')

            # toolbox'da Label oluştur
            exec(f'self.label{k} = PLabel(self.w)')
            exec(f'self.label{k}.setGeometry(45, 170, 100, 20)')
            exec(f"self.label{k}.setObjectName('label{k}')")
            exec(f"self.label{k}.installEventFilter(self)")
            exec(f"self.label{k}.setText('Etiket')")
            exec(f'self.label{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.label{k}.customContextMenuRequested.connect(self.myListWidgetContext)')

            # toolbox'da checkbutton oluştur    
            exec(f'self.checkButton{k} = PCheckButton(self.w)')
            exec(f'self.checkButton{k}.setGeometry(45, 200, 100, 20)')
            exec(f"self.checkButton{k}.installEventFilter(self)")
            exec(f"self.checkButton{k}.setObjectName('checkButton{k}')")
            exec(f"self.checkButton{k}.setText('Kontrol Butonu')")
            exec(f'self.checkButton{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.checkButton{k}.customContextMenuRequested.connect(self.myListWidgetContext)')

            # toolbox'da listbox oluştur 
            exec(f'self.listBox{k} = PListWidget(self.w)')
            exec(f'self.listBox{k}.setGeometry(45, 230, 100, 40)')
            exec(f"self.listBox{k}.installEventFilter(self)")
            exec(f"self.listBox{k}.setObjectName('listBox{k}')")
            exec(f'self.listBox{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.listBox{k}.customContextMenuRequested.connect(self.myListWidgetContext)')
            exec(f"self.listBox{k}.addItem('Liste Kutusu')")

            # toolbox'da radiobuton oluştur
            exec(f'self.radioButton{k} = PRadioButton(self.w)')
            exec(f'self.radioButton{k}.setGeometry(45, 280, 100, 20)')
            exec(f"self.radioButton{k}.installEventFilter(self)")
            exec(f"self.radioButton{k}.setObjectName('radioButton{k}')")
            exec(f"self.radioButton{k}.setText('Radyo Butonu')")
            exec(f'self.radioButton{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.radioButton{k}.customContextMenuRequested.connect(self.myListWidgetContext)')

            # toolbox'da scrollbar oluştur
            exec(f'self.scrollBar{k} = PScrollBar(self.w)')
            exec(f'self.scrollBar{k}.setGeometry(45, 310, 100, 20)')
            exec(f"self.scrollBar{k}.setObjectName('scrollBar{k}')")
            exec(f"self.scrollBar{k}.installEventFilter(self)")
            exec(f'self.scrollBar{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.scrollBar{k}.customContextMenuRequested.connect(self.myListWidgetContext)')

            # toolbox'da spinbox oluştur
            exec(f'self.spinBox{k} = PSpinBox(self.w)')
            exec(f'self.spinBox{k}.setGeometry(45, 340, 100, 20)')
            exec(f"self.spinBox{k}.setObjectName('spinBox{k}')")
            exec(f"self.spinBox{k}.installEventFilter(self)")
            exec(f'self.spinBox{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.spinBox{k}.customContextMenuRequested.connect(self.myListWidgetContext)')

            # toolbox'da plaintext oluştur
            exec(f'self.PlainTextEdit{k} = PPlainTextEdit(self.w)')
            exec(f'self.PlainTextEdit{k}.setGeometry(45, 370, 100, 40)')
            exec(f"self.PlainTextEdit{k}.installEventFilter(self)")
            exec(f"self.PlainTextEdit{k}.setObjectName('PlainTextEdit{k}')")
            exec(f'self.PlainTextEdit{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.PlainTextEdit{k}.customContextMenuRequested.connect(self.myListWidgetContext)')
            exec(f'self.PlainTextEdit{k}.insertPlainText("Metin Alanı")')

        # Kodların yazılacağı bloğu oluştur
        self.kodBlogu = QPlainTextEdit()
        #self.kodBlogu.setGeometry(80,380,600,150)
        
        # Özellik penceresi oluştur
        
        self.grouplayout = QtWidgets.QVBoxLayout(self.groupBox)
        
        self.groupBox.ozellik_text = QLineEdit()
        self.groupBox.textcol_label = QLabel("Yazı:")
        self.textcol_layout = QtWidgets.QHBoxLayout()
        self.textcol_layout.addWidget(self.groupBox.textcol_label)
        self.textcol_layout.addWidget(self.groupBox.ozellik_text)
        self.grouplayout.addLayout(self.textcol_layout)
        self.groupBox.textcol_label.hide()
        self.groupBox.ozellik_text.hide()
        
        self.groupBox.ozellik_baslik = QLineEdit()
        self.groupBox.titlecol_label = QLabel("Başlık:")
        self.titlecol_layout = QtWidgets.QHBoxLayout()
        self.titlecol_layout.addWidget(self.groupBox.titlecol_label)
        self.titlecol_layout.addWidget(self.groupBox.ozellik_baslik)
        self.grouplayout.addLayout(self.titlecol_layout)
        self.groupBox.titlecol_label.hide()
        self.groupBox.ozellik_baslik.hide()
        
        self.grouplayout.addStretch()
        
        
        self.w.show()

    def myListWidgetContext(self,position):
        #Popup menu
        sender = self.sender()
        objName = sender.objectName()
        popMenu = QMenu()
        delAct =QAction(QIcon('assets/delete.png'),"Sil",self)
        popMenu.addAction(delAct)

        delAct.triggered.connect(lambda: self.DeleteItem(objName))
        exec(f"popMenu.exec_(self.{objName}.mapToGlobal(position))")

    #Delete group
    def DeleteItem(self, objName):
        ObjectName = objName[:-1]
        if ObjectName == "comboBox":
            exec(f"self.{objName}.move(45,80)")
        elif ObjectName == "buton":
            exec(f"self.{objName}.move(45,110)")
        elif ObjectName == "lineEdit":
            exec(f"self.{objName}.move(45,140)")
        elif ObjectName == "label":
            exec(f"self.{objName}.move(45,170)")
        elif ObjectName == "checkButton":
            exec(f"self.{objName}.move(45,200)")
        elif ObjectName == "listBox":
            exec(f"self.{objName}.move(45,230)")
        elif ObjectName == "radioButton":
            exec(f"self.{objName}.move(45,280)")
        elif ObjectName == "scrollBar":
            exec(f"self.{objName}.move(45,310)")
        elif ObjectName == "spinBox":
            exec(f"self.{objName}.move(45,340)")
        else:
            exec(f"self.{objName}.move(45,370)") 
    
    def kodaDonusturFonksiyonu(self):
        try:
            self.kodBlogu.insertPlainText(f"""from tkinter import *   
from tkinter import ttk
top = Tk()
top.geometry("{self.pencere.geometry().right()}x{self.pencere.geometry().bottom() - 30 }")""")

            for k in range(1,6,1):
                exec(f"""if (self.label{k}.pos().x() > self.AracKutusu.geometry().right() and self.label{k}.pos().x() < self.pencere.geometry().right() + self.AracKutusu.geometry().right() and self.label{k}.pos().y() > self.pencere.geometry().top() and self.label{k}.pos().y() < self.pencere.geometry().bottom() + 33) : 
        self.kodBlogu.insertPlainText("\\nlabel{k} = Label(top, text = 'label{k}').place(width=100, height=20, x = " + str(self.label{k}.pos().x() - self.AracKutusu.geometry().right() - 15) + ", y = " + str(self.label{k}.pos().y() - self.pencere.geometry().top() - 79)+")")""")
                
                exec(f"""if (self.buton{k}.pos().x() > self.AracKutusu.geometry().right() and self.buton{k}.pos().x() < self.pencere.geometry().right() + self.AracKutusu.geometry().right() and self.buton{k}.pos().y() > self.pencere.geometry().top() and self.buton{k}.pos().y() < self.pencere.geometry().bottom() + 33) : 
        self.kodBlogu.insertPlainText("\\nbuton{k} = Button(top, text = 'buton{k}').place(width=100, height=20, x = " + str(self.buton{k}.pos().x() - self.AracKutusu.geometry().right() - 15) + ", y = " + str(self.buton{k}.pos().y() - self.pencere.geometry().top() - 79)+")")""")
                
                exec(f"""if (self.lineEdit{k}.pos().x() > self.AracKutusu.geometry().right() and self.lineEdit{k}.pos().x() < self.pencere.geometry().right() + self.AracKutusu.geometry().right() and self.lineEdit{k}.pos().y() > self.pencere.geometry().top() and self.lineEdit{k}.pos().y() < self.pencere.geometry().bottom() + 33) : 
        self.kodBlogu.insertPlainText("\\nlineEdit{k} = Entry(top, text = 'lineEdit{k}').place(width=100, height=20, x = " + str(self.lineEdit{k}.pos().x() - self.AracKutusu.geometry().right() - 15) + ", y = " + str(self.lineEdit{k}.pos().y() - self.pencere.geometry().top() - 79)+")")""")
                
                exec(f"""if (self.comboBox{k}.pos().x() > self.AracKutusu.geometry().right() and self.comboBox{k}.pos().x() < self.pencere.geometry().right() + self.AracKutusu.geometry().right() and self.comboBox{k}.pos().y() > self.pencere.geometry().top() and self.comboBox{k}.pos().y() < self.pencere.geometry().bottom() + 33) : 
        self.kodBlogu.insertPlainText("\\ncomboBox{k} = ttk.Combobox(top, text = 'comboBox{k}').place(width=100, height=20, x = " + str(self.comboBox{k}.pos().x() - self.AracKutusu.geometry().right() - 15) + ", y = " + str(self.comboBox{k}.pos().y() - self.pencere.geometry().top() - 79)+")")""")
                
                exec(f"""if (self.checkButton{k}.pos().x() > self.AracKutusu.geometry().right() and self.checkButton{k}.pos().x() < self.pencere.geometry().right() + self.AracKutusu.geometry().right() and self.checkButton{k}.pos().y() > self.pencere.geometry().top() and self.checkButton{k}.pos().y() < self.pencere.geometry().bottom() + 33) : 
        self.kodBlogu.insertPlainText("\\ncheckButton{k} = Checkbutton(top, text = 'checkButton{k}').place(width=100, height=20, x = " + str(self.checkButton{k}.pos().x() - self.AracKutusu.geometry().right() - 15) + ", y = " + str(self.checkButton{k}.pos().y() - self.pencere.geometry().top() - 79)+")")""")
                
                exec(f"""if (self.listBox{k}.pos().x() > self.AracKutusu.geometry().right() and self.listBox{k}.pos().x() < self.pencere.geometry().right() + self.AracKutusu.geometry().right() and self.listBox{k}.pos().y() > self.pencere.geometry().top() and self.listBox{k}.pos().y() < self.pencere.geometry().bottom() + 33) : 
        self.kodBlogu.insertPlainText("\\nlistBox{k} = Listbox(top).place(width=100, height=40, x = " + str(self.listBox{k}.pos().x() - self.AracKutusu.geometry().right() - 15) + ", y = " + str(self.listBox{k}.pos().y() - self.pencere.geometry().top() - 79)+")")""")
                
                exec(f"""if (self.radioButton{k}.pos().x() > self.AracKutusu.geometry().right() and self.radioButton{k}.pos().x() < self.pencere.geometry().right() + self.AracKutusu.geometry().right() and self.radioButton{k}.pos().y() > self.pencere.geometry().top() and self.radioButton{k}.pos().y() < self.pencere.geometry().bottom() + 33) : 
        self.kodBlogu.insertPlainText("\\nradioButton{k} = Radiobutton(top, text = 'radioButton{k}').place(width=100, height=20, x = " + str(self.radioButton{k}.pos().x() - self.AracKutusu.geometry().right() - 15) + ", y = " + str(self.radioButton{k}.pos().y() - self.pencere.geometry().top() - 79)+")")""")
                
                exec(f"""if (self.scrollBar{k}.pos().x() > self.AracKutusu.geometry().right() and self.scrollBar{k}.pos().x() < self.pencere.geometry().right() + self.AracKutusu.geometry().right() and self.scrollBar{k}.pos().y() > self.pencere.geometry().top() and self.scrollBar{k}.pos().y() < self.pencere.geometry().bottom() + 33) : 
        self.kodBlogu.insertPlainText("\\nscrollBar{k} = Scale(top).place(width=100, height=20, x = " + str(self.scrollBar{k}.pos().x() - self.AracKutusu.geometry().right() - 15) + ", y = " + str(self.scrollBar{k}.pos().y() - self.pencere.geometry().top() - 79)+")")""")
                
                exec(f"""if (self.spinBox{k}.pos().x() > self.AracKutusu.geometry().right() and self.spinBox{k}.pos().x() < self.pencere.geometry().right() + self.AracKutusu.geometry().right() and self.spinBox{k}.pos().y() > self.pencere.geometry().top() and self.spinBox{k}.pos().y() < self.pencere.geometry().bottom() + 33) : 
        self.kodBlogu.insertPlainText("\\nspinBox{k} = Spinbox(top, text = 'spinBox{k}').place(width=100, height=20, x = " + str(self.spinBox{k}.pos().x() - self.AracKutusu.geometry().right() - 15) + ", y = " + str(self.spinBox{k}.pos().y() - self.pencere.geometry().top() - 79)+")")""")
                
                exec(f"""if (self.PlainTextEdit{k}.pos().x() > self.AracKutusu.geometry().right() and self.PlainTextEdit{k}.pos().x() < self.pencere.geometry().right() + self.AracKutusu.geometry().right() and self.PlainTextEdit{k}.pos().y() > self.pencere.geometry().top() and self.PlainTextEdit{k}.pos().y() < self.pencere.geometry().bottom() + 33) : 
        self.kodBlogu.insertPlainText("\\ntext{k} = Text(top).place(width=100, height=40, x = " + str(self.PlainTextEdit{k}.pos().x() - self.AracKutusu.geometry().right() - 15) + ", y = " + str(self.PlainTextEdit{k}.pos().y() - self.pencere.geometry().top() - 79)+")")""")
            
            self.kodBlogu.insertPlainText("""
top.mainloop()""")
            f = open("pui.py", "w")
            f.write(self.kodBlogu.toPlainText())
            f.close()
            self.mesajKutusu = QMessageBox()
            self.mesajKutusu.setWindowTitle("Başarılı")
            self.mesajKutusu.setText("Kodunuz Başarıyla Üretilmiştir")
            self.mesajKutusu.setIcon(QMessageBox.Information)
            self.mesajKutusu.setStandardButtons(QMessageBox.Ok)
            self.mesajKutusu.exec()
        except:
            self.mesajKutusu = QMessageBox()
            self.mesajKutusu.setWindowTitle("Hata")
            self.mesajKutusu.setText("Kod Üretilirken Bir Hata Meydana Geldi")
            self.mesajKutusu.setIcon(QMessageBox.critical)
            self.mesajKutusu.setStandardButtons(QMessageBox.Ok)
            self.mesajKutusu.exec()
    
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease: 
            #Çop kutusu alanındaysa objeyi sol tarafa taşı.
            if (eval(f"self.{obj.objectName()}.pos().x() > self.AracKutusu.geometry().right() + self.copAlani.geometry().left()  - 31 and self.{obj.objectName()}.pos().x() < self.AracKutusu.geometry().right() + self.copAlani.geometry().left()  + 68 and self.{obj.objectName()}.pos().y() > self.copAlani.geometry().top() + 56 and self.{obj.objectName()}.pos().y() < self.copAlani.geometry().top() + 100")):
                ObjectName = obj.objectName()[:-1]
                if ObjectName == "comboBox":
                    exec(f"self.{obj.objectName()}.move(45,80)")
                elif ObjectName == "buton":
                    exec(f"self.{obj.objectName()}.move(45,110)")
                elif ObjectName == "lineEdit":
                    exec(f"self.{obj.objectName()}.move(45,140)")
                elif ObjectName == "label":
                    exec(f"self.{obj.objectName()}.move(45,170)")
                elif ObjectName == "checkButton":
                    exec(f"self.{obj.objectName()}.move(45,200)")
                elif ObjectName == "listBox":
                    exec(f"self.{obj.objectName()}.move(45,230)")
                elif ObjectName == "radioButton":
                    exec(f"self.{obj.objectName()}.move(45,280)")
                elif ObjectName == "scrollBar":
                    exec(f"self.{obj.objectName()}.move(45,310)")
                elif ObjectName == "spinBox":
                    exec(f"self.{obj.objectName()}.move(45,340)")
                else:
                    exec(f"self.{obj.objectName()}.move(45,370)")
                self.penceredeki_itemler.remove(obj)
            else:#Yoksa pencere dışındaysa pencerenin içine hareket ettir
                #Xerr = X tarafa ne kadar hareket ettirilmesi lazım
                Righterr = self.AracKutusu.geometry().right() + 15 + self.pencere.geometry().left() - obj.geometry().left() 
                Lefterr = obj.geometry().right() - (self.AracKutusu.geometry().right() + self.pencere.geometry().right())
                Boterr = self.pencere.geometry().top() + 75 - obj.geometry().top()
                Toperr = obj.geometry().bottom() - (self.pencere.geometry().bottom() + 45)
                #Eğer gereken miktar 0'dan büyükse o yöne doğru hareket ettir
                if(Righterr > 0):
                    obj.move(obj.pos().x() + Righterr, obj.pos().y())
                if(Lefterr > 0):
                    obj.move(obj.pos().x() - Lefterr, obj.pos().y())
                if(Boterr > 0):
                    obj.move(obj.pos().x(), obj.pos().y() + Boterr)
                if(Toperr > 0):
                    obj.move(obj.pos().x(), obj.pos().y() - Toperr)
                self.penceredeki_itemler.add(obj)
            mainwindow_p.pencere.readjustSize()
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if obj in self.penceredeki_itemler:
                self.createobjectprops(obj)
        return super().eventFilter(obj, event)
    
    def createobjectprops(self, obj):
        self.selected = obj
        self.deleteobjectprops()
        
        if "text" in obj.props:
            self.groupBox.textcol_label.show()
            self.groupBox.ozellik_text.show()
            self.groupBox.ozellik_text.textChanged.connect(self.mirrorText)
            self.groupBox.ozellik_text.setText(obj.text())
            
            
        if "title" in obj.props:
            self.groupBox.titlecol_label.show()
            self.groupBox.ozellik_baslik.show()
            self.groupBox.ozellik_baslik.textChanged.connect(self.mirrorText)
            self.groupBox.ozellik_baslik.setText(obj.windowTitle())
    
    def deleteobjectprops(self):
        for i in self.groupBox.findChildren(QWidget):
            i.hide()

    def mirrorText(self, obj):
        if "text" in self.selected.props:
            self.selected.setText(self.groupBox.ozellik_text.text())
        if "title" in self.selected.props:
            self.selected.setWindowTitle(self.groupBox.ozellik_baslik.text())


class PLabel(QLabel):
    
    def __init__(self, parent = None):
        super(PLabel, self).__init__(parent)
        self.name = ""
        self.props=["text"]
        #self.setMinimumSize(75,60)

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        # pos = self.pos()
        # print(pos.x(), pos.y()) #debug için pozisyon bilgisi
        if event.buttons() == Qt.LeftButton:
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
        pos = self.pos() #debug için pozisyon bilgisi
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        #super(DragButton, self).mouseReleaseEvent(event)

class PSpinBox(QSpinBox):
    
    def __init__(self, parent = None):
        super(PSpinBox, self).__init__(parent)
        self.name = ""
        self.props = []
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
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        #super(DragButton, self).mouseReleaseEvent(event)

class PPlainTextEdit(QPlainTextEdit):
    
    def __init__(self, parent = None):
        super(PPlainTextEdit, self).__init__(parent)
        self.name = ""
        self.props = []
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
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        #super(DragButton, self).mouseReleaseEvent(event)


class PScrollBar(QScrollBar):
    
    def __init__(self, parent = None):
        super(PScrollBar, self).__init__(parent)
        self.name = ""
        self.props = []
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
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        #super(DragButton, self).mouseReleaseEvent(event)


class PRadioButton(QRadioButton):
    
    def __init__(self, parent = None):
        super(PRadioButton, self).__init__(parent)
        self.name = ""
        self.props = ["text"]
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
        self.props = []
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
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        #super(DragButton, self).mouseReleaseEvent(event)

class PListWidget(QListWidget):
    
    def __init__(self, parent = None):
        super(PListWidget, self).__init__(parent)
        self.name = ""
        self.props = []
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
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        #super(DragButton, self).mouseReleaseEvent(event)


class PCheckButton(QCheckBox):
    
    def __init__(self, parent = None):
        super(PCheckButton, self).__init__(parent)
        self.name = ""
        self.props = ["text"]
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
        self.props = []
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
        #self.ledittoCode(pos)
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
        self.props = ["text"]
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
        #self.butontoCode(pos)
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
        self.props = []
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
        # print("--GroupBox--")
        # print(pos.x(), pos.y()) #debug için pozisyon bilgisi
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        #super(DragButton, self).mouseReleaseEvent(event)

if __name__ == "__main__":
    app = QApplication([])
    w = MainClass()
    app.exec_()
