from sklearn.model_selection import train_test_split #학습/검증 데이터 split 할 때 필요
from Price_Data_Analysis import x1_train,df_SaleRank
import torch
import re
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

#가격으로 x_train만든걸로 한 번 예측모델 만들어보기

#랜덤시드
torch.manual_seed(1)

#데이터 불러오기 - dataframe 형태임 -> torch.FloatTensor 하려면 리스트나 배열 형태여야함
x_train = x1_train #x_train = 가격
y_train = df_SaleRank["Sale Rank"].apply(lambda x: int("".join(re.findall(r'\d+', x)))) #판매지수
#print(x_train.head())
#print(x_train.tail())
#print(y_train.head())

#변수 선언
x_train = torch.FloatTensor(x_train.values)
y_train = torch.FloatTensor(y_train.values)


#x_train, y_train shape 확인
#print(type(x_train),type(y_train)) #<class 'torch.Tensor'> <class 'torch.Tensor'>
#print(x_train.shape,y_train.shape) #torch.Size([500, 17]) torch.Size([500])
"""x_train과 y_train의 Size가 둘다 행 500개로 같음"""


#학습데이터/검증 데이터 분리 8:2
X_train, X_test, y_train, y_test = train_test_split(x1_train, y_train, test_size=0.2, random_state=42)
#print(f"X_train.Size : {X_train.shape} y_train.Size : {y_train.shape} , X_test.Size : {X_test.shape} y_test.Size : {y_test.shape}")
#X_train.Size : (400, 17) y_train.Size : torch.Size([400]) , X_test.Size : (100, 17) y_test.Size : torch.Size([100])
"""학습/검증 데이터 잘 나눠짐"""

#두 가지의 Tensor를 모델에 학습시키기 위해서는 "행"의 개수가 맞아야 한다. 꼭 확인 해볼 것

#가중치와 편향의 초기화
"""
#torch.zeros -> 0으로 초기화 하고 시작
#torch.ones -> 1로 초기화 하고 시작
#W = torch.zeros(1, requires_grad=True)
#torch.tensor (내가 원하는 시작점, requires_grad=True) 하면 시간 절약, 대충 w가 예상이 될 때 학습 시작 w 값을 내가 지정
"""
##W = torch.zeros(1, requires_grad=True) #가중치 W 를 0으로 초기화
W = torch.zeros((17, 1), requires_grad=True)  # (17, 1) 크기로 맞춤
b = torch.zeros(1, requires_grad=True) #편향 b 를 0으로 초기화

#경사 하강법 구현 : lr = 학습률 (적절히 조정)
optimizer = optim.SGD([W, b], lr=0.5)

"""모델 학습"""
nb_epochs = 1000000 # 원하는만큼 경사 하강법을 반복

for epoch in range(nb_epochs + 1):

    #직선의 방정식 선언
    #hypothesis = x_train * W + b
    # 행렬 곱셈으로 가설 계산
    hypothesis = x_train @ W + b  # (500, 17) @ (17, 1) -> (500, 1)

    #비용 함수 선언 : 선형 회귀의 비용 함수에 해당되는 평균 제곱 오차(cost)를 선언
    cost = torch.mean((hypothesis - y_train) ** 2)

    # gradient를 0으로 초기화
    optimizer.zero_grad() 
    # 비용 함수를 미분하여 gradient 계산
    cost.backward() 
    # W와 b를 업데이트
    optimizer.step() 

    # 100번마다 로그 출력
    if epoch % 100 == 0:
        #print('Epoch {:4d}/{} W: {:.3f}, b: {:.3f} Cost: {:.6f}'.format(epoch, nb_epochs, W.item(), b.item(), cost.item()))
        print('Epoch {:4d}/{} W: {}, b: {:.3f} Cost: {:.6f}'.format(epoch, nb_epochs, W.view(-1).tolist(), b.item(), cost.item()))

#### cost 미쳣누 -> Cost: 95,896,354,816.000000 //95,894,978,560

""" 오류 발생!!!
  File "d:\Kim goeun\고진형 교수님\price_sale_prediction.py", line 62, in <module>
    cost = torch.mean((hypothesis - y_train) ** 2)
                       ~~~~~~~~~~~^~~~~~~~~
RuntimeError: The size of tensor a (17) must match the size of tensor b (400) at non-singleton dimension 1


1.hypothesis와 y_train의 텐서 크기가 일치하지 않아서 발생한 문제
2.x_train의 크기가 (400, 17)이고 W의 크기가 (1,)이기 때문에 x_train * W의 결과가 달라짐
3.선형 회귀 모델에서 행렬 곱셈을 이용해 예측값을 계산하도록 수정해야 해결가능
4.W를 (17, 1) 크기의 가중치 행렬로 정의하고, x_train과 행렬 곱셈을 수행해 y_train과 크기를 맞춰줘야 한다
"""


"""2번째 오류 발생
Traceback (most recent call last):
  File "d:\Kim goeun\고진형 교수님\price_sale_prediction.py", line 60, in <module>
    hypothesis = x_train * W + b
                 ~~~~~~~~^~~

1.x_train * W로 곱셈을 시도하면서 원소별 곱셈이 발생했기 때문에 오류 발생
2.선형 회귀 모델에서는 행렬 곱셈이 필요하므로 torch.matmul()을 사용해야 한다
3.* 연산자를 @ 연산자로 바꾸어 행렬 곱셈으로 계산을 진행하도록 수정
"""


"""3번째오류 발생
Traceback (most recent call last):
  File "d:\Kim goeun\고진형 교수님\price_sale_prediction.py", line 76, in <module>
    print('Epoch {:4d}/{} W: {:.3f}, b: {:.3f} Cost: {:.6f}'.format(epoch, nb_epochs, W.item(), b.item(), cost.item()))
                                                                                      ^^^^^^^^

1.W가 (17, 1) 크기의 텐서이기 때문에 .item() 메서드를 사용하여 단일 값을 추출할 수 없다. 
2. .item()은 스칼라 값(하나의 값)을 반환하는 텐서에서만 사용 가능
3.W의 값 전체를 출력하려면 W.view(-1).tolist()로 출력하거나, 각 요소의 값을 개별적으로 접근해야 한다                                                                                    
"""