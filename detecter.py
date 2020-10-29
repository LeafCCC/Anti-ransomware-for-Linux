#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import struct
import math


Safe_Ext=['docx','txt','pdf','doc','odt']

def entropy_calculation(list):  # 求出列表信息熵函数
    result = 0.0
    for i in list:
        if i > 0:
            result += i * math.log2(i)
    return -result


def get_entropy(file):#输入文件得到其信息熵
    if os.path.exists(file):
        file_path = os.path.abspath(file)  # 返回绝对路径
        file_size = os.path.getsize(file)  # 获取文件大小（字节）
    bytes_list = [0] * 256  # 创建一个256个元素的字节列表,用来统计频率

    try:
        with open(file_path, 'rb') as f:  # 只读方式打开二进制文件
            read_byte = f.read(1)
            counter = 0
            mb_counter = 0
            while read_byte != b'':
                value = struct.unpack('B', read_byte)[0]  # 输出字节对应数字，方便统计频率
                bytes_list[value] += 1  # 对应位置频率加1
                counter += 1  # 总记数加1
                if counter <=45:
                    bytes_list[value] += 0.8
                    file_size+=0.8
                read_byte = f.read(1)
        frequency_list = [i / file_size for i in bytes_list]  # 频率列表
        entropy = entropy_calculation(frequency_list)  # 计算出信息熵
        # print(entropy)
        return entropy
    except IOError:
        return 11
    except:
        return 00

def detect(directory,dict_entropy):
    file_list=[] #文件路径列表
    file_name=[] #文件名列表
    file_ext=[]  #文件后缀名列表
    danger_factor=0
    for root,dirs,files in os.walk(directory):#获取当前蜜罐目录下文件
        for name in files:
            file_list.append(os.path.join(root,name))
            file_name.append(name)
            if name.count('.')>0:
                file_ext.append(name.split('.',1)[1])
    entropy_sum=0
    number=0
    for file in file_list:#计算信息熵之和
        number+=1
        entropy_sum+=get_entropy(file)
    average=entropy_sum/number
    past_average=dict_entropy[directory]
    diff_average=average-past_average
    dict_entropy[directory]=average
    if diff_average<-0.15 or diff_average>0.15:
        danger_factor+=1
    for i in file_name:#文件名'.'统计
        if i.count('.')>1:
            danger_factor+=1
            break
    for t in file_ext:
        if t not in Safe_Ext:
            danger_factor+=1
            break
    return danger_factor

def entropy_init(dict_entropy):
    for key in dict_entropy.keys():
        file_list = []  # 文件路径列表
        file_name = []  # 文件名列表
        file_ext = []  # 文件后缀名列表
        for root, dirs, files in os.walk(key):  # 获取当前蜜罐目录下文件
            for name in files:
                file_list.append(os.path.join(root, name))
                file_name.append(name)
                if name.count('.') > 0:
                    file_ext.append(name.split('.', 1)[1])
        entropy_sum = 0
        number = 0
        for file in file_list:  # 计算信息熵之和
            number += 1
            entropy_sum += get_entropy(file)
        dict_entropy[key] = entropy_sum / number




