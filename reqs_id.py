import requests
import re
from bs4 import BeautifulSoup
import tkinter


def r_id(sf):
    # url = "https://www.luogu.com.cn/problem/list"
    urls = []
    for i in range(1):
        urls.append("https://www.luogu.com.cn/problem/list?difficulty=" + str(i) + "&page=1")

    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3877.400 QQBrowser/10.8.4533.400"
    }
    dif = ["暂无评定", "入门", "普及-", "普及／提高-", "普及+／提高", "提高+／省选-", "省选／NOI-", "NOI／NOI+／CTSC"]
    cnt = 0
    for url in urls:
        print("正在爬取难度为{}的题单".format(dif[cnt]))
        # sf.text.see(tkinter.END)
        resp = requests.get(url, headers=header)
        # print(resp.text)

        page_content = BeautifulSoup(resp.text, "html.parser")
        # print(page_content)
        page_main_content = page_content.find("div", attrs={"class": "lg-container"})

        # print(page_main_content)

        # problem_list = obj.finditer(page_content)
        #
        # for i in problem_list:
        #     print(i.group("name"))
        problem_list = page_main_content.find_all("li")
        # print(problem_list)
        obj = re.compile(r'<li>(?P<id>.*?)<a href=".*?">(?P<name>.*?)</a></li>')
        # print(problem_list)
        # test_str = '<li>P1035 <a href="P1035">[NOIP2002 普及组] 级数求和</a></li>'
        # iterator = obj.finditer(test_str)
        # for i in iterator:
        #     print(i.group("name"))
        with open("difficulty" + str(cnt) + ".txt", mode="w", encoding="utf-8") as f:

            for i in problem_list:
                # print(str(i))
                ite = obj.finditer(str(i))
                for j in ite:
                    print(j.group("id") + ' ' + j.group("name"))
                    # f.write(j.group("id")[1:5] + ' ' + j.group("name") + '\n')
                    f.write(j.group("id")[1:] + '\n')
        cnt += 1

if __name__ == "__main__":
    r_id()