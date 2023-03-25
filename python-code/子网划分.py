# -*- coding: UTF-8 -*-
import sys

'''初始化'''
str = "1.2.3.0/24/8" #初始化网络号、子网掩码、需求子网数量

'''切割网络号、子网掩码、子网数量'''
temp = str.split('/')
if len(temp) != 3 :
    print "输入不合法！程序终止！"
    sys.exit()

'''转换子网掩码、子网数量'''
subnetMask = int(temp[1]) #子网掩码
subnetNumber = int(temp[2]) #子网数量
if (subnetMask<2) or (subnetNumber<2) :
    print "子网掩码、子网数量至少为2！程序终止！"
    sys.exit()

'''切割、转换网络号到十进制'''
temp2 = temp[0].split('.')
if len(temp2) !=4 :
    print "网络号不合法！程序终止！"
    sys.exit()

ip10=[0]*4 #初始化每一段IP地址，十进制
for i in range(4) : #转为整形
    ip10[i]=int(temp2[i])
    if (ip10[i]<0) or (ip10[i]>255) :
        print "网络号不合法！程序终止！"
        sys.exit()

'''转换网络号到二进制'''
ip2=[0]*32 #初始化每一位IP地址，二进制
flag=0 #flag标记是否停止计算网络前缀
preNet=32 #preNet网络前缀个数(32-从后往前数，第一个不为0的数字)
k=31
for i in range(3,-1,-1) : #转为二进制，并保存到数组
    for j in range(8) :
        ip2[k] = ip10[i] >> j & 1 #>>运算，右移n位，高位补0
        k-=1
        if (flag==0) and (ip2[k+1]==0) : #计算网络前缀
            preNet-=1
        else:
            flag=1

if subnetMask < preNet :
    print "该网络号的子网掩码不合法！程序终止！"
    sys.exit()
if (1 << (32 - subnetMask)) < subnetNumber : #子网数不可超过主机数量,<<运算，左移n位，相当于2的n次方
    print "需求子网数超出最大主机数量！程序终止！"
    sys.exit()

'''计算应当划分的子网数量和每个子网的最大主机数量'''
realSubnetNumber = subnetNumber - 1 #假设输入的子网数量为2的幂次方,此处-1是避免是2的幂的情况，1是例外，但是上面已经排除
power = 1 #应该为2的几次幂
while (realSubnetNumber >> 1) != 0 : #相当于a=a/2,a/2!=0
    realSubnetNumber = realSubnetNumber >> 1
    power+=1
realSubnetNumber = 1 << power
maxHost = 1 << (32 - preNet - power) #每个子网的最大主机数量

'''分配ip'''
preIp=[[0 for col in range(4)] for row in range(realSubnetNumber)] #第一个ip
sufIp=[[0 for col in range(4)] for row in range(realSubnetNumber)] #最后一个ip
for i in range(realSubnetNumber) :
    '''设置子网号'''
    for j in range(power) : #子网号，递增
        ip2[subnetMask + power - j - 1] = i >> j & 1;
    '''设置第一个ip'''
    for j in range(subnetMask + power,32) :#填充0
        ip2[j]=0
    for j in range(4) : #计算每一段IP地址，十进制
        t=0 #计算数组对应的值
        for k in range(8) :
            t += ip2[(j << 3) + k] << (7 - k)
        preIp[i][j] = t #第一个ip
    '''设置最后一个ip'''
    for j in range(subnetMask + power,32) :#填充1
        ip2[j]=1
    for j in range(4) :
        t=0
        for k in range(8) :
            t += ip2[(j << 3) + k] << (7 - k)
        sufIp[i][j] = t #最后一个ip

'''输出'''
print u"根IP地址为：" , temp[0] , u" 子网掩码位数为：" , subnetMask
print "需求子网数量为：" , subnetNumber , " 实际划分的子网数量为：" , realSubnetNumber
print "每个子网最大的主机数量为：" , maxHost
for i in range(realSubnetNumber) :
    print "第 " , i , " 个子网可用地址：",\
    preIp[i][0] , "." , preIp[i][1] , "." , preIp[i][2] , "." , (preIp[i][3] + 1) , "\t ~ ",\
    sufIp[i][0] , "." , sufIp[i][1] , "." , sufIp[i][2] , "." , (sufIp[i][3] - 1),\
    "\t网络地址：" , preIp[i][0] , "." , preIp[i][1] , "." , preIp[i][2] , "." , preIp[i][3],\
    "\t广播地址：" , sufIp[i][0] , "." , sufIp[i][1] , "." , sufIp[i][2] , "." , sufIp[i][3]

