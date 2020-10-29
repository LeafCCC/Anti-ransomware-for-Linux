
**pip3 install psutil** 

**pip3 install watchdog**

**pip3 install PyQt5** </center>

Before using the backup function, you need to set up the disk partition. In this document, you can use the virtual machine for related operations.



Under VMware: virtual machine > Settings > Add > hard disk > SCSI > create a new virtual disk > Save as a single file > complete

After restarting the system, input the following commands in turn for partition operation:


<center>**fdisk /dev/sdb**

**m(help)** 
 
**n(create a new patition)** 

**1(choose patition number)**
 
**w(write the result)** </center>



Use the instruction **lsblk - f** to check. If sdb1 appears, it means that the partition is successful.

Finally,format it:**mkfs -t ext4 /dev/sdb1**

