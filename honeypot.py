#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import detecter
import psutil
import threading
from handleprocess import kill_process_tree
import signal
import initial

entropy_dict={initial.honeypot1:0,initial.honeypot2:0}


class MyDirEventHandler(FileSystemEventHandler):
    def on_moved(self, event):
        if event.is_directory:
            print('---------------------')
            print('moved:',event.src_path)
            print(entropy_dict[event.src_path])
            danger=detecter.detect(event.src_path,entropy_dict)
            print('danger is:',danger)
            if danger>0:
                print(danger)
                for p in psutil.process_iter():
                    if p.open_files() != []:
                        if event.src_path in p.open_files()[0][0]:
                            print('find danger')
                            kill_process_tree(p.pid,signal.SIGKILL)
            print(entropy_dict[event.src_path])
    def on_created(self, event):
        if event.is_directory:
            print('---------------------')
            print('created:',event.src_path)
            print(entropy_dict[event.src_path])
            danger = detecter.detect(event.src_path, entropy_dict)
            print(danger)
            if danger > 0:
                for p in psutil.process_iter():
                    if p.open_files() != []:
                        if event.src_path in p.open_files()[0][0]:
                            print('find danger')
                            kill_process_tree(p.pid,signal.SIGKILL)
            print(entropy_dict[event.src_path])
    def on_deleted(self, event):
        if event.is_directory:
            print('---------------------')
            print('deleted:',event.src_path)
            print(entropy_dict[event.src_path])
            danger = detecter.detect(event.src_path, entropy_dict)
            print(danger)
            if danger > 0:
                for p in psutil.process_iter():
                    if p.open_files() != []:
                        if event.src_path in p.open_files()[0][0]:
                            print('find danger')
                            kill_process_tree(p.pid,signal.SIGKILL)
            print(entropy_dict[event.src_path])
    def on_modified(self, event):
        if event.is_directory:
            print('---------------------')
            print('modified',event.src_path)
            print(entropy_dict[event.src_path])
            danger = detecter.detect(event.src_path, entropy_dict)
            print(danger)
            if danger > 0:
                for p in psutil.process_iter():
                    if p.open_files() != []:
                        if event.src_path in p.open_files()[0][0]:
                            print('find danger')
                            kill_process_tree(p.pid,signal.SIGKILL)
            print(entropy_dict[event.src_path])
"""
使用watchdog 监控文件的变化
"""
def watching(directory,Deside):
    detecter.entropy_init(entropy_dict)
    print('initial entropy is:', entropy_dict, '\n')
    # 创建观察者对象
    observer = Observer()
    # 创建事件处理对象
    fileHandler = MyDirEventHandler()
    # 为观察者设置观察对象与处理事件对象
    observer.schedule(fileHandler, directory, True)
    observer.start()
    while Deside.value:
        time.sleep(2)
    if Deside.value==0:
        observer.stop()
    observer.join()

def start_honeypot(Deside):
    print(isinstance(initial.honeypot1,str))
    t1 = threading.Thread(target=watching, args=(initial.honeypot1,Deside,))
    t2 = threading.Thread(target=watching, args=(initial.honeypot2, Deside,))
    t1.start()
    t2.start()
    print('start t1 t2')
    t1.join()
    t2.join()
    print('stop t1 t2')

