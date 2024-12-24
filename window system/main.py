import tkinter as tk
import tkintertools as tkt
from tkinter import messagebox
import requests
import json
from datetime import datetime
import random

# 全局变量，存储未完成的任务列表
unfinished_tasks = []

def fetch_unfinished_tasks():
    global unfinished_tasks  # 声明unfinished_tasks为全局变量
    url = "http://172.24.21.9:13276/tasks"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        today = datetime.now().strftime('%Y-%m-%d')
        unfinished_tasks = [task for task in data['data'] if
                            task['status'] == 0 and today == datetime.fromtimestamp(task['deadline'] / 1000).strftime(
                                '%Y-%m-%d')]
    else:
        print("请求失败，请检查URL或网络连接。")

def show_random_task():
    global unfinished_tasks  # 声明unfinished_tasks为全局变量
    if unfinished_tasks:  # 如果还有未完成的任务
        random_task = random.choice(unfinished_tasks)
        unfinished_tasks.remove(random_task)  # 显示后从列表中移除
        task_name = random_task['name']
        task_notes = random_task.get('notes', '无备注')
        task_deadline = datetime.fromtimestamp(random_task['deadline'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

        # 创建一个新的窗口
        reminder_window = tk.Toplevel()
        reminder_window.title("未完成任务提醒")
        reminder_window.geometry("350x250")

        label_title = tk.Label(reminder_window, text="任务提醒", font=("Arial", 16, "bold"), fg="#007BFF")
        label_title.pack(pady=10)

        label_task = tk.Label(reminder_window, text=f"任务：{task_name}", wraplength=320, font=("Arial", 12))
        label_task.pack(pady=5)

        label_deadline = tk.Label(reminder_window, text=f"截止时间：{task_deadline}", wraplength=320, font=("Arial", 11))
        label_deadline.pack(pady=5)

        label_notes = tk.Label(reminder_window, text=f"备注：{task_notes}", wraplength=320, font=("Arial", 11))
        label_notes.pack(pady=5)

        # 分隔线
        separator = tk.Frame(reminder_window, height=1, bg="#CCCCCC", bd=0, relief="flat")
        separator.pack(fill="x", padx=10, pady=10)

        # 按钮
        button = tk.Button(reminder_window, text="知道了", command=reminder_window.destroy)
        button.pack(pady=10)

        reminder_window.lift()  # bring to top
        reminder_window.attributes('-topmost', True)  # stay on top

        # 5分钟后再次提醒
        reminder_window.after(300000, show_random_task)
    else:
        # 如果所有任务都已提醒过，重新开始新一轮提醒
        fetch_unfinished_tasks()  # 重新获取任务列表
        show_random_task()  # 开始新一轮提醒

# 首先获取未完成的任务列表
fetch_unfinished_tasks()

# 创建主窗口并隐藏
root = tk.Tk()
root.withdraw()

# 检查是否有未完成的任务，如果有，则开始提醒
if unfinished_tasks:
    show_random_task()

# 启动主事件循环
root.mainloop()
