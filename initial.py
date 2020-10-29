import configparser
import os
import readJSON
import string
import random
import shutil

config = configparser.RawConfigParser()
config.read('config.ini')
Safe_Ext=['docx','txt','pdf','doc','odt']

def get_random_name():
    n = random.randint(1, 6)
    r = ''
    for i in range(n):
        s = string.ascii_letters
        r += random.choice(s)
    return r

def get_random_Ext():
    n = random.randint(0, 4)
    return Safe_Ext[n]

workplace = config.get('DEFAULT', 'workplace')
backupfile = config.get('DEFAULT', 'backupfile')
backupfilesafe = config.get('DEFAULT', 'backupfilesafe')
logfile = config.get('DEFAULT', 'logfile')
watchfile = config.get('DEFAULT', 'watchfile')
recoveryfile = config.get('DEFAULT','recoveryfile')
workplace=config.get('DEFAULT','workplace')
scandir=config.get('DEFAULT','scandir')
honeypot1 = workplace + '/honeypot'
honeypot2 = '/honeypot'
dirlist=[backupfile,backupfilesafe,watchfile,recoveryfile,scandir,honeypot1,honeypot2]


def initial_dirs_files():
    if not os.path.exists(workplace):
        os.makedirs(workplace)

    for dir in dirlist:
        if not os.path.exists(dir):
            os.makedirs(dir)

    if not os.path.exists(logfile):
        os.system(r"touch {}".format(logfile))  # 调用系统命令行来创建文件


data = readJSON.readJSONfile('data.json')
famous = data["famous"]
before = data["before"]
after = data['after']
sentences = data['sentences']


Repeatability = 2
def traversal(thelist):
    global Repeatability
    pool = list(thelist) * Repeatability
    while True:
        random.shuffle(pool)
        for i in pool:
            yield i

nextsentences = traversal(sentences)
nextfamous = traversal(famous)

def getfamous():
    global nextfamous
    xx = next(nextfamous)
    xx = xx.replace("a", random.choice(before))
    xx = xx.replace("b", random.choice(after))
    return xx

def AnotherParagraph():
    xx = ". "
    xx += "\r\n"
    xx += "    "
    return xx

def create_article():
    xx = get_random_name()
    for x in xx:
        tmp = str()
        while (len(tmp) < 6000):
            branch = random.randint(0, 100)
            if branch < 5:
                tmp += AnotherParagraph()
            elif branch < 20:
                tmp += getfamous()
            else:
                tmp += next(nextsentences)
        tmp = tmp.replace("x", xx)
        return tmp

def creat_honeypot():
    honeypotlist = [honeypot1, honeypot2]
    for dir in honeypotlist:
        n = random.randint(5, 10)
        for i in range(n):
            name=dir+'/'+get_random_name()+'.'+get_random_Ext()
            with open(name, 'w') as f:
                tmp=create_article()
                f.write(tmp)
        dirnew1 = dir +'/'+ 'hpreadme.docx'
        dirnew2 = dir +'/'+ 'modified.pdf'
        dirnew3 = dir +'/'+ 'hpreadme.odt'
        dirnew4 = dir +'/'+ 'readme.txt'
        shutil.copyfile('./file/hpreadme.docx',dirnew1)
        shutil.copyfile('./file/modified.pdf', dirnew2)
        shutil.copyfile('./file/modified.pdf', dirnew3)
        shutil.copyfile('./file/readme.txt', dirnew4)

if __name__ == '__main__':
    initial_dirs_files()
    creat_honeypot()