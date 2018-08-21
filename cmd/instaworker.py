"""
A python worker script :

Before run:
    * install all dependencies (project root folder) : pip3 install -r requirements.txt

    * setup the configuration
        * User and password as plain text
        * List of profiles to be scanned

    * go to the folder drivers and unzip the driver and change the variable webdriver_location , with the .exe file

    * RUN:
    python3 instaworker.py

"""
import os
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Config:
    INSTA_BASE_URL = "https://www.instagram.com/"
    LOGON_URL = INSTA_BASE_URL + "accounts/login/"
    # coloque os perfis
    PROFILES = ["tattoo4us", "monstrustattoobrasil"]
    USER = "<coloque aqui o usuario>"
    PWD = "coloque aqui a senha"


class Css:
    USERNAME_FIELD = "input[name='username']"
    PASSWORD_FIELD = "input[name='password']"
    LOGIN_BUTTON = "button"
    FOLLOWERS_LINK = "//a[contains(@href, {}/followers)]"
    FOLLOW_BUTTON = "//ul//button[ text() = 'Follow' or text() = 'Seguir' ]"
    CLOSE_MODAL_BUTTON = "//button[contains(text(), 'Close') or contains(text(), 'Fechar')]"
    IFRAME_END_LIST = "//iframe[title='Intentionally left blank']"


class InstaWorker:
    logger = None
    dir_path = None
    driver = None

    # maximo timeout to waiting an element be printed
    TIMEOUT = 20

    def __init__(self):
        self.set_up()

    def set_up(self):
        print("Set up called ")
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        webdriver_location = self.dir_path + "/../drivers/chromedriver"
        self.driver = webdriver.Chrome(executable_path=webdriver_location)

    def send_invites(self):
        print("invite called ")
        driver = self.driver

        self.do_login(driver)
        time.sleep(2)

        self.spy_profiles_pages(driver)

        time.sleep(10)
        driver.close()
        return None

    # open profiles page and invite all followers
    def spy_profiles_pages(self, driver):

        for profile in Config.PROFILES:
            # build profile url and open page
            profile_url = Config.INSTA_BASE_URL + profile
            print("Working on : {}".format(profile_url))
            time.sleep(5)
            driver.get(profile_url)
            time.sleep(1)

            # wait and click on followers link
            self.click_followers_link(profile)

            # click in all followers
            self.click_in_all_followers()


    # do insta login
    def do_login(self, driver):
        # open logon page
        driver.get(Config.LOGON_URL)

        # fill username and password
        self.fill_textbox(Css.USERNAME_FIELD, Config.USER)
        self.fill_textbox(Css.PASSWORD_FIELD, Config.PWD)

        # sleep to avoid block
        time.sleep(1)
        self.click_button(Css.LOGIN_BUTTON)

    # fill a text box
    def fill_textbox(self, css_path, value):
        WebDriverWait(self.driver, timeout=self.TIMEOUT) \
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, css_path)))
        field = self.driver.find_element(By.CSS_SELECTOR, css_path)
        field.send_keys(value)

    # load and send click to a button
    def click_button(self, css_path):
        WebDriverWait(self.driver, timeout=self.TIMEOUT) \
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, css_path)))
        button = self.driver.find_element(By.CSS_SELECTOR, css_path)
        button.click()

    def click_in_all_followers(self):

        # sleep to avoid authentication error
        time.sleep(2)

        # wait using close button, because profile
        # may have followers
        WebDriverWait(self.driver, timeout=self.TIMEOUT) \
            .until(EC.presence_of_element_located((By.XPATH, Css.CLOSE_MODAL_BUTTON)))

        time.sleep(2)

        # find all follow buttons and click follow
        buttons = self.driver.find_elements_by_xpath(Css.FOLLOW_BUTTON)
        for button in buttons:
            if button.is_displayed() and button.is_enabled():
                button.click()
                time.sleep(0.4)

        # find close modal button and click
        # before move to the next profile
        close_button = self.driver.find_element_by_xpath(Css.CLOSE_MODAL_BUTTON)
        close_button.click()

    def click_followers_link(self, profile):
        f_profile = Css.FOLLOWERS_LINK.format(profile)
        WebDriverWait(self.driver, timeout=self.TIMEOUT) \
            .until(EC.presence_of_element_located((By.XPATH, f_profile)))

        button = self.driver.find_element(By.XPATH, f_profile)
        button.click()


if __name__ == "__main__":
    worker = InstaWorker()
    try:
        worker.send_invites()
    except Exception as e:
        print(e.__cause__)
        worker.driver.close()
