from selenium import webdriver

# ChromeDriver가 설치된 디렉터리 경로를 직접 지정
chrome_driver_path = 'c:/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"executable_path={chrome_driver_path}")

# webdriver 초기화
driver = webdriver.Chrome(options=chrome_options)