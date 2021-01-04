import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton, QComboBox
from PyQt5.QtCore import Qt
from PyQt5 import uic

form_class = uic.loadUiType("form2.ui")[0]
#print(form_class, type(form_class))

class MyApp(QWidget, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.show()  # 창 보여주기

    def initUI(self):
        self.unit = "Byte"
        self.value = "0"
        #print(self.lineEdit.width())
        #print(self.lineEdit.height())

        # QLabel 에 기본적으로 화면에 보이는 값이 0
        self.defaultDisplay()

        # 오른쪽 정렬
        self.RightShow()

        # read-only
        self.ReadOnly()

        # 입력창의 글자 크기 변경
        lineEdit_font = self.lineEdit.font()
        lineEdit_font.setPointSize(lineEdit_font.pointSize() + 9)  # 현재 글 크기에서 +8 글 크기 늘리기
        self.lineEdit.setFont(lineEdit_font)  # 바뀐 폰트 정보로 설정

        # comboBox 변경할 수 있는 값 추가
        self.ComboValue()

        # 텍스트가 변경될 때 inputValue 함수를 호출
        self.lineEdit.textChanged[str].connect(self.inputValue)

        # 단위가 변경될 때 inputUnit 함수를 호출
        self.comboBox.activated[str].connect(self.inputUnit)

        # windows 창 제목
        self.setWindowTitle('Trans_cal')
        self.setGeometry(300, 300, 430, 430)    # windows 창 위치 및 크기

    def defaultDisplay(self):
        self.lineEdit.setText('0')
        self.byte_1.setText('0')
        self.kb_1.setText('0')
        self.mb_1.setText('0')
        self.gb_1.setText('0')

    def RightShow(self):
        self.lineEdit.setAlignment(Qt.AlignRight)
        self.byte_1.setAlignment(Qt.AlignRight)
        self.kb_1.setAlignment(Qt.AlignRight)
        self.mb_1.setAlignment(Qt.AlignRight)
        self.gb_1.setAlignment(Qt.AlignRight)

    def ReadOnly(self):
        self.byte_1.setReadOnly(True)
        self.kb_1.setReadOnly(True)
        self.mb_1.setReadOnly(True)
        self.gb_1.setReadOnly(True)

    def ComboValue(self):
        self.comboBox.addItem('Byte')
        self.comboBox.addItem('KB')
        self.comboBox.addItem('MB')
        self.comboBox.addItem('GB')


    def inputValue(self, value):
        #print(value, type(value))
        self.value = value

        # 0이나 0.0이 화면에 보이면 아무 행동도 안 함
        if self.lineEdit.text() == '0':
            return

        # 입력창에 공백이 될 경우 0으로 다시 채우기
        if self.lineEdit.text() == '':
            self.lineEdit.setText('0')


        # 숫자가 아닌 값이 입력될 경우 0으로 채우기

        # 입력이 숫자인지 여부
        diti = self.value.isdigit()
        #print("1 diti : {}".format(diti), type(diti))

        # 입력이 문자일 경우
        if diti == False:
            diti1 = '.' in self.lineEdit.text() # 입력창에 '.'이 있는지 확인

            if diti1 == True:   # '.'을 입력받은 경우(소수점)
                #print("2 diti : {}".format(diti))
                if self.lineEdit.text().find('.') == 1: # .으로 시작하
                    self.lineEdit.setText('0')
            if diti1 != True:
                self.lineEdit.setText('0')

        # if diti == True:    # 입력이 숫자일 경우
        #     if self.lineEdit.text().find('0') == 1: # 0으로 시작할 경우(실수) 0.1

        self.calculate()

    def inputUnit(self, unit):
        print(unit)
        self.unit = unit

        self.calculate()

    def calculate(self):
        if self.unit == "Byte":
            byteVar = self.value
            KBVar = float(self.value) / 1024
            MBVar = (float(self.value)/1024) / 1024
            GBVar = ((float(self.value)/1024)/1024) / 1024
            self.byte_1.setText(byteVar)
            self.kb_1.setText(str(KBVar))
            self.mb_1.setText(str(MBVar))
            self.gb_1.setText(str(GBVar))

        if self.unit == "KB":
            byteVar = float(self.value) * 1024
            KBVar = self.value
            MBVar = float(self.value) / 1024
            GBVar = (float(self.value)/1024) / 1024
            self.byte_1.setText(str(byteVar))
            self.kb_1.setText(KBVar)
            self.mb_1.setText(str(MBVar))
            self.gb_1.setText(str(GBVar))

        if self.unit == "MB":
            byteVar = (float(self.value)*1024) * 1024
            KBVar = float(self.value) * 1024
            MBVar = self.value
            GBVar = float(self.value) / 1024
            self.byte_1.setText(str(byteVar))
            self.kb_1.setText(str(KBVar))
            self.mb_1.setText(MBVar)
            self.gb_1.setText(str(GBVar))

        if self.unit == "GB":
            byteVar = ((float(self.value)*1024)*1024) * 1024
            KBVar = (float(self.value)*1024) * 1024
            MBVar = float(self.value) * 1024
            GBVar = self.value
            self.byte_1.setText(str(byteVar))
            self.kb_1.setText(str(KBVar))
            self.mb_1.setText(str(MBVar))
            self.gb_1.setText(GBVar)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())