from instapy import InstaPy
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import schedule

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

    def enterUsernamePassword(self, username_input, password_input):
        username = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, "div.-MzZI:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)")))
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

    def getFollowersNumber(self, page_id):
        page_url = IG_URL + page_id
        self.driver.get(page_url)
        page_content = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#react-root > section > main")))
        slfw = BeautifulSoup(page_content.get_attribute('innerHTML'), 'html.parser')
        num_flw = slfw.findAll('span', {'class': 'g47SY'})
        num = num_flw[1].getText()
        return num

    def followOtherpage(self, tag):
        tag_url = TAG_URL + tag
        self.driver.get(tag_url)
        sleep(7)
        self.driver.find_element_by_class_name('v1Nh3').click()
        sleep(7)
        flag = True
        while flag == True:
            try:
                btn_follower = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "/html/body/div[4]/div[2]/div/article/div[3]/section[2]/div/div[2]/button")))
                btn_follower.click()
                sleep(10)
                i = 1
                while i <= 7:
                    xpath = "/html/body/div[5]/div/div/div[2]/div/div/div[" + str(i) + "]/div[3]/button"
                    btn_follow = WebDriverWait(self.driver, 10).until(
                        expected_conditions.presence_of_element_located(
                            (By.XPATH, xpath)))
                    text = btn_follow.text
                    if text == "Follow":
                        btn_follow.click()
                    i += 1
                    sleep(5)
                    if (i == 7):
                        like_list = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
                        actionChain = webdriver.ActionChains(self.driver)
                        sleep(4)
                        actionChain.key_down(Keys.SPACE).perform()
                        for c in range(6):
                            j = 6
                            while (j <= 12):
                                xpath = "/html/body/div[5]/div/div/div[2]/div/div/div[" + str(j) + "]/div[3]/button"
                                btn_follow = WebDriverWait(self.driver, 10).until(
                                    expected_conditions.presence_of_element_located(
                                        (By.XPATH, xpath)))
                                text = btn_follow.text
                                if text == "Follow":
                                    btn_follow.click()
                                j += 1
                                sleep(5)
                            like_list = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
                            actionChain = webdriver.ActionChains(self.driver)
                            sleep(4)
                            actionChain.key_down(Keys.SPACE).perform()
                        i += 1
                flag = False
            except TimeoutException:
                btn_next = self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow")
                btn_next.click()
                sleep(5)

    def postComment(self, tag, comment):
        tag_url = TAG_URL + tag
        self.driver.get(tag_url)
        sleep(7)
        self.driver.find_element_by_class_name('v1Nh3').click()
        sleep(7)
        i = 0
        while (i < 15):
            try:
                btn_comment = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[2]/button")))
                btn_comment.click()
                comment_box = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "/html/body/div[4]/div[2]/div/article/div[3]/section[3]/div/form/textarea")))
                comment_box.send_keys(comment)
                sleep(5)
                btn_postComment = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "/html/body/div[4]/div[2]/div/article/div[3]/section[3]/div/form/button")))
                btn_postComment.click()
                sleep(5)
                btn_next = self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow")
                btn_next.click()
                sleep(5)
                i += 1
            except TimeoutException:
                btn_next = self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow")
                btn_next.click()
                sleep(5)

    def unfollow(self, page_id):
        page_url = IG_URL + page_id
        self.driver.get(page_url)
        sleep(5)
        btn_following = self.driver.find_element_by_partial_link_text('following')
        btn_following.click()
        sleep(5)
        WebDriverWait(self.driver, 10).until(lambda d: d.find_element_by_css_selector('div[role="dialog"]'))
        for i in range(300):
            self.driver.execute_script('''
            var fDialog = document.querySelector('div[role="dialog"] .isgrP');
            fDialog.scrollTop = fDialog.scrollHeight
            ''')
        for i in range(10):
            for i in range(10):
                self.driver.find_element_by_xpath('//button[text()="Following"]').click()
                self.driver.find_element_by_xpath('//button[text()="Unfollow"]').click()
                sleep(5)
            WebDriverWait(self.driver, 10).until(lambda d: d.find_element_by_css_selector('div[role="dialog"]'))
            for i in range(5):
                self.driver.execute_script('''
                var fDialog = document.querySelector('div[role="dialog"] .isgrP');
                fDialog.scrollTop = fDialog.scrollHeight
                ''')


if __name__ == '__main__':
    bot = Bot()
    bot.login()
    bot.enterUsernamePassword(username_input='radiomusighi', password_input='Hosein_77')


    def task():
        bot.unfollow('radiomusighi')
        bot.likePhoto("", 1)
        bot.postComment("", "")
        bot.getFollowersNumber(page_id="page")
        bot.followOtherpage("")


    schedule.every(10).seconds.do(task)
    while True:
        schedule.run_pending()
        sleep(1)

    # bot.login()
    # bot.enterUsernamePassword(username_input='radiomusighi', password_input='Hosein_77')
    # bot.unfollow('radiomusighi')
#     bot.postComment("موسیقی", "ممنون میشم مارو دنبال کنید")
#     bot.likePhoto()
#     bot.getFollowers()
#     bot.getFollowersNumber()
#     bot.followOtherpage("")
