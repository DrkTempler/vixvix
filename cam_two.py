from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import os
import logging
import time
import base64
import sys
import io

driver = None  # 전역 선언

def init_driver():
    global driver
    driver = setup_driver()

# 터미널에 로그출력
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ip
# def ip():
#     ip = "http://" + input("ip주소를 입력하세요").strip()
#     return ip

# 웹드라이버 기본값. 화면 보고싶으면 주석처리를 변경하세요
def setup_driver():
    options = Options()
    options.add_experimental_option("detach", True)
    # 헤드리스
    # options.add_argument("--headless") 
    # options.add_argument("--window-size=1920,1080") 
    # options.add_argument("--disable-gpu")  
    # options.add_argument("--disable-dev-shm-usage")
    # 창띄우기
    options.add_argument("--window-size=1920,1080")
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(3)
    return driver

# 캡처
def capture_picture(test_name):
    # 결과물 디렉토리(os 사용하여 없으면 폴더 만들기)
    directory = "D://Auto_test_result"
    os.makedirs(directory, exist_ok=True)
    screenshot_name = os.path.join(directory, f"{test_name}.png")
    # 뷰포트 너머까지 캡쳐하기
    mt = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
    size = mt["contentSize"]
    screenshot_config = {'captureBeyondViewport' : True,
                         'fromSurface' : True,
        "clip": {
            "x" : 0,
            "y" : 0,
            "width" : size["width"],
            "height" : size["height"],
            "scale" : 1
        }
    }
    screenshot = driver.execute_cdp_cmd("Page.captureScreenshot", screenshot_config)
    # Base64 디코딩
    with open(screenshot_name, "wb") as file:
        file.write(base64.b64decode(screenshot["data"]))
    logger.info(f"{test_name} capture complete")

def logout():
    element = driver.find_element(By.XPATH, '//*[@id="sidebar-shortcuts-large"]/a[4]')
    element.click()
    time.sleep(3)
    capture_picture("logout")

def logout_after_login(username, password):
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
    time.sleep(3)
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '#login_submit').click()
    time.sleep(3)

def logout_after_login_image(username, password):
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
    time.sleep(3)
    element = driver.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
    element.click()
    driver.find_element(By.CSS_SELECTOR, '#login_submit').click()
    time.sleep(3)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/a')
    element.click()
    time.sleep(1)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/ul/li[4]/a')
    element.click()
    time.sleep(5)

### 라이브 페이지 UI 자동화 ###
# 자동로그인
def login_auto(ip, username, password):
    driver.get(ip)
    # driver.get('http://' + input('ip 주소를 입력하세요'))
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '#login_submit').click()
    time.sleep(3)

# 메인화면이 띄워져있는 시나리오에서 id, pw만 입력
def login_short_image(username, password):
    time.sleep(5)
    try:
        driver.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
        time.sleep(3)
        element = driver.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
        element.click()
        driver.find_element(By.CSS_SELECTOR, '#login_submit').click()
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/a')
    element.click()
    time.sleep(1)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/ul/li[4]/a')
    element.click()
    time.sleep(5)
logger.info('option menu login complete')
time.sleep(5)

# 자동설정로그인
def login_auto_op(ip, username, password):
    driver.get(ip)
    # driver.get('http://' + input('ip 주소를 입력하세요'))
    time.sleep(5)
    try:
        driver.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
        time.sleep(3)
        element = driver.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
        element.click()
        driver.find_element(By.CSS_SELECTOR, '#login_submit').click()
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(5)
    logger.info('option menu login complete')
    time.sleep(5)
    capture_picture("vixcam_information")
    time.sleep(3)

# 초기화 후 pw 지정
# 초기화 후 admin1357로 강제 지정되며 이 블록은 쓸 수 없게 되었다
# 어쩌겠나 파인트리에서 수정하는게 공유되지 않는것을..
# 꼬우면 이직해~~~^^
# def reset_after_login(driver):
    # driver.refresh()
    time.sleep(5)
    # time.sleep(5)
    # element = driver.find_element(By.CSS_SELECTOR, '#edit-pwd-container > div:nth-child(2) > div > input')
    # element.send_keys("pass0001!")
    # time.sleep(3)
    # element = driver.find_element(By.CSS_SELECTOR, '#edit-pwd-container > div:nth-child(4) > div > input')
    # element.send_keys("pass0001!")
    # time.sleep(3)
    # capture_picture("초기화 후 pw 지정")
    # driver.find_element(By.CSS_SELECTOR, 'body > div > div > div > div.modal-footer > button').send_keys(Keys.ENTER)
    # time.sleep(3)
    # driver.find_element(By.CLASS_NAME, 'confirm').send_keys(Keys.ENTER)

# admin1357 강제지정으로 로그인 후 관리자 패스워드 변경
def reset_fix(username, password):
    driver.refresh()
    time.sleep(5)
    time.sleep(5)
    element = driver.find_element(By.CSS_SELECTOR, '#user')
    element.click()
    element.send_keys(username)
    time.sleep(3)
    element = driver.find_element(By.CSS_SELECTOR, '#pwd')
    element.click()
    element.send_keys('admin1357')
    time.sleep(3)
    element = driver.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
    element.click()
    element = driver.find_element(By.CSS_SELECTOR, '#login_submit')
    element.click()
    time.sleep(3)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/a')
    element.click()
    time.sleep(2)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/ul/li[1]/a')
    element.click()
    time.sleep(3)
    element = driver.find_element(By.CSS_SELECTOR, '#admin')
    element.click()
    time.sleep(1)
    element = driver.find_element(By.CSS_SELECTOR, '#btnEditUser')
    element.click()
    time.sleep(2)
    element = driver.find_element(By.CSS_SELECTOR, '#edit_user_list > div:nth-child(2) > div > input')
    element.click()
    element.send_keys(password)
    element = driver.find_element(By.CSS_SELECTOR, '#edit_user_list > div:nth-child(4) > div > input')
    element.click()
    element.send_keys(password)
    time.sleep(2)
    element = driver.find_element(By.CSS_SELECTOR, '#editUserModal > div > div > div.modal-footer > button.btn.btn-primary.btn-sm')
    element.click()
    time.sleep(2)
    element = driver.find_element(By.CSS_SELECTOR, 'body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button.confirm')
    element.click()

# 로그인
def login(ip, username, password):
    driver.get(ip)
    # driver.get('http://' + input('ip주소를 입력하세요'))
    time.sleep(5)
    try:
        element = driver.find_element(By.CSS_SELECTOR, '#user')
        element.click()
        element.send_keys(username)
        time.sleep(3)
        element = driver.find_element(By.CSS_SELECTOR, '#pwd')
        element.click()
        element.send_keys(password)
        time.sleep(3)
        element = driver.find_element(By.CSS_SELECTOR, '#login_submit')
        element.click()
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(5)
    logger.info('login complete')

# 로그인 실패 시나리오
def login_fail_test(ip, username):
    driver.get(ip)
    # driver.get('http://' + input('ip주소를 입력하세요'))
    time.sleep(5)
    # 최대 시도 스펙 바뀌면 바꾸세염
    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        print(f"{attempt}회 로그인 시도중")
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, '#pwd').send_keys("KILLYOU15%@")
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, '#login_submit').click()
        time.sleep(3)
        try:
            element = driver.find_element(By.ID, "lockdown_menu")
            if element.is_displayed():
                capture_picture("login_fail_test")
                print("Login Fail Test Pass!")
        except NoSuchElementException:
                print("WHAT THE FUCK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        driver.find_element(By.CSS_SELECTOR, '#user').clear()
        driver.find_element(By.CSS_SELECTOR, '#pwd').clear()

###라이브 페이지 자동화###
# 줌인&아웃 시나리오
def zoom():
    # 사이드바 출현여부
    element = driver.find_element(By.CSS_SELECTOR, '#menu_button')
    element.click()
    element.click()
    wait = WebDriverWait(driver, 10)
    sidebar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sidebar"]')))
    style = driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('display');", sidebar)
    time.sleep(5)
    if style == "block":
        print("Sidebar displaying now")
    else: 
        element = driver.find_element(By.CSS_SELECTOR, '#menu_button')
        element.click()
    # ptz 메뉴 열기
    time.sleep(5)
    ptzmenu = driver.find_element(By.CSS_SELECTOR, '#ptz_menu')
    if 'accordion-toggle' in ptzmenu.get_attribute("class"):
        print("Ptz Menu displaying on Sidebar now")
    else:
        ptzmenu.click()
    time.sleep(3)
    for i in range(80):
        element = driver.find_element(By.XPATH, '//*[@id="ptz_panel"]/div/div[1]/div[1]/div[1]/button')
        element.click()
        time.sleep(0.5)
    capture_picture("zoom_in")
    time.sleep(3)
    for i in range(80):
        element = driver.find_element(By.XPATH, '//*[@id="ptz_panel"]/div/div[1]/div[1]/div[3]/button')
        element.click()
        time.sleep(0.5)
    capture_picture("zoom_out")

# 다이렉트줌 시나리오
def directzoom():
    # 사이드바 출현여부
    element = driver.find_element(By.CSS_SELECTOR, '#menu_button')
    element.click()
    element.click()
    wait = WebDriverWait(driver, 10)
    sidebar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sidebar"]')))
    style = driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('display');", sidebar)
    time.sleep(5)
    if style == "block":
        print("Sidebar displaying now")
    else: 
        element = driver.find_element(By.CSS_SELECTOR, '#menu_button')
        element.click()
    # ptz 메뉴 열기
    time.sleep(5)
    ptzmenu = driver.find_element(By.CSS_SELECTOR, '#ptz_menu')
    if 'accordion-toggle' in ptzmenu.get_attribute("class"):
        print("Ptz Menu displaying on Sidebar now")
    else:
        ptzmenu.click()
    element = driver.find_element(By.XPATH, '//*[@id="ptz_panel"]/div/div[1]/div[7]/div/span/span[1]/span[6]')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    actions = ActionChains(driver)
    actions.click_and_hold(element).move_by_offset(100, 0).release().perform()
    time.sleep(3)
    capture_picture("directzoom_in")
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="ptz_panel"]/div/div[1]/div[7]/div/span/span[1]/span[6]')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    actions = ActionChains(driver)
    actions.click_and_hold(element).move_by_offset(-100, 0).release().perform()
    time.sleep(3)
    capture_picture("directzoom_out")

# 포커스 조작 시나리오
def focus():
    # 사이드바 출현여부
    element = driver.find_element(By.CSS_SELECTOR, '#menu_button')
    element.click()
    element.click()    
    wait = WebDriverWait(driver, 10)
    sidebar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sidebar"]')))
    style = driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('display');", sidebar)
    time.sleep(5)
    if style == "block":
        print("Sidebar displaying now")
    else: 
        element = driver.find_element(By.CSS_SELECTOR, '#menu_button')
        element.click()
    # ptz 메뉴 열기
    time.sleep(10)
    ptzmenu = driver.find_element(By.CSS_SELECTOR, '#colMenu5')
    if 'true' in ptzmenu.get_attribute("aria-expanded"):
        print("Ptz Menu displaying on Sidebar now")
    else:
        element = driver.find_element(By.CSS_SELECTOR, '#ptz_menu')
        element.click()
        print("Call Ptz Menu")
    # 포커스 조작
    time.sleep(5)
    for i in range(80):
        element = driver.find_element(By.XPATH, '//*[@id="ptz_panel"]/div/div[1]/div[3]/div[1]/button')
        element.click()
        time.sleep(0.5)
    capture_picture("focus_meele")
    time.sleep(3)
    element = driver.find_element(By.XPATH, '//*[@id="ptz_panel"]/div/div[1]/div[5]/div/button')
    element.click()
    time.sleep(6)
    capture_picture("focus_Auto")
    for i in range(80):
        element = driver.find_element(By.XPATH, '//*[@id="ptz_panel"]/div/div[1]/div[3]/div[3]/button')
        element.click()
        time.sleep(0.5)
    capture_picture("focus_far")

# 비디오 스트림 순회
def livestream():
    # 사이드바 출현여부
    element = driver.find_element(By.CSS_SELECTOR, '#menu_button')
    element.click()
    element.click()
    wait = WebDriverWait(driver, 10)
    sidebar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sidebar"]')))
    style = driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('display');", sidebar)
    time.sleep(5)
    if style == "block":
        print("Sidebar displaying now")
    else: 
        element = driver.find_element(By.CSS_SELECTOR, '#menu_button')
        element.click()
    # 라이브제어 메뉴 열기
    time.sleep(5)
    livecontrol = driver.find_element(By.CSS_SELECTOR, '#player_control_pannel > div.panel-heading > h4 > a')
    if 'accordion-toggle collapsed' in livecontrol.get_attribute("class"):
        livecontrol.click()
        print("Call livecontrol")
    else:
        print("livecontrol displaying Now")
    time.sleep(3)
    element = driver.find_element(By.XPATH, '//*[@id="stream2"]/label/div')
    element.click()
    time.sleep(5)
    capture_picture("Stream2")
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="stream3"]/label/div')
    element.click()
    time.sleep(5)
    capture_picture("Stream3")
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="stream4"]/label/div')
    element.click()
    time.sleep(5)
    capture_picture("Stream4")
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="stream1"]/label/div')
    element.click()
    time.sleep(5)
    capture_picture("Stream1")
    time.sleep(5)
### 라이브 페이지 UI 자동화 요기까지 ###

def no_alert():
    try:
        alert_button = driver.find_element(By.XPATH, "//div[contains(@class, 'sweet-alert') and contains(@class, 'visible')]//button[contains(@class, 'confirm')]")
        alert_button.click()
        print("F*** YOU ALERT")

    except NoSuchElementException:
        print("gogo next")

### 설정 > 비디오 & 이미지 > 이미지 자동화 시작 ###
# 이미지 자동 진입
def login_option_image(ip, username, password):
    global driver
    driver.get(ip)
    # driver.get('http://' + input('ip 주소를 입력하세요'))
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
    time.sleep(3)
    element = driver.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
    element.click()
    element = driver.find_element(By.CSS_SELECTOR, '#login_submit')
    element.click()
    time.sleep(3)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/a')
    element.click()
    time.sleep(1)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/ul/li[4]/a')
    element.click()
    time.sleep(5)
    logger.info('Option > Image now')
    time.sleep(5)

# 밝기 최소값 & 최대값 
def bright():
    # 밝기 최소값
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[1]/select'))
    select.select_by_value('1')
    time.sleep(1)
    # 확인 버튼
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(5)
    capture_picture("bright_low")
    time.sleep(5)
    # 밝기 최대값
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[1]/select'))
    select.select_by_value('100')
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(5)
    driver.refresh()
    time.sleep(5)
    capture_picture("bright_high")
    # 밝기 정상화
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[1]/select'))
    select.select_by_value('50')
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(5)
    driver.refresh()
    time.sleep(5)
    driver.refresh()
    time.sleep(5)
    capture_picture("bright_normal")
    time.sleep(5)

# 포화도 최소값 & 최대값
def saturation():
    # 포화도 최소값
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[2]/select'))
    select.select_by_value('1')
    time.sleep(1)
    # 확인 버튼
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(5)
    capture_picture("saturation_low")
    time.sleep(5)
    # 포화도 최대값
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[2]/select'))
    select.select_by_value('100')
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(5)
    capture_picture("saturation_high")
    time.sleep(5)
    # 포화도 정상화
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[2]/select'))
    select.select_by_value('65')
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(5)
    capture_picture("saturation_normal")
    time.sleep(5)

# 명암비 최소값 & 최대값
def contrast():
    # 명암비 최소값
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[3]/select'))
    select.select_by_value('1')
    time.sleep(1)
    # 확인 버튼
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(5)
    capture_picture("contrast_low")
    time.sleep(5)
    # 명암비 최대값
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[3]/select'))
    select.select_by_value('100')
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(5)
    capture_picture("contrast_high")
    time.sleep(5)
    # 명암비 정상화
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[3]/select'))
    select.select_by_value('55')
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(5)
    capture_picture("contrast_normal")
    time.sleep(5)

# 색조 최소값 & 최대값
def tone():
    # 색조 최소값
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[1]/select'))
    select.select_by_value('1')
    time.sleep(1)
    # 확인 버튼
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(5)
    capture_picture("tone_low")
    time.sleep(5)
    # 색조 최대값
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[1]/select'))
    select.select_by_value('30')
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(5)
    capture_picture("tone_high")
    time.sleep(5)
    # 색조 정상화
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[1]/select'))
    select.select_by_value('17')
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(5)
    capture_picture("tone_normal")
    time.sleep(5)

# 선명도 최소값 & 최대값
def sharpness():
    # 선명도 최소값
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[2]/select'))
    select.select_by_value('1')
    time.sleep(1)
    # 확인 버튼
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(5)
    capture_picture("sharpness_low")
    time.sleep(5)
    # 선명도 최대값
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[2]/select'))
    select.select_by_value('12')
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(5)
    capture_picture("sharpness_high")
    time.sleep(5)
    # 선명도 정상화
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[2]/select'))
    select.select_by_value('7')
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(3)
    driver.refresh()
    time.sleep(5)
    capture_picture("sharpness_normal")
    time.sleep(5)

# 반전모드 사용
def reversal():
    element = driver.find_element(By.XPATH, '//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[4]/label/div/ins')
    element.click()
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    driver.refresh()
    time.sleep(5)
    capture_picture("reversal_1")
    element = driver.find_element(By.XPATH, '//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[4]/label/div/ins')
    element.click()
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    element = driver.find_element(By.XPATH, '//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[5]/label/div/ins')
    element.click()
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    driver.refresh()
    time.sleep(5)
    capture_picture("reversal_2")
    element = driver.find_element(By.XPATH, '//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[4]/label/div/ins')
    element.click()
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(20)
    driver.refresh()
    time.sleep(5)
    capture_picture("reversal_all")
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[4]/label/div/ins')
    element.click()
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[5]/label/div/ins')
    element.click()
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(20)
    driver.refresh()
    time.sleep(5)
    capture_picture("reversal_disable")
    time.sleep(5)

# OSD 사용
def osd():
    # 탭 이동
    element = driver.find_element(By.XPATH, '//*[@id="tab-hdr-osd"]/a')
    element.click()
    # OSD 설정
    element = driver.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[1]/div/div[2]/div/div[1]/div/label/div/ins')
    element.click()
    element = driver.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[1]/div/div[2]/div/div[2]/div/label/div/ins')
    element.click()
    element = driver.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[1]/div/div[2]/div/div[3]/div/label/div/ins')
    element.click()
    element = driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]')
    element.click()
    time.sleep(5)
    capture_picture("OSD activate")
    time.sleep(5)
    # OSD 텍스트 변경
    element = driver.find_element(By.XPATH, '//*[@id="real_osd_text_content"]')
    element.clear()
    element.send_keys("Luvyou")
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(5)
    capture_picture("OSD Text")
    time.sleep(5)
    # OSD 누를때 / 항상 변경
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(3) > select'))
    select.select_by_value('always')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(5)
    capture_picture("OSD always")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(3) > select'))
    select.select_by_value('onpush')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(5)
    capture_picture("OSD onpush")
    # OSD 색상 변경
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
    select.select_by_value('White')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(5)
    capture_picture("OSD_White")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
    select.select_by_value('Black')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(5)
    capture_picture("OSD_Black")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
    select.select_by_value('Yellow')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(5)
    capture_picture("OSD_Yellow")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
    select.select_by_value('Cyan')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(5)
    capture_picture("OSD_Cyan")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
    select.select_by_value('Green')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(5)
    capture_picture("OSD_Green")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
    select.select_by_value('Magenta')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(5)
    capture_picture("OSD_Magenta")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
    select.select_by_value('Red')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(5)
    capture_picture("OSD_Red")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
    select.select_by_value('Blue')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(5)
    capture_picture("OSD_Blue")
    # OSD 슬라이더 최소값
    element = driver.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[2]/div/div[2]/div/div[1]/span[1]/span[6]')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    actions = ActionChains(driver)
    actions.click_and_hold(element).move_by_offset(-500, 0).release().perform()
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[2]/div/div[2]/div/div[2]/span[1]/span[6]')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    actions = ActionChains(driver)
    actions.click_and_hold(element).move_by_offset(-500, 0).release().perform()
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[2]/div/div[2]/div/div[3]/span[1]/span[6]')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    actions = ActionChains(driver)
    actions.click_and_hold(element).move_by_offset(-500, 0).release().perform()
    time.sleep(5)
    capture_picture("OSD slider low")
    element = driver.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[2]/div/div[2]/div/div[1]/span[1]/span[6]')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    actions = ActionChains(driver)
    actions.click_and_hold(element).move_by_offset(500, 0).release().perform()
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[2]/div/div[2]/div/div[2]/span[1]/span[6]')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    actions = ActionChains(driver)
    actions.click_and_hold(element).move_by_offset(500, 0).release().perform()
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[2]/div/div[2]/div/div[3]/span[1]/span[6]')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    actions = ActionChains(driver)
    actions.click_and_hold(element).move_by_offset(500, 0).release().perform()
    time.sleep(5)
    capture_picture("OSD slider high")

# 색온도
def faker():
    # 탭 이동
    element = driver.find_element(By.XPATH, '//*[@id="tab-hdr-awb"]/a')
    element.click()
    # 색온도 설정
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
    select.select_by_value('outdoor')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("rgb_outdoor")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
    select.select_by_value('bulb')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("rgb_bulb")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
    select.select_by_value('flourescent')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("rgb_flourescent")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
    select.select_by_value('clearsky')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("rgb_clearsky")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
    select.select_by_value('shade')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("rgb_shade")
    select.select_by_value('auto')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("rgb_auto")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
    select.select_by_value('manual')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("rgb_manual")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
    # 색온도 수동 값 MIN
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_wb_r_gain'))
    select.select_by_value('1')
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_wb_g_gain'))
    select.select_by_value('1')
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_wb_b_gain'))
    select.select_by_value('1')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("rgb_manual_MIN")
    # 색온도 수동 값 MAX
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_wb_r_gain'))
    select.select_by_value('255')
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_wb_g_gain'))
    select.select_by_value('255')
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_wb_b_gain'))
    select.select_by_value('255')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("rgb_manual_MAX")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
    select.select_by_value('auto')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)

# 세로모드
def vertical():
    # 탭 이동
    element = driver.find_element(By.XPATH, '//*[@id="tab-hdr-corridor"]/a')
    element.click()
    # 90도
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_corridor_enable'))
    select.select_by_value('1')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("vertical_90")
    # 270도
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_corridor_mode'))
    select.select_by_value('270degree')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("vertical_270")
    # 원상복귀
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_corridor_enable'))
    select.select_by_value('0')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("vertical_none")

# 광역역광보정
def wdr():
    # 탭 이동
    element = driver.find_element(By.XPATH, '//*[@id="tab-hdr-wdr"]/a')
    element.click()    
    # 광역역광보정 (WDR)
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_wdr_mode'))
    select.select_by_value('on')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("WDR_5level")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_wdr_level'))
    select.select_by_value('10')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("WDR_10level")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_wdr_level'))
    select.select_by_value('1')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("WDR_1level")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_wdr_mode'))
    select.select_by_value('off')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("WDR_off")
    # 디지털 광역역광보정(DWDR)
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_dwdr_mode'))
    select.select_by_value('on')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("DWDR_3level")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_dwdr_level'))
    select.select_by_value('16')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("DWDR_16level")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_dwdr_level'))
    select.select_by_value('1')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("DWDR_1level")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_dwdr_mode'))
    select.select_by_value('off')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("DWDR_off")    
    # 안개 보정 설정
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_defog_mode'))
    select.select_by_value('on')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("Defog_2level")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_defog_level'))
    select.select_by_value('3')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("Defog_3level")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_defog_level'))
    select.select_by_value('1')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("Defog_1level")
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_defog_mode'))
    select.select_by_value('off')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("Defog_off")   

# 역광보정
def blc():
    # 탭 이동
    element = driver.find_element(By.XPATH, '//*[@id="tab-hdr-blc"]')
    element.click()
    # 역광보정
    select = Select(driver.find_element(By.XPATH, '//*[@id="tab-blc"]/div/div[1]/div/div[2]/div/div[1]/select'))
    select.select_by_value('on')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("blc_5level")
    select = Select(driver.find_element(By.XPATH, '//*[@id="tab-blc"]/div/div[1]/div/div[2]/div/div[2]/select'))
    select.select_by_value('10')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("blc_10level")
    select = Select(driver.find_element(By.XPATH, '//*[@id="tab-blc"]/div/div[1]/div/div[2]/div/div[2]/select'))
    select.select_by_value('1')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("blc_1level")
    select = Select(driver.find_element(By.XPATH, '//*[@id="tab-blc"]/div/div[1]/div/div[2]/div/div[1]/select'))
    select.select_by_value('off')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("blc_off")
    # 하이라이트 보정 설정
    select = Select(driver.find_element(By.XPATH, '//*[@id="real_hlc_mode"]'))
    select.select_by_value('on')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("highlight_3level")
    select = Select(driver.find_element(By.XPATH, '//*[@id="tab-blc"]/div/div[2]/div/div[2]/div/div[2]/select'))
    select.select_by_value('5')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("highlight_10level")
    select = Select(driver.find_element(By.XPATH, '//*[@id="tab-blc"]/div/div[2]/div/div[2]/div/div[2]/select'))
    select.select_by_value('1')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("highlight_1level")
    select = Select(driver.find_element(By.XPATH, '//*[@id="real_hlc_mode"]'))
    select.select_by_value('off')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("highlight_off")

# 노이즈제거
def noise():
    # 탭 이동
    element = driver.find_element(By.XPATH, '//*[@id="tab-hdr-dnr"]')
    element.click()
    # 수준~
    select_elem = driver.find_element(By.CSS_SELECTOR, '#tab-dnr select')
    select = Select(select_elem)
    for option in select.options:
        value = option.get_attribute("value")
        disabled = option.get_attribute("disabled")

        if value == "on":
            if disabled:
                print("noise mode is now on")
            else:
                print("turn on noise mode")
                select.select_by_value("on")
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-dnr"]/div/div[2]/div/div[2]/select'))
    select.select_by_value('10')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("noise_10level")   
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-dnr"]/div/div[2]/div/div[2]/select'))
    select.select_by_value('1')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("noise_1level")    
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-dnr"]/div/div[2]/div/div[1]/select'))
    select.select_by_value('off')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("noise_off")   

# 렌즈보정
def compensation():
    # 탭 이동
    element = driver.find_element(By.XPATH, '//*[@id="tab-hdr-ldc"]')
    element.click() 
    # 켜~기
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-ldc"]/div/div[2]/div/div/select'))
    select.select_by_value('on')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("compensation_on") 
    # 끄~기
    select = Select(driver.find_element(By.XPATH,'//*[@id="tab-ldc"]/div/div[2]/div/div/select'))
    select.select_by_value('off')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    # 칩셋 성능이 그지같아서 저장하려면 클릭 여러번해야됌 아오 진짜 개빡쳐
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("compensation_off") 

# 주 & 야간
def day_night():
    time.sleep(10)
    # 탭 이동
    element = driver.find_element(By.XPATH, '//*[@id="tab-hdr-dnn"]/a')
    element.click() 
    # 야간
    select = Select(driver.find_element(By.XPATH,'//*[@id="real_dnn_mode"]'))
    select.select_by_value('night')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("night")     
    # 주간
    select = Select(driver.find_element(By.XPATH,'//*[@id="real_dnn_mode"]'))
    select.select_by_value('day')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("day")
    # 자동
    select = Select(driver.find_element(By.XPATH,'//*[@id="real_dnn_mode"]'))
    select.select_by_value('auto')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("auto")

# 디지털 줌(이미지단 뒤에 붙여서 쓰세여)
def digital_zoom():
    # 디지털 줌 메뉴로 이동
    driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/ul/li[6]/a').send_keys(Keys.ENTER)
    time.sleep(5)
    # 디지털 줌 체크박스 활성화
    driver.find_element(By.CSS_SELECTOR, '#setup-content > form > div:nth-child(2) > div > div > div > div:nth-child(1) > label > div > ins').click()
    # 디지털 줌 최대
    select = Select(driver.find_element(By.XPATH,'//*[@id="real_dz_level"]'))
    select.select_by_value('800')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("digital_zoom_8")
    # 디지털 줌 최소    
    select = Select(driver.find_element(By.XPATH,'//*[@id="real_dz_level"]'))
    select.select_by_value('100')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(10)
    capture_picture("digital_zoom_1")
    # 디지털 줌 끄기    
    driver.find_element(By.CSS_SELECTOR, '#setup-content > form > div:nth-child(2) > div > div > div > div:nth-child(1) > label > div > ins').click()
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    capture_picture(driver, 'digital_zoom_off')

# 신호 입력방식_PAL
def video_source_PAL():
    driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/ul/li[1]/a').send_keys(Keys.ENTER)
    time.sleep(5)
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_video_mode'))
    select.select_by_value('PAL')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(3)
    element = driver.find_element(By.CLASS_NAME, 'confirm')
    element.click()
    print("Change Source PAL")
    time.sleep(5)
    capture_picture("video_source_PAL")
    time.sleep(100)

# 신호 입력방식_NTSC
def video_source_NTSC():
    driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/ul/li[1]/a').send_keys(Keys.ENTER)
    time.sleep(5)
    select = Select(driver.find_element(By.CSS_SELECTOR,'#real_video_mode'))
    select.select_by_value('NTSC')
    driver.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
    time.sleep(3)
    element = driver.find_element(By.CLASS_NAME, 'confirm')
    element.click()
    print("Change Source NTSC")
    time.sleep(5)
    capture_picture("video_source_NTSC")
    time.sleep(100)

### 설정 > 비디오 & 이미지 > 이미지 자동화 끄읏 ###

### 설정 > 관리 > 재시작 / 초기화 / 공장초기화 ###
# 재시작
def restart():
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/a')
    element.click()
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/ul/li[5]/a')
    element.click()
    time.sleep(5)
    element = driver.find_element(By.NAME, 'btnRestart')
    element.click()
    time.sleep(3)
    element = driver.find_element(By.CLASS_NAME, 'confirm')
    element.click()
    print("get restart")
    time.sleep(5)
    capture_picture("restart")

# 초기화
def reset():
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/a')
    element.click()
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/ul/li[5]/a')
    element.click()
    time.sleep(5)
    element = driver.find_element(By.NAME, 'btnReset')
    element.click()
    time.sleep(3)
    element = driver.find_element(By.CLASS_NAME, 'confirm')
    element.click()
    print("reset Start")
    time.sleep(5)
    capture_picture("reset_start")
    time.sleep(60)
    capture_picture("reset_finish")

# 공장초기화
# *왠만하면 테스트 마지막에 배치하세요~~공장초기화 하고 재시작하기까지 시간이 많이 소요됩니다!!
def factory_reset():
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/a')
    element.click()
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/ul/li[5]/a')
    element.click()
    time.sleep(5)
    element = driver.find_element(By.NAME, 'btnDefault')
    element.click()
    time.sleep(3)
    element = driver.find_element(By.CLASS_NAME, 'confirm')
    element.click()
    print("factory reset On. bye bye bye")
    time.sleep(5)
    capture_picture("factory_reset_start")
# 팩토리 리셋 결과는 매뉴얼로 확인하세요~~~ ip가 DHCP나 192.168.0.100으로 변경됩니다~~~^^
### 설정 > 관리 > 재시작 / 초기화 / 공장초기화 끄~~읏 ###
### 설정 > 보안 > 사용자 계정 추가 및 삭제 ###
# 보안 메뉴 진입
def login_security(ip, username, password):
    global driver
    driver.get(ip)
    # driver.get('http://' + input('ip 주소를 입력하세요'))
    time.sleep(5)
    try:
        driver.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
        time.sleep(3)
        element = driver.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
        element.click()
        driver.find_element(By.CSS_SELECTOR, '#login_submit').click()
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(5)
    logger.info('Option Login Complete')
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/a')
    element.click()
    time.sleep(2)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/ul/li[1]/a')
    element.click()
    print("Option > Security Now")

# 사용자 추가
def user_add():
    for i in range(9):
        element = driver.find_element(By.ID, 'btnAddUser')
        element.click()
        time.sleep(2)
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#user_list > div:nth-child(1) > div > input')))
        element.click()
        element.send_keys(f"qaqaqa{i}")
        time.sleep(2)
        element = driver.find_element(By.CSS_SELECTOR, '#user_list > div:nth-child(2) > div > input')
        element.send_keys("pass0001!")
        time.sleep(2)
        element = driver.find_element(By.CSS_SELECTOR, '#user_list > div:nth-child(4) > div > input')
        element.send_keys("pass0001!")
        time.sleep(2)
        select = Select(driver.find_element(By.CSS_SELECTOR,'#user_list > div:nth-child(5) > div > select'))
        select.select_by_value('2')
        time.sleep(2)
        element = driver.find_element(By.CSS_SELECTOR, '#addUserModal > div > div > div.modal-footer > button.btn.btn-primary.btn-sm')
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        capture_picture(f"add_user_{i}")
        time.sleep(2)

# 사용자 삭제
def user_delete():
    for i in range(9):
        element = driver.find_element(By.ID, f"qaqaqa{i}")
        element.click()
        time.sleep(2)
        element = driver.find_element(By.ID, 'btnDeleteUser')
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        element = driver.find_element(By.CLASS_NAME, 'confirm')
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        capture_picture(f"delete_user_{i}")
        time.sleep(2)
### 설정 > 보안 > 사용자 완료완료
### 설정 > 날짜&시간 시작시작
#날짜&시간 메뉴 진입
def login_time(username, password):
    try:
        driver.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
        time.sleep(3)
        element = driver.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
        element.click()
        driver.find_element(By.CSS_SELECTOR, '#login_submit').click()
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(5)
    logger.info('Option Login Complete')
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/a')
    element.click()
    time.sleep(2)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/ul/li[2]/a')
    element.click()
    print("Option > Date&Time now")
    time.sleep(2)
    capture_picture("date_time_main")

#컴퓨터 시간과 동기화 
def local_time():
    element = driver.find_element(By.XPATH, '//*[@id="setup-content"]/div/form/div[1]/div[2]/div[2]/div/div[1]/label/div/ins')
    element.click()
    time.sleep(2)
    element = driver.find_element(By.ID, 'btnSaveSetup')
    element.click()
    time.sleep(2)
    capture_picture("local_time")
    time.sleep(20)

#NTP 서버와 동기화
def NTP_time():
    element = driver.find_element(By.XPATH, '//*[@id="setup-content"]/div/form/div[1]/div[2]/div[2]/div/div[5]/label/div/ins')
    element.click()
    time.sleep(2)
    element = driver.find_element(By.ID, 'btnSaveSetup')
    element.click()
    time.sleep(2)
    capture_picture("NTP_time")
    time.sleep(20)

#로그인 시간과 동기화
def login_same_time():
    element = driver.find_element(By.XPATH, '//*[@id="setup-content"]/div/form/div[1]/div[2]/div[2]/div/div[9]/div/label/div/ins')
    element.click()
    time.sleep(2)
    element = driver.find_element(By.ID, 'btnSaveSetup')
    element.click()
    time.sleep(2)
    capture_picture("login_same_time")
    time.sleep(20)

#써머타임
def summer_time():
    element = driver.find_element(By.XPATH, '//*[@id="setup-content"]/div/form/div[2]/div[1]/div[2]/div/div[2]/label/div/ins')
    element.click()
    time.sleep(2)
    element = driver.find_element(By.ID, 'btnSaveSetup')
    element.click()
    time.sleep(2)
    capture_picture("summer_time")
    time.sleep(20)

#년-월-일 12시간 포맷
def ymd_12():
    select = Select(driver.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(1) > select'))
    select.select_by_value('1')
    time.sleep(2)
    select = Select(driver.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(2) > select'))
    select.select_by_value('2')
    time.sleep(2)
    element = driver.find_element(By.ID, 'btnSaveSetup')
    element.click()
    time.sleep(20)
    capture_picture("ymd_12")

#년-월-일 24시간 포맷
def ymd_24():
    select = Select(driver.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(1) > select'))
    select.select_by_value('1')
    time.sleep(2)
    select = Select(driver.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(2) > select'))
    select.select_by_value('1')
    time.sleep(2)
    element = driver.find_element(By.ID, 'btnSaveSetup')
    element.click()
    time.sleep(20)
    capture_picture("ymd_24")

#월-일-년 24시간 포맷
def mdy_24():
    select = Select(driver.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(1) > select'))
    select.select_by_value('2')
    time.sleep(2)
    select = Select(driver.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(2) > select'))
    select.select_by_value('1')
    time.sleep(2)
    element = driver.find_element(By.ID, 'btnSaveSetup')
    element.click()
    time.sleep(20)
    capture_picture("mdy_24")

#일-월-년 24시간 포맷
def dmy_24():
    select = Select(driver.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(1) > select'))
    select.select_by_value('3')
    time.sleep(2)
    select = Select(driver.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(2) > select'))
    select.select_by_value('1')
    time.sleep(2)
    element = driver.find_element(By.ID, 'btnSaveSetup')
    element.click()
    time.sleep(20)
    capture_picture("dmy_24")
###설정 > 날짜&시간 끄읏~
###설정 > 언어
def login_language(ip, username, password):
    driver.get(ip)
    # driver.get('http://' + input('ip 주소를 입력하세요'))
    time.sleep(5)
    try:
        driver.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
        time.sleep(3)
        element = driver.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
        element.click()
        driver.find_element(By.CSS_SELECTOR, '#login_submit').click()
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(5)
    logger.info('Login > Option now')
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/a')
    element.click()
    time.sleep(2)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/ul/li[4]/a')
    element.click()
    print("language menu now")
    time.sleep(2)
    capture_picture("language")

def language_english():
    select = Select(driver.find_element(By.CSS_SELECTOR,'#language_list'))
    select.select_by_value('English')
    time.sleep(2)
    element = driver.find_element(By.CSS_SELECTOR, '#main-container > div.main-content > div > div.page-content.animated.fadeInRight > div.page-header > h1 > button')
    element.click()
    time.sleep(5)
    capture_picture("English")

def language_korean():
    select = Select(driver.find_element(By.CSS_SELECTOR,'#language_list'))
    select.select_by_value('Korean')
    time.sleep(2)
    element = driver.find_element(By.CSS_SELECTOR, '#main-container > div.main-content > div > div.page-content.animated.fadeInRight > div.page-header > h1 > button')
    element.click()
    time.sleep(5)
    capture_picture("Korean")
###설정 > 언어 끄읏
###설정 > 오디오
def login_audio(ip, username, password):
    driver.get(ip)
    # driver.get('http://' + input('ip 주소를 입력하세요'))
    time.sleep(5)
    try:
        driver.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
        time.sleep(3)
        element = driver.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
        element.click()
        driver.find_element(By.CSS_SELECTOR, '#login_submit').click()
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(5)
    logger.info('Option Login Complete')
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[3]/a')
    element.click()
    time.sleep(2)
    print("Option > Audio now")
    time.sleep(2)
    capture_picture("audio_default")

# 오디오 기능 활성화
def audio_activate():
    element = driver.find_element(By.XPATH, '//*[@id="main-container"]/div[2]/div/div[2]/div[2]/form/div/div/div[2]/div/div[1]/label/div/ins')
    element.click()
    element = driver.find_element(By.CSS_SELECTOR, '#main-container > div.main-content > div > div.page-content.animated.fadeInRight > div.page-header > h1 > button')
    element.click()
    time.sleep(5)
    capture_picture("audio_activated")

# 오디오 각종 기능 활성화
def audio_option_check():
    select = Select(driver.find_element(By.CSS_SELECTOR,'#main-container > div.main-content > div > div.page-content.animated.fadeInRight > div.row > form > div > div > div.widget-body > div > div:nth-child(2) > select'))
    select.select_by_value('G711A')
    time.sleep(2)
    element = driver.find_element(By.XPATH, '//*[@id="main-container"]/div[2]/div/div[2]/div[2]/form/div/div/div[2]/div/div[6]/label/div/ins')
    element.click()
    time.sleep(2)
    select = Select(driver.find_element(By.CSS_SELECTOR,'#main-container > div.main-content > div > div.page-content.animated.fadeInRight > div.row > form > div > div > div.widget-body > div > div:nth-child(5) > select'))
    select.select_by_value('4.0')
    time.sleep(2)
    select = Select(driver.find_element(By.CSS_SELECTOR,'#main-container > div.main-content > div > div.page-content.animated.fadeInRight > div.row > form > div > div > div.widget-body > div > div:nth-child(8) > select'))
    select.select_by_value('4.0')
    time.sleep(2)
    element = driver.find_element(By.CSS_SELECTOR, '#main-container > div.main-content > div > div.page-content.animated.fadeInRight > div.page-header > h1 > button')
    element.click()
    time.sleep(5)
    capture_picture("audio_option_check")
###설정>오디오 끄읏


def main_capture(ip, username, password):
    login_option_image(ip, username, password)
    video_source_PAL()
    reset_fix(username, password)
    login_option_image(ip, username, password)
    video_source_NTSC()
    reset_fix(username, password)
    login_option_image(ip, username, password)
    bright()
    saturation()
    contrast()
    tone()
    sharpness()
    reversal()
    osd()
    logout()
    logout_after_login_image(username, password)
    faker()
    wdr()
    blc()
    noise()
    compensation()
    logout()
    logout_after_login_image(username, password)
    day_night()
    digital_zoom()
    logout()
    logout_after_login(username, password)
    livestream()
    focus()
    directzoom()
    zoom()
    logout()
    login_security(ip, username, password)
    user_add()
    user_delete()
    login_time(username, password)
    local_time()
    NTP_time()
    login_same_time()
    logout()
    login_time(username, password)
    summer_time()
    ymd_24()
    mdy_24()
    dmy_24()
    ymd_12()
    logout()
    login_audio(ip, username, password)
    audio_activate()
    audio_option_check()
    logout()
    login_language(ip, username, password)
    language_english()
    language_korean()
    login_fail_test(ip, username)
    time.sleep(300)
    driver.refresh()
    time.sleep(5)
    login_auto_op(ip, username, password)
    factory_reset()

if __name__ == "__main__":
    print("👉 드라이버 초기화 시작")
    init_driver()
    print("👉 드라이버 초기화 끝. 상태:", driver)

    print("👉 캡처 실행")
    main_capture()