# This Python file uses the following encoding: utf-8

from PyQt5.QtGui import QPixmap, QPen
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtCore import QRectF, Qt, QSize

# view to display the cam/video/image
class displayCam(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setFixedSize(QSize(750,750))
        self.imSize = QSize(0,0)
    
    def setImage(self, pixmap):
        scaledPix = pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
        self.scene.clear()
        self.imSize = scaledPix.size()
        self.scene.addPixmap(scaledPix)

