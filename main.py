import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,QHBoxLayout,QToolButton,QLineEdit,QLabel,QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QSize
import cv2
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
        dialog = QFileDialog(self, windowTitle='Selectionner image/video')
        dialog.setFileMode(dialog.ExistingFile)
        dialog.setNameFilter("Image files (*.png *.jpg *.jpeg *.ppm *.mp4)")
        if self.pathFinderLbl.text():
            dialog.setDirectory(self.pathFinderLbl.text())
        dialog.exec_()
        if len(dialog.selectedFiles()) > 0:
            self.pathFinderLbl.setText(dialog.selectedFiles()[0])
            if ".mp4" in dialog.selectedFiles()[0] :
                cap = cv2.VideoCapture(dialog.selectedFiles()[0])
                # get total number of frames
                totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                print(totalFrames)
                # check for valid frame number
                while True:
                    ret, frame = cap.read()
                    if not frame is None:
                        height, width, channel = frame.shape
                        bytesPerLine = 3 * width
                        qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_BGR888)
                        self.view.setImage(QPixmap.fromImage(qImg))
                        self.setBoundingBox(0.5, 0.5, 0.3, 0.3)
                        self.setSign("bounding box 0.5 0.5 0.3 0.3")
                    if cv2.waitKey(20) & 0xFF == ord('q'):
                        break
            else :
                im = QPixmap(dialog.selectedFiles()[0])
                self.view.setImage(im)
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

