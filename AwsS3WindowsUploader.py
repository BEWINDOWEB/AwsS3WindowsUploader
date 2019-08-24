#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import boto3
import os
import sys
import threading
import configparser

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                   self._filename, self._seen_so_far, self._size,
                   percentage))
            sys.stdout.flush()
            try:
                progress(self._seen_so_far, self._size)
            except:
                print("出错")

def filefound():
    filepath= askopenfilename()
    if (filepath != ""):
        (filename_prefix, filename) = os.path.split(filepath)
        text_filepath.delete(0.0, END)
        text_filepath.insert(END, filepath)
        text_filename.delete(0.0, END)
        text_filename.insert(INSERT, filename)

def fileupload():
    filepath = text_filepath.get(0.0, END)[:-1]
    filename = text_filename.get(0.0, END)[:-1]
    bucket = text_bucket.get(0.0, END)[:-1]
    key = text_key.get(0.0, END)[:-1]
    aws_access_key_id = text_aws_access_key_id.get(0.0, END)[:-1]
    aws_secret_access_key = text_aws_secret_access_key.get(0.0, END)[:-1]
    region_name = text_region_name.get(0.0, END)[:-1]
    print("文件路径=" + filepath +
          "\n新文件名=" + filename +
          "\n桶=" + bucket +
          "\n键=" + key +
          "\nawskid=" + aws_access_key_id +
          "\nawssak=" + aws_secret_access_key +
          "\n区域=" + region_name + "\n")
    t = threading.Thread(target=s3upload,
                         args=(filepath, aws_access_key_id, aws_secret_access_key, region_name, bucket, key, filename))
    t.setDaemon(True)
    t.start()
    var_upload_botton.set("正在上传")
    upload_button.configure(state='disable')
def clear_progress(canvas):
    canvas.delete(ALL)
    var_upload_percentage.set("")
    var_upload_botton.set("上传文件到s3")
    upload_button.configure(state='active')

def progress(current, total):
    # 填充进度条
    canvas.create_rectangle(1.5, 1.5, current/total*canvas_width, 23, fill="green")
    window.update()
    # 填写进度
    var_upload_percentage.set(str(round(current/total*100, 2)) + "%")

def s3upload(srcPath, aws_access_key_id, aws_secret_access_key, region_name, bucket, key, filename):
    try:
        session = boto3.Session(
            aws_access_key_id = aws_access_key_id,
            aws_secret_access_key = aws_secret_access_key,
            region_name = region_name)
        s3 = session.resource('s3')
        s3.meta.client.upload_file(srcPath, bucket, key + "/" + filename,
                                   Callback=ProgressPercentage(srcPath))
    except:
        messagebox.showerror("上传结果", "文件上传失败！请检查请求参数和网络连接")
        clear_progress(canvas)
        return False
    else:
        messagebox.showinfo("上传结果", "文件上传成功！")
        clear_progress(canvas)

def save_config():
    bucket = text_bucket.get(0.0, END)[:-1]
    key = text_key.get(0.0, END)[:-1]
    aws_access_key_id = text_aws_access_key_id.get(0.0, END)[:-1]
    aws_secret_access_key = text_aws_secret_access_key.get(0.0, END)[:-1]
    region_name = text_region_name.get(0.0, END)[:-1]
    print(aws_access_key_id, aws_secret_access_key, region_name, bucket, key)
    try:
        conf.set("aws_account", "aws_kid", aws_access_key_id)
        conf.set("aws_account", "aws_sak", aws_secret_access_key)
        conf.set("bucket_info", "region_name", region_name)
        conf.set("bucket_info", "bucket", bucket)
        conf.set("bucket_info", "key", key)
        conf.write(open(cfgpath, "w+")) #w是替换，r+是修改
    except:
        messagebox.showerror("配置保存结果", "保存失败！")
        return False
    else:
        messagebox.showinfo("配置保存结果", "保存成功！")
if __name__ == '__main__':

    # 读取配置
    curpath = os.path.dirname(os.path.realpath(__file__))
    cfgpath = os.path.join(curpath, "config.ini")
    conf = configparser.ConfigParser()
    conf.read(cfgpath, "utf-8")
    aws_kid = conf.get("aws_account", "aws_kid")
    aws_sak = conf.get("aws_account", "aws_sak")
    region_name = conf.get("bucket_info", "region_name")
    bucket = conf.get("bucket_info", "bucket")
    key = conf.get("bucket_info", "key")

    # 1. 创建容器
    window = Tk()
    window.title("s3文件上传工具")
    window.geometry('600x320')
    window.wm_resizable(False,False)


    # 2. 文本
    untitle_label = Label(window, text='本地文件路径').place(x=10, y=10, relx=0.07)
    text_filepath = Text(window, width=50, height=1)
    text_filepath.insert(INSERT, "请上传文件...")
    text_filepath.place(x=140, y=15)

    untitle_label = Label(window, text='s3文件名').place(x=10, y=40, relx=0.11)
    text_filename = Text(window, width=50, height=1)
    text_filename.insert(INSERT, "")
    text_filename.place(x=140, y=45)

    untitle_label = Label(window, text='aws_kid').place(x=10, y=70, relx=0.11)
    text_aws_access_key_id = Text(window, width=50, height=1)
    text_aws_access_key_id.insert(INSERT, aws_kid)
    text_aws_access_key_id.place(x=140, y=75)

    untitle_label = Label(window, text='aws_sak').place(x=10, y=100, relx=0.11)
    text_aws_secret_access_key = Text(window, width=50, height=1)
    text_aws_secret_access_key.insert(INSERT, aws_sak)
    text_aws_secret_access_key.place(x=140, y=105)

    untitle_label = Label(window, text='区域（region_name）').place(x=10, y=130, relx=0.00)
    text_region_name = Text(window, width=50, height=1)
    text_region_name.insert(INSERT, region_name)
    text_region_name.place(x=140, y=135)

    untitle_label = Label(window, text='桶（bucket）').place(x=10, y=160, relx=0.08)
    text_bucket = Text(window, width=50, height=1)
    text_bucket.insert(INSERT, bucket)
    text_bucket.place(x=140, y=165)

    untitle_label = Label(window, text='键（key）').place(x=10, y=190, relx=0.11)
    text_key = Text(window, width=50, height=1)
    text_key.insert(INSERT, key)
    text_key.place(x=140, y=195)

    untitle_label = Label(window, text='操作').place(x=10, y=230, relx=0.15)
    save_button = Button(window, text="保存配置", command=save_config)
    save_button.place(x=140, y=225)
    file_chosen_button = Button(window, text="选择文件", command=filefound)
    file_chosen_button.place(x=220, y=225)
    var_upload_botton = StringVar(window, "上传文件到s3")
    upload_button = Button(window, textvariable=var_upload_botton, command=fileupload)
    upload_button.place(x=300, y=225)


    untitle_label = Label(window, text='上传进度').place(x=10, y=270, relx=0.11)
    canvas_width = 350
    canvas = Canvas(window, width=canvas_width, height=22, bg="white")
    canvas.place(x=140, y=270)
    var_upload_percentage = StringVar(window, "")
    untitle_label = Label(window, textvariable=var_upload_percentage).place(x=140, y=300)

    mainloop()

