import tkinter as tk
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
        task_notes = random_task.get('notes', '')
        task_deadline = datetime.fromtimestamp(random_task['deadline'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

        # 创建一个新的窗口
        reminder_window = tk.Toplevel()
        reminder_window.title("未完成任务提醒")
        reminder_window.geometry("300x180")

        # 设置窗口位置到屏幕左上角
        reminder_window.geometry(f"300x180+0+0")  # 窗口左上角位置

        # 禁止缩放并隐藏窗口栏
        reminder_window.resizable(False, False)
        reminder_window.overrideredirect(True)

        # 设置窗口透明度
        reminder_window.attributes('-alpha', 0.9)

        # 使用grid布局调整控件
        label_title = tk.Label(reminder_window, text="任务提醒", font=("Arial", 14, "bold"), fg="#007BFF")
        label_title.grid(row=0, column=0, pady=5)

        # 任务名
        label_task = tk.Label(reminder_window, text=f"任务：{task_name}", wraplength=280, font=("Arial", 12))
        label_task.grid(row=1, column=0, pady=2)

        # 截止时间
        label_deadline = tk.Label(reminder_window, text=f"截止时间：{task_deadline}", wraplength=280, font=("Arial", 10))
        label_deadline.grid(row=2, column=0, pady=2)

        # 备注（仅在备注不为空时显示）
        if task_notes:
            label_notes = tk.Label(reminder_window, text=f"备注：{task_notes}", wraplength=280, font=("Arial", 10))
            label_notes.grid(row=3, column=0, pady=2)

        # 确认按钮
        button = tk.Button(reminder_window, text="知道了", command=reminder_window.destroy)
        button.grid(row=4, column=0, pady=10)

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
root.withdraw()  # 隐藏主窗口

# 通过创建透明Toplevel窗口避免任务栏显示
root.protocol("WM_DELETE_WINDOW", lambda: None)  # 禁止主窗口关闭

# 检查是否有未完成的任务，如果有，则开始提醒
if unfinished_tasks:
    show_random_task()

# 启动主事件循环
root.mainloop()
