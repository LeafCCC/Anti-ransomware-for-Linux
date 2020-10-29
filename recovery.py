import os
import configparser

config = configparser.RawConfigParser()
config.read('config.ini')

backupfile = config.get('DEFAULT', 'backupfile')
backupfilesafe = config.get('DEFAULT', 'backupfilesafe')
logfile = config.get('DEFAULT', 'logfile')
dsk = config.get('DEFAULT', 'dsk')
mountfile = config.get('DEFAULT', 'mountfile')
watchfile = config.get('DEFAULT', 'watchfile')
recoveryfile = config.get('DEFAULT','recoveryfile')

def recover():
    os.system('mount '+dsk+' '+mountfile)
    for root,dirs,files in os.walk(backupfilesafe):
        for f in files:
            src = os.path.join(root, f)
            dest = os.path.join(recoveryfile, os.path.relpath(root, backupfilesafe))
            if not os.path.isdir(os.path.dirname(dest)):
                try:
                    os.makedirs(os.path.dirname(dest))
                except:
                    pass
            os.system("cp \'"+src+"\' "+dest)
    os.system('umount '+mountfile)
