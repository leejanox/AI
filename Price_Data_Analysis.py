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

## 마지막!
# 다중선형회귀모델을 만들때 쓸 x1_train 으로 만들기
# 단위를 구간화하여 범주형 특징으로 변환 -> 근데 만약 다른 x2,x3 같은 train 데이터랑 크기가 같아야 하나?
# 아무튼 x1_train 데이터와 나중에 평가할 데이터를 8:2로 나누기는 모델 만들기 전에!
# 구간화해서 변수 만들기가 첫번째

#가격 구간화 하기 x1_train 용 -> pd.cut

Range2000_SP = pd.cut(df["Sale Price"], bins=range(3000,42000,2000),right=False, labels=False) #할인가 3300원부터 시작이였으니까 3000원부터 42000원까지 2000원단위로 구간화

#핫 인코딩? 구간화 시킨 Range2000_SP 의 각 구간들을 독립된 열로 만들어 준다. 

x1_train = pd.get_dummies(Range2000_SP, prefix="Range2000_SP")

print(x1_train.head()) # 여기서 출력 결과가 0,1 이 아닌 True,False가 나왔음 (문제 생김 ㅇㅇ)
"""
이유: pd.get_dummies가 이진값을 True/False로 변환했기 때문 -> 0,1 으로 나와야 다중선형회귀 모델에서 사용 가능

1.pd.get_dummies 를 만들때 자동으로 데이터 타입이 0,1로 나오게 하기

:pd.get_dummies는 일반적으로 자동으로 0과 1의 값을 사용하여 더미 변수를 생성하는데 False/True 형태로 나오는 경우는 데이터에 bool 타입이 포함되었거나, NaN 같은 결측치가 포함된 경우이다.
자동으로 0/1 형태의 더미 변수를 생성하기 위해서는 따로 결측치가 있는지 확인후 결측치를 0으로 대체하는 등 처리해서 더미 변수를 생성해야 한다.

print(df["Sale Price"].insull().sum()) #결측치 개수 확인
df["Sale Price"].fillna(0,inplace=True) #결측치가 있다면 결측치를 0으로 대체
그 다음 pd.get_dummies을 사용하며 더미변수 생성

2. .astype(int) 사용하여 0,1 로 변환
"""

#더미 만든것 출력 결과 0,1로 나오게 다시 바꾸기
x1_train=pd.get_dummies(Range2000_SP,prefix="Range2000_SP").astype(int)

print(x1_train.head())

#그럼 여기서 출력되는 0,1 결과값은 뭘 의미하는가?
# 각 열의 0 or 1의 값은:
# Sale Price가 특정 가격 구간에 속하는지를 나타내는 값

#pd.concat을 사용해서 Sale Price와 x1_train을 결합 axis=1 ->열 단위로 합치는 것
# "Sale Price" 열과 더미변수를 하나의 dataframe으로 결합

combine_data=pd.concat([df[["Sale Price"]],x1_train],axis=1)

print(combine_data.head()) #  이렇게 보면 한권의 책 마다 어느 가격의 구간에 속하는지 0,1 로 확인가능
