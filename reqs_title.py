import re
import urllib.request,urllib.error
import requests
import bs4
import os
import sys
import tkinter

baseUrl = "https://www.luogu.com.cn/problem/P"
savePath = "F:\\new_MY\\Stu\\软工\\lg\\problems\\"
dif = ["暂无评定", "入门", "普及-", "普及／提高-", "普及+／提高", "提高+／省选-", "省选／NOI-", "NOI／NOI+／CTSC"]

def main_title(rg, sf):
    id_list = [[]]
    print("正在读取题单......")
    for i in range(8):
        id_list.append([])
        with open("difficulty" + str(i) + ".txt") as f:
            x = f.readline()
            # print(x)
            while (x != ""):
                id_list[i].append(int(x[0:4]))
                # print(x[0:4])
                x = f.readline()

    # print("计划爬取共{}级难度的题目".format(len(id_list)-1))
    for i in range(rg, rg+1):
        print("正在爬取题目级别为：{}".format(dif[i]))
        for j in id_list[i]:
            html = getHTML(baseUrl + str(j))
            if html == "error":
                print("爬取失败，可能是不存在该题或无权查看")
            else:
                problemMD = getMD(html)
                print("爬取题目P{}成功！正在保存...".format(j), end="")
                saveData(problemMD, "P" + str(j) + ".md", i, "P" + str(j))
                print("保存成功!")
                # sys.stdout.flush()
            sf.text.see(tkinter.END)

        print("级别为：{}的题目爬取完毕".format(dif[i]))

def getHTML(url):
    headers = {
        "user-agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 85.0.4183.121 Safari / 537.36"
    }
    resp = requests.get(url=url, headers=headers)
    resp.encoding = 'utf-8'
    page_text = resp.text
    # request = urllib.request.Request(url = url,headers = headers)
    # response = urllib.request.urlopen(request)
    # page_content = bs4.BeautifulSoup(resp.text, "html.parser")
    # html = response.read().decode('utf-8')
    if str(page_text).find("Exception") == -1:        #洛谷中没找到该题目或无权查看的提示网页中会有该字样
        return resp.text
    else:
        return "error"

def getMD(html):
    bs = bs4.BeautifulSoup(html, "html.parser")
    x = bs.select("article")
    if len(x) > 0:
        core = x[0]
        # print(core)
        md = str(core)
        md = re.sub("\$", "", md)
        md = re.sub("<h1>", "# ", md)
        md = re.sub("<h2>", "## ", md)
        md = re.sub("<h3>", "#### ", md)
        md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
        return md
    else:
        return ""

def saveData(data,filename,dif_n,id):
    cfilename = savePath + dif[dif_n] + "\\" + id + "\\" + filename
    if not os.path.exists(savePath + dif[dif_n] + "/" + id):
        os.makedirs(savePath + dif[dif_n] + "/" + id)
    with open(cfilename, "w", encoding="utf-8") as f:
        for d in data:
            f.writelines(d)
        f.close()
