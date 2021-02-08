import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,QHBoxLayout,QToolButton,QLineEdit,QLabel,QFileDialog
from PyQt5.QtGui import QPixmap, QImage,QIcon
from PyQt5.QtCore import Qt, QSize
import cv2
from ImageProcessing import *
from displayCam import *

# main window of the app
class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.initWindow()
        self.initSignalSlot()
        self.imP = ImageProcessing()
        self.stop = False
    #initialisation of buttons and layout
    def initWindow(self):
        # create buttons
        self.pathFinderBtn = QToolButton() #use to get the path of image or video on the file system
        self.dashCamBtn = QPushButton() # use to launch dashCam
        self.dashCamBtn.setIcon(QIcon('dashCam.png')) # add image to dash cam button
        self.dashCamBtn.setFixedSize(QSize(25,25)) # change size
        self.launchBtn = QPushButton("Stop") # add button to stop video
        # create label
        self.signName = QLabel("Choose picture")
        self.pathFinderLbl = QLabel("") # label that will display the path of the image selected
        self.pathFinderLbl.setStyleSheet("border: 1px solid black;")
        # create view
        self.view = displayCam() # the view where the image/video will be displayed
        self.view.setAlignment(Qt.AlignCenter)
        # create layout
        mainLyt = QVBoxLayout()
        pathFinderLyt = QHBoxLayout()
        mainLyt.setAlignment(Qt.AlignCenter)
        pathFinderLyt.addWidget(self.pathFinderLbl)
        pathFinderLyt.addWidget(self.pathFinderBtn)
        mainLyt.addWidget(self.view)
        mainLyt.addWidget(self.dashCamBtn)
        mainLyt.addWidget(self.signName)
        mainLyt.addLayout(pathFinderLyt)
        mainLyt.addWidget(self.launchBtn)
        self.launchBtn.hide() # hide stop button until video launch
        self.setLayout(mainLyt)

    #initialise slot of buttons
    def initSignalSlot(self):
        self.launchBtn.clicked.connect(self.stopVideo) # click to stop video
        self.dashCamBtn.clicked.connect(self.dashCamCap) # click to launch dashCam
        self.pathFinderBtn.clicked.connect(self.getImagePath) # click to get path of image/video

    # stop video
    def stopVideo(self):
        print('stopped')
        if not self.stop:
            self.stop = True
            self.launchBtn.hide() # hide stop button

    # launch video
    def launchVideo(self):
        print('launched')
        self.stop = False
        self.launchBtn.show()

    # get the capture of the dash cam
    def dashCamCap(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if not frame is None and ret:
            self.processVideo(cap)

    # use to process an image with its path
    def processImage(self,imagePath):
        im = self.imP.predict_path(imagePath) # retrieves the image from processing
        # transform image from opencv to QImage
        height, width, channel = im.shape
        bytesPerLine = 3 * width
        qImg = QImage(im.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # display image
        self.view.setImage(QPixmap(qImg))



    def processVideo(self,cap):
        # get total number of frames
        totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        print(totalFrames)
        # show stop button
        self.launchVideo()
        # check for valid frame number
        while cap.isOpened():
            ret, frame = cap.read() # get frame
            if not frame is None:
                # retrieves the image after process
                image = self.imP.predict_im(frame)
                # transform image from opencv to QImage
                height, width, channel = image.shape
                bytesPerLine = 3 * width
                qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_BGR888)
                #display image
                self.view.setImage(QPixmap.fromImage(qImg))
            # wait 1ms before getting new frame (or stopped if stop button press)
            if cv2.waitKey(1) & 0xFF == ord('q') or self.stop:
                break
        # hide stop button
        self.stopVideo()

    # use to process video or image from system file
    def getImagePath(self):
        # create dialog box to get image or video
        dialog = QFileDialog(self, windowTitle='Selectionner image/video')
        dialog.setFileMode(dialog.ExistingFile)
        # set image/video type that are authorized to open
        dialog.setNameFilter("Image files (*.png *.jpg *.jpeg *.ppm *.mp4)")
        # go back to the last directory where the image was selected
        if self.pathFinderLbl.text():
            dialog.setDirectory(self.pathFinderLbl.text())
        # show dialog box
        dialog.exec_()
        # get path from image/video selected
        if len(dialog.selectedFiles()) > 0:
            self.pathFinderLbl.setText(dialog.selectedFiles()[0])
            if ".mp4" in dialog.selectedFiles()[0] :
                # video processing
                cap = cv2.VideoCapture(dialog.selectedFiles()[0])
                self.processVideo(cap)
            else :
                # image processing
                self.processImage(dialog.selectedFiles()[0])
        print(dialog.selectedFiles())



if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    # launch window
    fen = Fenetre()
    fen.show()

    app.exec_()

