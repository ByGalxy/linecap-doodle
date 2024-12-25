import tkintertools as tkt
import tkinter.messagebox as messagebox
import pywinstyles


def ask() -> None:
    if messagebox.askyesno(message="是否关闭窗口？"):
        root.destroy()


size = 550, 300
root = tkt.Tk(title="linecap-doodle", size=size)
root.center()

# 设置不允许缩放窗口
root.resizable(False, False)
pywinstyles.apply_style(root, "mica")
root.shutdown(ask)

cv = tkt.Canvas(root, zoom_item=True)
cv.place(width=1280, height=720)

tkt.IconButton(cv, (1, 1), text="设置", image=tkt.PhotoImage(file="img/1001.png").resize(32, 32))
root.attributes('-alpha', 0.8)

root.mainloop()
