
# !/usr/bin/env python

import os
import datetime
import pyinotify
import logging
import os.path
import shutil
import configparser

config = configparser.RawConfigParser()
config.read('config.ini')

backupfile = config.get('DEFAULT', 'backupfile')
backupfilesafe = config.get('DEFAULT', 'backupfilesafe')
logfile = config.get('DEFAULT', 'logfile')
dsk = config.get('DEFAULT', 'dsk')
mountfile = config.get('DEFAULT', 'mountfile')
watchfile = config.get('DEFAULT', 'watchfile')
workplace = config.get('DEFAULT', 'workplace')



class MyEventHandler(pyinotify.ProcessEvent):
    if not os.path.exists(workplace):
        os.makedirs(workplace)
    logging.basicConfig(level=logging.INFO, filename=logfile)

    def __init__(self):
        today = datetime.date.today().day
        for root,dirs,files in os.walk(backupfile):
            for f in files:
                fname = os.path.join(root,f)
                fdate = datetime.date.fromtimestamp(os.path.getctime(fname)).day
                if fdate != today:
                    os.remove(fname)
        print("monitoring...")

    def remove_file_two_hours_ago(self):
        try:
            shutil.rmtree(os.path.join(backupfile, str(((datetime.datetime.now().hour) + 22) % 24)))
        except:
            pass
    logging.info("Starting monitor...")

    def process_IN_ACCESS(self, event):
        logging.info("ACCESS event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))
        copy_file(os.path.join(event.path, event.name),
                  os.path.join(backupfile, str(datetime.datetime.now().hour), os.path.relpath(event.path, watchfile)),
                  event.name)
        self.remove_file_two_hours_ago()

    def process_IN_ATTRIB(self, event):
        logging.info("IN_ATTRIB event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))
        self.remove_file_two_hours_ago()


    def process_IN_CLOSE_NOWRITE(self, event):
        logging.info("CLOSE_NOWRITE event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))
        copy_file(os.path.join(event.path,event.name), os.path.join(backupfile, str(datetime.datetime.now().hour), os.path.relpath(event.path,watchfile)), event.name)
        self.remove_file_two_hours_ago()

    def process_IN_CLOSE_WRITE(self, event):
        logging.info("CLOSE_WRITE event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))
        dst = os.path.join(backupfilesafe, os.path.relpath(event.path, watchfile))
        copy_file_to_safety_place(os.path.join(backupfile, str(datetime.datetime.now().hour), os.path.relpath(event.path,watchfile), event.name), dst, event.name)
        copy_file_to_safety_place(os.path.join(backupfile, str((datetime.datetime.now().hour)-1), os.path.relpath(event.path,watchfile), event.name), dst, event.name)
        self.remove_file_two_hours_ago()

    def process_IN_CREATE(self, event):
        logging.info("CREATE event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))
        self.remove_file_two_hours_ago()


    def process_IN_DELETE(self, event):
        logging.info("DELETE event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))
        dst = os.path.join(backupfilesafe, os.path.relpath(event.path, watchfile))
        copy_file_to_safety_place(os.path.join(backupfile, str(datetime.datetime.now().hour), os.path.relpath(event.path,watchfile), event.name), dst, event.name)
        copy_file_to_safety_place(os.path.join(backupfile, str((datetime.datetime.now().hour)-1), os.path.relpath(event.path,watchfile), event.name), dst, event.name)
        self.remove_file_two_hours_ago()

    def process_IN_MODIFY(self, event):
        logging.info("MODIFY event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))
        self.remove_file_two_hours_ago()

    def process_IN_OPEN(self, event):
        logging.info("OPEN event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))
        self.remove_file_two_hours_ago()



# 将临时备份区的文件拷贝到备份磁盘空间
def copy_file_to_safety_place(src,dest,filename):
    if filename[len(filename)-3:] == 'swp':
        return 0
    if filename[len(filename)-3:] == 'swx':
        return 0
    if os.path.isfile(src):
       try:
            if not os.path.isdir(dest):
                try:
                    os.makedirs(dest)
                except:
                    pass
            print('backup to safe place:'+src)
            os.system('mount '+dsk+' '+mountfile)
            #os.system("cp \'"+src+"\' "+dest)
            shutil.copy(src,dest)
            os.system('umount '+mountfile)
            os.remove(src)
       except:
            print("error while backup")

'''
    if os.path.isfile(src):
        if not os.path.isdir(dest):
            try:
                os.makedirs(dest)
                cmd = "sudo chattr +a" + dest
                os.system(cmd)
                #os.system("sudo chattr +a" + dest)
            except:
                pass
        if not os.path.isfile(dest+"/"+filename):
            shutil.copy(src, dest)
            cmd="sudo chattr +a" + dest+"/"+filename
            os.system(cmd)
            #os.remove(src)
'''


# 将src目录中的内容拷贝到dest目录
# 如果dest或者其子目录不存在，先创建
def copy_file(src, dest,filename):
    if filename[len(filename)-3:] == 'swp':
        return 0
    if filename[len(filename)-3:] == 'swx':
        return 0
    if os.path.isfile(src):
        if not os.path.isdir(dest):
            try:
                os.makedirs(dest)
            except:
                pass
        if not os.path.isfile(dest+"/"+filename):
            print("temporary backup:"+src)
            shutil.copy(src, dest)
           # cmd="sudo chattr +a" + dest+"/"+filename
           # os.system(cmd)
        else:
            pass
            #os.remove(dest+"/"+filename)
            #print("update temporary backup:"+src)
            #shutil.copy(src, dest)

'''
pyinotify监控文件，若打开，则备份到backup文件夹，以时间小时数列目录，若被删除，则备份到安全区（safety文件夹）
自动删除两个小时前的备份到backup文件夹的文件（如果原文件还没有被删除，还没有被备份到安全区）以节省空间

'''
def main():
    # watch manager
    wm = pyinotify.WatchManager()
    wm.add_watch(watchfile, pyinotify.ALL_EVENTS, rec=True)
    eh = MyEventHandler()

    # notifier
    notifier = pyinotify.Notifier(wm, eh)

    notifier.loop()



'''
class File(object):
    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise OSError('{file_path} not exist'.format(file_path = file_path))
        self.file_path = os.path.abspath(file_path)

    def status(self):
        open_fd_list = self.__get_all_fd()
        open_count = len(open_fd_list)
        is_opened = False
        if open_count > 0:
            is_opened = True

        return {'is_opened': is_opened, 'open_count': open_count}

    def __get_all_pid(self):
        """获取当前所有进程"""
        return [ _i for _i in os.listdir('/proc') if _i.isdigit()]

    def __get_all_fd(self):
        """获取所有已经打开该文件的fd路径"""
        all_fd = []
        for pid in self.__get_all_pid():
            _fd_dir = '/proc/{pid}/fd'.format(pid = pid)
            if os.access(_fd_dir, os.R_OK) == False:
                continue

            for fd in os.listdir(_fd_dir):
                fd_path = os.path.join(_fd_dir, fd)
                if os.path.exists(fd_path) and os.readlink(fd_path) == self.file_path:
                    all_fd.append(fd_path)

        return all_fd
'''



if __name__ == "__main__":
    main()

















