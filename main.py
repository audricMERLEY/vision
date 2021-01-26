import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,QHBoxLayout,QToolButton,QLineEdit,QLabel,QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize
from displayCam import *

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
        self.signName = QLabel("Choose picture")
        self.pathFinderLbl = QLabel("")
        self.pathFinderLbl.setStyleSheet("border: 1px solid black;")
        # create view
        self.view = displayCam()
        self.view.setAlignment(Qt.AlignCenter)
        # create layout
        mainLyt = QVBoxLayout()
        pathFinderLyt = QHBoxLayout()
        mainLyt.setAlignment(Qt.AlignCenter)
        pathFinderLyt.addWidget(self.pathFinderLbl)
        pathFinderLyt.addWidget(self.pathFinderBtn)
        mainLyt.addWidget(self.view)
        mainLyt.addWidget(self.signName)
        mainLyt.addLayout(pathFinderLyt)
        mainLyt.addWidget(self.launchBtn)
        self.setLayout(mainLyt)

    def initSignalSlot(self):
        self.launchBtn.clicked.connect(self.launchProcessing)
        self.pathFinderBtn.clicked.connect(self.getImagePath)

    def launchProcessing(self):
        print('launched')

    def getImagePath(self):
        dialog = QFileDialog(self, windowTitle='Selectionner image')
        dialog.setFileMode(dialog.ExistingFile)
        dialog.setNameFilter("Image files (*.png *.jpg *.jpeg *.ppm)")
        if self.pathFinderLbl.text():
            dialog.setDirectory(self.pathFinderLbl.text())
        dialog.exec_()
        if len(dialog.selectedFiles()) > 0:
            im = QPixmap(dialog.selectedFiles()[0])
            self.view.setImage(im)
            self.pathFinderLbl.setText(dialog.selectedFiles()[0])
            self.setBoundingBox(0.5, 0.5, 0.3, 0.3)
            self.setSign("bounding box 0.5 0.5 0.3 0.3")
        print(dialog.selectedFiles())


    def setBoundingBox(self, xCenterNorm, yCenterNorm, widthNorm, heightNorm):
        self.view.addRectangle(xCenterNorm, yCenterNorm, widthNorm, heightNorm)

    def setSign(self,content) :
        self.signName.setText(content)

if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    fen = Fenetre()
    fen.show()

    app.exec_()

