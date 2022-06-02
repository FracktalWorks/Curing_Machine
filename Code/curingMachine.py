#!/usr/bin/python

Development = False

import curingMachineUI
from materials import materials
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
import keyboard
import dialog
import styles
import re
import logging
import io
import requests
import sys
import subprocess

from collections import OrderedDict
import logging

# if not Development:
if not Development:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setmode(GPIO.BCM)  # Use the board numbering scheme
    GPIO.setwarnings(False)  # Disable GPIO warnings H

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

def getIP(interface):
    try:
        scan_result = \
            (subprocess.Popen("ifconfig | grep " + interface + " -A 1", stdout=subprocess.PIPE, shell=True).communicate()[0]).decode("utf-8")
        # Processing STDOUT into a dictionary that later will be converted to a json file later
        rInetAddr = r"inet\s*([\d.]+)"
        rInet6Addr = r"inet6"
        mt6Ip = re.search(rInet6Addr, scan_result)
        mtIp = re.search(rInetAddr, scan_result)
        if not(mt6Ip) and mtIp and len(mtIp.groups()) == 1:
            return str(mtIp.group(1))
    except:
        return None
def getWifiAp():
    try:
        ap = subprocess.Popen("iwgetid -r",
                              stdout=subprocess.PIPE, shell=True).communicate()[0].rstrip()
        if not ap:
            return "Not connected"
        return ap.decode("utf-8")
    except:
        return "Error"

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
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.buzzerPin, GPIO.OUT)
            GPIO.output(self.buzzerPin, GPIO.LOW)
        pass

    @run_async
    def buzz(self):
        if not Development:
            GPIO.setup(self.buzzerPin, GPIO.OUT)
            GPIO.output(self.buzzerPin, (GPIO.HIGH))
            time.sleep(0.005)
            GPIO.setup(self.buzzerPin, GPIO.OUT)
            GPIO.output(self.buzzerPin, GPIO.LOW)
        pass


buzzer = BuzzerFeedback(12)
'''
Definition of AC motor. 
'''


class AcMotor(object):
    def __init__(self, acMotorPin):
        if not Development:
            GPIO.cleanup()
            self.acMotorPin = acMotorPin
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.acMotorPin, GPIO.OUT)
            GPIO.output(self.acMotorPin, GPIO.LOW)

    @run_async
    def start(self):
        if not Development:
            GPIO.setup(self.acMotorPin, GPIO.OUT)
            GPIO.output(self.acMotorPin, (GPIO.HIGH))
        pass

    @run_async
    def stop(self):
        if not Development:
            GPIO.setup(self.acMotorPin, GPIO.OUT)
            GPIO.output(self.acMotorPin, GPIO.LOW)
        pass




turnTable = AcMotor(16)

'''
Definition of UV LED. 
'''


class UvLed(object):
    def __init__(self, uvLedPin):
        if not Development:
            GPIO.cleanup()
            self.uvLedPin = uvLedPin
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.uvLedPin, GPIO.OUT)
            GPIO.output(self.uvLedPin, GPIO.LOW)

    @run_async
    def start(self):
        if not Development:
            GPIO.setup(self.uvLedPin, GPIO.OUT)
            GPIO.output(self.uvLedPin, (GPIO.HIGH))
        pass

    @run_async
    def stop(self):
        if not Development:
            GPIO.setup(self.uvLedPin, GPIO.OUT)
            GPIO.output(self.uvLedPin, GPIO.LOW)
        pass


uvLed = UvLed(26)
'''
Definition of AC Heater. 
'''


class AcHeater(object):
    def __init__(self, acHeaterPin):
        if not Development:
            GPIO.cleanup()
            self.acHeaterPin = acHeaterPin
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.acHeaterPin, GPIO.OUT)
            GPIO.output(self.acHeaterPin, GPIO.LOW)

    @run_async
    def start(self):
        if not Development:
            GPIO.setup(self.acHeaterPin, GPIO.OUT)
            GPIO.output(self.acHeaterPin, (GPIO.HIGH))
        pass

    @run_async
    def stop(self):
        if not Development:
            GPIO.setup(self.acHeaterPin, GPIO.OUT)
            GPIO.output(self.acHeaterPin, GPIO.LOW)
        pass


heater = AcHeater(20)
'''
Definition of Magnetic Lock. 
'''


class MagLock(object):
    def __init__(self, magLockPin):
        if not Development:
            GPIO.cleanup()
            self.magLockPin = magLockPin
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.magLockPin, GPIO.OUT)
            GPIO.output(self.magLockPin, (GPIO.HIGH))

    @run_async
    def start(self):
        if not Development:
            GPIO.setup(self.magLockPin, GPIO.OUT)
            GPIO.output(self.magLockPin, GPIO.LOW)

        pass

    @run_async
    def stop(self):
        if not Development:
            GPIO.setup(self.magLockPin, GPIO.OUT)
            GPIO.output(self.magLockPin, (GPIO.HIGH))
        pass


magLock = MagLock(21)
'''
Declaring Objects
'''

# buzzer = BuzzerFeedback(12)
# turnTable = AcMotor(16)
# uvLed = UvLed(26)
# heater = AcHeater(20)
# magLock = MagLock(21)

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

class ClickableLineEdit(QtWidgets.QLineEdit):
    clicked_signal = QtCore.pyqtSignal()
    def __init__(self, parent):
        QtWidgets.QLineEdit.__init__(self, parent)
    def mousePressEvent(self, QMouseEvent):
        buzzer.buzz()
        self.clicked_signal.emit()


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
        self.timerChangedFlag = False

    def setupUi(self, MainWindow):
        super(MainUiClass, self).setupUi(MainWindow)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Gotham"))
        font.setPointSize(15)
        self.materialComboBox.addItems(sorted(materials.keys()))
        # print (materials.keys())

        self.wifiPasswordLineEdit = ClickableLineEdit(self.wifiSettingsPage)
        self.wifiPasswordLineEdit.setGeometry(QtCore.QRect(0, 170, 480, 60))
        self.wifiPasswordLineEdit.setFont(font)
        self.wifiPasswordLineEdit.setStyleSheet(styles.textedit)
        self.wifiPasswordLineEdit.setObjectName(_fromUtf8("wifiPasswordLineEdit"))

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
        self.materialComboBox.activated.connect(self.materialPresetSelected)
        self.wifiSettingsButton.pressed.connect(self.wifiSettings)
        self.wifiPasswordLineEdit.clicked_signal.connect(lambda: self.startKeyboard(self.wifiPasswordLineEdit.setText))

        # WifiSetings page
        self.wifiSettingsSSIDKeyboardButton.pressed.connect(
            lambda: self.startKeyboard(self.wifiSettingsComboBox.addItem))
        self.wifiSettingsCancelButton.pressed.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.mainPage))
        self.wifiSettingsDoneButton.pressed.connect(self.acceptWifiSettings)

    ''' +++++++++++++++++++++++++++++++++Wifi Config+++++++++++++++++++++++++++++++++++ '''

    def acceptWifiSettings(self):
        wlan0_config_file = io.open("/etc/wpa_supplicant/wpa_supplicant.conf", "r+", encoding='utf8')
        wlan0_config_file.truncate()
        ascii_ssid = self.wifiSettingsComboBox.currentText()
        # unicode_ssid = ascii_ssid.decode('string_escape').decode('utf-8')
        wlan0_config_file.write(u"country=IN\n")
        wlan0_config_file.write(u"ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
        wlan0_config_file.write(u"update_config=1\n")
        wlan0_config_file.write(u"network={\n")
        wlan0_config_file.write(u'ssid="' + str(ascii_ssid) + '"\n')
        # if self.hiddenCheckBox.isChecked():
        #     wlan0_config_file.write(u'scan_ssid=1\n')
        # wlan0_config_file.write(u"scan_ssid=1\n")
        if str(self.wifiPasswordLineEdit.text()) != "":
            wlan0_config_file.write(u'psk="' + str(self.wifiPasswordLineEdit.text()) + '"\n')
        # wlan0_config_file.write(u"key_mgmt=WPA-PSK\n")
        wlan0_config_file.write(u'}')
        wlan0_config_file.close()
        self.restartWifiThreadObject = ThreadRestartNetworking(ThreadRestartNetworking.WLAN)
        self.restartWifiThreadObject.signal.connect(self.wifiReconnectResult)
        self.restartWifiThreadObject.start()
        self.wifiMessageBox = dialog.dialog(self,
                                            "Restarting networking, please wait...",
                                            icon="exclamation-mark.png",
                                            buttons=QtWidgets.QMessageBox.Cancel)
        if self.wifiMessageBox.exec_() in {QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel}:
            self.stackedWidget.setCurrentWidget(self.networkSettingsPage)

    def wifiReconnectResult(self, x):
        self.wifiMessageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        if x is not None:
            print("Ouput from signal " + x)
            self.wifiMessageBox.setLocalIcon('success.png')
            self.wifiMessageBox.setText('Connected, IP: ' + x)
            self.wifiMessageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.ipStatus.setText(x)  # sets the IP addr. in the status bar

        else:
            self.wifiMessageBox.setText("Not able to connect to WiFi")


    def wifiSettings(self):
        self.stackedWidget.setCurrentWidget(self.wifiSettingsPage)
        self.wifiSettingsComboBox.clear()
        self.wifiSettingsComboBox.addItems(self.scan_wifi())

    def scan_wifi(self):
        '''
        uses linux shell and WIFI interface to scan available networks
        :return: dictionary of the SSID and the signal strength
        '''
        # scanData = {}
        # print "Scanning available wireless signals available to wlan0"
        scan_result = \
            subprocess.Popen("iwlist wlan0 scan | grep 'ESSID'", stdout=subprocess.PIPE, shell=True).communicate()[0]
        # Processing STDOUT into a dictionary that later will be converted to a json file later
        scan_result = scan_result.decode('utf8').split(
            'ESSID:')  # each ssid and pass from an item in a list ([ssid pass,ssid paas])
        scan_result = [s.strip() for s in scan_result]
        scan_result = [s.strip('"') for s in scan_result]
        scan_result = filter(None, scan_result)
        return scan_result


    def startKeyboard(self, returnFn, onlyNumeric=False, noSpace=False, text=""):
        '''
        starts the keyboard screen for entering Password
        '''
        keyBoardobj = keyboard.Keyboard(onlyNumeric=onlyNumeric, noSpace=noSpace, text=text)
        keyBoardobj.keyboard_signal.connect(returnFn)
        keyBoardobj.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        keyBoardobj.show()

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
        try:
            if self.timeSpinBox.value() == 0:
                QtWidgets.QMessageBox.warning(self, 'Warning', 'Set Timer in Settings Tab First')
            else:
                if self.playPauseButton.isChecked() is False:
                    if self.uvStartStopButton.isChecked():
                        uvLed.start()
                    if self.tempStartStopButton.isChecked():
                        heater.start()
                    turnTable.start()
                    magLock.start()
                    self.controlTabWidget.setTabEnabled(1, False)
                    self.materialPreset.setText((self.materialComboBox.currentText()))
                    if self.pauseFlag == True:
                        if self.timerChangedFlag == False:
                            self.curingTimerThreadObject = ThreadCuringTimer(self.timeRemaining)
                        else:
                            self.curingTime = self.timeSpinBox.value() * 60
                            self.curingTimerThreadObject = ThreadCuringTimer(self.curingTime)
                            self.timerChangedFlag = False
                        self.pauseFlag = False
                    else:
                        self.curingTime = self.timeSpinBox.value() * 60
                        self.curingTimerThreadObject = ThreadCuringTimer(self.curingTime)
                        self.timerChaingedFlag = False

                    self.curingTimerThreadObject.curing_done_signal.connect(self.curingDoneAction)
                    self.curingTimerThreadObject.progress_bar_signal.connect(self.updateProgressBar)
                    self.curingTimerThreadObject.time_remaining_signal.connect(self.timeRemainingAction)
                    self.curingTimerThreadObject.start()

                else:
                    self.curingTimerThreadObject.stop()
                    self.pauseFlag = True
                    self.controlTabWidget.setTabEnabled(1, True)
                    heater.stop()
                    turnTable.stop()
                    uvLed.stop()
                    magLock.stop()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Error', str(e))

    def stopAction(self):
        '''
        Stops Curing
        '''
        try:
            self.curingTimerThreadObject.stop()
            self.pauseFlag = False
            self.playPauseButton.setChecked(False)
            self.progressBar.setValue(0)
            self.timeRemainingLabel.setText(str(0) + " Seconds")
            self.controlTabWidget.setTabEnabled(1, True)
            self.timeSpinBox.setEnabled(True)
            heater.stop()
            turnTable.stop()
            uvLed.stop()
            magLock.stop()
            self.timerChaingedFlag = False
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Error', str(e))

    def toggleUvLed(self):
        '''
        Action to perform with UV LED button is toggled
        '''
        self.materialComboBox.setCurrentIndex(self.materialComboBox.findText('Custom'))
        pass

    def toggleHeater(self):
        '''
        overide Material Preset combobox
        set combobox to custom
        retain previous state of other settings
        toggle state of heater
        '''
        self.materialComboBox.setCurrentIndex(self.materialComboBox.findText('Custom'))
        pass

    def timerChangedAction(self):
        '''
        overide Material Preset combobox
        set combobox to custom
        retain previous state of other settings
        toggle state of heater
        '''
        #self.materialComboBox.setCurrentIndex(self.materialComboBox.findText('Custom'))
        self.timerChangedFlag = True

    def curingDoneAction(self):
        try:
            print('curing done')
            self.progressBar.setValue(100)
            self.pauseFlag = False
            self.playPauseButton.setChecked(False)
            self.timeRemainingLabel.setText(str(0) + ' Seconds')
            self.controlTabWidget.setTabEnabled(1, True)
            self.timeSpinBox.setEnabled(True)
            heater.stop()
            turnTable.stop()
            uvLed.stop()
            magLock.stop()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Error', str(e))

    def updateProgressBar(self, timeRemaining):
        self.timeRemainingLabel.setText(self.convert(timeRemaining))
        if timeRemaining < self.curingTime:
            self.progressBar.setValue((((self.curingTime - timeRemaining) / self.curingTime)) * 100)
        pass

    def timeRemainingAction(self, timeRemaining):
        self.timeRemaining = timeRemaining  # Time Remining in Seconds

    def materialPresetSelected(self):
        try:
            if not materials[self.materialComboBox.currentText()] == 'Custom':
                if materials[self.materialComboBox.currentText()]['temp'] == True:
                    self.tempStartStopButton.setChecked(True)
                else:
                    self.tempStartStopButton.setChecked((False))
                if materials[self.materialComboBox.currentText()]['uvLed'] == True:
                    self.uvStartStopButton.setChecked(True)
                else:
                    self.uvStartStopButton.setChecked((False))
                if materials[self.materialComboBox.currentText()]['Time'] > 0:
                    self.timeSpinBox.setValue(materials[self.materialComboBox.currentText()]['Time'])
                else:
                    self.timeSpinBox.setValue(10)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Error', str(e))

    # Python Program to Convert seconds
    # into hours, minutes and seconds

    def convert(self, seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        return "%d:%02d:%02d" % (hour, minutes, seconds)


class ThreadCuringTimer(QtCore.QThread):
    curing_done_signal = QtCore.pyqtSignal()
    progress_bar_signal = QtCore.pyqtSignal(int)
    time_remaining_signal = QtCore.pyqtSignal(int)

    def __init__(self, curingTime):
        super(ThreadCuringTimer, self).__init__()
        self.curingTime = curingTime

    def run(self):
        try:
            self.startTime = time.time()
            self.timeElapsed = (time.time() - self.startTime)
            while self.timeElapsed <= self.curingTime:
                self.progress_bar_signal.emit(self.curingTime - self.timeElapsed)
                time.sleep(1)
                self.timeElapsed = (time.time() - self.startTime)
            self.curing_done_signal.emit()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Error', str(e))

    #
    def stop(self):
        try:
            if self.timeElapsed <= self.curingTime:
                self.time_remaining_signal.emit(self.curingTime - self.timeElapsed)
            self.terminate()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Error', str(e))


class ThreadRestartNetworking(QtCore.QThread):
    WLAN = "wlan0"
    ETH = "eth0"
    signal = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, interface):
        super(ThreadRestartNetworking, self).__init__()
        self.interface = interface
    def run(self):
        self.restart_interface()
        attempt = 0
        while attempt < 3:
            # print(getIP(self.interface))
            if getIP(self.interface):
                self.signal.emit(getIP(self.interface))
                break
            else:
                attempt += 1
                time.sleep(5)
        if attempt >= 3:
            self.signal.emit(None)

    def restart_interface(self):
        '''
        restars wlan0 wireless interface to use new changes in wpa_supplicant.conf file
        :return:
        '''
        if self.interface == "wlan0":
            subprocess.call(["wpa_cli","-i",  self.interface, "reconfigure"], shell=False)
        if self.interface == "eth0":
            subprocess.call(["ifconfig",  self.interface, "down"], shell=False)
            time.sleep(1)
            subprocess.call(["ifconfig", self.interface, "up"], shell=False)
        # subprocess.call(["ifdown", "--force", self.interface], shell=False)
        # subprocess.call(["ifup", "--force", self.interface], shell=False)
        time.sleep(5)



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
