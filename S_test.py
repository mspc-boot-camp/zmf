import requests
import json
import os  # path
import threading

def get_path(path, name):
    path = path + name

    if not os.path.exists(path):
        os.mkdir(path)  # make directory
    return path


def get_a(url,header,param):
    response = requests.get(url=url, headers=header, params=param)  # 得到网页内容
    response.encoding = 'utf-8'
    response = response.text  # 转换为string
    data_s = json.loads(response)   # 把字符串转换成json数据
    a = data_s["data"]  # 提取data里的数据
    return a


def get_image_url(a):
    image_url = list()
    for i in range(len(a) - 1):  # 去掉最后一个空数据
        data = a[i].get("thumbURL", "not exist")  # 防止报错 key error
        image_url.append(data)  # append 尾插字符串 将图片的链接给到image_url的列表中
    return image_url


def get_save(image_url, header, path, n):

    for image_src in image_url:
        image_data = requests.get(url=image_src, headers=header).content  # 提取图片内容数据
        image_name = '{}'.format(n + 1) + '.jpg'  # 图片名
        image_path = path + '/' + image_name  # 图片保存路径
        with open(image_path, 'wb') as f:  # 保存数据
            f.write(image_data)
            print(image_name, '下载成功啦！！！')
            f.close()
        n += 1
    return n


def get_all(name, keyword, page):
    # name = "xiaohuamao"
    path = 'E:/Code/'
    path = get_path(path, name)

    url = 'https://image.baidu.com/search/acjson?'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'}
    # keyword = input('请输入你想下载的内容：')
    # page = input('请输入你想爬取的页数：')
    page = int(page) + 1

    n = 0
    pn = 1

    for _ in range(1, page):

        param = {
            'tn': 'resultjson_com',
            'logid': ' 7517080705015306512',
            'ipn': 'rj',
            'ct': '201326592',
            'is': '',
            'fp': 'result',
            'queryWord': keyword,
            'cl': '2',
            'lm': '-1',
            'ie': 'utf-8',
            'oe': 'utf-8',
            'adpicid': '',
            'st': '',
            'z': '',
            'ic': '',
            'hd': '',
            'latest': '',
            'copyright': '',
            'word': keyword,
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': '',
            'istype': '',
            'qc': '',
            'nc': '1',
            'fr': '',
            'expermode': '',
            'force': '',
            'cg': 'star',
            'pn': pn,
            'rn': '30',
            'gsm': '1e',
        }


        a = get_a(url, header, param)
        image_url = get_image_url(a)
        n =get_save(image_url, header, path, n)

        pn += 29

class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, keyword, page):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.keyword = keyword
        self.page = page
        get_all(self.name, self.keyword, self.page)

if __name__ == '__main__':

    keyword_1 = input('请输入你想下载的内容：')
    page_1 = input('请输入你想爬取的页数：')

    # keyword_2 = input('请输入你想下载的内容：')
    # page_2 = input('请输入你想爬取的页数：')

    thread_cat = myThread(1, "小花猫", keyword_1, page_1)
    # thread_dog = myThread(2, "真狗啊", keyword_2, page_2)

    thread_cat.start()
    # thread_dog.start()
    thread_cat.join()
    # thread_dog.join()

    print('主程序结束')
