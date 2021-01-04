import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit)
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QToolButton, QSizePolicy
from PyQt5.QtCore import Qt

class Button(QToolButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 50)
        size.setWidth(max(size.width(), size.height()))
        return size

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def createButton(self, text):
        button = Button(text)
        return button

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(15)

        font = self.display.font()
        font.setPointSize(font.pointSize() + 8)
        self.display.setFont(font)

        self.grid.addWidget(self.display, 0, 0, 1, 4)

        ac_botton = self.createButton('AC')
        ac_botton.setStyleSheet("background-color: #CBCCCE")
        self.grid.addWidget(ac_botton, 1, 0, 1, 1)

        ti_botton = self.createButton('+/-')
        ti_botton.setStyleSheet("background-color: #CBCCCE")
        self.grid.addWidget(ti_botton, 1, 1, 1, 1)

        ti1_botton = self.createButton('%')
        ti1_botton.setStyleSheet("background-color: #CBCCCE")
        self.grid.addWidget(ti1_botton, 1, 2, 1, 1)

        divbotton = self.createButton('/')
        divbotton.setStyleSheet("background-color: #FA6212")
        self.grid.addWidget(divbotton, 1, 3, 1, 1)

        botton_7 = self.createButton('7')
        self.grid.addWidget(botton_7, 2, 0, 1, 1)

        botton_8 = self.createButton('8')
        self.grid.addWidget(botton_8, 2, 1, 1, 1)

        botton_9 = self.createButton('9')
        self.grid.addWidget(botton_9, 2, 2, 1, 1)

        mulbotton = self.createButton('*')
        mulbotton.setStyleSheet("background-color: #FA6212")
        self.grid.addWidget(mulbotton, 2, 3, 1, 1)

        botton_4 = self.createButton('4')
        self.grid.addWidget(botton_4, 3, 0, 1, 1)

        botton_5 = self.createButton('5')
        self.grid.addWidget(botton_5, 3, 1, 1, 1)

        botton_6 = self.createButton('6')
        self.grid.addWidget(botton_6, 3, 2, 1, 1)

        subbotton = self.createButton("-")
        subbotton.setStyleSheet("background-color: #FA6212")
        self.grid.addWidget(subbotton, 3, 3, 1, 1)

        botton_1 = self.createButton('1')
        self.grid.addWidget(botton_1, 4, 0, 1, 1)

        botton_2 = self.createButton('2')
        self.grid.addWidget(botton_2, 4, 1, 1, 1)

        botton_3 = self.createButton('3')
        self.grid.addWidget(botton_3, 4, 2, 1, 1)

        addbotton = self.createButton('+')
        addbotton.setStyleSheet("background-color: #FA6212")
        self.grid.addWidget(addbotton, 4, 3, 1, 1)

        botton_0 = self.createButton('0')
        self.grid.addWidget(botton_0, 5, 0, 1, 2)

        dot_botton = self.createButton('+')
        self.grid.addWidget(dot_botton, 5, 2, 1, 1)

        resultbotton = self.createButton('=')
        resultbotton.setStyleSheet("background-color: #FA6212")
        self.grid.addWidget(resultbotton, 5, 3, 1, 1)


        self.setWindowTitle('calculator')
        self.setGeometry(300, 300, 300, 330)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())