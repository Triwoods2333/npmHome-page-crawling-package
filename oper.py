from playwright.sync_api import sync_playwright
import subprocess
import pandas as pd
from datetime import datetime
import time


def find_matching_indexes(list1, list2):
    matching_indexes = [i for i, item in enumerate(list1) if item in list2]
    return matching_indexes


def get_duplicate_indexes(df, names, publishs):
    # 将"name"列和"publish"列的值转换为字符串
    df_values = df['name'].astype(str) + df['publish'].astype(str)
    combined_values = [name + publish for name, publish in zip(names, publishs)]
    # 找到重复项的索引
    df_values_list = df_values.values.tolist()
    # 判断两个列表中是否有相同元素，并获取它们的位置
    matching_indexes = find_matching_indexes(combined_values, df_values_list)

    return matching_indexes


def remove_elements_by_index(*lists, indexes):
    # 根据索引删除元素
    for lst in lists:
        for i in sorted(indexes, reverse=True):
            del lst[i]


def download_source_code(package_name, download_path):
    command = f"npm pack {package_name}"
    subprocess.run(command, shell=True, cwd=download_path)


def task():
    # 在这里编写想要定时运行的任务代码
    print("定时任务执行")
    df = pd.read_csv('C:/Users/97091/Desktop/getgithub/file/result.csv',encoding='utf-8')

    # 获取当前时间
    current_time = datetime.now()
    print("当前时间：", current_time)

    names = []
    publishs = []
    times = []
    current_times = []
    # 指定要下载源代码的npm软件包名称和下载位置
    download_path = 'C:/Users/97091/Desktop/getgithub/npm_download'

    p = sync_playwright().start()
    browser = p.chromium.launch_persistent_context(
        # 指定本机用户缓存地址
        user_data_dir=f"C:/Users/97091/Desktop",
        # 接收下载事件
        accept_downloads=True,
        # 设置 GUI 模式
        headless=False,
        bypass_csp=True,
        slow_mo=1000,
        channel="chrome"
    )
    page = browser.pages[0]
    url = "https://www.npmjs.com/"
    page.goto(url)
    time.sleep(3)

    lis = page.query_selector('ul[aria-labelledby="recently-updated-packages-header"]').query_selector_all('li')
    print(len(lis))
    for li in lis:
        names.append(li.query_selector('h3').inner_text())
        content = li.query_selector('span[aria-hidden="true"]').inner_text()
        publishs.append(content.split(' • ')[0])
        times.append(content.split(' • ')[1])
        current_times.append(current_time)
    browser.close()

    # 判断是否有重复值
    duplicate_indexes = get_duplicate_indexes(df, names, publishs)
    print(duplicate_indexes)
    # 根据索引删除元素
    remove_elements_by_index(names, publishs, times, current_times, indexes=duplicate_indexes)
    print(len(names))

    download_paths = []
    for index, name in enumerate(names):
        # 调用命令行下载源代码并设置下载位置
        print(name)
        download_source_code(name, download_path)
        download_paths.append(
            download_path + '/' + name.replace('@', '').replace('/', '-') + '-' + publishs[index].split(' ')[
                1] + '.tgz')

    new_dict = {}
    new_dict['name'] = names
    new_dict['publish'] = publishs
    new_dict['time'] = times
    new_dict['current_time'] = current_times
    new_dict['download'] = download_paths

    df1 = pd.DataFrame.from_dict(new_dict)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_csv('C:/Users/97091/Desktop/getgithub/file/result.csv', index=False)


# 设置定时任务的时间间隔（以秒为单位）
interval = 60 * 60 * 24

while True:
    # 执行任务
    task()

    # 等待指定的时间间隔
    time.sleep(interval)
