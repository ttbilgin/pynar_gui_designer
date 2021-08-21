import json, os

from PyQt5.QtWidgets import QFileDialog, QMessageBox

def kaydet(ana_pencere):
    dialog = QFileDialog()
    dialog.setViewMode(QFileDialog.List)
    
    filename = dialog.getSaveFileName(None, "Kaydet", os.path.dirname(os.path.abspath(__file__)), "Python GUI File (*.pyn)")
    
    if(not filename[0]):
        return
    
    with open(filename[0], "w") as outfile:
        outfile.write("[")
        for i in ana_pencere.penceredeki_itemler:
            liste = {"obje_ismi": i.objectName(), "pos": str(i.pos().x()) + "," + str(i.pos().y()), "size": str(i.width()) + "," + str(i.height())}
            if i == ana_pencere.selected:
                ana_pencere.deleteStyle(i, "border: ")
            liste["css"] = i.styleSheet()
            if i == ana_pencere.selected:
                ana_pencere.selectedHighlight(i)
            try:
                liste["text"] = i.text()
            except Exception as e:
                pass
            json.dump(liste, outfile, ensure_ascii = False, indent = 4)
            outfile.write(",")
        #MdiWindow
        liste = {"başlık": ana_pencere.pencere.windowTitle(),  "size": str(ana_pencere.pencere.width()) + "," + str(ana_pencere.pencere.height()), "css": ana_pencere.pencere.styleSheet()}
        json.dump(liste, outfile, ensure_ascii = False, indent = 4)
        outfile.write("]")

def yukle(ana_pencere):

    dialog = QFileDialog()
    dialog.setViewMode(QFileDialog.List)

    filename = dialog.getOpenFileName(None, "Aç", os.path.dirname(os.path.abspath(__file__)), filter="Python GUI File (*.pyn)")

    if(not filename[0]):
        return

    for i in ana_pencere.penceredeki_itemler.copy():
        ana_pencere.removeObject(i)
    with open(filename[0], "r") as infile:
        try:
            obje_listesi = json.load(infile)
        except json.decoder.JSONDecodeError as e:
            error_win = QMessageBox()
            error_win.setText("Geçersiz Dosya")
            error_win.setWindowTitle("Hata")
            error_win.exec_()
            return
        for obje in obje_listesi[:-1]:
            try:
                exec(f"""
ana_pencere.{obje["obje_ismi"]}.setText("{obje["text"]}")
""")
            except KeyError:
                pass
            exec(f"""
ana_pencere.{obje["obje_ismi"]}.move({obje["pos"]})
ana_pencere.{obje["obje_ismi"]}.setStyleSheet("{obje["css"]}")
ana_pencere.{obje["obje_ismi"]}.resize({obje["size"]})
ana_pencere.penceredeki_itemler.add(ana_pencere.{obje["obje_ismi"]})
""")
    #MdiWindow
    objeson = obje_listesi[-1]
    exec(f"""
ana_pencere.pencere.setStyleSheet("{objeson["css"]}")
ana_pencere.pencere.resize({objeson["size"]})
ana_pencere.pencere.setWindowTitle("{objeson["başlık"]}")
""")
    #Hiçbir objenin seçili gözükmemesini sağla
    ana_pencere.deleteStyle(ana_pencere.pencere, "border: ")
    ana_pencere.hideObjectProps()
    ana_pencere.selected = None