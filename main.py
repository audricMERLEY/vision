import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,QHBoxLayout,QToolButton,QLineEdit,QLabel,QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QSize

class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.initWindow()
        self.initSignalSlot()

    def initWindow(self):
        # create buttons
        self.pathFinderBtn = QToolButton()
        self.launchBtn = QPushButton("Launch")
        # create label
        self.imageLbl = QLabel("")
        self.pathFinderLbl = QLabel("")
        self.pathFinderLbl.setStyleSheet("border: 1px solid black;")
        self.imageLbl.setFixedSize(QSize(500,500))
        self.imageLbl.setAlignment(Qt.AlignCenter)
        # create layout
        mainLyt = QVBoxLayout()
        pathFinderLyt = QHBoxLayout()
        mainLyt.setAlignment(Qt.AlignCenter)
        pathFinderLyt.addWidget(self.pathFinderLbl)
        pathFinderLyt.addWidget(self.pathFinderBtn)
        mainLyt.addWidget(self.imageLbl)
        mainLyt.addLayout(pathFinderLyt)
        mainLyt.addWidget(self.launchBtn)
        self.setLayout(mainLyt)

    def initSignalSlot(self):
        self.launchBtn.clicked.connect(self.launchProcessing)
        self.pathFinderBtn.clicked.connect(self.getImagePath)


    def launchProcessing(self):
        self.imageLbl.setText('test')

    def getImagePath(self):
        dialog = QFileDialog(self, windowTitle='Selectionner image')
        dialog.setFileMode(dialog.ExistingFile)
        dialog.setNameFilter("Image files (*.png *.jpg *.jpeg *.ppm)")
        if self.pathFinderLbl.text():
            dialog.setDirectory(self.pathFinderLbl.text())
        dialog.exec_()
        if len(dialog.selectedFiles()) > 0:
            im = QPixmap(dialog.selectedFiles()[0])
            size = self.imageLbl.size()
            scaledPix = im.scaled(size, Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
            self.imageLbl.setPixmap(scaledPix)

            self.pathFinderLbl.setText(dialog.selectedFiles()[0])
        print(dialog.selectedFiles())


if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    fen = Fenetre()
    fen.show()

    app.exec_()

