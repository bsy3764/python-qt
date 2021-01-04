import os
import sys
from PyQt5.QtWidgets import QFileDialog, QGroupBox
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np
from PyQt5 import uic

form_class = uic.loadUiType("form3.ui")[0]
counter = 0

class MyApp(QWidget, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.show()  # 창 보여주기

    def initUI(self):
        self.setWindowTitle('Image File')
        self.move(300, 300)

        self.none.setChecked(True)  # none 버튼이 선택되어진 상태로 시작함

        self.file.clicked.connect(self.openfile)    # '파일선택' 푸시 버튼이 눌리면 openfile 함수 호출

        # 라디오버튼이 눌렸을 경우
        self.none.clicked.connect(self.Radio)  # 'none' 라디오 버튼을 클릭 시
        self.blur.clicked.connect(self.Radio)   # 'blur' 라디오 버튼을 클릭 시
        self.sharpen.clicked.connect(self.Radio)  # 'sharpen' 라디오 버튼을 클릭 시

        # 체크박스 선택할 경우
        self.gray.stateChanged.connect(self.Check)
        self.invert.stateChanged.connect(self.Check)

        # 저장 버튼 클릭할 경우
        self.save.clicked.connect(self.fileSave)

    def openfile(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open file', './')

        pixmap = QPixmap(self.fname)   # Qt 에서 이미지 가져오기

        # 이미지 크기를 label 사이즈 맞춰주기
        # QLabel 1, 2 크기는 같음
        self.lbl_W = self.lbl1.width()    # 라벨의 가로길이
        self.lbl_H = self.lbl1.height()   # 라벨의 세로길이

        # 이미지를 라벨의 크기로 변경, 비율무시
        self.src_pixmap = pixmap.scaled(self.lbl_W, self.lbl_H, aspectRatioMode=Qt.IgnoreAspectRatio)

        self.lbl1.setPixmap(self.src_pixmap)    # Qt 에서 원본 이미지 보여주기
        self.lbl2.setPixmap(self.src_pixmap)  # Qt 에서 원본 이미지 보여주기

        # opencv 로 이미지 효과를 넣기 위해 이미지 읽어오기
        self.src = cv2.imread(self.fname)  # opencv 이미지 읽어오기
        self.src1 = cv2.cvtColor(self.src, cv2.COLOR_BGR2RGB)

    def result_imgShow(self, rec_img):
        self.fix_pixmap = rec_img

        # 이미지 pix 이 홀수일 때, 이미지 깨짐을 방지하기 위해
        width = self.fix_pixmap.shape[1]
        height = self.fix_pixmap.shape[0]
        bytesPerLine = width * 3

        Qimging = QImage(self.fix_pixmap.data, width, height, bytesPerLine, QImage.Format_RGB888)
        qimg = QPixmap.fromImage(Qimging)

        qimg_resize = qimg.scaled(self.lbl_W, self.lbl_H, aspectRatioMode=Qt.IgnoreAspectRatio)

        # 결과 이미지를 Qt 에서 보여주기
        self.lbl2.setPixmap(qimg_resize)  # Qt 에서 결과 이미지 보여주기

    def Radio(self):
        self.result1 = 0

        RButton = self.sender()
        if self.blur == RButton:
            # print("blur")

            self.result1 = cv2.blur(self.src1, (4, 4))   # blur 효과 주기

            # 결과 이미지를 Qt 에서 보여주기
            self.result_imgShow(self.result1)

        if self.sharpen == RButton:
            # print("sharpen")
            sharpening_2 = np.array([[-1, -1, -1, -1, -1],
                                     [-1, 2, 2, 2, -1],
                                     [-1, 2, 9, 2, -1],
                                     [-1, 2, 2, 2, -1],
                                     [-1, -1, -1, -1, -1]]) / 9.0
            self.result1 = cv2.filter2D(self.src1, -1, sharpening_2)

            # 결과 이미지를 Qt 에서 보여주기
            self.result_imgShow(self.result1)

        if self.none == RButton:
            # print("none")
            self.result1 = self.src1

            # 결과 이미지를 Qt 에서 보여주기
            self.result_imgShow(self.result1)

        self.Check()

    def Check(self):

        # self.result2 = self.result1
        # cv2.imshow('after radio', self.result2)

        CBox = self.sender()
        # print( type( CBox ) )
        self.invertB = self.invert.isChecked()  # invert 박스에 선택됬는지 여부 확인
        self.grayB = self.gray.isChecked()  # gray 박스에 선택됬는지 여부 확인

        if self.invert == CBox or self.invertB == True or self.invertB == False:
            # print("invert")

            if self.invertB == True:
                # print("invert : {}".format(self.invertB))
                self.result2 = cv2.bitwise_not(self.result1)

                # 결과 이미지를 Qt 에서 보여주기
                self.result_imgShow(self.result2)

            if self.invertB == False:
                # print("invert : {}".format(self.invertB))
                # 결과 이미지를 Qt 에서 보여주기
                self.result2 = self.result1

                # 결과 이미지를 Qt 에서 보여주기
                self.result_imgShow(self.result2)

        if self.gray == CBox or self.grayB == True or self.grayB == False:

            # cv2.imshow('after invert', self.result2)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            #print("gray")

            if self.grayB == True:
                # print("gray : {}".format(self.grayB))
                self.result3 = cv2.cvtColor(self.result2, cv2.COLOR_RGB2GRAY)   # 이미지 색깔 변경하기
                self.result3 = cv2.cvtColor(self.result3, cv2.COLOR_GRAY2RGB)

                # 결과 이미지를 Qt 에서 보여주기
                self.result_imgShow(self.result3)

            if self.grayB == False:
                # print("gray : {}".format(self.grayB))
                self.result3 = self.result2

                # 결과 이미지를 Qt 에서 보여주기
                self.result_imgShow(self.result3)


    def fileSave(self):
        # print("save")
        global counter
        result_img = cv2.cvtColor(self.result3, cv2.COLOR_RGB2BGR)

        # cv2.imshow('before save', result_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if not os.path.exists('test1'):
            os.makedirs('test1')

        cv2.imwrite('test1/fix_img.%i'%counter+'.jpg', result_img)

        counter = counter + 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
