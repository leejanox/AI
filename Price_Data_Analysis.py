import csv
import re 
import pandas as pd
import matplotlib.pyplot as plt
#matplot 한글폰트 설정 
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows의 경우
# 깨짐 방지 (음수 기호가 깨지는 경우 처리)
plt.rcParams['axes.unicode_minus'] = False

"""
matplotlib에서 사용할 수 있는 폰트 목록 확인

# 시스템에 설치된 폰트 목록 출력
import matplotlib.font_manager as fm

for font in fm.fontManager.ttflist:
    print(font.name)
"""


#가격구간 마다 판매량 보기
#기준 1000원 -> 어떤 가격일때 판매량이 가장 높은지
#할인 판매가가 "N/A" 일수도 있으니 (1)정가 기준 (2)할인가 기준 으로 두개 보기

#csv 파일 읽어오기

df=pd.read_csv("InfoAll.csv")

#읽어온 csv에서 판매지수 = 판매량 따로 저장하기
#판매지수 column이  | 판매지수 131,028 판매지수란? 이런식으로 긁어와지니까 여기서 숫자만 추출
#문자열 내의 숫자만 골라내려면 str.isdigit() 메서드를 사용하면 된다고 함

#판매지수 숫자만 추출
df_SaleRank=df[["Sale Rank"]] #시리즈 ->dataframe

# "Sale Rank" 열에서 숫자만 추출하여 Series로 저장
# 원본 csv Sale Rank 아예 바꾸기
df["Sale Rank"]= df_SaleRank["Sale Rank"].apply(lambda x: int("".join(re.findall(r'\d+', x))))


#읽어온 csv 가격의 최댓값과 최솟값 찾기

# 쉼표와 "원"을 제거하고 숫자형으로 변환
df["Original Price"] = df["Original Price"].apply(lambda x: int(x.replace(",", "").replace("원", "")))
df["Sale Price"] = df["Sale Price"].apply(lambda x: int(x.replace(",", "").replace("원", "")))

#pd.to_numeric()를 사용해 변환에 실패한 값(NaN, "N/A" 등)을 자동으로 NaN으로 처리
df["Original Price"]=pd.to_numeric(df["Original Price"])
df["Sale Price"]=pd.to_numeric(df["Sale Price"])

#(1) 정가 
max_OPrice=df["Original Price"].max()
min_OPrice=df["Sale Price"].min()

#(2) 할인가
max_SPrice=df["Sale Price"].max()
min_SPrice=df["Sale Price"].min()

#print(f"정가 : max={max_OPrice},min={min_OPrice}, 할인가 : max={max_SPrice}, min={min_SPrice}")


#그래프 그릴거니까 pip install matplotlib 
#가격 min~max 사이로 필터링
#df에 있는 가격중 min_Price ~max_Price 가격의 데이터만 선택

#(1)정가
#filtered_OPrice=df[(df["Original Price"]>=min_OPrice) & (df["Original Price"]<=max_OPrice)] #가격대 범위 : 최솟값~ 최댓값
#filtered_OPrice=df[(df["Original Price"]>=min_OPrice) & (df["Original Price"]<= 80000)]
filtered_OPrice=df[(df["Original Price"]>=min_OPrice) & (df["Original Price"]<= 35000)]
#(2)할인가
#filtered_SPrice=df[(df["Sale Price"]>=min_SPrice) & (df["Sale Price"]<=max_SPrice)] #가격대 범위 : 최솟값~ 최댓값
#filtered_SPrice=df[(df["Sale Price"]>=min_SPrice) & (df["Sale Price"]<=80000)]
filtered_SPrice=df[(df["Sale Price"]>=min_SPrice) & (df["Sale Price"]<=35000)]

#가격을 구간별로 나눠서 x축, 판매지수를 y축으로 해서 히스토그램을 그리기

"""
# 가격대 분포를 min_OPrice~max_OPrice로 했을 때

#(1)정가
plt.figure(figsize=(10,6))
plt.hist(filtered_OPrice["Original Price"], bins=20, weights=df["Sale Rank"], color="pink", edgecolor="black")
plt.title(f"정가 가격대별 판매량 분포 (가격 범위: {min_OPrice}~{max_OPrice}원)")
plt.xlabel("가격 (원)")
plt.ylabel("판매량")
plt.show()

#(2)할인가
plt.figure(figsize=(10,6))
plt.hist(filtered_SPrice["Sale Price"], bins=20, weights=df["Sale Rank"], color="skyblue", edgecolor="black")
plt.title(f"할인 가격대별 판매량 분포 (가격 범위: {min_SPrice}~{max_SPrice}원)")
plt.xlabel("할인가격 (원)")
plt.ylabel("판매량")
plt.show()


##여기까지 찍었을때 범위가 너무 커서 그래프가 앞쪽에 쏠리는 현상 발생
##그래프로 찍을 x축 범위를 min_OPrice~ 80000원 정도로 변경해야 할듯
"""

#가격대 분포를 min_OPrice~80000원으로 했을 때
#변경 사항 : 가격 범위 -> x축인 가격 범위를 바꿔줌 (68줄) 따라서 가중치인 y축에 들어갈 df["Sale Rank"]도 바꿔야함 ->filtered_OPrice["Sale Rank"]

"""
#(1)정가
plt.figure(figsize=(10,6))
plt.hist(filtered_OPrice["Original Price"], bins=20, weights=filtered_OPrice["Sale Rank"], color="red", edgecolor="black")
plt.title(f"정가 가격대별 판매량 분포 (가격 범위: {min_OPrice} ~ 80000원)")
plt.xlabel("가격 (원)")
plt.ylabel("판매량")
plt.show()

#(2)할인가
plt.figure(figsize=(10,6))
plt.hist(filtered_SPrice["Sale Price"], bins=20, weights=filtered_SPrice["Sale Rank"], color="skyblue", edgecolor="black")
plt.title(f"할인 가격대별 판매량 분포 (가격 범위: {min_SPrice}~80000원)")
plt.xlabel("할인가격 (원)")
plt.ylabel("판매량")
plt.show()


### 여기까지 확인 결과 가격 분포 min_OPrice~ 35000원이 딱 알맞을 듯 => 보통 책 가격 평균 분포가 저 사이인듯함
"""

#(1)정가
plt.figure(figsize=(10,6))
plt.hist(filtered_OPrice["Original Price"], bins=20, weights=filtered_OPrice["Sale Rank"], color="red", edgecolor="black")
plt.title(f"정가 가격대별 판매량 분포 (가격 범위: {min_OPrice} ~ 35000원)")
plt.xlabel("가격 (원)")
plt.ylabel("판매량")
plt.show()

#(2)할인가
plt.figure(figsize=(10,6))
plt.hist(filtered_SPrice["Sale Price"], bins=20, weights=filtered_SPrice["Sale Rank"], color="skyblue", edgecolor="black")
plt.title(f"할인 가격대별 판매량 분포 (가격 범위: {min_SPrice}~35000원)")
plt.xlabel("할인가격 (원)")
plt.ylabel("판매량")
plt.show()

### 확인결과 ###

# 중간 부분에 판매량이 확 높아지는 구간이 있고, 너무 가격이 낮거나 높으면 판매량이 훅 떨어짐
# 가격의 한 기준을 잡으려면 판매량이 확 떨어지는 구간을 찾아야함
# 어차피 사람들이 책을 구매하는 가격 = 할인 가격 이니까 정가는 이제 딱히 안 봐도 될듯

#가격 구간별로 판매량 보기 -> 5000원 단위로 구간 나누기

Range_SPrice = pd.cut(filtered_SPrice["Sale Price"], bins=range(0,40000,5000)) #가격 나누기
group_SaleRank = filtered_SPrice.groupby(Range_SPrice)["Sale Rank"].sum() #구간별 판매량 합계

#그래프
plt.figure(figsize=(10, 6))
group_SaleRank.plot(kind='bar', color='yellow', edgecolor='black')
plt.title("5,000원 단위 할인가격 구간별 판매량")
plt.xlabel("할인가격 구간 (원)")
plt.ylabel("판매량")
plt.xticks(rotation=45)
plt.show()

#확인결과
#할인가가 20000원을 넘어가면 판매량이 확 감소함

#결론 : 판매량 예측시 가격이 20000원을 초과하면 판매량이 떨어질 가능성 존재!!!!!!

### 가격 기준 = 할인가 20000원! ####