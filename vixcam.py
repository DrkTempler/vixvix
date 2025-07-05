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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CamTwo:
    def __init__(self):
        self.driver = self.setup_self()
        self.testname = None

    def setup_self(self):
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument("--window-size=1920,1080")

        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(3)
        return driver

    def open_url(self, url):
        self.driver.get(url)

    def close_browser(self):
        self.driver.quit()

    def test_name(self, testname):
        self.test_name = testname
        logger.info(f"테스트 기능 명 : {testname}")
    
    def capture_picture(self):
        if not  self.testname:
            raise   ValueError
        # 결과물 디렉토리(os 사용하여 없으면 폴더 만들기)
        directory = "D://Auto_test_result"
        os.makedirs(directory, exist_ok=True)
        screenshot_name = os.path.join(directory, f"{self.testname}.png")
        # 크롬한정기능
        mt = self.execute_cdp_cmd("Page.getLayoutMetrics", {})
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
        screenshot = self.execute_cdp_cmd("Page.captureScreenshot", screenshot_config)
        # Base64 디코딩
        with open(screenshot_name, "wb") as file:
            file.write(base64.b64decode(screenshot["data"]))
        logger.info(f"{self.testname} capture complete")

    def logout(self):
        element = self.find_element(By.XPATH, '//*[@id="sidebar-shortcuts-large"]/a[4]')
        element.click()
        time.sleep(3)
        self.capture_picture(self, "logout")

    def logout_after_login(self, username, password):
        time.sleep(5)
        self.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
        time.sleep(3)
        self.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
        time.sleep(3)
        time.sleep(3)
        self.find_element(By.CSS_SELECTOR, '#login_submit').click()
        time.sleep(3)

    def logout_after_login_image(self, username, password):
        time.sleep(5)
        self.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
        time.sleep(3)
        self.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
        time.sleep(3)
        element = self.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
        element.click()
        self.find_element(By.CSS_SELECTOR, '#login_submit').click()
        time.sleep(3)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/a')
        element.click()
        time.sleep(1)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/ul/li[4]/a')
        element.click()
        time.sleep(5)

    ### 라이브 페이지 UI 자동화 ###
    # 자동로그인
    def login_auto(self, ip, username, password):
        self.get(ip)
        # self.get('http://' + input('ip 주소를 입력하세요'))
        time.sleep(5)
        self.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
        time.sleep(3)
        self.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
        time.sleep(3)
        self.find_element(By.CSS_SELECTOR, '#login_submit').click()
        time.sleep(3)

    # 자동설정로그인
    def login_auto_op(self, ip, username, password):
        self.get(ip)
        # self.get('http://' + input('ip 주소를 입력하세요'))
        time.sleep(5)
        try:
            self.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
            time.sleep(3)
            self.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
            time.sleep(3)
            element = self.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
            element.click()
            self.find_element(By.CSS_SELECTOR, '#login_submit').click()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)
        logger.info('option menu login complete')
        time.sleep(5)
        self.capture_picture(self, "vixcam_information")
        time.sleep(3)

    # 초기화 후 pw 지정
    # 초기화 후 admin1357로 강제 지정되며 이 블록은 쓸 수 없게 되었다
    # 어쩌겠나 파인트리에서 수정하는게 공유되지 않는것을..
    # 꼬우면 이직해~~~^^
    # def reset_after_login(self):
        # self.refresh()
        # time.sleep(5)
        # element = self.find_element(By.CSS_SELECTOR, '#edit-pwd-container > div:nth-child(2) > div > input')
        # element.send_keys("pass0001!")
        # time.sleep(3)
        # element = self.find_element(By.CSS_SELECTOR, '#edit-pwd-container > div:nth-child(4) > div > input')
        # element.send_keys("pass0001!")
        # time.sleep(3)
        # capture_picture(self, "초기화 후 pw 지정")
        # self.find_element(By.CSS_SELECTOR, 'body > div > div > div > div.modal-footer > button').send_keys(Keys.ENTER)
        # time.sleep(3)
        # self.find_element(By.CLASS_NAME, 'confirm').send_keys(Keys.ENTER)

    # admin1357 강제지정으로 로그인 후 관리자 패스워드 변경
    def reset_fix(self, username, password):
        self.refresh()
        time.sleep(5)
        element = self.find_element(By.CSS_SELECTOR, '#user')
        element.click()
        element.send_keys(username)
        time.sleep(3)
        element = self.find_element(By.CSS_SELECTOR, '#pwd')
        element.click()
        element.send_keys('admin1357')
        time.sleep(3)
        element = self.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
        element.click()
        element = self.find_element(By.CSS_SELECTOR, '#login_submit')
        element.click()
        time.sleep(3)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/a')
        element.click()
        time.sleep(2)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/ul/li[1]/a')
        element.click()
        time.sleep(3)
        element = self.find_element(By.CSS_SELECTOR, '#admin')
        element.click()
        time.sleep(1)
        element = self.find_element(By.CSS_SELECTOR, '#btnEditUser')
        element.click()
        time.sleep(2)
        element = self.find_element(By.CSS_SELECTOR, '#edit_user_list > div:nth-child(2) > div > input')
        element.click()
        element.send_keys(password)
        element = self.find_element(By.CSS_SELECTOR, '#edit_user_list > div:nth-child(4) > div > input')
        element.click()
        element.send_keys(password)
        time.sleep(2)
        element = self.find_element(By.CSS_SELECTOR, '#editUserModal > div > div > div.modal-footer > button.btn.btn-primary.btn-sm')
        element.click()
        time.sleep(2)
        element = self.find_element(By.CSS_SELECTOR, 'body > div.sweet-alert.showSweetAlert.visible > div.sa-button-container > button.confirm')
        element.click()

    # 로그인
    def login(self, ip, username, password):
        self.get(ip)
        # self.get('http://' + input('ip주소를 입력하세요'))
        time.sleep(5)
        try:
            element = self.find_element(By.CSS_SELECTOR, '#user')
            element.click()
            element.send_keys(username)
            time.sleep(3)
            element = self.find_element(By.CSS_SELECTOR, '#pwd')
            element.click()
            element.send_keys(password)
            time.sleep(3)
            element = self.find_element(By.CSS_SELECTOR, '#login_submit')
            element.click()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)
        logger.info('login complete')

    # 로그인 실패 시나리오
    def login_fail_test(self, ip, username):
        self.get(ip)
        # self.get('http://' + input('ip주소를 입력하세요'))
        time.sleep(5)
        # 최대 시도 스펙 바뀌면 바꾸세염
        max_attempts = 5
        for attempt in range(1, max_attempts + 1):
            print(f"{attempt}회 로그인 시도중")
            time.sleep(5)
            self.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
            time.sleep(3)
            self.find_element(By.CSS_SELECTOR, '#pwd').send_keys("KILLYOU15%@")
            time.sleep(3)
            self.find_element(By.CSS_SELECTOR, '#login_submit').click()
            time.sleep(3)
            try:
                element = self.find_element(By.ID, "lockdown_menu")
                if element.is_displayed():
                    self.capteure_picture(self, "login_fail_test")
                    print("Login Fail Test Pass!")
            except NoSuchElementException:
                    print("WHAT THE FUCK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            self.find_element(By.CSS_SELECTOR, '#user').clear()
            self.find_element(By.CSS_SELECTOR, '#pwd').clear()

    ###라이브 페이지 자동화###
    # 줌인&아웃 시나리오
    def zoom(self):
        # 사이드바 출현여부
        element = self.find_element(By.CSS_SELECTOR, '#menu_button')
        element.click()
        element.click()
        wait = WebDriverWait(self, 10)
        sidebar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sidebar"]')))
        style = self.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('display');", sidebar)
        time.sleep(5)
        if style == "block":
            print("Sidebar displaying now")
        else: 
            element = self.find_element(By.CSS_SELECTOR, '#menu_button')
            element.click()
        # ptz 메뉴 열기
        time.sleep(5)
        ptzmenu = self.find_element(By.CSS_SELECTOR, '#ptz_menu')
        if 'accordion-toggle' in ptzmenu.get_attribute("class"):
            print("Ptz Menu displaying on Sidebar now")
        else:
            ptzmenu.click()
        time.sleep(3)
        for i in range(80):
            element = self.find_element(By.XPATH, '//*[@id="ptz_panel"]/div/div[1]/div[1]/div[1]/button')
            element.click()
            time.sleep(0.5)
        self.capteure_picture(self, "zoom_in")
        time.sleep(3)
        for i in range(80):
            element = self.find_element(By.XPATH, '//*[@id="ptz_panel"]/div/div[1]/div[1]/div[3]/button')
            element.click()
            time.sleep(0.5)
        self.capteure_picture(self, "zoom_out")

    # 다이렉트줌 시나리오
    def directzoom(self):
        # 사이드바 출현여부
        element = self.find_element(By.CSS_SELECTOR, '#menu_button')
        element.click()
        element.click()
        wait = WebDriverWait(self, 10)
        sidebar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sidebar"]')))
        style = self.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('display');", sidebar)
        time.sleep(5)
        if style == "block":
            print("Sidebar displaying now")
        else: 
            element = self.find_element(By.CSS_SELECTOR, '#menu_button')
            element.click()
        # ptz 메뉴 열기
        time.sleep(5)
        ptzmenu = self.find_element(By.CSS_SELECTOR, '#ptz_menu')
        if 'accordion-toggle' in ptzmenu.get_attribute("class"):
            print("Ptz Menu displaying on Sidebar now")
        else:
            ptzmenu.click()
        element = self.find_element(By.XPATH, '//*[@id="ptz_panel"]/div/div[1]/div[7]/div/span/span[1]/span[6]')
        self.execute_script("arguments[0].scrollIntoView();", element)
        actions = ActionChains(self)
        actions.click_and_hold(element).move_by_offset(100, 0).release().perform()
        time.sleep(3)
        self.capteure_picture(self, "directzoom_in")
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="ptz_panel"]/div/div[1]/div[7]/div/span/span[1]/span[6]')
        self.execute_script("arguments[0].scrollIntoView();", element)
        actions = ActionChains(self)
        actions.click_and_hold(element).move_by_offset(-100, 0).release().perform()
        time.sleep(3)
        self.capteure_picture(self, "directzoom_out")

    # 포커스 조작 시나리오
    def focus(self):
        # 사이드바 출현여부
        element = self.find_element(By.CSS_SELECTOR, '#menu_button')
        element.click()
        element.click()    
        wait = WebDriverWait(self, 10)
        sidebar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sidebar"]')))
        style = self.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('display');", sidebar)
        time.sleep(5)
        if style == "block":
            print("Sidebar displaying now")
        else: 
            element = self.find_element(By.CSS_SELECTOR, '#menu_button')
            element.click()
        # ptz 메뉴 열기
        time.sleep(10)
        ptzmenu = self.find_element(By.CSS_SELECTOR, '#colMenu5')
        if 'true' in ptzmenu.get_attribute("aria-expanded"):
            print("Ptz Menu displaying on Sidebar now")
        else:
            element = self.find_element(By.CSS_SELECTOR, '#ptz_menu')
            element.click()
            print("Call Ptz Menu")
        # 포커스 조작
        time.sleep(5)
        for i in range(80):
            element = self.find_element(By.XPATH, '//*[@id="ptz_panel"]/div/div[1]/div[3]/div[1]/button')
            element.click()
            time.sleep(0.5)
        self.capteure_picture(self, "focus_meele")
        time.sleep(3)
        element = self.find_element(By.XPATH, '//*[@id="ptz_panel"]/div/div[1]/div[5]/div/button')
        element.click()
        time.sleep(6)
        self.capteure_picture(self, "focus_Auto")
        for i in range(80):
            element = self.find_element(By.XPATH, '//*[@id="ptz_panel"]/div/div[1]/div[3]/div[3]/button')
            element.click()
            time.sleep(0.5)
        self.capteure_picture(self, "focus_far")

    # 비디오 스트림 순회
    def livestream(self):
        # 사이드바 출현여부
        element = self.find_element(By.CSS_SELECTOR, '#menu_button')
        element.click()
        element.click()
        wait = WebDriverWait(self, 10)
        sidebar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sidebar"]')))
        style = self.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('display');", sidebar)
        time.sleep(5)
        if style == "block":
            print("Sidebar displaying now")
        else: 
            element = self.find_element(By.CSS_SELECTOR, '#menu_button')
            element.click()
        # 라이브제어 메뉴 열기
        time.sleep(5)
        livecontrol = self.find_element(By.CSS_SELECTOR, '#player_control_pannel > div.panel-heading > h4 > a')
        if 'accordion-toggle collapsed' in livecontrol.get_attribute("class"):
            livecontrol.click()
            print("Call livecontrol")
        else:
            print("livecontrol displaying Now")
        time.sleep(3)
        element = self.find_element(By.XPATH, '//*[@id="stream2"]/label/div')
        element.click()
        time.sleep(5)
        self.capteure_picture(self, "Stream2")
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="stream3"]/label/div')
        element.click()
        time.sleep(5)
        self.capteure_picture(self, "Stream3")
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="stream4"]/label/div')
        element.click()
        time.sleep(5)
        self.capteure_picture(self, "Stream4")
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="stream1"]/label/div')
        element.click()
        time.sleep(5)
        self.capteure_picture(self, "Stream1")
        time.sleep(5)
    ### 라이브 페이지 UI 자동화 요기까지 ###

    def no_alert(self):
        try:
            alert_button = self.find_element(By.XPATH, "//div[contains(@class, 'sweet-alert') and contains(@class, 'visible')]//button[contains(@class, 'confirm')]")
            alert_button.click()
            print("F*** YOU ALERT")

        except NoSuchElementException:
            print("gogo next")

    ### 설정 > 비디오 & 이미지 > 이미지 자동화 시작 ###
    # 이미지 자동 진입
    def login_option_image(self, ip, username, password):
        self.get(ip)
        # self.get('http://' + input('ip 주소를 입력하세요'))
        time.sleep(5)
        self.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
        time.sleep(3)
        self.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
        time.sleep(3)
        element = self.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
        element.click()
        element = self.find_element(By.CSS_SELECTOR, '#login_submit')
        element.click()
        time.sleep(3)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/a')
        element.click()
        time.sleep(1)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/ul/li[4]/a')
        element.click()
        time.sleep(5)
        logger.info('Option > Image now')
        time.sleep(5)

    # 밝기 최소값 & 최대값 
    def bright(self):
        # 밝기 최소값
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[1]/select'))
        select.select_by_value('1')
        time.sleep(1)
        # 확인 버튼
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(3)
        self.capteure_picture(self, "bright_low")
        time.sleep(5)
        # 밝기 최대값
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[1]/select'))
        select.select_by_value('100')
        time.sleep(1)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        self.capteure_picture(self, "bright_high")
        # 밝기 정상화
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[1]/select'))
        select.select_by_value('50')
        time.sleep(1)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        self.capteure_picture(self, "bright_normal")

    # 포화도 최소값 & 최대값
    def saturation(self):
        # 포화도 최소값
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[2]/select'))
        select.select_by_value('1')
        time.sleep(1)
        # 확인 버튼
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(3)
        self.capteure_picture(self, "saturation_low")
        time.sleep(5)
        # 포화도 최대값
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[2]/select'))
        select.select_by_value('100')
        time.sleep(1)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(3)
        self.capteure_picture(self, "saturation_high")
        time.sleep(5)
        # 포화도 정상화
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[2]/select'))
        select.select_by_value('65')
        time.sleep(1)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(3)
        self.capteure_picture(self, "saturation_normal")

    # 명암비 최소값 & 최대값
    def contrast(self):
        # 명암비 최소값
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[3]/select'))
        select.select_by_value('1')
        time.sleep(1)
        # 확인 버튼
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(3)
        self.capteure_picture(self, "contrast_low")
        time.sleep(5)
        # 명암비 최대값
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[3]/select'))
        select.select_by_value('100')
        time.sleep(1)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(3)
        self.capteure_picture(self, "contrast_high")
        time.sleep(5)
        # 명암비 정상화
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[1]/div[3]/select'))
        select.select_by_value('55')
        time.sleep(1)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(3)
        self.capteure_picture(self, "contrast_normal")

    # 색조 최소값 & 최대값
    def tone(self):
        # 색조 최소값
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[1]/select'))
        select.select_by_value('1')
        time.sleep(1)
        # 확인 버튼
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(3)
        self.capteure_picture(self, "tone_low")
        time.sleep(5)
        # 색조 최대값
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[1]/select'))
        select.select_by_value('30')
        time.sleep(1)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(3)
        self.capteure_picture(self, "tone_high")
        time.sleep(5)
        # 색조 정상화
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[1]/select'))
        select.select_by_value('17')
        time.sleep(1)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(3)
        self.capteure_picture(self, "tone_normal")

    # 선명도 최소값 & 최대값
    def sharpness(self):
        # 선명도 최소값
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[2]/select'))
        select.select_by_value('1')
        time.sleep(1)
        # 확인 버튼
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(3)
        self.capteure_picture(self, "sharpness_low")
        time.sleep(5)
        # 선명도 최대값
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[2]/select'))
        select.select_by_value('12')
        time.sleep(1)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(3)
        self.capteure_picture(self, "sharpness_high")
        time.sleep(5)
        # 선명도 정상화
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[2]/select'))
        select.select_by_value('7')
        time.sleep(1)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(3)
        self.capteure_picture(self, "sharpness_normal")

    # 반전모드 사용
    def reversal(self):
        element = self.find_element(By.XPATH, '//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[4]/label/div/ins')
        element.click()
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        self.capteure_picture(self, "reversal_red")
        element = self.find_element(By.XPATH, '//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[4]/label/div/ins')
        element.click()
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[5]/label/div/ins')
        element.click()
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[5]/label/div/ins')
        element.click()
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        self.capteure_picture(self, "reversal_blue")
        element = self.find_element(By.XPATH, '//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[4]/label/div/ins')
        element.click()
        time.sleep(2)
        element = self.find_element(By.XPATH, '//*[@id="tab-basic"]/div/div[2]/div/div/div[2]/div[5]/label/div/ins')
        element.click()
        time.sleep(5)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(20)
        self.refresh()
        self.capteure_picture(self, "reversal_purple")

    # OSD 사용
    def osd(self):
        # 탭 이동
        element = self.find_element(By.XPATH, '//*[@id="tab-hdr-osd"]/a')
        element.click()
        # OSD 설정
        element = self.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[1]/div/div[2]/div/div[1]/div/label/div/ins')
        element.click()
        element = self.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[1]/div/div[2]/div/div[2]/div/label/div/ins')
        element.click()
        element = self.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[1]/div/div[2]/div/div[3]/div/label/div/ins')
        element.click()
        element = self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]')
        element.click()
        time.sleep(5)
        self.capteure_picture(self, "OSD activate")
        time.sleep(5)
        # OSD 텍스트 변경
        element = self.find_element(By.XPATH, '//*[@id="real_osd_text_content"]')
        element.clear()
        element.send_keys("Luvyou")
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        self.capteure_picture(self, "OSD Text")
        time.sleep(5)
        # OSD 누를때 / 항상 변경
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(3) > select'))
        select.select_by_value('always')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        self.capteure_picture(self, "OSD always")
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(3) > select'))
        select.select_by_value('onpush')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        self.capteure_picture(self, "OSD onpush")
        # OSD 색상 변경
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
        select.select_by_value('White')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        self.capteure_picture(self, "OSD_White")
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
        select.select_by_value('Black')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        self.capteure_picture(self, "OSD_Black")
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
        select.select_by_value('Yellow')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        self.capteure_picture(self, "OSD_Yellow")
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
        select.select_by_value('Cyan')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        self.capteure_picture(self, "OSD_Cyan")
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
        select.select_by_value('Green')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        self.capteure_picture(self, "OSD_Green")
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
        select.select_by_value('Magenta')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        self.capteure_picture(self, "OSD_Magenta")
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
        select.select_by_value('Red')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        self.capteure_picture(self, "OSD_Red")
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-osd > div > div:nth-child(1) > div > div.widget-body > div > div:nth-child(5) > select'))
        select.select_by_value('Blue')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(5)
        self.capteure_picture(self, "OSD_Blue")
        # OSD 슬라이더 최소값
        element = self.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[2]/div/div[2]/div/div[1]/span[1]/span[6]')
        self.execute_script("arguments[0].scrollIntoView();", element)
        actions = ActionChains(self)
        actions.click_and_hold(element).move_by_offset(-500, 0).release().perform()
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[2]/div/div[2]/div/div[2]/span[1]/span[6]')
        self.execute_script("arguments[0].scrollIntoView();", element)
        actions = ActionChains(self)
        actions.click_and_hold(element).move_by_offset(-500, 0).release().perform()
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[2]/div/div[2]/div/div[3]/span[1]/span[6]')
        self.execute_script("arguments[0].scrollIntoView();", element)
        actions = ActionChains(self)
        actions.click_and_hold(element).move_by_offset(-500, 0).release().perform()
        time.sleep(5)
        self.capteure_picture(self, "OSD slider low")
        element = self.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[2]/div/div[2]/div/div[1]/span[1]/span[6]')
        self.execute_script("arguments[0].scrollIntoView();", element)
        actions = ActionChains(self)
        actions.click_and_hold(element).move_by_offset(500, 0).release().perform()
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[2]/div/div[2]/div/div[2]/span[1]/span[6]')
        self.execute_script("arguments[0].scrollIntoView();", element)
        actions = ActionChains(self)
        actions.click_and_hold(element).move_by_offset(500, 0).release().perform()
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="tab-osd"]/div/div[2]/div/div[2]/div/div[3]/span[1]/span[6]')
        self.execute_script("arguments[0].scrollIntoView();", element)
        actions = ActionChains(self)
        actions.click_and_hold(element).move_by_offset(500, 0).release().perform()
        time.sleep(5)
        self.capteure_picture(self, "OSD slider high")

    # 색온도
    def faker(self):
        # 탭 이동
        element = self.find_element(By.XPATH, '//*[@id="tab-hdr-awb"]/a')
        element.click()
        # 색온도 설정
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
        select.select_by_value('outdoor')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "rgb_outdoor")
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
        select.select_by_value('bulb')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "rgb_bulb")
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
        select.select_by_value('flourescent')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "rgb_flourescent")
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
        select.select_by_value('clearsky')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "rgb_clearsky")
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
        select.select_by_value('shade')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "rgb_shade")
        select.select_by_value('auto')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "rgb_auto")
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
        select.select_by_value('manual')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "rgb_manual")
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
        # 색온도 수동 값 MIN
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_wb_r_gain'))
        select.select_by_value('1')
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_wb_g_gain'))
        select.select_by_value('1')
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_wb_b_gain'))
        select.select_by_value('1')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "rgb_manual_MIN")
        # 색온도 수동 값 MAX
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_wb_r_gain'))
        select.select_by_value('255')
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_wb_g_gain'))
        select.select_by_value('255')
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_wb_b_gain'))
        select.select_by_value('255')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "rgb_manual_MAX")
        select = Select(self.find_element(By.CSS_SELECTOR,'#tab-awb > div > div.widget-body > div > div:nth-child(1) > select'))
        select.select_by_value('auto')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)

    # 세로모드
    def vertical(self):
        # 탭 이동
        element = self.find_element(By.XPATH, '//*[@id="tab-hdr-corridor"]/a')
        element.click()
        # 90도
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_corridor_enable'))
        select.select_by_value('1')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "vertical_90")
        # 270도
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_corridor_mode'))
        select.select_by_value('270degree')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "vertical_270")
        # 원상복귀
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_corridor_enable'))
        select.select_by_value('0')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "vertical_none")

    # 광역역광보정
    def wdr(self):
        # 탭 이동
        element = self.find_element(By.XPATH, '//*[@id="tab-hdr-wdr"]/a')
        element.click()    
        # 광역역광보정 (WDR)
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_wdr_mode'))
        select.select_by_value('on')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "WDR_5level")
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_wdr_level'))
        select.select_by_value('10')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "WDR_10level")
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_wdr_level'))
        select.select_by_value('1')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "WDR_1level")
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_wdr_mode'))
        select.select_by_value('off')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "WDR_off")
        # 디지털 광역역광보정(DWDR)
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_dwdr_mode'))
        select.select_by_value('on')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "DWDR_3level")
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_dwdr_level'))
        select.select_by_value('16')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "DWDR_16level")
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_dwdr_level'))
        select.select_by_value('1')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "DWDR_1level")
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_dwdr_mode'))
        select.select_by_value('off')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "DWDR_off")    
        # 안개 보정 설정
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_defog_mode'))
        select.select_by_value('on')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "Defog_2level")
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_defog_level'))
        select.select_by_value('3')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "Defog_3level")
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_defog_level'))
        select.select_by_value('1')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "Defog_1level")
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_defog_mode'))
        select.select_by_value('off')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "Defog_off")   

    # 역광보정
    def blc(self):
        # 탭 이동
        element = self.find_element(By.XPATH, '//*[@id="tab-hdr-blc"]')
        element.click()
        # 역광보정
        select = Select(self.find_element(By.XPATH, '//*[@id="tab-blc"]/div/div[1]/div/div[2]/div/div[1]/select'))
        select.select_by_value('on')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "blc_5level")
        select = Select(self.find_element(By.XPATH, '//*[@id="tab-blc"]/div/div[1]/div/div[2]/div/div[2]/select'))
        select.select_by_value('10')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "blc_10level")
        select = Select(self.find_element(By.XPATH, '//*[@id="tab-blc"]/div/div[1]/div/div[2]/div/div[2]/select'))
        select.select_by_value('1')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "blc_1level")
        select = Select(self.find_element(By.XPATH, '//*[@id="tab-blc"]/div/div[1]/div/div[2]/div/div[1]/select'))
        select.select_by_value('off')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "blc_off")
        # 하이라이트 보정 설정
        select = Select(self.find_element(By.XPATH, '//*[@id="real_hlc_mode"]'))
        select.select_by_value('on')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "highlight_3level")
        select = Select(self.find_element(By.XPATH, '//*[@id="tab-blc"]/div/div[2]/div/div[2]/div/div[2]/select'))
        select.select_by_value('5')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "highlight_10level")
        select = Select(self.find_element(By.XPATH, '//*[@id="tab-blc"]/div/div[2]/div/div[2]/div/div[2]/select'))
        select.select_by_value('1')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "highlight_1level")
        select = Select(self.find_element(By.XPATH, '//*[@id="real_hlc_mode"]'))
        select.select_by_value('off')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "highlight_off")

    # 노이즈제거
    def noise(self):
        # 탭 이동
        element = self.find_element(By.XPATH, '//*[@id="tab-hdr-dnr"]')
        element.click()
        # 수준~
        select_elem = self.find_element(By.CSS_SELECTOR, '#tab-dnr select')
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
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-dnr"]/div/div[2]/div/div[2]/select'))
        select.select_by_value('10')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "noise_10level")   
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-dnr"]/div/div[2]/div/div[2]/select'))
        select.select_by_value('1')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "noise_1level")    
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-dnr"]/div/div[2]/div/div[1]/select'))
        select.select_by_value('off')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "noise_off")   

    # 렌즈보정
    def compensation(self):
        # 탭 이동
        element = self.find_element(By.XPATH, '//*[@id="tab-hdr-ldc"]')
        element.click() 
        # 켜~기
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-ldc"]/div/div[2]/div/div/select'))
        select.select_by_value('on')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "compensation_on") 
        # 끄~기
        select = Select(self.find_element(By.XPATH,'//*[@id="tab-ldc"]/div/div[2]/div/div/select'))
        select.select_by_value('off')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        # 칩셋 성능이 그지같아서 저장하려면 클릭 여러번해야됌 아오 진짜 개빡쳐
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "compensation_off") 

    # 주 & 야간
    def day_night(self):
        time.sleep(10)
        # 탭 이동
        element = self.find_element(By.XPATH, '//*[@id="tab-hdr-dnn"]/a')
        element.click() 
        # 야간
        select = Select(self.find_element(By.XPATH,'//*[@id="real_dnn_mode"]'))
        select.select_by_value('night')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "night")     
        # 주간
        select = Select(self.find_element(By.XPATH,'//*[@id="real_dnn_mode"]'))
        select.select_by_value('day')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "day")
        # 자동
        select = Select(self.find_element(By.XPATH,'//*[@id="real_dnn_mode"]'))
        select.select_by_value('auto')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "auto")

    # 디지털 줌(이미지단 뒤에 붙여서 쓰세여)
    def digital_zoom(self):
        # 디지털 줌 메뉴로 이동
        self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/ul/li[6]/a').send_keys(Keys.ENTER)
        time.sleep(5)
        # 디지털 줌 체크박스 활성화
        self.find_element(By.CSS_SELECTOR, '#setup-content > form > div:nth-child(2) > div > div > div > div:nth-child(1) > label > div > ins').click()
        # 디지털 줌 최대
        select = Select(self.find_element(By.XPATH,'//*[@id="real_dz_level"]'))
        select.select_by_value('800')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "digital_zoom_8")
        # 디지털 줌 최소    
        select = Select(self.find_element(By.XPATH,'//*[@id="real_dz_level"]'))
        select.select_by_value('100')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(10)
        self.capteure_picture(self, "digital_zoom_1")
        # 디지털 줌 끄기    
        self.find_element(By.CSS_SELECTOR, '#setup-content > form > div:nth-child(2) > div > div > div > div:nth-child(1) > label > div > ins').click()
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        self.capteure_picture(self, 'digital_zoom_off')

    # 신호 입력방식_PAL
    def video_source_PAL(self):
        self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/ul/li[1]/a').send_keys(Keys.ENTER)
        time.sleep(5)
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_video_mode'))
        select.select_by_value('PAL')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(3)
        element = self.find_element(By.CLASS_NAME, 'confirm')
        element.click()
        print("Change Source PAL")
        time.sleep(5)
        self.capteure_picture(self, "video_source_PAL")
        time.sleep(100)

    # 신호 입력방식_NTSC
    def video_source_NTSC(self):
        self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[2]/ul/li[1]/a').send_keys(Keys.ENTER)
        time.sleep(5)
        select = Select(self.find_element(By.CSS_SELECTOR,'#real_video_mode'))
        select.select_by_value('NTSC')
        self.find_element(By.XPATH, '//*[@id="btnSaveSetup"]').send_keys(Keys.ENTER)
        time.sleep(3)
        element = self.find_element(By.CLASS_NAME, 'confirm')
        element.click()
        print("Change Source NTSC")
        time.sleep(5)
        self.capteure_picture(self, "video_source_NTSC")
        time.sleep(100)

    ### 설정 > 비디오 & 이미지 > 이미지 자동화 끄읏 ###

    ### 설정 > 관리 > 재시작 / 초기화 / 공장초기화 ###
    # 재시작
    def restart(self):
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/a')
        element.click()
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/ul/li[5]/a')
        element.click()
        time.sleep(5)
        element = self.find_element(By.NAME, 'btnRestart')
        element.click()
        time.sleep(3)
        element = self.find_element(By.CLASS_NAME, 'confirm')
        element.click()
        print("get restart")
        time.sleep(5)
        self.capteure_picture(self, "restart")

    # 초기화
    def reset(self):
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/a')
        element.click()
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/ul/li[5]/a')
        element.click()
        time.sleep(5)
        element = self.find_element(By.NAME, 'btnReset')
        element.click()
        time.sleep(3)
        element = self.find_element(By.CLASS_NAME, 'confirm')
        element.click()
        print("reset Start")
        time.sleep(5)
        self.capteure_picture(self, "reset_start")
        time.sleep(60)
        self.capteure_picture(self, "reset_finish")

    # 공장초기화
    # *왠만하면 테스트 마지막에 배치하세요~~공장초기화 하고 재시작하기까지 시간이 많이 소요됩니다!!
    def factory_reset(self):
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/a')
        element.click()
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/ul/li[5]/a')
        element.click()
        time.sleep(5)
        element = self.find_element(By.NAME, 'btnDefault')
        element.click()
        time.sleep(3)
        element = self.find_element(By.CLASS_NAME, 'confirm')
        element.click()
        print("factory reset On. bye bye bye")
        time.sleep(5)
        self.capteure_picture(self, "factory_reset_start")
    # 팩토리 리셋 결과는 매뉴얼로 확인하세요~~~ ip가 DHCP나 192.168.0.100으로 변경됩니다~~~^^
    ### 설정 > 관리 > 재시작 / 초기화 / 공장초기화 끄~~읏 ###
    ### 설정 > 보안 > 사용자 계정 추가 및 삭제 ###
    # 보안 메뉴 진입
    def login_security(self, ip, username, password):
        self.get(ip)
        # self.get('http://' + input('ip 주소를 입력하세요'))
        time.sleep(5)
        try:
            self.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
            time.sleep(3)
            self.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
            time.sleep(3)
            element = self.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
            element.click()
            self.find_element(By.CSS_SELECTOR, '#login_submit').click()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)
        logger.info('Option Login Complete')
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/a')
        element.click()
        time.sleep(2)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/ul/li[1]/a')
        element.click()
        print("Option > Security Now")

    # 사용자 추가
    def user_add(self):
        for i in range(9):
            element = self.find_element(By.ID, 'btnAddUser')
            element.click()
            time.sleep(2)
            element = WebDriverWait(self, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#user_list > div:nth-child(1) > div > input')))
            element.click()
            element.send_keys(f"qaqaqa{i}")
            time.sleep(2)
            element = self.find_element(By.CSS_SELECTOR, '#user_list > div:nth-child(2) > div > input')
            element.send_keys("pass0001!")
            time.sleep(2)
            element = self.find_element(By.CSS_SELECTOR, '#user_list > div:nth-child(4) > div > input')
            element.send_keys("pass0001!")
            time.sleep(2)
            select = Select(self.find_element(By.CSS_SELECTOR,'#user_list > div:nth-child(5) > div > select'))
            select.select_by_value('2')
            time.sleep(2)
            element = self.find_element(By.CSS_SELECTOR, '#addUserModal > div > div > div.modal-footer > button.btn.btn-primary.btn-sm')
            element.send_keys(Keys.ENTER)
            time.sleep(2)
            self.capteure_picture(self, f"add_user_{i}")
            time.sleep(2)

    # 사용자 삭제
    def user_delete(self):
        for i in range(9):
            element = self.find_element(By.ID, f"qaqaqa{i}")
            element.click()
            time.sleep(2)
            element = self.find_element(By.ID, 'btnDeleteUser')
            element.send_keys(Keys.ENTER)
            time.sleep(2)
            element = self.find_element(By.CLASS_NAME, 'confirm')
            element.send_keys(Keys.ENTER)
            time.sleep(2)
            self.capteure_picture(self, f"delete_user_{i}")
            time.sleep(2)
    ### 설정 > 보안 > 사용자 완료완료
    ### 설정 > 날짜&시간 시작시작
    #날짜&시간 메뉴 진입
    def login_time(self, ip, username, password):
        self.get(ip)
        # self.get('http://' + input('ip 주소를 입력하세요'))
        time.sleep(5)
        try:
            self.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
            time.sleep(3)
            self.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
            time.sleep(3)
            element = self.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
            element.click()
            self.find_element(By.CSS_SELECTOR, '#login_submit').click()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)
        logger.info('Option Login Complete')
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/a')
        element.click()
        time.sleep(2)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/ul/li[2]/a')
        element.click()
        print("Option > Date&Time now")
        time.sleep(2)
        self.capteure_picture(self, "date_time_main")

    #컴퓨터 시간과 동기화 
    def local_time(self):
        element = self.find_element(By.XPATH, '//*[@id="setup-content"]/div/form/div[1]/div[2]/div[2]/div/div[1]/label/div/ins')
        element.click()
        time.sleep(2)
        element = self.find_element(By.ID, 'btnSaveSetup')
        element.click()
        time.sleep(2)
        self.capteure_picture(self, "local_time")
        time.sleep(20)

    #NTP 서버와 동기화
    def NTP_time(self):
        element = self.find_element(By.XPATH, '//*[@id="setup-content"]/div/form/div[1]/div[2]/div[2]/div/div[5]/label/div/ins')
        element.click()
        time.sleep(2)
        element = self.find_element(By.ID, 'btnSaveSetup')
        element.click()
        time.sleep(2)
        self.capteure_picture(self, "NTP_time")
        time.sleep(20)

    #로그인 시간과 동기화
    def login_same_time(self):
        element = self.find_element(By.XPATH, '//*[@id="setup-content"]/div/form/div[1]/div[2]/div[2]/div/div[9]/div/label/div/ins')
        element.click()
        time.sleep(2)
        element = self.find_element(By.ID, 'btnSaveSetup')
        element.click()
        time.sleep(2)
        self.capteure_picture(self, "login_same_time")
        time.sleep(20)

    #써머타임
    def summer_time(self):
        element = self.find_element(By.XPATH, '//*[@id="setup-content"]/div/form/div[2]/div[1]/div[2]/div/div[2]/label/div/ins')
        element.click()
        time.sleep(2)
        element = self.find_element(By.ID, 'btnSaveSetup')
        element.click()
        time.sleep(2)
        self.capteure_picture(self, "summer_time")
        time.sleep(20)

    #년-월-일 12시간 포맷
    def ymd_12(self):
        select = Select(self.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(1) > select'))
        select.select_by_value('1')
        time.sleep(2)
        select = Select(self.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(2) > select'))
        select.select_by_value('2')
        time.sleep(2)
        element = self.find_element(By.ID, 'btnSaveSetup')
        element.click()
        time.sleep(20)
        self.capteure_picture(self, "ymd_12")

    #년-월-일 24시간 포맷
    def ymd_24(self):
        select = Select(self.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(1) > select'))
        select.select_by_value('1')
        time.sleep(2)
        select = Select(self.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(2) > select'))
        select.select_by_value('1')
        time.sleep(2)
        element = self.find_element(By.ID, 'btnSaveSetup')
        element.click()
        time.sleep(20)
        self.capteure_picture(self, "ymd_24")

    #월-일-년 24시간 포맷
    def mdy_24(self):
        select = Select(self.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(1) > select'))
        select.select_by_value('2')
        time.sleep(2)
        select = Select(self.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(2) > select'))
        select.select_by_value('1')
        time.sleep(2)
        element = self.find_element(By.ID, 'btnSaveSetup')
        element.click()
        time.sleep(20)
        self.capteure_picture(self, "mdy_24")

    #일-월-년 24시간 포맷
    def dmy_24(self):
        select = Select(self.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(1) > select'))
        select.select_by_value('3')
        time.sleep(2)
        select = Select(self.find_element(By.CSS_SELECTOR,'#setup-content > div > form > div:nth-child(2) > div:nth-child(3) > div.widget-body > div > div:nth-child(2) > select'))
        select.select_by_value('1')
        time.sleep(2)
        element = self.find_element(By.ID, 'btnSaveSetup')
        element.click()
        time.sleep(20)
        self.capteure_picture(self, "dmy_24")
    ###설정 > 날짜&시간 끄읏~
    ###설정 > 언어
    def login_language(self, ip, username, password):
        self.get(ip)
        # self.get('http://' + input('ip 주소를 입력하세요'))
        time.sleep(5)
        try:
            self.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
            time.sleep(3)
            self.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
            time.sleep(3)
            element = self.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
            element.click()
            self.find_element(By.CSS_SELECTOR, '#login_submit').click()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)
        logger.info('Login > Option now')
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/a')
        element.click()
        time.sleep(2)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[6]/ul/li[4]/a')
        element.click()
        print("language menu now")
        time.sleep(2)
        self.capteure_picture(self, "language")

    def language_english(self):
        select = Select(self.find_element(By.CSS_SELECTOR,'#language_list'))
        select.select_by_value('English')
        time.sleep(2)
        element = self.find_element(By.CSS_SELECTOR, '#main-container > div.main-content > div > div.page-content.animated.fadeInRight > div.page-header > h1 > button')
        element.click()
        time.sleep(5)
        self.capteure_picture(self, "English")

    def language_korean(self):
        select = Select(self.find_element(By.CSS_SELECTOR,'#language_list'))
        select.select_by_value('Korean')
        time.sleep(2)
        element = self.find_element(By.CSS_SELECTOR, '#main-container > div.main-content > div > div.page-content.animated.fadeInRight > div.page-header > h1 > button')
        element.click()
        time.sleep(5)
        self.capteure_picture(self, "Korean")
    ###설정 > 언어 끄읏
    ###설정 > 오디오
    def login_audio(ip, self, username, password):
        self.get(ip)
        # self.get('http://' + input('ip 주소를 입력하세요'))
        time.sleep(5)
        try:
            self.find_element(By.CSS_SELECTOR, '#user').send_keys(username)
            time.sleep(3)
            self.find_element(By.CSS_SELECTOR, '#pwd').send_keys(password)
            time.sleep(3)
            element = self.find_element(By.CSS_SELECTOR, '#login_form > p:nth-child(8) > div > ins')
            element.click()
            self.find_element(By.CSS_SELECTOR, '#login_submit').click()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)
        logger.info('Option Login Complete')
        time.sleep(5)
        element = self.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[3]/a')
        element.click()
        time.sleep(2)
        print("Option > Audio now")
        time.sleep(2)
        self.capteure_picture(self, "audio_default")

    # 오디오 기능 활성화
    def audio_activate(self):
        element = self.find_element(By.XPATH, '//*[@id="main-container"]/div[2]/div/div[2]/div[2]/form/div/div/div[2]/div/div[1]/label/div/ins')
        element.click()
        element = self.find_element(By.CSS_SELECTOR, '#main-container > div.main-content > div > div.page-content.animated.fadeInRight > div.page-header > h1 > button')
        element.click()
        time.sleep(5)
        self.capteure_picture(self, "audio_activated")

    # 오디오 각종 기능 활성화
    def audio_option_check(self):
        select = Select(self.find_element(By.CSS_SELECTOR,'#main-container > div.main-content > div > div.page-content.animated.fadeInRight > div.row > form > div > div > div.widget-body > div > div:nth-child(2) > select'))
        select.select_by_value('G711A')
        time.sleep(2)
        element = self.find_element(By.XPATH, '//*[@id="main-container"]/div[2]/div/div[2]/div[2]/form/div/div/div[2]/div/div[6]/label/div/ins')
        element.click()
        time.sleep(2)
        select = Select(self.find_element(By.CSS_SELECTOR,'#main-container > div.main-content > div > div.page-content.animated.fadeInRight > div.row > form > div > div > div.widget-body > div > div:nth-child(5) > select'))
        select.select_by_value('4.0')
        time.sleep(2)
        select = Select(self.find_element(By.CSS_SELECTOR,'#main-container > div.main-content > div > div.page-content.animated.fadeInRight > div.row > form > div > div > div.widget-body > div > div:nth-child(8) > select'))
        select.select_by_value('4.0')
        time.sleep(2)
        element = self.find_element(By.CSS_SELECTOR, '#main-container > div.main-content > div > div.page-content.animated.fadeInRight > div.page-header > h1 > button')
        element.click()
        time.sleep(5)
        self.capteure_picture(self, "audio_option_check")
    ###설정>오디오 끄읏