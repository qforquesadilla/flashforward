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
        TBA
        '''

        # config
        self.__toolRootDir = os.path.abspath(os.path.dirname(__file__))
        self.__configPath = os.path.normpath(os.path.join(self.__toolRootDir, 'data/config.json'))
        self.__parametersPath = os.path.normpath(os.path.join(self.__toolRootDir, 'data/parameters.json'))
        self.__slatePath = os.path.normpath(os.path.join(self.__toolRootDir, 'data/slate.png'))

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
        TBA
        '''

        # load json
        with open(self.__configPath) as c:
            configData = json.load(c)

        # restore values
        ffmpegDir = configData.get('ffmpegDir', None)
        self.__ffmpegPath = os.path.normpath(os.path.join(ffmpegDir, 'ffmpeg.exe'))
        self.__ffplayPath = os.path.normpath(os.path.join(ffmpegDir, 'ffplay.exe'))
        self.__ffprobePath = os.path.normpath(os.path.join(ffmpegDir, 'ffprobe.exe'))


    def __setParameters(self):
        '''
        TBA
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
        TBA
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
        TBA
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
        '''
        TBA
        '''

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

        if mode == 'play':
            cmd = self.__ffplayPath + ' ' + inputPath + ' -autoexit -alwaysontop'
 
            print(cmd)

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            subprocess.Popen(cmd, startupinfo=startupinfo)

        # TODO: Support other two modes


    def __onChangeMode(self, qPushButton):
        '''
        TBA
        '''

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
        '''
        TBA
        '''

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
        '''
        TBA
        '''

        pass
        # TODO: Show preview of slate image here


    def __onAddQueuePressed(self, qListWidget):
        '''
        TBA
        '''

        print(qListWidget)
        #qTableWidget.insertRow(0)


    def __onRemoveQueuePressed(self, qListWidget):
        '''
        TBA
        '''

        print(qListWidget)
        #row = qTableWidget.currentRow()
        #if row != -1:
        #    qTableWidget.removeRow(row)


    ###########
    # METHODS #
    ###########


    def __createSlate(self, imagePath, textPath, outputPath):
        '''
        TBA
        '''

        fontPath = r'C\\://WINDOWS/Fonts/arial.ttf'
        textPath = r'E\\://pepepe//slate.txt'

        filterComplex = '[1:v]'
        filterComplex += 'scale=640:360,'
        #filterComplex += 'colorspace=bt709,'##########
        filterComplex += 'format=yuv420p'
        filterComplex += '[overlay];'

        filterComplex += '[0:v][overlay]'
        filterComplex += 'overlay=1185:100'
        filterComplex += '[output];'

        filterComplex += '[output]'
        filterComplex += 'drawtext='
        filterComplex += 'fontfile=%s:' % fontPath
        filterComplex += 'textfile="%s":' % textPath
        filterComplex += 'fontcolor=white:'
        filterComplex += 'fontsize=35:'
        filterComplex += 'line_spacing=70:'
        filterComplex += 'x=250:y=110'

        cmd = ''
        cmd += '%s ' % self.__ffmpegPath
        cmd += '-i %s ' % self.__slatePath
        cmd += '-i %s ' % imagePath
        cmd += '-filter_complex "%s" ' % filterComplex
        cmd += '%s' % outputPath

        print(cmd)

        if os.path.exists(outputPath):
            os.remove(outputPath)

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        subprocess.Popen(cmd, startupinfo=startupinfo)


    def __createContactSheet(self):
        '''
        Get images from given .edl and movie, and create a movie showing all thumbnails (for FFprobe?)
        '''

        pass


    ########
    # MISC #
    ########


    def __getMode(self):
        '''
        TBA
        '''

        for qPushButton in [self.__mainUi.renderPBT, self.__mainUi.playPBT, self.__mainUi.probePBT]:
            if '#E4EAA0' in qPushButton.styleSheet():
                return qPushButton.objectName().replace('PBT', '')


    def __getLineEdit(self, qLineEdit):
        '''
        TBA
        '''

        return qLineEdit.text()


    def __setLineEdit(self, qLineEdit, value):
        '''
        TBA
        '''

        return qLineEdit.setText(value)


    def __getComboBox(self, qComboBox):
        '''
        TBA
        '''

        return qComboBox.currentText()


    def __setComboBox(self, qComboBox, value):
        '''
        TBA
        '''

        return qComboBox.setCurrentText(value)


    def __addComboBox(self, qComboBox, items):
        '''
        TBA
        '''

        for item in items:
            qComboBox.addItem(item)
        return items


    def __getCheckBox(self, qCheckBox):
        '''
        TBA
        '''

        return qCheckBox.isChecked()


    def __setCheckBox(self, qCheckBox, bool):
        '''
        TBA
        '''

        return qCheckBox.setChecked(bool)


    def __getTextEdit(self, qTextEdit):
        '''
        TBA
        '''

        return qTextEdit.toPlainText()


if __name__ == '__main__':
    Flashforward()






