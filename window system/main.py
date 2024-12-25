import tkintertools as tkt
import tkinter.messagebox as messagebox
import pywinstyles


def ask() -> None:
    if messagebox.askyesno(message="是否关闭窗口？"):
        root.destroy()


# 0.0.2 创建并绑定按钮; 学会了创建按钮2333
def setup_settings_click():
    print("23333啊啊啊，我居然被点击了啊！！！")


size = 550, 300
root = tkt.Tk(title="linecap-doodle", size=size)
root.center()

# 设置不允许缩放窗口
root.resizable(False, False)
pywinstyles.apply_style(root, "mica")
root.shutdown(ask)

cv = tkt.Canvas(root, zoom_item=True)
cv.place(width=1280, height=720)

tkt.IconButton(cv, (1, 1), text="设置", image=tkt.PhotoImage(file="img/1001.png").resize(32, 32),
               command=setup_settings_click)
root.attributes('-alpha', 0.8)

root.mainloop()
