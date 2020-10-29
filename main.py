import sys
import os
import datetime
import configparser
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QGraphicsOpacityEffect,QDesktopWidget,QMessageBox
from PyQt5.QtWidgets import QApplication,QInputDialog,QSplashScreen,QLineEdit
from PyQt5 import QtGui
from PyQt5 import QtCore
import honeypot
import multiprocessing
import backup
import recovery
import initial
import scan

config = configparser.RawConfigParser()
config.read('config.ini')

class MyApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setFixedSize(self.width(), self.height())

    def initUI(self):

        #set pictures below
        map1 = QPixmap("./img/img2.png")
        lb1 = QLabel(self)
        lb1.setPixmap(map1)
        lb1.move(25,12)

        map2 = QPixmap("./img/img3.png")
        map2 = map2.scaled(203, 203, QtCore.Qt.KeepAspectRatio)
        lb2 = QLabel(self)
        lb2.setPixmap(map2)
        lb2.move(485, 12)

        map3 = QPixmap("./img/img41.png")
        map3 = map3.scaled(203, 203, QtCore.Qt.KeepAspectRatio)
        lb3 = QLabel(self)
        lb3.setPixmap(map3)
        lb3.move(25, 230)

        map32= QPixmap("./img/img42.png")
        map32 = map32.scaled(203, 203, QtCore.Qt.KeepAspectRatio)
        lb32 = QLabel(self)
        lb32.setPixmap(map32)
        lb32.move(25, 322)

        map4 = QPixmap("./img/img51.png")
        map4 = map4.scaled(203, 203, QtCore.Qt.KeepAspectRatio)
        lb4 = QLabel(self)
        lb4.setPixmap(map4)
        lb4.move(248, 230)

        map42 = QPixmap("./img/img52.png")
        map42 = map42.scaled(203, 203, QtCore.Qt.KeepAspectRatio)
        lb42 = QLabel(self)
        lb42.setPixmap(map42)
        lb42.move(248, 322)

        map5 = QPixmap("./img/img6.png")
        map5 = map5.scaled(203, 203, QtCore.Qt.KeepAspectRatio)
        lb5 = QLabel(self)
        lb5.setPixmap(map5)
        lb5.move(472, 230)

        #set font
        font = QtGui.QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)

        font.setPointSize(10)
        font.setWeight(100)

        #set button
        self.btn_1 = QPushButton("ON/OFF",self)
        self.btn_1.setFont(font)
        self.btn_1.setCheckable(True)
        self.btn_1.clicked[bool].connect(self.event1)
        self.btn_1.move(350,76)
        self.btn_1.setStyleSheet("background-color: rgb(245, 245, 245);")

        self.btn_2 = QPushButton("ON/OFF", self)
        self.btn_2.setFont(font)
        self.btn_2.setCheckable(True)
        self.btn_2.clicked[bool].connect(self.event2)
        self.btn_2.move(350, 123)

        op1 = QGraphicsOpacityEffect()
        op1.setOpacity(0.2)
        self.btn_3 = QPushButton("", self)
        self.btn_3.setFont(font)
        self.btn_3.clicked.connect(self.event3)
        self.btn_3.move(25, 230)
        self.btn_3.resize(203, 80)
        self.btn_3.setGraphicsEffect(op1)

        op12 = QGraphicsOpacityEffect()
        op12.setOpacity(0.2)
        self.btn_32 = QPushButton("", self)
        self.btn_32.setFont(font)
        self.btn_32.clicked.connect(self.event32)
        self.btn_32.move(25, 322)
        self.btn_32.resize(203, 80)
        self.btn_32.setGraphicsEffect(op12)

        op2 = QGraphicsOpacityEffect()
        op2.setOpacity(0.2)
        self.btn_4 = QPushButton("", self)
        self.btn_4.setFont(font)
        self.btn_4.clicked.connect(self.event4)
        self.btn_4.move(248, 230)
        self.btn_4.resize(203, 80)
        self.btn_4.setGraphicsEffect(op2)

        op22 = QGraphicsOpacityEffect()
        op22.setOpacity(0.2)
        self.btn_42 = QPushButton("", self)
        self.btn_42.setFont(font)
        self.btn_42.clicked.connect(self.event42)
        self.btn_42.move(248, 322)
        self.btn_42.resize(203, 80)
        self.btn_42.setGraphicsEffect(op22)

        op3 = QGraphicsOpacityEffect()
        op3.setOpacity(0.2)
        self.btn_5 = QPushButton("", self)
        self.btn_5.setFont(font)
        self.btn_5.clicked.connect(self.event5)
        self.btn_5.move(472, 230)
        self.btn_5.resize(204, 171)
        self.btn_5.setGraphicsEffect(op3)

        op4 = QGraphicsOpacityEffect()
        op4.setOpacity(0.2)
        self.btn_6 = QPushButton("", self)
        self.btn_6.setFont(font)
        self.btn_6.clicked.connect(self.event6)
        self.btn_6.move(485, 12)
        self.btn_6.resize(190, 202)
        self.btn_6.setGraphicsEffect(op4)

        self.resize(700, 420)
        self.center()
        self.setWindowTitle('Anti-ransomware for linux')  # 创建一个窗口标题
        self.setWindowIcon(QIcon('./img/img1.jpg'))  # 创建一个QIcon对象并接收一个我们要显示的图片路径作为参数。
        self.show()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Confirm Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()  # 获得主窗口的一个矩形特定几何图形。这包含了窗口的框架。
        cp = QDesktopWidget().availableGeometry().center()  # 算出相对于显示器的绝对值。
        # 并且从这个绝对值中，我们获得了屏幕中心点。
        qr.moveCenter(cp)  # 矩形已经设置好了它的宽和高。现在我们把矩形的中心设置到屏幕的中间去。
        # 矩形的大小并不会改变。
        self.move(qr.topLeft())  # 移动了应用窗口的左上方的点到qr矩形的左上方的点，因此居中显示在我们的屏幕上。

    def event1(self,status): #honeypot module
        Deside=multiprocessing.Value('i',1)
        if status==True:
            self.btn_1.setStyleSheet("background-color: rgb(200,200,200);")
            print('honeypot starting...')
            global p
            p = multiprocessing.Process(target=honeypot.start_honeypot,args=(Deside,))
            p.start()
            QMessageBox.information(self, 'Confirm Message', '诱捕检测模块开启', QMessageBox.Yes)
        if status==False:
            self.btn_1.setStyleSheet("background-color: rgb(245,245,245);")
            Deside.value=0
            p.join()
            print('honeypot stopping...')
            QMessageBox.information(self, 'Confirm Message', '诱捕检测模块关闭', QMessageBox.Yes)

    def event2(self,status): #backupmodule
        if status==True:
            self.btn_2.setStyleSheet("background-color: rgb(200,200,200);")
            print('backup starting...')
            global process_backup
            process_backup=multiprocessing.Process(target=backup.main)
            process_backup.start()
            QMessageBox.information(self, 'Confirm Message', '备份模块开启', QMessageBox.Yes)
        if status==False:
            self.btn_2.setStyleSheet("background-color: rgb(245,245,245);")
            process_backup.terminate()
            process_backup.join()
            print('backup stopping...')
            QMessageBox.information(self, 'Confirm Message', '备份模块关闭', QMessageBox.Yes)

    def event3(self): #settings,and the same the next two
        watchfile = config.get('DEFAULT', 'workplace')
        text1, okPressed = QInputDialog.getText(self, "Get backup dir", "备份工作区:", QLineEdit.Normal, watchfile)
        if okPressed and text1 != '':
            if text1[-1]=='/':
                text1=text1[:-1]
            backupfile=text1+'/tmp_backup/'
            backupfilesafe=text1+'/newdisk/backup/'
            logfile = text1+'/log.txt'
            mountfile=text1+'/newdisk/'
            workplace=text1
            recoveryfile=text1+'/recovery/'
            scandir=text1+'/scan/'
            config.set("DEFAULT", "backupfile", backupfile)
            config.set("DEFAULT", "backupfilesafe", backupfilesafe)
            config.set("DEFAULT", "logfile", logfile)
            config.set("DEFAULT", "mountfile", mountfile)
            config.set("DEFAULT", "workplace", workplace)
            config.set("DEFAULT", "recoveryfile", recoveryfile)
            config.set("DEFAULT", "scandir", scandir)
            config.write(open("config.ini", "w"))

    def event32(self):
        watchfile = config.get('DEFAULT', 'watchfile')
        text1, okPressed = QInputDialog.getText(self, "Get watchfile dir", "备份监控区:", QLineEdit.Normal, watchfile)
        if okPressed and text1 != '':
            config.set("DEFAULT", "watchfile", text1)
            config.write(open("config.ini", "w"))


    def event4(self):
        dsk = config.get('DEFAULT', 'dsk')
        text1, okPressed = QInputDialog.getText(self, "Get dsk dir", "挂载的盘区:", QLineEdit.Normal, dsk)
        if okPressed and text1 != '':
            config.set("DEFAULT", "dsk", text1)
            config.write(open("config.ini", "w"))

    def event42(self): #initial
        print(datetime.datetime.now())
        initial.initial_dirs_files()
        initial.creat_honeypot()
        QMessageBox.information(self, 'Confirm Message', '初始化成功', QMessageBox.Yes)
        print(datetime.datetime.now())

    def event5(self): #recovery
        process_recovery = multiprocessing.Process(target=recovery.recover)
        process_recovery.start()
        process_recovery.join()
        print('recovery finished')
        QMessageBox.information(self, 'Confirm Message', '数据恢复成功', QMessageBox.Yes)

    def event6(self): #scan
        watchfile = config.get('DEFAULT', 'watchfile')
        text6, okPressed = QInputDialog.getText(self, "Get scan dir", "需要扫描的目录:", QLineEdit.Normal, watchfile)
        if okPressed and text6 != '':
            result=scan.scan(text6)
            if result=="":
                QMessageBox.information(self, 'Confirm Message', '没有潜在的危险', QMessageBox.Yes)
            else:
                scandir=config.get('DEFAULT','scandir')
                a = datetime.datetime.now()
                logtime=datetime.datetime.strftime(a,'%H:%M:%S')
                with open(scandir+'log'+logtime, 'w') as f:
                    f.write(result)
                QMessageBox.information(self, 'Confirm Message', '有潜在的危险,请查看目录下文件:'+scandir, QMessageBox.Yes)

if __name__ == '__main__':
    print(os.getpid())
    app = QApplication(sys.argv)

    splash = QSplashScreen() #程序启动画面
    splash.setPixmap(QPixmap('./img/img1.jpg'))
    splash.show()
    splash.close()

    ex = MyApplication()
    sys.exit(app.exec_())


