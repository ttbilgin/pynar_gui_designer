from PyQt5 import QtWidgets,QtGui, QtCore
from PyQt5.QtCore import QDir, QFile, QUrl, Qt, QSize, QRect
from PyQt5.QtGui import QGuiApplication, QFont, QTextCursor, QIcon
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import (QMenu, QAbstractItemView, QGridLayout, qApp, QAction, QMainWindow, QToolBar,
QWidget,QApplication, QTextEdit, QPushButton, QLabel, QDesktopWidget, QCheckBox, QListWidget, QRadioButton, 
QSlider, QSpinBox, QPushButton,QLineEdit,QComboBox,QGroupBox,QPlainTextEdit, QMessageBox, QMdiSubWindow, QMdiArea, QColorDialog)
from tkinter import *

import saveload

mainwindow_p = None

DEFAULT_WINDOW_COLOR = "#f0f0f0"

class MdiWindow(QtWidgets.QMdiSubWindow):
    color = DEFAULT_WINDOW_COLOR
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowSystemMenuHint)
        self.setWindowTitle("Başlık")
        self.props = ["title", "color", "width", "height"]
        self.setStyleSheet(f"background-color: {DEFAULT_WINDOW_COLOR};")
        #self.setFixedSize(400, 80)

    def closeEvent(self, event):
        # do stuff
        event.ignore()		

    def mouseMoveEvent(self, event):
        self.move(QtCore.QPoint(10,10))
        super().mouseMoveEvent(event)
    
    def mousePressEvent(self, event):
        event.accept()
        mainwindow_p.onClick(self)
        super().mousePressEvent(event)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        try:
            mainwindow_p.groupBox.ozellik_yukseklik_textbox.setText(str(self.size().height()))
            mainwindow_p.groupBox.ozellik_genislik_textbox.setText(str(self.size().width()))
        except AttributeError:
            pass
    
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

        self.kodaDonustur = QAction(QIcon('assets/headerLogo1.png'), 'Tasarımınızı PyNar Editörüne Aktarın', self)
        self.kodaDonustur.setShortcut('Ctrl+Q')
        self.kodaDonustur.triggered.connect(self.kodaDonusturFonksiyonu)
        self.toolbar.addAction(self.kodaDonustur)
        
        self.kaydet = QAction(QIcon('assets/savefile.png'), 'Tasarımınızı Kaydedin', self)
        self.kaydet.setShortcut('Ctrl+S')
        self.kaydet.triggered.connect(self.kaydetFonksiyonu)
        self.toolbar.addAction(self.kaydet)
        
        self.yukle = QAction(QIcon('assets/loadfile.png'), 'Tasarım Yükleyin', self)
        self.yukle.triggered.connect(self.yukleFonksiyonu)
        self.toolbar.addAction(self.yukle)
        
        for k in range(5,0,-1):
            # toolbox'da Combobox oluştur
            exec(f'self.comboBox{k} = PComboBox(self.w)')
            exec(f'self.comboBox{k}.setGeometry(45, 80, 100, 25)')
            exec(f"self.comboBox{k}.setObjectName('comboBox{k}')")
            exec(f"self.comboBox{k}.installEventFilter(self)")
            exec(f'self.comboBox{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.comboBox{k}.customContextMenuRequested.connect(self.myListWidgetContext)')
            exec(f"self.comboBox{k}.addItem('Açılan Kutu')")

            # toolbox'da 3 PushButton oluştur
            exec(f'self.buton{k} = PPushButton(self.w)')
            exec(f'self.buton{k}.setGeometry(45, 110, 100, 25)')
            exec(f"self.buton{k}.setObjectName('buton{k}')")
            exec(f"self.buton{k}.installEventFilter(self)")
            exec(f"self.buton{k}.setText('Buton')")
            exec(f'self.buton{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.buton{k}.customContextMenuRequested.connect(self.myListWidgetContext)')

            # toolbox'da LineEdit oluştur
            exec(f'self.lineEdit{k} = PLineEdit(self.w)')
            exec(f'self.lineEdit{k}.setGeometry(45, 140, 100, 25)')
            exec(f"self.lineEdit{k}.setObjectName('lineEdit{k}')")
            exec(f"self.lineEdit{k}.installEventFilter(self)")
            exec(f"self.lineEdit{k}.setText('Metin Kutusu')")
            exec(f'self.lineEdit{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.lineEdit{k}.customContextMenuRequested.connect(self.myListWidgetContext)')

            # toolbox'da Label oluştur
            exec(f'self.label{k} = PLabel(self.w)')
            exec(f'self.label{k}.setGeometry(45, 170, 100, 25)')
            exec(f"self.label{k}.setObjectName('label{k}')")
            exec(f"self.label{k}.installEventFilter(self)")
            exec(f"self.label{k}.setText('Etiket')")
            exec(f'self.label{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.label{k}.customContextMenuRequested.connect(self.myListWidgetContext)')

            # toolbox'da checkbutton oluştur    
            exec(f'self.checkButton{k} = PCheckButton(self.w)')
            exec(f'self.checkButton{k}.setGeometry(45, 200, 100, 25)')
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
            exec(f'self.radioButton{k}.setGeometry(45, 280, 100, 25)')
            exec(f"self.radioButton{k}.installEventFilter(self)")
            exec(f"self.radioButton{k}.setObjectName('radioButton{k}')")
            exec(f"self.radioButton{k}.setText('Radyo Butonu')")
            exec(f'self.radioButton{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.radioButton{k}.customContextMenuRequested.connect(self.myListWidgetContext)')

            # toolbox'da scrollbar oluştur
            exec(f'self.scrollBar{k} = PSlider(Qt.Horizontal, self.w)')
            exec(f'self.scrollBar{k}.setGeometry(45, 310, 100, 25)')
            exec(f"self.scrollBar{k}.setObjectName('scrollBar{k}')")
            exec(f"self.scrollBar{k}.installEventFilter(self)")
            exec(f'self.scrollBar{k}.setContextMenuPolicy(Qt.CustomContextMenu)')
            exec(f'self.scrollBar{k}.customContextMenuRequested.connect(self.myListWidgetContext)')

            # toolbox'da spinbox oluştur
            exec(f'self.spinBox{k} = PSpinBox(self.w)')
            exec(f'self.spinBox{k}.setGeometry(45, 340, 100, 25)')
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
        
        # Özellik penceresinin layout'unu oluştur.
        self.ozellik_layout = QtWidgets.QVBoxLayout(self.groupBox)
        
        #Metin(text) özelliğine denk gelen özellik penceresi widgetları'nı oluşturma ve düzenleme.
        self.groupBox.ozellik_metin_textbox = QLineEdit()
        self.groupBox.ozellik_metin_label = QLabel("Yazı:")
        self.ozellik_metin_layout = QtWidgets.QHBoxLayout()
        self.ozellik_metin_layout.addWidget(self.groupBox.ozellik_metin_label)
        self.ozellik_metin_layout.addWidget(self.groupBox.ozellik_metin_textbox)
        self.ozellik_layout.addLayout(self.ozellik_metin_layout)
        
        #Başlık(title) özelliğine denk gelen özellik penceresi widgetları'nı oluşturma ve düzenleme.
        self.groupBox.ozellik_baslik_textbox = QLineEdit()
        self.groupBox.ozellik_baslik_label = QLabel("Başlık:")
        self.ozellik_baslik_layout = QtWidgets.QHBoxLayout()
        self.ozellik_baslik_layout.addWidget(self.groupBox.ozellik_baslik_label)
        self.ozellik_baslik_layout.addWidget(self.groupBox.ozellik_baslik_textbox)
        self.ozellik_layout.addLayout(self.ozellik_baslik_layout)
        
        #Renk(color) özelliğine denk gelen özellik penceresi widgetları'nı oluşturma ve düzenleme.
        self.groupBox.ozellik_renk_textbox = ColorLineEdit(self)
        self.groupBox.ozellik_renk_label = QLabel("Renk:")
        self.ozellik_renk_layout = QtWidgets.QHBoxLayout()
        self.ozellik_renk_layout.addWidget(self.groupBox.ozellik_renk_label)
        self.ozellik_renk_layout.addWidget(self.groupBox.ozellik_renk_textbox)
        self.ozellik_layout.addLayout(self.ozellik_renk_layout)
        
        #Boyut özelliğinin metin kutusuna sadece sayı girilmesini sağlamak için gerekli
        self.intonly = QtGui.QIntValidator()
        
        #Boyut(size) özelliğine denk gelen özellik penceresi widgetları'nı oluşturma ve düzenleme.
        
        #Genişlik
        
        self.groupBox.ozellik_genislik_textbox = QLineEdit()
        self.groupBox.ozellik_genislik_textbox.setValidator(self.intonly)
        self.groupBox.ozellik_genislik_label = QLabel("Genişlik:")
        self.ozellik_genislik_layout = QtWidgets.QHBoxLayout()
        self.ozellik_genislik_layout.addWidget(self.groupBox.ozellik_genislik_label)
        self.ozellik_genislik_layout.addWidget(self.groupBox.ozellik_genislik_textbox)
        self.ozellik_layout.addLayout(self.ozellik_genislik_layout)
        
        #Yükseklik
        
        self.groupBox.ozellik_yukseklik_textbox = QLineEdit()
        self.groupBox.ozellik_yukseklik_textbox.setValidator(self.intonly)
        self.groupBox.ozellik_yukseklik_label = QLabel("Yükseklik:")
        self.ozellik_yukseklik_layout = QtWidgets.QHBoxLayout()
        self.ozellik_yukseklik_layout.addWidget(self.groupBox.ozellik_yukseklik_label)
        self.ozellik_yukseklik_layout.addWidget(self.groupBox.ozellik_yukseklik_textbox)
        self.ozellik_layout.addLayout(self.ozellik_yukseklik_layout)
        
        #Özellik penceresini üste hizalı olacak şekilde düzenleme ve bütün widget'ları görünmez yapma
        self.ozellik_layout.addStretch()
        self.hideObjectProps()
        
        #Pencereyi gösterme
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
        counter = 0
        self.kodBlogu.clear()
        self.kodBlogu.insertPlainText(f"""import tkinter as tk
import tkinter.ttk as ttk
class App:
    def __init__(self,root):
        self.s = ttk.Style()
        self.s.theme_use('alt')
        root.geometry("{self.pencere.geometry().right()}x{self.pencere.geometry().bottom() - 30 }")
        """)
        counter = 0
        commands = ""
        for i in self.penceredeki_itemler:
            counter += 1
            try:
                if(i.color == ""):
                    i.color = self.pencere.color
            except:
                pass
            q_origin_class_name = type(i).__bases__[0].__name__
            
            #Combobox
            
            if(q_origin_class_name == "QComboBox"):
                self.kodBlogu.insertPlainText(f"""
        self.s.map("self.Combobox{counter}.TCombobox", fieldbackground = [('!active', '{i.color}'), ('active', '{i.color}'), ('pressed', '{i.color}')])
        self.Combobox{counter} = ttk.Combobox(root, style = "self.Combobox{counter}.TCombobox")
        self.Combobox{counter}.place(width={i.size().width()}, height={i.size().height()}, x = {i.pos().x() - self.AracKutusu.geometry().right() - 15}, y = {i.pos().y() - self.pencere.geometry().top() - 79})
""")
            
            #Button
            
            if(q_origin_class_name == "QPushButton"):
                self.kodBlogu.insertPlainText(f"""
        self.s.map("self.Button{counter}.TButton", background = [('!active', '{i.color}'), ('active', '{i.color}'), ('pressed', '{i.color}')])
        self.Button{counter} = ttk.Button(root, text = "{i.text()}", command = self.Button{counter}clicked, style = "self.Button{counter}.TButton")
        self.Button{counter}.place(width={i.size().width()}, height={i.size().height()}, x = {i.pos().x() - self.AracKutusu.geometry().right() - 15}, y = {i.pos().y() - self.pencere.geometry().top() - 79})
""")
                commands += f"""
    def Button{counter}clicked(self):
        print("Button{counter} clicked")
"""
            
            #LineEdit/Entry
            
            if(q_origin_class_name == "QLineEdit"):
                self.kodBlogu.insertPlainText(f"""
        self.s.map("self.Entry{counter}.TEntry", fieldbackground = [('!active', '{i.color}'), ('active', '{i.color}'), ('pressed', '{i.color}')])
        self.Entry{counter} = ttk.Entry(root, text = "{i.text()}", style = "self.Entry{counter}.TEntry")
        self.Entry{counter}.place(width={i.size().width()}, height={i.size().height()}, x = {i.pos().x() - self.AracKutusu.geometry().right() - 15}, y = {i.pos().y() - self.pencere.geometry().top() - 79})
""")
            
            #Label
            
            if(q_origin_class_name == "QLabel"):
                self.kodBlogu.insertPlainText(f"""
        self.s.map("self.Label{counter}.TLabel", background = [('!active', '{i.color}'), ('active', '{i.color}'), ('pressed', '{i.color}')])
        self.Label{counter} = ttk.Label(root, text = "{i.text()}", style = "self.Label{counter}.TLabel")
        self.Label{counter}.place(width={i.size().width()}, height={i.size().height()}, x = {i.pos().x() - self.AracKutusu.geometry().right() - 15}, y = {i.pos().y() - self.pencere.geometry().top() - 79})
""")
            
            #Checkbox/Checkbutton
            
            if(q_origin_class_name == "QCheckBox"):
                self.kodBlogu.insertPlainText(f"""
        self.s.map("self.Checkbutton{counter}.TCheckbutton", background = [('!active', '{i.color}'), ('active', '{i.color}'), ('pressed', '{i.color}')])
        self.Checkbutton{counter} = ttk.Checkbutton(root, text = "{i.text()}", command = self.Checkbutton{counter}clicked, style = "self.Checkbutton{counter}.TCheckbutton")
        self.Checkbutton{counter}.place(width={i.size().width()}, height={i.size().height()}, x = {i.pos().x() - self.AracKutusu.geometry().right() - 15}, y = {i.pos().y() - self.pencere.geometry().top() - 79})
""")
                commands += f"""
    def Checkbutton{counter}clicked(self):
        print("Checkbutton{counter} clicked")
"""
            
            #ListWidget/Listbox
            
            if(q_origin_class_name == "QListWidget"):
                self.kodBlogu.insertPlainText(f"""
        self.Listbox{counter} = tk.Listbox(root, bg = "{i.color}")
        self.Listbox{counter}.place(width={i.size().width()}, height={i.size().height()}, x = {i.pos().x() - self.AracKutusu.geometry().right() - 15}, y = {i.pos().y() - self.pencere.geometry().top() - 79})
""")
            
            #Radiobutton
            
            if(q_origin_class_name == "QRadioButton"):
                self.kodBlogu.insertPlainText(f"""
        self.s.map("self.Radiobutton{counter}.TRadiobutton", background = [('!active', '{i.color}'), ('active', '{i.color}'), ('pressed', '{i.color}')])
        self.Radiobutton{counter} = ttk.Radiobutton(root, text = "{i.text()}", command = self.Radiobutton{counter}clicked, style = "self.Radiobutton{counter}.TRadiobutton")
        self.Radiobutton{counter}.place(width={i.size().width()}, height={i.size().height()}, x = {i.pos().x() - self.AracKutusu.geometry().right() - 15}, y = {i.pos().y() - self.pencere.geometry().top() - 79})
""")
                commands += f"""
    def Radiobutton{counter}clicked(self):
        print("Radiobutton{counter} clicked")
"""
            #Slider/Scale
            
            if(q_origin_class_name == "QSlider"):
                self.kodBlogu.insertPlainText(f"""
        self.s.map("self.Scale{counter}.Horizontal.TScale", background = [('!active', '{mainwindow_p.pencere.color}'), ('active', '{mainwindow_p.pencere.color}'), ('pressed', '{mainwindow_p.pencere.color}')])
        self.Scale{counter} = ttk.Scale(root, command = self.Scale{counter}changed, from_=0, to = 10, style = "self.Scale{counter}.Horizontal.TScale")
        self.Scale{counter}.place(width=(width={i.size().width()}, height={i.size().height()}, x = {i.pos().x() - self.AracKutusu.geometry().right() - 15}, y = {i.pos().y() - self.pencere.geometry().top() - 79})
""")
                commands += f"""
    def Scale{counter}changed(self, x):
        print(x)
"""
            #Spinbox
            
            if(q_origin_class_name == "QSpinBox"):
                self.kodBlogu.insertPlainText(f"""
        self.Spinbox{counter} = tk.Spinbox(root, command = self.Spinbox{counter}changed, from_=0, to = 10, bg = "{i.color}")
        self.Spinbox{counter}.place(width=(width={i.size().width()}, height={i.size().height()}, x = {i.pos().x() - self.AracKutusu.geometry().right() - 15}, y = {i.pos().y() - self.pencere.geometry().top() - 79})
""")
                commands += f"""
    def Spinbox{counter}changed(self):
        print(self.Spinbox{counter}.get())
"""
            
            #PlainTextEdit/Text
            
            if(q_origin_class_name == "QPlainTextEdit"):
                self.kodBlogu.insertPlainText(f"""
        self.Text{counter} = tk.Text(root, bg = "{i.color}")
        self.Text{counter}.insert(tk.END, "{i.toPlainText()}")
        self.Text{counter}.place(width={i.size().width()}, height={i.size().height()}, x = {i.pos().x() - self.AracKutusu.geometry().right() - 15}, y = {i.pos().y() - self.pencere.geometry().top() - 79})
""")

        #Son eklemeler
        self.kodBlogu.insertPlainText(commands)

        self.kodBlogu.insertPlainText(f"""
if __name__ == "__main__":
    root = tk.Tk()
    root['bg'] = "{mainwindow_p.pencere.color}"
    root.title("{mainwindow_p.pencere.windowTitle()}")
    app = App(root)
    root.mainloop()
""")
        #pui.py dosyasını yazma
        try:
            f = open("pui.py", "w", encoding = "utf-8")
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
    
    #Verilen objeyi sil.
    def removeObject(self, obj):
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
        #Pencerede bulunanlar listesinden objeyi çıkar.
        try:
            self.penceredeki_itemler.remove(obj)
        except KeyError:
            pass
        self.selected = None
        self.hideObjectProps()
        try:
            obj.initVars()
            obj.setStyleSheet("")
        except Exception as e:
            print(e)
    
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease: 
            if (eval(f"self.{obj.objectName()}.pos().x() > self.AracKutusu.geometry().right() + self.copAlani.geometry().left()  - 31 and self.{obj.objectName()}.pos().x() < self.AracKutusu.geometry().right() + self.copAlani.geometry().left()  + 68 and self.{obj.objectName()}.pos().y() > self.copAlani.geometry().top() + 56 and self.{obj.objectName()}.pos().y() < self.copAlani.geometry().top() + 100")):#Çop kutusu alanındaysa objeyi sil.
               self.removeObject(obj)
            else:#Yoksa pencere dışındaysa pencerenin içine hareket ettir
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
                # self.selectedHighlight(obj)
                # self.createObjectProps(obj)
                self.onClick(obj)
        return super().eventFilter(obj, event)
        
    #Verilen objedeki belirli bir css parametresini silen fonksiyon.
    def deleteStyle(self, obj, param):
        if obj == None:
            return
        ss = obj.styleSheet()
        start = ss.find(param)
        if(start > -1):
            end = ss.find(";", start)
            ss = ss[:start] + ss[end + 1:]
            obj.setStyleSheet(ss)
    
    #Bir widget'a tıklandığında yapılması gerekenleri içeren fonksiyon.
    def onClick(self, obj):
        self.deleteStyle(self.selected, "border: ")
        self.deleteStyle(self.pencere, "border: ")
        self.selectedHighlight(obj)
        self.createObjectProps(obj)
    
    #Verilen objedeki belirli bir css parametresini değiştiren fonksiyon.
    def addStyle(self, obj, param, value):
        ss = obj.styleSheet()
        #Eğer parametre yoksa yeni bir satır ekle.
        if(ss.find(param) == -1):
            newstyle = ss + param + value + ";"
            obj.setStyleSheet(newstyle)
            return
        start = ss.find(param) + len(param)
        end = ss.find(";", start)
        ss = ss[:start] + value + ss[end:]
        obj.setStyleSheet(ss)
    
    #Seçilen widget'ın çerçevesini mavi yapan fonksiyon.
    def selectedHighlight(self, obj):
        self.addStyle(obj, "border: ", "3px solid blue")
    
    #Tıklanan widget'ın özelliklerini göstermeye yarayan fonksiyon.
    def createObjectProps(self, obj):
        self.selected = obj
        self.hideObjectProps()
        
        if "text" in obj.props:
            self.groupBox.ozellik_metin_label.show()
            self.groupBox.ozellik_metin_textbox.show()
            self.groupBox.ozellik_metin_textbox.textEdited.connect(self.mirrorText)
            self.groupBox.ozellik_metin_textbox.setText(obj.text())
            
        if "title" in obj.props:
            self.groupBox.ozellik_baslik_label.show()
            self.groupBox.ozellik_baslik_textbox.show()
            self.groupBox.ozellik_baslik_textbox.textEdited.connect(self.mirrorText)
            self.groupBox.ozellik_baslik_textbox.setText(obj.windowTitle())
        
        if "color" in obj.props:
            self.groupBox.ozellik_renk_label.show()
            self.groupBox.ozellik_renk_textbox.show()
            self.addStyle(self.groupBox.ozellik_renk_textbox, "background-color: ", obj.color)
            self.groupBox.ozellik_renk_textbox.color = obj.color
            
        if "width" in obj.props:
            self.groupBox.ozellik_genislik_label.show()
            self.groupBox.ozellik_genislik_textbox.show()
            self.groupBox.ozellik_genislik_textbox.textEdited.connect(self.mirrorText)
            self.groupBox.ozellik_genislik_textbox.setText(str(obj.size().width()))
            
        if "height" in obj.props:
            self.groupBox.ozellik_yukseklik_label.show()
            self.groupBox.ozellik_yukseklik_textbox.show()
            self.groupBox.ozellik_yukseklik_textbox.textEdited.connect(self.mirrorText)
            self.groupBox.ozellik_yukseklik_textbox.setText(str(obj.size().height()))
    
    #Özellik penceresindeki bütün özellikleri gizle.
    def hideObjectProps(self):
        for i in self.groupBox.findChildren(QWidget):
            i.hide()
    
    #Özellik penceresindeki parametrelerin değişmesi üzerine penceredeki widgetların bu değşikliğe göre değişmesini sağlayan fonksiyon.
    def mirrorText(self, obj):
        if "text" in self.selected.props:
            self.selected.setText(self.groupBox.ozellik_metin_textbox.text())
        if "title" in self.selected.props:
            self.selected.setWindowTitle(self.groupBox.ozellik_baslik_textbox.text())
        if "width" in self.selected.props:
            try:
                self.selected.resize(int(self.groupBox.ozellik_genislik_textbox.text()), self.selected.size().height())
            except:
                pass
        if "height" in self.selected.props:
            try:
                self.selected.resize(self.selected.size().width(), int(self.groupBox.ozellik_yukseklik_textbox.text()))
            except Exception as e:
                pass
    
    #Renk özelliğine tıklandığında ve bir renk seçildiğinde objenin ve renk textboxunun rengini değiştiren fonksiyon.
    def colorChange(self):
        x = QColorDialog().getColor()
        if(not x.isValid()):
            return
        chosenColor = x.name()
        self.addStyle(self.groupBox.ozellik_renk_textbox, "background-color: ", chosenColor)
        #self.groupBox.ozellik_renk_textbox.setStyleSheet(f"background-color: {chosenColor}")
        self.addStyle(self.selected, "background-color: ", chosenColor)
        #self.selected.setStyleSheet(f"background-color: {chosenColor}")
        self.groupBox.ozellik_renk_textbox.color = chosenColor
        self.selected.color = chosenColor
    
    def kaydetFonksiyonu(self):
        saveload.kaydet(self)
        
    def yukleFonksiyonu(self):
        saveload.yukle(self)
        

class PLabel(QLabel):

    def __init__(self, parent = None):
        super(PLabel, self).__init__(parent)
        self.initVars()
        #self.setMinimumSize(75,60)

    def initVars(self):
        self.name = ""
        self.color = ""
        self.props=["text", "color", "width", "height"]
        self.resize(100,25)

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
        self.initVars()
        #self.setMinimumSize(75,60)
    
    def initVars(self):
        self.name = ""
        self.color = "#ffffff"
        self.props = ["color", "width", "height"]
        self.resize(100,25)
    
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
        self.initVars()
        #self.setMinimumSize(75,60)
    
    def initVars(self):
        self.name = ""
        self.color = "#ffffff"
        self.props = ["color", "width", "height"]
        self.resize(100,25)
    
    def mousePressEvent(self, event):
        #eventFilter'da düzgün çalışmadığı için kod buraya alındı
        if self in mainwindow_p.penceredeki_itemler:
            mainwindow_p.onClick(self)
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


class PSlider(QSlider):

    def __init__(self, Orientation, parent = None):
        super(PSlider, self).__init__(Orientation, parent)
        self.initVars()
        #self.setMinimumSize(75,60)
    
    def initVars(self):
        self.name = ""
        self.props = ["width", "height"]
        self.resize(100,25)
    
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
        self.initVars()
        #self.setMinimumSize(75,60)
    
    def initVars(self):
        self.name = ""
        self.color = ""
        self.props = ["text", "color", "width", "height"]
        self.resize(100,25)
        
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
        self.initVars()
        #self.setMinimumSize(75,60)
    
    def initVars(self):
        self.name = ""
        self.props = ["color", "width", "height"]
        self.color = "#ffffff"
        self.resize(100,25)
    
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
        self.initVars()
        #self.setMinimumSize(75,60)
    
    def initVars(self):
        self.name = ""
        self.color = "#ffffff"
        self.props = ["color", "width", "height"]
        self.resize(100,40)
        
    def mousePressEvent(self, event):
        #eventFilter'da düzgün çalışmadığı için kod buraya alındı
        if self in mainwindow_p.penceredeki_itemler:
            mainwindow_p.onClick(self)
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
        self.initVars()
        #self.setMinimumSize(75,60)
    
    def initVars(self):
        self.name = ""
        self.color = ""
        self.props = ["text", "color", "width", "height"]
        self.resize(100,25)

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
        self.initVars()
        #self.setMinimumSize(75,60)

    def initVars(self):
        self.name = ""
        self.color = "#ffffff"
        self.props = ["color", "width", "height"]
        self.resize(100,25)

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
        self.initVars()
        #self.setMinimumSize(75,60)

    def initVars(self):
        self.name = ""
        self.color = DEFAULT_WINDOW_COLOR
        self.props = ["text", "color", "width", "height"]
        self.resize(100,25)
    
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
        self.initVars()
        #self.setMinimumSize(150,100)

    def initVars(self):
        self.name = ""
        self.color = "#ffffff"
        self.props = ["color", "width", "height"]
        self.resize(100,25)
    
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

class ColorLineEdit(QLineEdit):

    def __init__(self, mainp, parent  = None):
        super(ColorLineEdit, self).__init__(parent)
        self.setReadOnly(True)
        color = ""
        self.mainp = mainp
    def mousePressEvent(self, event):
        self.mainp.colorChange()
        super().mousePressEvent(event)

if __name__ == "__main__":
    app = QApplication([])
    w = MainClass()
    app.exec_()
