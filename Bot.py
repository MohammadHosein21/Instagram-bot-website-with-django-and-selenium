from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup

IG_URL = 'http://instagram.com/'
TAG_URL = 'http://www.instagram.com/explore/tags/'


class Bot:
    def __init__(self):
        # options = webdriver.ChromeOptions()
        # options.add_argument("headless")
        # self.driver = webdriver.Chrome(executable_path='chromedriver.exe',chrome_options=options)
        self.driver = webdriver.Chrome(executable_path='chromedriver.exe')

    def login(self):
        self.driver.get(IG_URL)
        sleep(1)
        # self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[2]/div/p/a/span").click()

    def enterUsernamePassword(self, username_input, password_input):
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

        page_url = 'https://www.instagram.com/' + page_id
        self.driver.get(page_url)

        followers_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')))
        followers_btn.click()
        sleep(3)

        pup = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div')))

        last_height, current_height = 0, 1

        while last_height != current_height:
            sleep(2)

            last_height = current_height

            current_height = self.driver.execute_script("""
        		arguments[0].scrollTo(0, arguments[0].scrollHeight);
        		return arguments[0].scrollHeight;
        		""", pup)

    def getFollowersNumber(self, page_id):
        page_url = IG_URL + page_id
        self.driver.get(page_url)

        page_content = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#react-root > section > main")))
        slfw = BeautifulSoup(page_content.get_attribute('innerHTML'), 'html.parser')
        num_flw = slfw.findAll('span', {'class': 'g47SY'})
        num = num_flw[1].getText()
        return num

    def followOtherpage(self, tag, amount):
        tag_url = TAG_URL + tag
        self.driver.get(tag_url)
        sleep(7)
        self.driver.find_element_by_class_name('v1Nh3').click()
        sleep(7)
        try:
            btn_view = WebDriverWait(self.driver, 15).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "/html/body/div[4]/div[2]/div/article/div[3]/section[2]/div/span")))
            while (btn_view):
                btn_next = self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow")
                btn_next.click()
                btn_view = WebDriverWait(self.driver, 15).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "/html/body/div[4]/div[2]/div/article/div[3]/section[2]/div/span")))
                sleep(5)
        except TimeoutException:
            btn_follower = WebDriverWait(self.driver, 15).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "/html/body/div[4]/div[2]/div/article/div[3]/section[2]/div/div[2]/button")))
            btn_follower.click()
            sleep(10)
            for i in range(1, amount + 1):
                xpath = "/html/body/div[5]/div/div/div[2]/div/div/div[" + str(i) + "]/div[3]/button"
                btn_follow = WebDriverWait(self.driver, 15).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, xpath)))
                btn_follow.click()
                sleep(10)
                if (i == 10):
                    sleep(60)

# if __name__ == '__main__':
#     bot = Bot()
#     bot.login()
#     bot.enterUsernamePassword(username_input='radiomusighi', password_input='Hosein_77')
# bot.likePhoto("fun", 2)
# bot.getFollowers("mmdhoseinborumnd")
# bot.getFollowersNumber("mmdhoseinborumnd")
# bot.followOtherpage('موسیقی', 1)
