import html2text
import selenium, time, pyperclip, pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import tkinter
import re
import urllib.request, urllib.error
import requests
import bs4
import os
from PIL import ImageTk, Image

def t_get_captcha(captcha_entry, window, testinput):
    # 获取输入的验证码
    captcha = captcha_entry.get()
    # 在这里可以使用输入的验证码进行后续处理
    print("输入的验证码：", captcha)
    # 输入验证码到网页
    testinput.click()
    testinput.send_keys(str(captcha))
    testinput.send_keys(Keys.ENTER)

    # 关闭窗口
    window.destroy()

def main_solve(sf):
    root = tkinter.Tk()

    # 定义区
    browser = webdriver.Chrome()
    browser.minimize_window()  # 最大化窗口
    wait = WebDriverWait(browser, 10)  # 等待加载10s

    # from selenium.webdriver.support import expected_conditions as EC
    # from selenium.common.exceptions import TimeoutException, NoSuchElementException
    safari = webdriver.Chrome()
    safari.get("https://www.luogu.com.cn/auth/login")
    safari.minimize_window()
    WebDriverWait(safari, 5)

    baseUrl = "https://www.luogu.com.cn/problem/solution/P"
    savePath = "F:\\new_MY\\Stu\\软工\\lg\\problems\\"
    dif = ["暂无评定", "入门", "普及-", "普及／提高-", "普及+／提高", "提高+／省选-", "省选／NOI-", "NOI／NOI+／CTSC"]

    id_list = [[]]
    for i in range(1, 2):
        id_list.append([])
        with open("difficulty" + str(i) + ".txt") as f:
            x = f.readline()
            while (x != ""):
                id_list[i].append(int(x[0:4]))
                # print(x[0:4])
                x = f.readline()

    # login()
    print("请输入验证码：\n")
    t = ""
    time.sleep(20)
    userinput = safari.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div/div/div/div/div/div/div[1]/div/input')
    passinput = safari.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div/div/div/div/div/div/div[2]/div/input')
    testinput = safari.find_element(By.XPATH,
                                    '//*[@id="app"]/div[2]/main/div/div/div/div/div/div/div[3]/div/div[1]/input')
    # loginlogo=safari.find_element(By.XPATH,'//*[@id="app"]/div[2]/main/div/div/div/div/div/div/button')
    userinput.click()
    userinput.send_keys("18650697758")
    passinput.click()
    passinput.send_keys("qj030504")

    # 获取验证码图片
    screenshot_filename = "screenshot.png"
    safari.save_screenshot(screenshot_filename)
    captcha_input = safari.find_element(By.XPATH,
                                        '//*[@id="app"]/div[2]/main/div/div/div/div/div/div/div[3]/div/div[1]/input')
    captcha_location = captcha_input.location
    captcha_size = captcha_input.size
    captcha_x = captcha_location['x']
    captcha_y = captcha_location['y']
    captcha_width = captcha_size['width']
    captcha_height = captcha_size['height']

    # 裁剪验证码图片
    captcha_image = Image.open(screenshot_filename)
    captcha_image = captcha_image.crop(
        (captcha_x + 70, captcha_y + 70, captcha_x + captcha_width + 400, captcha_y + captcha_height + 200))

    # 显示验证码图片
    captcha_photo = ImageTk.PhotoImage(captcha_image)
    captcha_label = tkinter.Label(root, image=captcha_photo)
    captcha_label.pack()

    # 创建验证码输入框
    captcha_entry = tkinter.Entry(root)
    captcha_entry.pack()

    # 创建提交按钮
    submit_button = tkinter.Button(root, text="提交", command=lambda: t_get_captcha(captcha_entry, root, testinput))
    submit_button.pack()


    WebDriverWait(safari, 5)
    time.sleep(5)

    print("计划爬取共{}级难度的题解".format(len(id_list) - 1))
    for i in range(1, 2):
        print("正在爬取级别为：{}的题解".format(dif[i]))
        for j in id_list[i]:
            try:
                safari.get(baseUrl + str(j))
                WebDriverWait(safari, 20)
                time.sleep(1)
                mark_text = safari.find_element(By.CSS_SELECTOR,
                                                '#app > div.main-container > main > div > section.main > div > div.card-body > div > div.block > div > div:nth-child(1) > div > div.main > div.collapsed-wrapper > div > div')
                time.sleep(2)
                text = mark_text.get_attribute("innerHTML")
                text = html2text.html2text(text)
                """
                # text = re.sub("\$", " ", text)
                # text = re.sub("代码", " ", text)
                text = re.sub("<h1>", "# ", text)
                text = re.sub("<h2>", "## ", text)
                text = re.sub("<h3>", "#### ", text)
                text = re.sub("</?[a-zA-Z]+[^<>]*>", "", text)
                """
                # print(text)
                time.sleep(1.5)
                print("爬取P{}的题解成功！正在保存...".format(j), end="")
                cfilename = savePath + str(dif[i]) + "\\P" + str(j) + "\\" + "题解：P" + str(j) + ".md"
                if not os.path.exists(savePath + str(dif[i]) + "/P" + str(j)):
                    os.makedirs(savePath + str(dif[i]) + "/P" + str(j))
                with open(cfilename, "w", encoding="utf-8") as f:
                    f.writelines(text)
                    f.close()
                print("保存成功!")
            except WebDriverException as e:
                print("该题暂未有题解")
            finally:
                sf.text.see(tkinter.END)
                time.sleep(2.5)
        print("题目级别为：{}的题解爬取完毕".format(dif[i]))
    safari.quit()