"""
每个细胞有两种状态-存活ON或死亡OFF，每个细胞与以自身为中心的周围八格细胞产生互动。
1)人口过少：当周围低于2个（不包含2个）存活细胞时， 本单元活细胞死亡。
2)稳定：当周围有2个或3个存活细胞时， 本单元细胞保持原样。
3)人口过剩：当周围有3个以上的存活细胞时，本单元活细胞死亡。
4)繁殖：当周围有3个存活细胞时，本单元细胞存活/活化。
2020.4.12
By 卢博文，吴沁忆，刘继林
"""
import sys
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QSlider, QWidget, QLabel, QPushButton, QGroupBox, QLineEdit,QLCDNumber
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QRect, QCoreApplication, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen
import numpy as np

# ui主窗口，包含显示运算结果的Board，开始，停止按钮，窗口边长输入，密度，演化速度滑动条
class life(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        '''initiates application UI'''
        self.tboard = Board(self)
        self.tboard.resize(720,720)
        self.tboard.move(10,10)

        # 开始按钮
        self.beginbutton = QPushButton(self)
        self.beginbutton.setGeometry(QRect(790, 70, 131, 51))
        self.beginbutton.setObjectName("beginbutton")
        self.beginbutton.clicked.connect(self.tboard.beginbuttonClicked)

        # 停止按钮
        self.stopbutton = QPushButton(self)
        self.stopbutton.setGeometry(QRect(790, 150, 131, 51))
        self.stopbutton.setObjectName("stopbutton")
        self.stopbutton.clicked.connect(self.tboard.stopbuttonClicked)

        self.groupBox = QGroupBox(self)
        self.groupBox.setGeometry(QRect(750, 270, 211, 391))
        self.groupBox.setObjectName("groupBox")

        # 窗口边长输入
        self.Nchanger = QLineEdit(self.groupBox)
        self.Nchanger.setGeometry(QRect(100, 80, 51, 21))
        self.Nchanger.setObjectName("Nchanger")
        self.Nchanger.setText("50")
        self.Nchanger.editingFinished.connect(self.editingFinished)

        # 密度滑动条lcd显示
        self.densitylcd = QLCDNumber(self.groupBox)
        self.densitylcd.setGeometry(QRect(130, 140, 64, 23))
        self.densitylcd.setObjectName("densitylcd")
        self.densitylcd.setDigitCount(3)
        self.densitylcd.setSegmentStyle(QLCDNumber.Flat)

        # 速度滑动条lcd显示
        self.speedlcd = QLCDNumber(self.groupBox)
        self.speedlcd.setGeometry(QRect(130, 230, 64, 23))
        self.speedlcd.setObjectName("speedlcd")
        self.speedlcd.setDigitCount(3)
        self.speedlcd.setSegmentStyle(QLCDNumber.Flat)

        # 密度滑动条
        self.horizontalSlider = QSlider(self.groupBox)
        self.horizontalSlider.setGeometry(QRect(30, 170, 160, 22))
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setValue(30)
        self.densitylcd.display(30)
        self.horizontalSlider.valueChanged.connect(self.densityvalueChanged)

        # 速度滑动条
        self.speedchanger = QSlider(self.groupBox)
        self.speedchanger.setGeometry(QRect(30, 260, 160, 22))
        self.speedchanger.setOrientation(Qt.Horizontal)
        self.speedchanger.setObjectName("speedchanger")
        self.speedchanger.setMaximum(600)
        self.speedchanger.setMinimum(15)
        self.speedchanger.setValue(200)
        self.speedlcd.display(415)
        self.speedchanger.valueChanged.connect(self.speedvalueChanged)

        # 控件名称定义
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setGeometry(QRect(30, 80, 81, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setGeometry(QRect(30, 140, 131, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setGeometry(QRect(30, 230, 121, 21))
        self.label_4.setObjectName("label_4")
        _translate = QCoreApplication.translate
        self.beginbutton.setText(_translate("MainWindow", "开始"))
        self.stopbutton.setText(_translate("MainWindow", "停止"))
        self.groupBox.setTitle(_translate("MainWindow", "         参数设置"))
        self.label_2.setText(_translate("MainWindow", "图窗边长："))
        self.label_3.setText(_translate("MainWindow", "初始细胞密度："))
        self.label_4.setText(_translate("MainWindow", "演化速度："))

        self.resize(980, 740)
        self.setFixedSize(980, 740)
        self.center()
        self.setWindowTitle('game of life')
        self.show()

    # 将窗口置于屏幕中央
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    # 密度滑动条移动时调用函数
    def densityvalueChanged(self):
        self.tboard.density = self.horizontalSlider.value()/100
        self.densitylcd.display(self.horizontalSlider.value())

    # 速度滑动条移动时调用函数
    def speedvalueChanged(self):
        self.tboard.Speed = self.speedchanger.value()
        self.speedlcd.display(600 - self.speedchanger.value() + 15)

    # 窗口边长变化时调用函数
    def editingFinished(self):
        self.tboard.N = int(self.Nchanger.text())


# Board类，用来显示细胞的状态，实现细胞每一代的更新
class Board(QFrame):
    Speed = 200
    N = 50
    density = 0.3
    vals = [1, 0]

    # 开始按钮按下时调用函数
    def beginbuttonClicked(self):
        self.start()

    # 停止按钮按下时调用按钮
    def stopbuttonClicked(self):
        self.s = np.ones((self.N, self.N))
        # self.timer.stop()
        self.killTimer(self.timer.timerId())

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''

        self.timer = QBasicTimer() # 定义timer
        self.setFocusPolicy(Qt.StrongFocus)
        self.s = np.zeros((self.N, self.N))

    # 用于计算一个细胞显示在窗口上的大小
    def squareWidth(self):
        return 720 / self.N

    def squareHeight(self):
        return 720 / self.N

    def start(self):

        self.s = np.random.choice(self.vals, self.N * self.N, p=[self.density, 1 - self.density]).reshape(self.N,self.N) # 随机初始化一个细胞状态
        self.isStarted = True
        self.isWaitingAfterLine = False

        self.timer.start(self.Speed, self) # 使用当前speed开始timer

    # 重写paintevent， 利用drewSquare函数来将细胞状态一个一个画上去
    def paintEvent(self, event):
        painter = QPainter(self)
        s = self.s

        for i in range(self.N):
            for j in range(self.N):
                if s[i][j] == 1:
                    self.drawSquare(painter, i*self.squareWidth(), j*self.squareHeight(), 1)

    # 随时间更新显示
    def timerEvent(self, event):

        if event.timerId() == self.timer.timerId():
            self.cells_update()

        else:
            super(Board, self).timerEvent(event)

    # 给定坐标，颜色，来画一个方块
    def drawSquare(self, painter, x, y, shape):

        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2,
                         self.squareHeight() - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1,
                         y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)

        pen = QPen(Qt.black, 5, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(0, 0, 0, 720)
        painter.drawLine(0, 720, 720, 720)
        painter.drawLine(720, 720, 720, 0)
        painter.drawLine(720, 0, 0, 0)

    # 更新函数，通过细胞的现状态，返回细胞的下一个状态
    def cells_update(self):
        N = self.N
        s = self.s
        s2 = np.zeros((N, N))
        for i in range(1, N-1):
            for j in range(1, N-1):
                arround = np.array([[s[i - 1, j - 1], s[i - 1, j], s[i - 1, j + 1]],
                                    [s[i, j - 1], 0, s[i, j + 1]],
                                    [s[i + 1, j - 1], s[i + 1, j], s[i + 1, j + 1]]])
                if arround.sum() == 3:
                    s2[i, j] = 1
                elif s[i, j] == 0 and arround.sum() == 2:
                    s2[i, j] = 0
                elif s[i, j] == 1 and arround.sum() == 2:
                    s2[i, j] = 1
                else:
                    s2[i, j] = 0
        self.s = s2
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = life()
    sys.exit(app.exec_())