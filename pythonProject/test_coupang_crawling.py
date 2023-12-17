from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

# 함수 정보 : list 페이지 크롤링 후 필요한 정보 추출
## 여기서는 상세 페이지로 이동하는 case로 작성함.
### 상세 페이지 이동 url을 크롤링으로 얻은 뒤, 각 페이지 별 crawling 추가 예정
def crawl_website(url):
    try:
        # ChromeDriver 경로 설정
        chrome_driver_path = 'c:/chromedriver'

        # webdriver 초기화
        options = webdriver.ChromeOptions()
        options.add_argument(f"executable_path={chrome_driver_path}")

        driver = webdriver.Chrome(options=options)

        print("Crawling " + url)
        # 웹페이지에 GET 요청 보내기
        driver.get(url)

        # 웹 페이지 로딩을 위해 충분히 대기 (이 부분이 필요할 수 있습니다.)
        driver.implicitly_wait(10)

        # 페이지에서 원하는 요소 찾기  얼음 정수기로 정함 2번째에 있음
        elements = driver.find_elements(By.XPATH, '//div[@class="dcBestProductWrap"]')[1]
        href_links = elements.find_elements(By.TAG_NAME, 'li')
        print(len(href_links))
        detail_url_list = []
        for link in href_links:
            path = "https://www.skmagic-shop.kr/"
            sub_path = link.get_attribute('onclick').replace("location.href=", "").replace("\'", "").replace("'", "")
            print(path+sub_path)
            detail_url_list.append(path+sub_path)
        return detail_url_list

    except Exception as e:
        print('error : {}'.format(e))
        raise e
    finally:
        # 크롬 브라우저 닫기
        driver.quit()
def wait_for_condition(driver):
    return driver.execute_script("return document.readyState === 'complete';")

# 제품 상세 페이지 크롤링
## 제품 상세 페이지 내 평가 내용 크롤링
### 간단하게
def crawl_website_detail(url):
    try:
        # ChromeDriver 경로 설정
        chrome_driver_path = 'c:/chromedriver'

        # webdriver 초기화
        options = webdriver.ChromeOptions()
        options.add_argument(f"executable_path={chrome_driver_path}")

        driver = webdriver.Chrome(options=options)

        print("Crawling " + url)
        # 웹페이지에 GET 요청 보내기
        driver.get(url)

        # 웹 페이지 로딩을 위해 충분히 대기 (이 부분이 필요할 수 있습니다.)
        WebDriverWait(driver,10).until(wait_for_condition)

        # 페이지에서 원하는 요소 찾기

        ## 공통사항 추출
        di_container = driver.find_element(By.XPATH, '//article[@id="diContainer"]')
        di_content = di_container.find_element(By.ID, 'diContent')
        di_con = di_content.find_element(By.ID, 'diCon')
        dc_product_detail_wrap = di_con.find_element(By.XPATH, '//div[@class="dcProductDetailWrap"]')

        ## 제품 명 조회
        dc_product_info_wrap_clear_fix = dc_product_detail_wrap.find_element(By.XPATH, '//div[contains(@class, "dcProductInfoWrap") and contains(@class, "clearfix")]')
        dc_info_wrap = dc_product_info_wrap_clear_fix.find_element(By.XPATH, '//div[@class = "dcInfoWrap"]')
        dc_pd_name= dc_info_wrap.find_element(By.XPATH, '//div[@class="dcPDNameWrap"]/h3[@class="dcH3Title"]').text


        ## 리뷰 영역 조회
        dc_customer_review_wrap = dc_product_detail_wrap.find_element(By.XPATH, '//div[@class="dcCustomerReviewWrap"]')
        dc_review_list_wrap = dc_customer_review_wrap.find_element(By.XPATH, '//div[@class="dcReviewListWrap"]')
        dc_review_list = dc_review_list_wrap.find_element(By.TAG_NAME, 'ul')
        review_list = dc_review_list.find_elements(By.TAG_NAME, 'li')
        detail_comment_list = []
        for review in review_list:
            user = review.find_element(By.TAG_NAME, 'p').text
            lower_div = review.find_element(By.XPATH, '//div[@class="dcReviewCon"]')
            dc_star_score = lower_div.find_element(By.XPATH, '//p[@class="dcStarScore"]')
            star_score = dc_star_score.find_element(By.TAG_NAME, 'span').get_attribute('class')[-1]
            dc_review_content = lower_div.find_element(By.XPATH, '//div[@class="dcReviewCon"]/div/p[@class="dcText"]').text
            print(dc_review_content)
            review_data = {"사용자": user,"별점": star_score, "내용": dc_review_content}
            detail_comment_list.append(review_data)

        print(len(detail_comment_list))
        df = pd.DataFrame({"제품" : dc_pd_name, "리뷰" : detail_comment_list})
        print("=========================end=================================")
        return df
        # 상세 페이지 crawling start

    except Exception as e:
        print('error : {}'.format(e))
        raise e
    finally:
        # 크롬 브라우저 닫기
        driver.quit()

if __name__ == "__main__":
    print("start crawling website")
    # 크롤링할 홈페이지 URL
    target_url = "https://www.skmagic-shop.kr/user/best_product"

    # 상세 url 구하기
    ## 크롤링 함수 호출
    detail_url_list = crawl_website(target_url)

    # 상세 페이지 내 댓글 가져오기
    ## 테스트 용으로 로컬에서 작업했기 때문에 10건만 가져올 예정
    ### 댓글 또한 list 형식으로 뽑아온다.
    #### 댓글 리스트 들의 묶음이므로 리스트 안의 리스트 구조로 작성
    ##### 단 댓글 리스트는 dataframe형식으로 내려줄 예정
    ###### list[list[DataFrame{}]]
    total_comment_list = []
    for detail_url in detail_url_list:
        df = crawl_website_detail(detail_url)
        # dataFrame으로 변환
        total_comment_list.append(df)
    print(total_comment_list)

