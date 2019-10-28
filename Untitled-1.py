from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog

from bs4 import BeautifulSoup

import time

firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
driver = webdriver.Firefox(firefox_profile=firefox_profile)

actions = ActionChains(driver)
wait = WebDriverWait(driver, 20)

url = "https://www.okcupid.com/questions?rqid="
num = 1


class get_Login:
    global usrname, pwd
    def __init__(self):
        self.root = Tk()
        self.label = Label(self.root, text="Enter your OKCupid login")
        self.label.pack(side=TOP)
        self.usrlabel = Label(self.root, text="Email:")
        self.usrlabel.pack()
        self.f = Entry(self.root)
        self.f.pack()
        self.pwdlabel = Label(self.root, text="Password:")
        self.pwdlabel.pack()
        self.e=Entry(self.root, show="*")
        self.e.pack()
        self.button = Button(self.root, text="Go", command=self.get_creds)
        self.button.pack()
        self.root.attributes("-topmost", True)
        self.root.mainloop()

    def get_creds(self):
        globals()["username"] = self.f.get()
        globals()["password"] = self.e.get()

        driver.get(url+"1")
        time.sleep(2)
        username_field = driver.find_element_by_class_name("login2017-username")
        password_field = driver.find_element_by_class_name("login2017-password")

        username_field.send_keys(username)
        driver.implicitly_wait(1)

        password_field.send_keys(password)
        driver.implicitly_wait(1)

        driver.find_element_by_css_selector(".banner-close-button").click()
        driver.implicitly_wait(2)

        time.sleep(2)
        driver.find_element_by_class_name("login2017-actions-button").click() #log in

        self.root.destroy()

app = get_Login()
# print(username, password)
f = open("okc_questions.txt", "a")

def session_cycle(usrname=username, psswrd=password):
    driver.quit()
    driver = webdriver.Firefox(firefox_profile=firefox_profile)

    driver.get(url+"1")
    time.sleep(2)
    username_field = driver.find_element_by_class_name("login2017-username")
    password_field = driver.find_element_by_class_name("login2017-password")

    username_field.send_keys(username)
    driver.implicitly_wait(1)

    password_field.send_keys(password)
    driver.implicitly_wait(1)

    driver.find_element_by_css_selector(".banner-close-button").click()
    driver.implicitly_wait(2)

    time.sleep(2)
    driver.find_element_by_class_name("login2017-actions-button").click()

def get_question(num, f=f, _await_val="question"):
    driver.get(url+str(num))

    if _await_val=="question":
        await_val = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "questionspage-multipartquestion-questiontext")))
    elif _await_val=="answers":
        await_val = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "questionspage-multipartquestion-answers-answer-label")))
    else: raise EXCEPTION

    ActionChains(driver).move_to_element(await_val).perform()
    soup = BeautifulSoup(driver.page_source, features="lxml")
    question = soup.find("h1", "questionspage-multipartquestion-questiontext").get_text()
    answers = [a.get_text() for a in soup.find_all("div", "questionspage-multipartquestion-answers-answer-label")]
    ans_str = '"'+'", "'.join(answers)+'"'
    f.write(str(num)+':{question: "'+question+'", answers:{'+ans_str+'}}\n')

for num in range(3031, 464459, 1):
    try:
        get_question(num)
    except ConnectionRefusedError:
        session_cycle()
        get_question(num)
    except TimeoutException:
        get_question(num, _await_val="answers")
