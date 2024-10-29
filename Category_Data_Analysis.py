# 책 장르와 판매량 연관성

import csv
import re
import pandas as pd
#matplotlib 사용 및 한글 font 깨짐 방지 + 음수 기호 깨짐 방지
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

#csv 파일 읽어오기
df =pd.read_csv("InfoAll.csv")
#print(df.head())

#가져와야 하는 정보 = "Sale Rank", "Category"

df_SaleRank = df["Sale Rank"] #판매지수
df_Category = df["category"] #장르
#print(f"판매지수 : {df_SaleRank}, 카테고리 : {df_Category}")

#Sale Rank 열 숫자만 추출
df_SaleRank = df['Sale Rank'].apply(lambda x: int("".join(re.findall(r"\d+",x))))
#print(df_SaleRank)

#category에 있는 장르의 종류 확인
category_type = df_Category.unique() #카테고리 열의 고유한 값 배열 반환
#print(len(category_type)) #89개;;?

#같은 장르의 책들 판매량을 모두 더하기
#판매지수와 카테고리만 들어있는 dataframe 만들어야 하나?
concat_df = pd.concat([df_Category,df_SaleRank],axis=1)
#print(concat_df.head())
#print(type(concat_df)) # good
#concat_df를 groupby 할건데 카테고리에 있는 타입들 기준으로 판매량을 합칠거니까
category_sale_sum = concat_df.groupby("category")["Sale Rank"].sum()
#print(category_sale_sum) 

#문제점
#print(category_type)
"""
['한국소설' '시/희곡' '경제' '글쓰기' '인문/교양' '영미소설' '처세술/삶의 자...' '청소년 문학' '액션'
 '테마소설' '영어' '1-2학년' '로맨스' '장르소설' '투자/재테크' '감성/가족 에세...' '성공학/경력관리' '요리'
 '철학/사상' '자녀교육' '4-6세' '심리' '3-4학년' '한국 에세이' '사회비평/비판' '동양철학' '5-6학년'
 '건강에세이/건강...' '천문학' '생명과학' '인간관계' '언론학/미디어론' '일본어' '동물 에세이' '공무원' '일본소설'
 '한국사능력검정...' '컴퓨터 입문/활...' '프랑스소설' '경영' '판타지' '웹툰' 'CEO/비즈니스맨' '스포츠'
 '한국사/한국문화' '삶의 자세와 지...' '인공지능' '외국 에세이' '인터넷 비즈니스' '사회학' '정치/외교'
 '컴퓨터 수험서' '주제로 읽는 인...' '독일소설' '공부법' '명사/연예인 에...' '독서/비평' '역사와 문화 교...'
 '임신/출산' '수학' '라이트노벨' '마케팅/세일즈' '화술/협상/회의...' '아트북' '미술' '기독교(개신교)'
 '초등고학년-중등' '공포/추리' '드라마' '질병과 치료법' '0-3세' '연애/사랑 에세...' '세계사/세계문화'
 '성공스토리' '세계각국소설' '대중음악' '경제/금융/회계/...' '육아' 'OS/데이터베이스' '교육' '예술일반/예술사'
 '서양철학' '그림 에세이' '예술 에세이' '취업/상식/적성...' '국가자격/전문사...' '여성 에세이' '취미기타'
 '다이어트/미용']
 """

#많아도 너무 많다.
#category_sale_sum 을 판매량이 높은 순대로 줄 세워서 20개만 뽑아보자 (내림차.,..순..?)
Top20_CSS = category_sale_sum.sort_values(ascending=False).head(20)
#print(Top20_CSS)
"""
category
한국소설           21629028
영어              3189663
인문/교양           3055572
시/희곡            2229888
처세술/삶의 자...     2210361
투자/재테크          2005482
청소년 문학          1828398
경제              1606185
1-2학년           1510305
영미소설            1481106
심리              1034517
한국사능력검정...       925968
자녀교육             868788
3-4학년            854457
한국 에세이           774474
글쓰기              732735
성공학/경력관리         703389
장르소설             690921
테마소설             653148
인간관계             645801
"""
#1-2학년, 3-4 학년,한국사능력검정시험,영어 같은 경우는 학습지 및 문제집이므로 제외
filter_top20_category = Top20_CSS.drop(["1-2학년","3-4학년","영어","한국사능력검정..."])
#print(filter_top20_category)