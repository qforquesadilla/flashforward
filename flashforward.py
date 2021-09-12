import os
import sys
import json
import subprocess
from functools import partial

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QMessageBox
from PySide2.QtCore import QFile

'''
FlashForward
'''


class Flashforward(object):

    def __init__(self):
        '''
        '''

        # config
        self.__toolRootDir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        self.__configPath = os.path.normpath(os.path.join(self.__toolRootDir, 'data/config.json'))
        self.__parametersPath = os.path.normpath(os.path.join(self.__toolRootDir, 'data/parameters.json'))

        self.__setupConfig()

        # ui & commands
        self.__buildUi()
        self.__setParameters()
        self.__mainUi.show()

        self.__mainUi.ffmpegLE.setText(self.__ffmpegPath)

        self.__linkCommands()

        print('\n\n################\n# FLASHFORWARD #\n################\n')
        sys.exit(self.__app.exec_())


    def __setupConfig(self):
        '''
        '''

        # load json
        with open(self.__configPath) as c:
            configData = json.load(c)

        # restore values
        ffmpegDir = configData.get('ffmpegDir', None)
        self.__ffmpegPath = os.path.normpath(os.path.join(self.__toolRootDir, 'bin/ffmpeg.exe'))
        self.__ffplayPath = os.path.normpath(os.path.join(self.__toolRootDir, 'bin/ffplay.exe'))
        self.__ffprobePath = os.path.normpath(os.path.join(self.__toolRootDir, 'bin/ffprobe.exe'))


    def __setParameters(self):
        '''
        '''

        # load json
        with open(self.__parametersPath) as c:
            parametersData = json.load(c)

        # get values
        codec = parametersData.get('codec', None)
        resolution = parametersData.get('resolution', None)
        frameRate = parametersData.get('frameRate', None)
        colorspace = parametersData.get('colorspace', None)

        # set value to qComboBox
        self.__addComboBox(self.__mainUi.codecCB, codec.values())
        self.__addComboBox(self.__mainUi.resolutionCB, resolution.values())
        self.__addComboBox(self.__mainUi.frameRateCB, frameRate.values())
        self.__addComboBox(self.__mainUi.colorspaceCB, colorspace.values())


    def __buildUi(self):
        '''
        '''

        # define ui file paths
        self.__app = QApplication(sys.argv)
        mainUiPath = os.path.normpath(os.path.join(self.__toolRootDir, 'interface/main.ui')).replace('\\', '/')

        # open ui files
        loader = QUiLoader()
        mainUiFile = QFile(mainUiPath)
        mainUiFile.open(QFile.ReadOnly)

        # create ui objects
        self.__mainUi = loader.load(mainUiFile)


    def __linkCommands(self):
        '''
        '''

        # main ui
        self.__mainUi.renderPBT.clicked.connect(partial(self.__onChangeMode, self.__mainUi.renderPBT))
        self.__mainUi.playPBT.clicked.connect(partial(self.__onChangeMode, self.__mainUi.playPBT))
        self.__mainUi.probePBT.clicked.connect(partial(self.__onChangeMode, self.__mainUi.probePBT))

        self.__mainUi.ffmpegTB.clicked.connect(partial(self.__onSetPath, self.__mainUi.ffmpegLE))
        self.__mainUi.inputTB.clicked.connect(partial(self.__onSetPath, self.__mainUi.inputLE))
        self.__mainUi.outputTB.clicked.connect(partial(self.__onSetPath, self.__mainUi.outputLE))
        self.__mainUi.queueAddPB.clicked.connect(partial(self.__onAddQueuePressed, self.__mainUi.queueLW))
        self.__mainUi.queueRemovePB.clicked.connect(partial(self.__onRemoveQueuePressed, self.__mainUi.queueLW))

        # double click at ListWidget

        self.__mainUi.runPB.clicked.connect(self.__onRunPressed)



    ############
    # COMMANDS #
    ############


    def __onRunPressed(self):
        mode = self.__getMode()
        inputPath = self.__getLineEdit(self.__mainUi.inputLE)
        outputPath = self.__getLineEdit(self.__mainUi.outputLE)
        codec = self.__getComboBox(self.__mainUi.codecCB)
        resolution = self.__getComboBox(self.__mainUi.resolutionCB)
        frameRate = self.__getComboBox(self.__mainUi.frameRateCB)
        colorspace = self.__getComboBox(self.__mainUi.colorspaceCB)
        slate = self.__getCheckBox(self.__mainUi.slateCB)
        burnin = self.__getCheckBox(self.__mainUi.burninCB)
        note = self.__getLineEdit(self.__mainUi.noteLE)
        print(mode)
        print(inputPath)
        print(outputPath)
        print(codec)
        print(resolution)
        print(frameRate)
        print(colorspace)
        print(slate)
        print(note)


    def __onChangeMode(self, qPushButton):
        objectName = qPushButton.objectName()
        
        styleSheetOn = 'background-color: #E4EAA0; color: #313333'
        styleSheetOff = 'background-color: #313333; color: #f8f8f8;'
        
        if objectName == 'renderPBT':
            self.__mainUi.renderPBT.setStyleSheet(styleSheetOn)
            self.__mainUi.playPBT.setStyleSheet(styleSheetOff)
            self.__mainUi.probePBT.setStyleSheet(styleSheetOff)

        if objectName == 'playPBT':
            self.__mainUi.renderPBT.setStyleSheet(styleSheetOff)
            self.__mainUi.playPBT.setStyleSheet(styleSheetOn)
            self.__mainUi.probePBT.setStyleSheet(styleSheetOff)

        elif objectName == 'probePBT':
            self.__mainUi.renderPBT.setStyleSheet(styleSheetOff)
            self.__mainUi.playPBT.setStyleSheet(styleSheetOff)
            self.__mainUi.probePBT.setStyleSheet(styleSheetOn)


    def __onSetPath(self, qLineEdit):
        objectName = qLineEdit.objectName()

        if objectName == 'ffmpegLE':
            path = QFileDialog.getExistingDirectory()
    
        else:
            path, flt = QFileDialog.getOpenFileName(caption='File Selection',
                                                    dir='.',
                                                    filter='All Files (*)')

        if not path:
            return

        self.__setLineEdit(qLineEdit, path)


    def onSlateClicked(self):
        pass
        # TODO: Show preview of slate image here


    def __onAddQueuePressed(self, qListWidget):
        print(qListWidget)
        #qTableWidget.insertRow(0)


    def __onRemoveQueuePressed(self, qListWidget):
        print(qListWidget)
        #row = qTableWidget.currentRow()
        #if row != -1:
        #    qTableWidget.removeRow(row)




    ########
    # MISC #
    ########

    def __getMode(self):
        for qPushButton in [self.__mainUi.renderPBT, self.__mainUi.playPBT, self.__mainUi.probePBT]:
            if '#E4EAA0' in qPushButton.styleSheet():
                return qPushButton.objectName().replace('PBT', '')

    def __getLineEdit(self, qLineEdit):
        return qLineEdit.text()

    def __setLineEdit(self, qLineEdit, value):
        return qLineEdit.setText(value)

    def __getComboBox(self, qComboBox):
        return qComboBox.currentText()

    def __setComboBox(self, qComboBox, value):
        return qComboBox.setCurrentText(value)

    def __addComboBox(self, qComboBox, items):
        for item in items:
            qComboBox.addItem(item)
        return items

    def __getCheckBox(self, qCheckBox):
        return qCheckBox.isChecked()

    def __setCheckBox(self, qCheckBox, bool):
        return qCheckBox.setChecked(bool)

    def __getTextEdit(self, qTextEdit):
        return qTextEdit.toPlainText()


if __name__ == "__main__":
    Flashforward()






