#!/usr/bin/python

Development = True

import curingMachineUI
from materials import materials
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
from collections import OrderedDict
import logging



if not Development:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)  # Use the board numbering scheme
    GPIO.setwarnings(False)  # Disable GPIO warnings H


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

def run_async(func):
    '''
    Function decorater to make methods run in a thread
    '''
    from threading import Thread
    from functools import wraps

    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl

    return async_func


'''
Definition of Buzzer. 
'''
class BuzzerFeedback(object):
    def __init__(self, buzzerPin):
        if not Development:
            GPIO.cleanup()
            self.buzzerPin = buzzerPin
            GPIO.setup(self.buzzerPin, GPIO.OUT)
            GPIO.output(self.buzzerPin, GPIO.LOW)
        pass

    @run_async
    def buzz(self):
        if not Development:
            GPIO.output(self.buzzerPin, (GPIO.HIGH))
            time.sleep(0.005)
            GPIO.output(self.buzzerPin, GPIO.LOW)
        pass


'''
Definition of AC motor. 
'''
class AcMotor(object):
    def __init__(self, acMotorPin):
        if not Development:
            GPIO.cleanup()
            self.acMotorPin = acMotorPin
            GPIO.setup(self.acMotorPin, GPIO.OUT)
            GPIO.output(self.acMotorPin, GPIO.LOW)
        pass

'''
Definition of UV LED. 
'''
class UvLed(object):
    def __init__(self, uvLedPin):
        if not Development:
            GPIO.cleanup()
            self.uvLedPin = uvLedPin
            GPIO.setup(self.uvLedPin, GPIO.OUT)
            GPIO.output(self.uvLedPin, GPIO.LOW)
        pass
'''
Definition of AC Heater. 
'''
class AcHeater(object):
    def __init__(self, acHeaterPin):
        if not Development:
            GPIO.cleanup()
            self.acHeaterPin = acHeaterPin
            GPIO.setup(self.acHeaterPin, GPIO.OUT)
            GPIO.output(self.acHeaterPin, GPIO.LOW)
        pass
'''
Definition of Magnetic Lock. 
'''
class MagLock(object):
    def __init__(self, magLockPin):
        if not Development:
            GPIO.cleanup()
            self.magLockPin = magLockPin
            GPIO.setup(self.magLockPin, GPIO.OUT)
            GPIO.output(self.magLockPin, GPIO.LOW)
        pass


'''
Declaring Objects
'''

buzzer = BuzzerFeedback(12)
turnTable = AcMotor(16)
uvLed = UvLed(26)
heater = AcHeater(20)
magLock = MagLock(21)

'''
To get the buzzer to beep on button press
'''

OriginalPushButton = QtWidgets.QPushButton
OriginalToolButton = QtWidgets.QToolButton

class QPushButtonFeedback(QtWidgets.QPushButton):
    def mousePressEvent(self, QMouseEvent):
        buzzer.buzz()
        OriginalPushButton.mousePressEvent(self, QMouseEvent)


class QToolButtonFeedback(QtWidgets.QToolButton):
    def mousePressEvent(self, QMouseEvent):
        buzzer.buzz()
        OriginalToolButton.mousePressEvent(self, QMouseEvent)


QtWidgets.QToolButton = QToolButtonFeedback
QtWidgets.QPushButton = QPushButtonFeedback




class MainUiClass(QtWidgets.QMainWindow, curingMachineUI.Ui_MainWindow):
    

    def __init__(self):
        '''
        This method gets called when an object of type MainUIClass is defined
        '''
        super(MainUiClass, self).__init__()
        try:
            self.setupUi(self)
            for spinbox in self.findChildren(QtWidgets.QSpinBox):
                lineEdit = spinbox.lineEdit()
                lineEdit.setReadOnly(True)
                lineEdit.setDisabled(True)
                p = lineEdit.palette()
                p.setColor(QtGui.QPalette.Highlight, QtGui.QColor(40, 40, 40))
                lineEdit.setPalette(p)
        except Exception as e:
            self._logger.error(e)
        self.setActions()
        self.timeElapsed = 0
        self.timeRemaining = 0
        self.pauseFlag = False



    def setupUi(self, MainWindow):
        super(MainUiClass, self).setupUi(MainWindow)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Gotham"))
        font.setPointSize(15)
        self.materialComboBox.addItems(sorted(materials.keys()))
        # print (materials.keys())

    def setActions(self):

        '''
        defines all the Slots and Button events.
        '''

        # Operate Screen:
        self.playPauseButton.pressed.connect(self.playPauseAction)
        self.stopButton.pressed.connect(self.stopAction)
        self.uvStartStopButton.pressed.connect(self.toggleUvLed)
        self.tempStartStopButton.pressed.connect(self.toggleHeater)
        self.timeSpinBox.valueChanged.connect(self.timerChangedAction)


    def playPauseAction(self):
        '''
        get status of all the settings buttons
        start timer thread
        dissable settings tab
        start progress bar as time elaplsed/time remining

    or

        get time remaining value
        set it on the timer
        set combobox to custom
        ungreay settings
        '''
        if self.timeSpinBox.value() == 0:
            QtWidgets.QMessageBox.warning(self,'Warning','Set Timer in Settings Tab First')
        else:
            if self.playPauseButton.isChecked() is False:
                if self.uvStartStopButton.isChecked() :
                    pass
                if self.tempStartStopButton.isChecked() :
                    pass
                self.materialPreset.setText((self.materialComboBox.currentText()))
                if  self.pauseFlag:
                    self.curingTimerThreadObject = ThreadCuringTimer(self.timeRemaining)
                    self.pauseFlag = False
                else:
                    self.curingTime = self.timeSpinBox.value()
                    self.curingTimerThreadObject = ThreadCuringTimer(self.curingTime)

                self.curingTimerThreadObject.curing_done_signal.connect(self.curingDoneAction)
                self.curingTimerThreadObject.progress_bar_signal.connect(self.updateProgressBar)
                self.curingTimerThreadObject.time_remaining_signal.connect(self.timeRemainingAction)
                self.curingTimerThreadObject.start()

            else:
                self.curingTimerThreadObject.stop()
                self.pauseFlag = True

    def stopAction(self):
        '''
        ungreay settings
        stop all working
        clear progress bar
        stop timer thread

        '''
        self.curingTimerThreadObject.stop()
        self.pauseFlag = False
        self.playPauseButton.setChecked(False)
        self.progressBar.setValue(0)
        self.timeRemainingLabel.setText(str(0) + " Seconds")
        pass
    def toggleUvLed(self):
        '''
        overide Material Preset combobox
        set combobox to custom
        retain previous state of other settings
        toggle state of heater
        '''
        self.materialComboBox.addItem('Custom')
        self.materialComboBox.setCurrentIndex(self.materialComboBox.findText('Custom'))
        pass
    def toggleHeater(self):
        '''
        overide Material Preset combobox
        set combobox to custom
        retain previous state of other settings
        toggle state of heater
        '''
        self.materialComboBox.addItem('Custom')
        self.materialComboBox.setCurrentIndex(self.materialComboBox.findText('Custom'))
        pass
    def timerChangedAction(self):
        '''
        overide Material Preset combobox
        set combobox to custom
        retain previous state of other settings
        toggle state of heater
        '''
        self.materialComboBox.addItem('Custom')
        self.materialComboBox.setCurrentIndex(self.materialComboBox.findText('Custom'))
        pass

    def curingDoneAction(self):
        print('curing done')
        self.progressBar.setValue(100)
        self.pauseFlag = False
        self.playPauseButton.setChecked(False)
        self.timeRemainingLabel.setText(str(0) + ' Seconds')
        pass

    def updateProgressBar(self, timeRemaining):
        self.timeRemainingLabel.setText(str(int(timeRemaining)) + ' Seconds')
        self.progressBar.setValue((((self.curingTime - timeRemaining)/self.curingTime))*100)
        pass
    def timeRemainingAction(self,timeRemaining):
        self.timeRemaining = timeRemaining

class ThreadCuringTimer(QtCore.QThread):
    curing_done_signal = QtCore.pyqtSignal()
    progress_bar_signal = QtCore.pyqtSignal(int)
    time_remaining_signal = QtCore.pyqtSignal(int)

    def __init__(self, curingTime):
        super(ThreadCuringTimer, self).__init__()
        self.curingTime = curingTime

    def run(self):
        self.startTime = time.time()
        self.timeElapsed = (time.time() - self.startTime)
        while self.timeElapsed <= self.curingTime:
            self.progress_bar_signal.emit(self.curingTime - self.timeElapsed)
            time.sleep(1)
            self.timeElapsed = (time.time() - self.startTime)
        self.curing_done_signal.emit()
    #
    def stop(self):
        if self.timeElapsed <= self.curingTime:
            self.time_remaining_signal.emit(self.curingTime - self.timeElapsed)
        self.terminate()





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # Intialize the library (must be called once before other functions).
    # Creates an object of type MainUiClass
    MainWindow = MainUiClass()
    MainWindow.show()
    # MainWindow.showFullScreen()
    # MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    # Create NeoPixel object with appropriate configuration.
    # charm = FlickCharm()
    # charm.activateOn(MainWindow.FileListWidget)
sys.exit(app.exec_())