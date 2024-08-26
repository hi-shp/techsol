import os
import time
import pyautogui
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 아이디와 비밀번호 가져오기
user_id = os.getenv('MY_ID')
user_password = os.getenv('MY_PASSWORD')

# 크롬 웹드라이버 경로 설정
driver_path = 'C:\\together-main\\Source\\chromedriver-win64\\chromedriver.exe'

# 크롬 서비스 객체 생성
service = Service(driver_path)

# 웹드라이버 설정
options = webdriver.ChromeOptions()

def extract_text_from_image(image_path):
    mathpix_driver = webdriver.Chrome(service=service, options=options)

    try:
        # Mathpix 웹 페이지 열기
        mathpix_driver.get('https://snip.mathpix.com/home')

        # ID 입력창 찾기 및 입력
        id_input = WebDriverWait(mathpix_driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )
        id_input.clear()
        id_input.send_keys(user_id)

        # 비밀번호 입력창 찾기 및 입력
        password_input = WebDriverWait(mathpix_driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )
        password_input.clear()
        password_input.send_keys(user_password)

        # 로그인 버튼 클릭
        login_button = WebDriverWait(mathpix_driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'submit-button'))
        )
        login_button.click()

        # 로그인 후 특정 요소가 나타날 때까지 대기하고 클릭
        action_box = WebDriverWait(mathpix_driver, 20).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="root"]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/div/div/div/div[1]/div/div[3]/div[2]'))
        )
        action_box.click()

        # 'Create Snip by Image Upload' 요소가 나타날 때까지 대기하고 클릭
        create_snip = WebDriverWait(mathpix_driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//li[@tabindex="0" and @role="menuitem"]//span[text()="Create Snip by Image Upload"]'))
        )
        create_snip.click()

        # 파일 탐색기 제어 (파일 경로 입력 및 열기 버튼 클릭)
        time.sleep(2)
        pyautogui.write(image_path)
        pyautogui.press('enter')

        # 지정된 요소가 나타날 때까지 대기
        target_element = WebDriverWait(mathpix_driver, 20).until(
            EC.presence_of_element_located((By.XPATH,
                                            '//div[@class="text-sm leading-6 py-1.25"]//div[@class="flex text-secondary"]//div[@class="overflow-hidden text-ellipsis whitespace-nowrap"]'))
        )
        extracted_text = target_element.text

        return extracted_text

    finally:
        mathpix_driver.quit()
