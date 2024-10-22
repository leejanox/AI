import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

#엑셀파일 읽어서 상품번호를 가져오기
df = pd.read_excel("economy.xlsx")

pd_ids= df["상품번호"].tolist()

# 웹드라이버 설정 (크롬 드라이버 경로 지정)
driver = webdriver.Chrome()



# CSV 파일 생성
with open('Info.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 컬럼명 작성
    writer.writerow(["Name", "Author", "Publisher", "Rating", "Review Count", "Sale Rank", "Original Price", "Sale Price"])

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
            
            try:
                #책 제목
                name = driver.find_element(By.CLASS_NAME, 'gd_name').text
            except:
                name = "N/A"
            try:

                #저자
                author = driver.find_element(By.CLASS_NAME,'gd_auth').text
            except:
                author = "N/A"
            try:
                #출판사
                publisher = driver.find_element(By.CLASS_NAME, 'gd_pub').text
            except:
                publisher = "N/A"
            try:
                #평점 점수
                rating = driver.find_element(By.CLASS_NAME, 'yes_b').text
            except:
                rating = "N/A"
            try:
                #리뷰 개수
                reviewCount = driver.find_element(By.CLASS_NAME,"txC_blue").text
            except:
                reviewCount="N/A"
            try:
                #판매지수
                saleRating = driver.find_element(By.CLASS_NAME,"gd_sellNum").text
            except:
                saleRating = "N/A"
            try:
                #정가
                originalPrice = driver.find_element(By.CLASS_NAME,"yes_m").text
                #/html/body/div/div[4]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td/span/em
            except:
                originalPrice = "N/A"
            try:
                #판매가
                salePrice = driver.find_element(By.CLASS_NAME, 'nor_price').text
                #/html/body/div/div[4]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[2]/td/span/em
            except:
                salePrice = "N/A"
            
            #만약 데이터가 정상적으로 들어왔으면 data_found = True
            if name != "N/A" or author != "N/A" or publisher != "N/A" or rating != "N/A" or reviewCount !="N/A" or saleRating != "N/A" or originalPrice != "N/A" or salePrice != "N/A":
                data_found=True
            
            if data_found:
                #데이터가 정상적으로 있으면 CSV 파일에 기록
                writer.writerow([name, author, publisher, rating, reviewCount, saleRating, originalPrice, salePrice])
                print("저장완료")
                break
            else:
                print(f"상품번호 {pd_id} 페이지에 데이터가 없습니다.")
                break
#웹드라이버 종료
driver.quit()