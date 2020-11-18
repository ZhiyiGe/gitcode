import requests
from urllib.request import urlretrieve
import os
from tkinter import *
from tkinter.filedialog import askdirectory


# 获取网址的HTML,再return给正则函数
def get_html(url):
    r = requests.get(url)
    return r.text


# 用正则库解析HTML,获取网页中文件的url,再return给下载函数
def get_url(html):
    urls = re.findall('<a class="js-navigation-open"[^>]+href=["\'](.*?)["\']', html, re.S | re.M)
    titles = re.findall('<a class="js-navigation-open" title="(.*?)"', html, re.S | re.M)
    return urls, titles


# 判断是否文件夹,True是文件夹,False不是,警告:该判断仅利用是否为 .字母 结尾来判断是否为文件夹,存在缺陷,有可能误判
def judge(title):
    pattern = '[\w.]+\.\w+'
    if re.findall(pattern, title) == []:
        return True
    else:
        return False


# 文件夹处理
def folders(folderUrl, folderTitle, oldPath):
    print('下载 ' + folderTitle + ' 文件夹')
    savepath = str(oldPath) + '/' + folderTitle
    os.makedirs(savepath)
    # os.mkdir(savepath)
    html = get_html(folderUrl)
    urls, titles = get_url(html)
    for url, title in zip(urls, titles):
        oldurl = 'https://github.com' + url
        pattern = re.compile('/blob')
        url = pattern.sub('', url)
        print(title)
        if judge(title) == False:
            download('https://raw.githubusercontent.com' + url, title, savepath)
        else:
            folders(oldurl, title, savepath)


# 将一个网页中的文件全部下载,不考虑文件夹
def download(url, title, savepath='./'):
    def reporthook(a, b, c):
        # 显示下载进度
        if c != 0:
            print("\rdownloading: %5.1f%%" % (a * b * 100.0 / c), end="")

    # filename = os.path.basename(url)
    filename = title
    # 判断文件是否存在，如果不存在则下载
    if not os.path.isfile(os.path.join(savepath, filename)):
        print('Downloading data from %s' % url)
        urlretrieve(url, os.path.join(savepath, filename), reporthook=reporthook)
        print('\nDownload finished!')
    else:
        print('File already exsits!')
    # 获取文件大小
    filesize = os.path.getsize(os.path.join(savepath, filename))
    # 文件大小默认以Bytes计， 转换为Mb
    print('File size = %.2f Mb' % (filesize / 1024 / 1024))


# 选择存储位置
def selectPath():
    global path_  # 全局
    path_ = askdirectory()
    path.set(path_)


# achieve_url=StringVar()
# 按扭调用的下载函数，得到url和路径之后通过此函数进行下载
def guiDownload():
    achieve_url = e_url.get()
    html = get_html(achieve_url)
    urls, titles = get_url(html)
    savepath = path_
    for url, title in zip(urls, titles):
        oldurl = 'https://github.com' + url
        pattern = re.compile('/blob')
        url = pattern.sub('', url)
        url = 'https://raw.githubusercontent.com' + url
        if judge(title):
            download(url, title, savepath)
        else:
            folders(oldurl, title, savepath)


# Tkinter图形界面
root = Tk()
root.title('Github一键下载器')
path = StringVar()
path_cun = StringVar()

# 第一行，下载地址标签及输入框
l_url = Label(root, text='下载地址')
l_url.grid(row=0, sticky=W)
e_url = Entry(root)
e_url.grid(row=0, column=1, sticky=E)

# 第二行,目标路径标签及路径选择按钮
Label(root, text="目标路径:").grid(row=1, column=0)
Entry(root, textvariable=path).grid(row=1, column=1)
Button(root, text="路径选择", command=selectPath).grid(row=1, column=2)

# 第三行登陆按扭，command绑定事件,激发下载事件
b_login = Button(root, text='下载', command=guiDownload)
b_login.grid(row=2, column=0, sticky=E)

root.mainloop()

