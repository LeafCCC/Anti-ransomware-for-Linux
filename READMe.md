## 1. Introduction
   This repository is a simple project to protect the Linux system from ransomware.AS it is just a contest project by undergraduates, we can't ensure sufficient effectiveness.Thus, please still be cautious when you use it.
## 2. Environment construction


This project is carried out under the Linux environment. The specific programming language is python3.7. Ubuntu 18.04 in Linux has its own Python 3.6. If you need to upgrade to 3.7, the process is as follows:


<p align="center" >
 sudo apt install python3.7
 
 <p align="center" >
 sudo apt install python3-pip


If you point to python3.6 when using the pip command, you only need to use **python3.7 - m pip install** during installation:

<p align="center" >
pip3 install pyinotify

 
 <p align="center" >
pip3 install shutil

 
 <p align="center" >
pip3 install configparser

 
 <p align="center" >
pip3 install psutil

 
 <p align="center" >
pip3 install watchdog

 
 <p align="center" >
pip3 install PyQt5 </p>

Before using the backup function, you need to set up the disk partition. In this document, you can use the virtual machine for related operations.



Under VMware: virtual machine > Settings > Add > hard disk > SCSI > create a new virtual disk > Save as a single file > complete

After restarting the system, input the following commands in turn for partition operation:


<p align="center" >
 fdisk /dev/sdb
 
 <p align="center" >
m(help)
  
 <p align="center" >
n(create a new patition)
 
 <p align="center" >
1(choose patition number)
  
 <p align="center" >
w(write the result) 

</p>



Use the instruction **lsblk - f** to check. If sdb1 appears, it means that the partition is successful.

Finally,format it: **mkfs -t ext4 /dev/sdb1**
