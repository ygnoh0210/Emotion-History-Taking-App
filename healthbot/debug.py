# -*- coding: utf-8 -*-

# logging 관련
from logging.config import dictConfig
import logging

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file']
    }
})


# 필요 모듈 import
import konlpy
import numpy as np 
import pandas as pd
from konlpy.tag import Okt

import regex as re
okt = Okt()

import tkinter
from tkinter import *
from PIL import Image, ImageTk

import pickle



"""##### 사용할 데이터 로드"""

# entity 데이터 로드
data = np.load('entity.npy', allow_pickle=True)
entity_data_modi = pd.DataFrame(data)

# intent 데이터 로드 후 결측치 변환
intent_data = pd.read_csv('intent.csv')
intent_data = intent_data.iloc[:,1:]
intent_data = intent_data.fillna(' ')
for i in range(len(intent_data)):  # 정규식을 이용한 특수문자 제거
    for j in range(len(intent_data.columns)):
        intent_data.iloc[i,j] = intent_data.iloc[i,j].replace("'", '').replace(")", '').replace("(", '').replace(",", '')

# QA 데이터 로드
with open('QA_pair.pickle', 'rb') as handle:
    QA = pickle.load(handle)



"""# 데이터 preprocess

##### intent data 전처리
"""

# data 형태소 추출 후 원본 data에 합쳐주는 함수
def data_generate(columns_name):
    colum_list = intent_data[columns_name].tolist()
    a = []
    for i in colum_list:
        if i != " ":
            a.append(okt.morphs(i))
        else:
            a.append('')
    df = pd.Series(a, name=columns_name+"_변환")
    df = pd.concat([intent_data,df],axis=1)
    return df

# data 처리
a = list(intent_data.columns)

for i in a:
    intent_data = data_generate(i)

# 대표 개체명 추출
intent_data_개체명 = intent_data.iloc[:,0]

# 데이터셋 생성
intent_data_modi = intent_data.iloc[:,105:]
intent_data_modi = pd.concat([intent_data_개체명,intent_data_modi], axis=1)




"""# 답변 출력 함수

##### entity 추출
"""

# entity 추출 함수
final_entity = [] # 말 그대로 최종 entity 
a = [] # QA_pair에 넘겨주는 부분(전체 set - entity set)
error_check = [] # entity와 intent의 error check list

def entity_extract(input):
    # 필요한 리스트 만들기
    pos_entity = []
    pos_index = []

    # input을 형태소 처리 후 집합으로 변경
    morp_input = set(okt.morphs(input))
    
    # 형태소 처리된 entity data 값을 한개씩 불러와서, 처리된 input 값과 겹치는 부분(=result)만 골라내기
    # morp_input = 형태소 처리된 input 값
    # morp_dataset = 형태소 처리된 entity DB
    # result = morp_input, morp_dataset의 교집합
    for i in range(172):
        for j in range(17):
            morp_dataset = set(entity_data_modi.iloc[i,j])
            result = morp_dataset & morp_input

    # result와 morp_dataset의 교집합의 원소가 하나 이상이고 데이터와 일치하는 경우 pos_entity list에 추가, 그리고 그 경우에 i값(=데이터의 index 값)을 pos_index list에 추가
            if len(result) != 0 and result == morp_dataset:
                pos_entity.append(result)
                pos_index.append(i)

    # 가장 많이 겹치는 부분의 인덱스를 불러옴
    # 예외처리 : 만약 겹치는 부분이 없다면, 이전의 인덱스를 불러옴
    try: 
        entity_index = pos_index[np.argmax(pos_entity)]

        # 대표 entity 출력
        entity = entity_data_modi.iloc[entity_index,0]
        error_check.append("1")
        final_entity.clear()
        final_entity.append(entity)
        a.append(morp_input - np.max(pos_entity))
        return a[0]
    
    except:
        a = set(okt.morphs(input))
        return a




"""##### intent 추출"""

# intent 추출 함수
final_intent = []
final_intent_f = []
morp_dataset_f = []
morp_input_f = [] 

def intent_extract(a):
    # 필요한 리스트 만들기
    pos_intent = []
    pos_index = []
   
    # 형태소 처리된 intent data 값을 한개씩 불러와서, 처리된 input 값과 겹치는 부분(=result)만 골라내기
    # morp_dataset = 형태소 처리된 intent DB
    # result = morp_input, morp_dataset의 교집합
    for i in range(34):
        for j in range(105):
            morp_dataset = set(intent_data_modi.iloc[i,j])
            result = morp_dataset & a

    # result와 morp_dataset의 교집합의 원소가 하나 이상이고 데이터와 일치하는 경우 pos_intent list에 추가, 그리고 그 경우에 i값(=데이터의 index 값)을 pos_index list에 추가
            if len(result) != 0 and result == morp_dataset:
                pos_intent.append(result)
                pos_index.append(i)

    # a가 가장 많이 겹치는 부분의 인덱스를 불러옴
    # 예외처리 : 만약 겹치는 부분이 없다면, 이전의 인덱스를 불러옴
    try:
        intent_index = pos_index[np.argmax(pos_intent)]

        # 대표 intent 출력
        intent = intent_data_modi.iloc[intent_index,0]
        error_check.append("1")
        final_intent.clear()
        final_intent.append(intent)

        # 변수를 list에 담아준다.
        morp_dataset_f.append(morp_dataset)
        morp_dataset.append()

        return final_intent
    
    except:
        return final_intent




"""##### Q&A 매칭 함수"""

def QA_pair(final_entity,final_intent):
    key = final_entity + ' ' + final_intent
    try:
        return QA[key]
    except:
        return ('entity는 있으나 그에 맞는 intent가 없음')




"""# 실행"""
#Creating GUI with tkinter

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    logging.debug(msg)
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Arial", 13))
        
        # 여기서부터 예측 구간
        try:
            a = intent_extract(entity_extract(msg))
            if len(error_check) == 0:
                res = 'entity와 intent 모두 DB에 없음'
            else:
                if QA_pair(final_entity[0], a[0]) == 0:
                    res = 'DB에 아예 없음'
                else:
                    res = QA_pair(final_entity[0], a[0])
        except:
            res = '다시 질문해주세요!'

        ChatLog.insert(END, "entity: " + final_entity[0]+ '\n')
        ChatLog.insert(END, "intent: " + a[0] + '\n\n')
        ChatLog.insert(END, "Bot: " + res + '\n\n')
        error_check.clear()

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)  


base = Tk()
base.title("신안 해저문화재 챗봇")
base.geometry("800x500")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Arial",16,'bold'), text="보내기", width="9", height=5,
                    bd=0, bg="#666666", activebackground="#888888",fg='#000000',
                    command= send)

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")

#설명창
Explain = Text(base, bd=0, bg="white", height="8", width="55", font="Arial")
Explain.insert(tkinter.CURRENT,'학무늬 베개\n\n- 고려高麗 13세기\n- 11. 3 ×16×8.9cm\n- 1984년 입수\n- 신안20336\n\n넓적한 판板 6개를 잇대어 만든 베개이다. 베개의 윗면과 아랫면에는 원을 중심으로 안팎에 학과 구름무늬를 장식했다. 앞면과 뒷면에는 원 2개 안에 국화를 장식하고 그 바깥에 넝쿨무늬를 역상감逆象嵌[무늬의 바탕을 파내고 흰색 흙으로 메우는 기법] 기법으로 장식했다. 베개의 양쪽 마구리에 대는 베갯모 부분에는 커다란 구멍을 냈으며, 바탕 면에는 넝쿨무늬를 역상감 기법으로 장식했다. 이 넝쿨무늬는 학무늬 완[도230, 신안6554]처럼 이파리에 가는 선을 다시 그어 한층 더 섬세하게 표현했다. 규석 받침 자국이 한쪽 마구리 4곳에서만 확인되어서 옆으로 세워 가마에서 구웠음을 알 수 있다. 세련된 장식과 비율이 돋보이는 이 베개는 현재 남아 있는 고려청자 베개의 적은 수량을 감안할 때 자료로서 가치가 높다. 사용한 흔적은 보이지 않는다. 이것과 비슷한 베개가 강진이나 부안 일대의 가마터에서 나왔다.')
Explain.pack()

#설명창 scrollbar
E_scrollbar = Scrollbar(base, command=Explain.yview)
Explain['yscrollcommand'] = E_scrollbar.set


# 이미지 넣기
img = ImageTk.PhotoImage(file="1.jpg")
panel = Label(base, image = img)
panel.pack()


# EntryBox.bind("<Return>", send)

#Place all components on the screen
scrollbar.place(x=776,y=6, height=386)
ChatLog.place(x=406,y=6, height=386, width=370)
EntryBox.place(x=406, y=401, height=90, width=265)
SendButton.place(x=675, y=401, height=90)
E_scrollbar.place(x=376,y=256, height=240)
Explain.place(x=6,y=256, height=240, width=370)
panel.place(x=6,y=6, height=250, width=370)

base.mainloop()
