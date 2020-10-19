from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup

IG_URL = 'http://instagram.com/'
TAG_URL = 'http://www.instagram.com/explore/tags/'


class Bot:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='chromedriver.exe')

    def login(self):
        self.driver.get(IG_URL)
        sleep(1)
        # self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[2]/div/p/a/span").click()

    def enterUsernamePassword(self,username_input,password_input):
        username = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, "div.-MzZI:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)")))
        # username = self.driver.find_element_by_css_selector(
        #     "div.-MzZI:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)")
        username.click()
        username.send_keys(username_input)
        password = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, "div.-MzZI:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)")))
        password.click()
        password.send_keys(password_input)
        btn_login = self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div")
        btn_login.click()
        sleep(10)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button").click()
        sleep(15)
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()

    def likePhoto(self, tag, count):
        tag_url = TAG_URL + tag
        self.driver.get(tag_url)
        sleep(5)
        self.driver.find_element_by_class_name('v1Nh3').click()
        sleep(7)
        x = 0
        while (x < count):
            btn_like = self.driver.find_element_by_xpath(
                "/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button")
            btn_like.click()
            sleep(5)
            btn_next = self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow")
            btn_next.click()
            sleep(5)
            x += 1

    def getFollowers(self, page_id):
        page_url = IG_URL + page_id
        self.driver.get(page_url)

        btn_followers = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")))
        btn_followers.click()
        sleep(3)

        pup = WebDriverWait(self.driver, 10).until(
            (expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div"))))

        last_height, current_height = 0, 1

        while last_height != current_height:
            sleep(2)
            last_height = current_height
            current_height = self.driver.execute_script(
                """arguments[0].scrollTo(0,arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;""", pup)

    def getFollowersNumber(self, page_id):
        page_url = IG_URL + page_id
        self.driver.get(page_url)

        page_content = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#react-root > section > main")))
        slfw = BeautifulSoup(page_content.get_attribute('innerHTML'), 'html.parser')
        num_flw = slfw.findAll('span', {'class': 'g47SY'})
        num = num_flw[1].getText()
        return num


# if __name__ == '__main__':
#     bot = Bot()
#     bot.login()
#     bot.enterUsernamePassword()
#     # bot.likePhoto("fun", 2)
#     # bot.getFollowers("mmdhoseinborumnd")
#     bot.getFollowersNumber("mmdhoseinborumnd")
