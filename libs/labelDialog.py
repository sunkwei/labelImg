#!/usr/bin/python
#coding: utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from lib import newIcon, labelValidator

BB = QDialogButtonBox

class LabelDialog(QDialog):

    def __init__(self, text="Enter object label", parent=None, listItem=None):
        super(LabelDialog, self).__init__(parent)
        self.edit = QLineEdit()
        self.edit.setText(text)
        self.edit.setValidator(labelValidator())
        self.edit.editingFinished.connect(self.postProcess)
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        if listItem is not None and len(listItem) > 0:
            self.listWidget = QListWidget(self)
            for item in listItem:
                if type(item) is str:
                    item = item.decode('utf-8')
                self.listWidget.addItem(item)
            self.listWidget.itemClicked.connect(self.listItemClick)
            layout.addWidget(self.listWidget)

        # 选择 pose
        self.poseWidget = QComboBox(self)
        self.poseWidget.addItem('Unspecified')
        self.poseWidget.addItem('Left')
        self.poseWidget.addItem('Right')
        self.poseWidget.addItem('Frontal')
        self.poseWidget.addItem('Rear')
        self.poseWidget.setCurrentIndex(0)
        layout.addWidget(self.poseWidget)

        # 选择 truncated
        self.truncatedWidget = QCheckBox("Truncated", self)
        self.truncatedWidget.setCheckState(Qt.Unchecked)
        layout.addWidget(self.truncatedWidget)

        # 选择 difficult
        self.diffifultWidget = QCheckBox("Difficult", self)
        self.diffifultWidget.setCheckState(Qt.Unchecked)
        layout.addWidget(self.diffifultWidget)

        self.setLayout(layout)

    def validate(self):
        if self.edit.text().trimmed():
            self.accept()

    def postProcess(self):
        self.edit.setText(self.edit.text().trimmed())

    def popUp(self, text='', move=True, shape=None):
        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)
        
        if shape:
            if shape.pose:
                if shape.pose == 'Unspecified':
                    self.poseWidget.setCurrentIndex(0)
                elif shape.pose == 'Left':
                    self.poseWidget.setCurrentIndex(1)
                elif shape.pose == 'Right':
                    self.poseWidget.setCurrentIndex(2)
                elif shape.pose == 'Frontal':
                    self.poseWidget.setCurrentIndex(3)
                elif shape.pose == 'Rear':
                    self.poseWidget.setCurrentIndex(4)
            if shape.truncated:
                self.truncatedWidget.setCheckState(Qt.Checked)
            if shape.difficult:
                self.diffifultWidget.setCheckState(Qt.Checked)
        if move:
            self.move(QCursor.pos())
        if self.exec_():
            pose = str(self.poseWidget.currentText())
            truncated = 1 if self.truncatedWidget.checkState() != Qt.Unchecked else 0
            difficult = 1 if self.diffifultWidget.checkState() != Qt.Unchecked else 0
            return self.edit.text(), pose, truncated, difficult
        else:
            return None,None,0,0

    def listItemClick(self, tQListWidgetItem):
        text = tQListWidgetItem.text().trimmed()
        self.edit.setText(text)
