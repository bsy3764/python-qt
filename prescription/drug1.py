import re
import sys
import pandas as pd
import urllib.request   # URL을 가져오기 위한 파이썬 모듈
import os
import cv2
import random
import numpy as np
import matplotlib.pyplot as plt
import glob
import math
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QDate, QTime, Qt
from selenium import webdriver
from bs4 import BeautifulSoup as bs, BeautifulSoup
from urllib.request import urlopen
import urllib.parse

form_class = uic.loadUiType("drug.ui")[0]

data = pd.read_csv('./공공데이터개방_낱알식별목록.csv')
drug_name = pd.DataFrame(data['품목명'])

drug_simple_name = []
for i, row in drug_name.iterrows():
    drug_simple_name.append(re.split('[/,-,(,),|,<,>,\[,\]. :]',drug_name['품목명'][i])[0])

drug_simple_name = pd.DataFrame(drug_simple_name)
drug_simple_name.columns = ['simple_name']
new_data = pd.concat([data, drug_simple_name], axis=1)
# new_data[ new_data['simple_name'] == '갈미정']

class MyApp(QWidget, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.show()  # 창 보여주기

    def initUI(self):
        self.setWindowTitle('prescription')
        self.move(300, 300)

        self.name.returnPressed.connect(self.Write_name)
        self.Select_sex()
        self.Select_age()
        self.date_time()

        self.init_drug()

        self.drug.returnPressed.connect(self.Write_drug)
        self.waring0.setText("주의사항")
        self.waring0.setReadOnly(True)
        self.info0.setText("약 정보")
        self.info0.setReadOnly(True)

    def Write_name(self):
        self.name.setText()

    def Select_sex(self):
        self.sex.addItem('Woman')
        self.sex.addItem('Man')

    def Select_age(self):
        self.age.addItem('5-7')
        self.age.addItem('8-10')
        self.age.addItem('11-13')
        self.age.addItem('14-16')
        self.age.addItem('17-19')
        self.age.addItem('20-27')
        self.age.addItem('28-34')
        self.age.addItem('35-47')
        self.age.addItem('48-55')
        self.age.addItem('56-65')
        self.age.addItem('66-73')
        self.age.addItem('74-')

    def date_time(self):
        now = QDate.currentDate()  # 현재 날짜를 반환
        time = QTime.currentTime()  # 현재 시간을 반환
        date = now.toString('yyyy-MM-dd(dddd)')
        date1 = time.toString('hh:mm:ss')
        self.date.setText(date + ' / ' + date1)

    def init_drug(self):
        self.drug1.pixmap() == None
        self.drug2.pixmap() == None
        self.drug3.pixmap() == None
        self.drug4.pixmap() == None
        self.drug5.pixmap() == None

    def Write_drug(self):
        drug_name = self.drug.text() + '.jpg'
        print("약 이름 : {}".format(drug_name))
        drug_Img_dir = './drug_image/'  # 결과 이미지 저장할 파일, 경로
        self.drug_img_name = os.path.join(drug_Img_dir, drug_name)

        if os.path.isfile(self.drug_img_name):    # 파일이 있다면
            pixmap = QPixmap(self.drug_img_name)   # Qt 에서 이미지 가져오기

            # 이미지 크기를 label 사이즈 맞춰주기
            # QLabel 1 ~ 5 크기는 같음
            self.drug_W = self.drug1.width()  # 라벨의 가로길이
            self.drug_H = self.drug1.height()  # 라벨의 세로길이

            # 이미지를 라벨의 크기로 변경, 비율무시
            self.src_pixmap = pixmap.scaled(self.drug_W, self.drug_H, aspectRatioMode=Qt.IgnoreAspectRatio)

            # 이미지가 있다면 다음 칸에 이미지를 출력시키기
            drug_name_list = [self.drug1, self.drug2, self.drug3, self.drug4, self.drug5]
            drug_info_list = [self.info1, self.info2, self.info3, self.info4, self.info5]
            for num in drug_name_list:
                if num.pixmap() == None: # 해당 칸에 이미지가 없다면
                    num.setPixmap(self.src_pixmap)  # Qt 에서 원본 이미지 보여주기
                    break
                # elif num.pixmap() != None:   # 해당 칸에 이미지가 있다면
                #     continue
            # print(self.drug1.pixmap(), type(self.drug1.pixmap()))
            # print(self.drug2.pixmap(), type(self.drug2.pixmap()))

            # 약 내용 크롤링 하기
            # 약품 일련 번호 가져오기
            simple_name = self.drug.text()
            print("simple_name : {}".format(simple_name))
            drug_num = new_data[new_data['simple_name'] == simple_name]['품목일련번호']
            drug_num = list(drug_num)
            drug_num = str(drug_num[0])
            print("drug_num : {}".format(drug_num))

            driver = webdriver.Firefox(executable_path='/home/test/opencv/geckodriver')

            url = "https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq=" + str(drug_num)

            driver.get(url)
            req = driver.page_source
            soup = BeautifulSoup(req, 'html.parser')

            drug_info = soup.select_one('#_ee_doc > p')

            driver.quit()

            # print(drug_info.text, type(drug_info.text))
            # print(self.info1.text())

            for num in drug_info_list:
                if num.text() == '': # 해당 칸에 글자가 안 써있다면
                    num.setText(simple_name + '\n' + drug_info.text)  # Qt 에서 크롤링으로 가져온 정보를 입력하기
                    break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())