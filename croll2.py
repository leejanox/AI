#croll 좀 더 깔끔하게
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


#엑셀파일 읽어서 상품번호를 가져오기
df = pd.read_excel("종합베스트.xlsx")

pd_ids= df["상품번호"].tolist()

# 웹드라이버 설정 (크롬 드라이버 경로 지정)
driver = webdriver.Chrome()
    
# CSV 파일 생성
with open('InfoAll.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 컬럼명 작성
    writer.writerow(["Name", "Author", "Publisher", "Rating", "Review Count", "Sale Rank", "Original Price", "Sale Price","category"])

    for pd_id in pd_ids:
        #웹사이트 접속 url 바꾸기
        url= f"https://www.yes24.com/Product/Goods/{pd_id}"
        # 웹사이트 접속
        driver.get(url)
        time.sleep(5)  # 페이지 로딩 대기

        # 다음 페이지가 없을 때까지 크롤링 반복
        while True:
            #데이터가 있는지 없는지 확인
            data_found = False
            
            datas = []
            
            #찾을 데이터 classname
            classnames = ["gd_name",'gd_auth','gd_pub','yes_b','txC_blue',"gd_sellNum","yes_m","nor_price"]

            for i in range(len(classnames)):
                try:
                    data = driver.find_element(By.CLASS_NAME,classnames[i]).text
                    #만약 데이터가 찾은 데이터가 있으면 data_found = True
                    datas.append(data)
                    data_found = True
                    print(f'{i} : {data}')
                except:
                    datas.append("N/A")

            #classname으로 안긁힘
            try:
                dataXpath = driver.find_element(By.XPATH,"/html/body/div/div[3]/div/div[3]/a").text
                datas.append(dataXpath)
                data_found=True
                print(dataXpath)
            except:
                datas.append("N/A")

            if data_found == True:
                #데이터가 정상적으로 있으면 CSV 파일에 기록
                writer.writerow(datas)
                print("저장완료")
                break
            else:
                print(f"상품번호 {pd_id} 페이지에 데이터가 없습니다.")
                break
#웹드라이버 종료
driver.quit()
