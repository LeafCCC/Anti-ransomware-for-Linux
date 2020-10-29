import os

danger_Ext=[".aes",".cry",".krab", ".bip",".dbger",".ARROW" ,".ARENA",".IQ",".lucky",
            ".crypted",".BIG4+",".CRAB",".SATAN",".VYA+",".MAKGR",".PANDA",".ALCO",
            ".CHAK",".TRUE",".SHUNK","GOTHAM",".GRANNY",".RESERVE",".LIN",".YAYA",
            ".SEXY",".BUNNY",".FREEMAN",".sigrun",".block",".cesar",".MASTER",".YOYO" ]
def scan(dirname):
    result=''
    for maindir, subdir, file_name_list in os.walk(dirname):
        #print("1:",maindir) #当前主目录
        #print("2:",subdir) #当前主目录下的所有目录
        #print("3:",file_name_list)  #当前主目录下的所有文件
        for filename in file_name_list:
            decision=0
            for i in danger_Ext:
                if i in filename:
                    decision=1
                    break
            if decision==1:
                apath = os.path.join(maindir, filename)  # 合并成一个完整路径
                print("may be dangerous suffix",apath)
                result+="may be dangerous suffix"+apath+"\n"
            num = filename.count(".0")+filename.count(".1")+filename.count(".2")+filename.count(".3")+filename.count(".4")+filename.count(".5")+filename.count(".6")+filename.count(".7")+filename.count(".8")+filename.count(".9")
            if(filename.count(".")-num >=2):
                apath = os.path.join(maindir, filename)  # 合并成一个完整路径
                result +="more than one . in "+apath+"\n"
                print("more than one . in ",apath)
    return result

