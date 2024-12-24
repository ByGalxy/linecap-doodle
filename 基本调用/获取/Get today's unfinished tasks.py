import requests
import json
from datetime import datetime, timedelta

def get_unfinished_tasks():
    # 改成你的目标URL
    url = "http://172.24.21.9:13276/tasks"

    # 发送GET请求
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析JSON数据
        data = response.json()
        
        # 获取今天的日期
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 转换今天的日期为时间戳
        today_timestamp = int(datetime.now().timestamp() * 1000)
        
        # 筛选今天未完成的任务
        unfinished_tasks = []
        for task in data['data']:
            # 检查任务是否未完成且今天到期
            if task['status'] == 0 and today == datetime.fromtimestamp(task['deadline'] / 1000).strftime('%Y-%m-%d'):
                unfinished_tasks.append(task)
        
        # 如果有未完成的任务，返回True
        if unfinished_tasks:
            for task in unfinished_tasks:
                print(f"任务名称: {task['name']}, 截止时间: {datetime.fromtimestamp(task['deadline'] / 1000).strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        else:
            print("今天没有未完成的任务。")
            return False
    else:
        print("请求失败，请检查URL或网络连接。")
        return False

# 调用函数
get_unfinished_tasks()
