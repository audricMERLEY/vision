# This Python file uses the following encoding: utf-8

from PyQt5.QtGui import QPixmap, QPen
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtCore import QRectF, Qt, QSize
class displayCam(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setFixedSize(QSize(500,500))
        self.imSize = QSize(0,0)
    
    def setImage(self, pixmap):
        scaledPix = pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
        self.scene.clear()
        self.imSize = scaledPix.size()
        self.scene.addPixmap(scaledPix)
    
    def addRectangle(self, xNormCenter, yNormCenter, widthNorm, heightNorm):
        width = self.imSize.width()
        height = self.imSize.height()
        xInit = (xNormCenter - widthNorm/2.0)*width
        yInit = (yNormCenter - heightNorm/2.0)*height
        recItem = QGraphicsRectItem(QRectF(xInit, yInit, widthNorm*width, heightNorm*height))
        recItem.setPen(QPen(Qt.blue,3))
        self.scene.addItem(recItem)

