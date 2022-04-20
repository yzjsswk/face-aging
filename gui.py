from asyncio.windows_events import NULL
import os
import shutil
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk


def load_picture(file_path):
    if not file_path.endswith(('png', 'PNG', 'jpg', 'JPG')):
        print('File ingored: ' + file_path)
        return NULL
    pic = Image.open(file_path)
    pic = pic.resize((480, 480), Image.NEAREST)
    return pic        

def load_pictures(dic_path):
    file_list = os.listdir(dic_path)
    pictures = []
    for file_name in file_list:
        pic = load_picture(dic_path + file_name)
        if pic != NULL:
            pictures.append(pic)
    print(len(pictures), 'pictures loaded.')
    return pictures

class main_window:
    def __init__(self):
        # 模型路径
        self.model_path = "HRFAE-master/"
        # 输入
        self.pic_input = ""
        # 结果集
        self.pic_res = []
        # 窗口框架
        self.root = Tk()
        self.root.title("毕业设计: 人脸年龄编辑")
        self.root.geometry('800x600+400+300')
        # 年龄选择器
        self.age_selector = Scale (
            self.root,
            sliderlength = 20,
            from_ = 20,
            to = 60,
            resolution = 4,
            orient = HORIZONTAL,
            command = self.show_res,
        )
        self.age_selector.place(x = 340, y = 545)
        # 显示图片的图床
        self.pic_bed = Label(self.root)
        self.pic_bed.place(x = 150, y = 60)
        # 选择路径的提示文本
        self.text1 = Label(self.root, text = "目标路径: ")
        self.text1.place(x = 50, y = 25)
        # 选择路径的文本输入框和值
        self.var_input = StringVar()
        self.entry_input = Entry (
            self.root, 
            width = 40, 
            textvariable = self.var_input
        )
        self.entry_input.place(x = 115, y = 25)
        # 选择路径的按钮
        self.button_input = Button (
            self.root, 
            text = "...", 
            command = self.select_input
        )
        self.button_input.place(x = 405, y = 20)
        # 生成按钮
        self.button_make = Button (
            self.root,
            text = "生成",
            command = self.make
        )
        self.button_make.place(x = 605, y = 20)
        # 生成进度
        self.percent = Label(self.root)
        self.percent.place(x = 655, y = 20)
        # loop
        self.root.mainloop()

    # 选择图片按钮的功能
    def select_input(self):
        path = askopenfilename()
        pic = load_picture(path)
        if pic != NULL:
            self.pic_input = path
            self.var_input.set(path)
            self.show_pic(pic)
        else:
            self.var_input.set("error")

    # 在图床展示image
    def show_pic(self, ima: Image):
        pic = ImageTk.PhotoImage(ima)
        self.pic_bed.config(image = pic)
        self.pic_bed.image = pic

    # 展示结果集的第id张图片
    def show_res(self, id):
        self.show_pic(self.pic_res[(int(id)-20)//4])

    def set_percent(self, a, b):
        cur = "%d/%d"%(a, b)
        self.percent.config(text = cur)
        self.percent.text = cur

    # 生成结果集(运行模型)
    def make(self):
        if not self.pic_input.endswith(('png', 'PNG', 'jpg', 'JPG')):
            return
        fmt = self.pic_input[-3:]
        op_clear_workpath1 = "rm -rf " + self.model_path + "test/input/*"
        op_clear_workpath2 = "rm -rf " + self.model_path + "test/output/*"
        os.system(op_clear_workpath1)
        os.system(op_clear_workpath2)
        shutil.copy(self.pic_input, self.model_path + "test/input/input." + fmt)
        #self.set_percent(0, 11)
        #for i in range(20, 64, 4):
            #op_run_model = "cd "+ self.model_path + " && python test.py --config 001 --target_age %d"%i
            #os.system(op_run_model)
            #self.set_percent((i-20)//4+1, 11)
        op_run_model = "cd "+ self.model_path + " && python test.py --config 001"    
        os.system(op_run_model)
        self.pic_res = load_pictures(self.model_path + "test/output/")
main_window()


