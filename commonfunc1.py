import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import re
from itertools import chain
from collections import Counter
from  datetime import datetime
import statistics
import itertools
import matplotlib as mpl
import copy
import config1 as conf
import math
import time

#CPU and Memory utilization graphs from log file..................................................

def mem(sub,logfile):
    mem = []
    newlistmem = []
    memtime=[]
    tim=[]
    substr = sub
    with open (logfile, 'rt') as myfile:
        for line in myfile:
            if line.find(substr) != -1:
                mem.extend(re.split(r'[|\s]\s*', line))
    for (value,total) in zip(mem[2::10],mem[1::10]):
        new_elem = int(value)/int(total)
        newlistmem.append(new_elem*100)
    for d,t in zip(mem[7::10],mem[8::10]):
       tim.append(d+" "+t)
    date_obj = []
    for temp in tim:
        date_obj.append(datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f'))
    dates = md.date2num(date_obj)
    Data_Printing(newlistmem,substr)
    Data_Plotting(dates,newlistmem,"Memory Utilisation","Memory","Memory_Utilisation.png")

def cpu(str1,logfile):
    cpu=[]
    newlistcpu=[]
    cputime=[]
    word=[]
    substr1=str1
    valu=substr1.split()
    with open (logfile, 'rt') as myfile:
        for line in myfile:
            if line.find(valu[0])!= -1 and line.find(valu[1])!= -1:
                cpu.append(line)
    for x in cpu:
        word.append(re.split(r'[|\s]\s*', x))
    for y in word:
        if y[0] == valu[0] and y[1]==valu[1]:
            l=len(y)
            newlistcpu.append(100-float(y[l-4]))
            cputime.append(y[l-3]+" "+y[l-2])
    date_obj = []
    for temp in cputime:
        date_obj.append(datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f'))
    dates = md.date2num(date_obj)
    Data_Printing(newlistcpu,str1)
    Data_Plotting(dates,newlistcpu,"CPU Utilisation for Avg "+valu[1],"CPU Values","CPU_Utilisation"+valu[1]+".png")


def Data_Printing(value,string1):
    if string1 == "Mem:      ":
       mem1=str(round(max(value),2))+"%"
       mem2=str(round(min(value),2))+"%"
       mem3=str(round(statistics.mean(value),2))+"%"
       #index=open("index.html").read().format(p1=mem1,p2=mem2,p3=mem3)
       f= open("Mem.html","w")
       wrapper1="<head><style>table, th, td {border: 1px solid black;border-collapse: collapse;}th, td {padding: 15px;}</style></head><body><p><b>Memory Utilisation :</b></p><table><tr><td>Maximum </td><td>Minimum </td><td>Average </td></tr><tr><td>%s</td><td>%s</td><td>%s</td></tr></table></body>"
       whole=wrapper1 %(mem1,mem2,mem3)
       f.write(whole)
       f.close()
    else:
       val=string1.split()
       cpu1=str(round(max(value),2))+"%"
       cpu2=str(round(min(value),2))+"%"
       cpu3=str(round(statistics.mean(value),2))+"%"
       f= open("Average "+val[1]+".html","w")
       wrapper1="<head><style>table, th, td {border: 1px solid black;border-collapse: collapse;}th, td {padding: 15px;}</style></head><body><p><b>CPU Utilisation %s :</b></p><table><tr><td>Maximum </td><td>Minimum</td><td>Average </td></tr><tr><td>%s</td><td>%s</td><td>%s</td></tr></table></body>"
       whole=wrapper1 %("Average "+val[1],cpu1,cpu2,cpu3)
       f.write(whole)
       f.close()

def Data_Plotting(x,y,title,yaxis,sa):
    ax=plt.gca()
    #fig = plt.figure()
    plt.subplots_adjust(bottom=0.3)
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks( rotation=30, horizontalalignment='right' )
    if "Memory" == yaxis or "CPU Values" == yaxis:
        plt.ylim(ymax = 100, ymin = 0)
    plt.plot(x,y)
    plt.title(title)
    plt.xlabel('Duration')
    plt.ylabel(yaxis)
    plt.savefig(sa,bbox_inches='tight')
    plt.clf()
    #plt.show()

def Data_preparation(fname,avg,memory):
    mem(memory,fname)
    for i in avg:
        cpu(i,fname)
#CHECKING FOR REBOOT AND TO DISPLAY THE FINAL UPTIME..............................................
def uptime(fname):
    #open and read lines from log-file
    infile=open(fname,"r")
    lines=infile.readlines()
    upout=open("uptime.txt","w+")
    v = False
    for line in lines:
        line=line.strip()
        if conf.device_prompt+" uptime" in line:
            v=True
        elif conf.device_prompt+" free" in line:
            v=False
        elif v:
            upout.write(line+"\n")
    upout.close()
    upout=open("uptime.txt","r")
    upl=upout.readlines()

    tmp=[]

    uptemp=open("uptime.txt","r")
    uplt=uptemp.readlines()
    for i in uplt:
        j=i.find("load")
        tmp.append(i[12:j-3])
    tmp3=[]

    #convert the sliced value of uptime into integer and reduce it into seconds
    a=[]
    for i in tmp:
        if "min" in i and ":" not in i and "day" not in i :
            m=i[0:2]
            tmp3.append(int(m)*60)
        elif ":" in i and "day" not in i and "min" not in i:
            h, m = i.split(':')
            tmp3.append(int(h) * 3600 + int(m)*60)
        elif "day" in i and "min" in i:
            tmp3.append(int(i[0])*24*3600+int(i[7:9])*60 )
        elif "day"  in i and ":" in i:
            a=re.split(r'[:\s]\s*', i)
            d=int(a[0])
            h,m=int(a[len(a)-2]),int(a[len(a)-1])
            tmp3.append(d*24*3600+h*3600+m*60)

    final="The final uptime :"+i
    tmp2=copy.deepcopy(tmp3)
    tmp2.sort()
    c=0
    #compare if items in orginal list(containing seconds) to get number of restarts
    for i in range(0,len(tmp3)-1):
        if tmp3[i]<tmp3[i+1]:
           continue
        else:
            c=c+1
    n="Number of reboots : "+str(c)
    if len(tmp2) !=0 and len(tmp3) != 0:
        if tmp2==tmp3:
            up="No problem in uptime"
        else:
            up=" Device has rebooted"
    else:
        up="No uptime values available \n"

    f= open("UPtime.html","w")
    wrapper1="<p>%s <br/>%s <br/>%s <br/></p>"
    whole=wrapper1 %(final,n,up)
    f.write(whole)
    f.close()
    infile.close()
#NETWORK TOPOLOGY..............................................................................

def network(fname):
    file1 = open(fname,"r")
    lines = file1.readlines()
    file2 = open("temp.txt","w+")
    for i in lines:
        if i!="\n":
            file2.write(i)
    file2.close()
    f3=open("temp.txt","r")
    line=f3.readlines()
    dno=[]
    ip=[]
    for i in line:
        i=i.strip()
        if re.match(r"^-- DB (.*):",i):
            dno.append(i[7:9])
        elif re.match(r"^QCA IEEE 1905.1 device:.*",i):
                ip.append(i[24:41])


    f3.close()
    dno=[int(i) for i in dno]
    ul=[]
    for x in dno:
        if x not in ul:
            ul.append(x)
    ul.sort(reverse=True)

    g = globals()
    for i in range(1,ul[0]+1):
         g['sat_{}'.format(i)] = []
         g['rel_{}'.format(i)] = []
         g['ups_{}'.format(i)] = []

    f3=open("temp.txt","r")
    line=f3.readlines()
    f4=open("tmp1.txt","w+")
    for i in line:
        for j in range(1,ul[0]+1):
            i=i.strip()
            if re.match(r"^#"+str(j)+".*",i):
                      f4.write(i+"\n")
                      break
            elif re.match(r"^Upstream Device:.*",i):
                      f4.write(i+"\n")
                      break
    f4=open("tmp1.txt","r")
    lines=f4.readlines()
    pre=""
    #fetching satellite address,relation,upstream info
    for i in lines:
        for j in range(1,ul[0]+1):
            if re.match(r"^Upstream Device:.*",i)and re.match(r"^#"+str(j)+".*",pre):
                  g['ups_%s' % j].append(i[17:34])
        pre=i
    f3=open("temp.txt","r")
    line=f3.readlines()
    prev=""

    for i in line:
        for j in range(1,ul[0]+1):
            i=i.strip()
            if re.match(r"^#"+str(j)+".*",i):
                  g['sat_%s' % j].append(i[28:45])

            elif re.match(r"Relation:.*",i) and re.match(r"^#"+str(j)+".*",prev):
                g['rel_%s' % j].append(i[10:25])

        prev=i
    f3.close()

    f=False
    trel=[]
    #checking if there is any change in topology
    for i in range(0,len(ip)):
        for j in range(1,ul[0]+1):
            if g['rel_%s' % j][i]=="Direct Neighbor" :
                f=True
                continue
            else:
                f=False
                break
        if f==True:
            trel.append("Star")

        else:
            trel.append("Daisy chain")

    #printing the router-satellite connectivities
    fout=open("Topo_output.txt","a")
    fout.truncate(0)
    for i in range(0,len(ip)):
            fout.write("\nIteration "+str(i+1)+"\n")
            fout.write("Router : "+ip[i]+" is connected to "+str(dno[i])+" satellites \n")
            if trel[i]=="Star":
                    fout.write("Satellites follows Star topology \n")

            else:
                    fout.write("Satellites follows Daisy Chain topology \n")


    fout.write("\n")
    m=0
    #check for change in topology (considering attributes such as MAC address,number_of_satellites,upstream,type_of topology)
    for i in range(1,ul[0]+1):
            if all(ele == g['sat_%s' % str(i)][0] for ele in g['sat_%s' % str(i)]):
                m+=1
                fout.write("No change in MAC address of satellite: "+str(i)+"\n")
                continue
            else:

                fout.write("Change in MAC address of satellite: "+str(i)+"\n")
                continue
    fout.write("\n")
    for i in range(0,len(dno)-1):
        if dno[i]!=dno[i+1]:
                fout.write("Change in number of satellite\n")
                break
        else:
            fout.write("No change in number of satellite\n")
            break
    fout.write("\n")
    u=0
    for i in range(1,ul[0]+1):
            if all(ele == g['ups_%s' % str(i)][0] for ele in g['ups_%s' % str(i)]):
                u+=1
                fout.write("No change in upstream of satellite: "+str(i)+"\n")
                continue
            else:

                fout.write("Change in upstream of satellite: "+str(i)+"\n")
                continue
    fout.write("\n")
    t=0
    for i in range(0,len(ip)-1):
        if trel[i]!=trel[i+1]:
            t+=1

    for i in range(0,len(dno)-1):
            if u!=ul[0] and m!=ul[0] and t!=len(ip)-1 :
                fout.write("change in topology \n")
                break
            else:
                fout.write("No change in topology \n")
                break
#NETWORK VISUALISATION...........................................................................


def picrep(fname):
    f1=open(fname,"r")
    lines=f1.readlines()
    f2=open("tm.txt","w+")
    c=False
    #open the file and pick lines that are necessary for network visualization
    for i in lines:
        if "-- ME:" in i:
            c=True
        elif "/# exit" in i or re.match(r"@$",i):
            c=False
        elif c==True:
            f2.write(i)
    f2.close()
    f2=open("tm.txt","r")
    line=f2.readlines()
    n=0
    for i in line:
        i=i.strip()
        if re.match(r"^QCA IEEE .*",i):
            ip=i[24:41]
        elif  re.match(r"^-- DB (.*):",i):
            n=int(i[7:9])

    f2=open("tm.txt","r")
    line=f2.readlines()
    sat=[]
    rel=[]
    ups=[]
    j=1
    #slicing the previously processed lines to get satellite address,its relation and to which device it is connected
    for i in line:
        i=i.strip()
        if re.match(r"^#"+str(j)+": QCA IEEE .*",i):
                sat.append(i[28:45])
                j=j+1
        elif re.match(r"^Relation: .*",i):
                rel.append(i[10:25])
        elif re.match(r"^Upstream Device:.*",i)and "Upstream Device: None" not in i:
                ups.append(i[17:34])
    #printing the contents of list in required format

    f= open("Topo_output_visual.html","a")
    f.truncate(0)
    wrapper1="<head><style>table, th, td {border: 1px solid black;border-collapse: collapse;}th, td {padding: 15px;}</style></head><body><table><tr><td>%s</td><td>%s</td><td>%s</td></tr></table></body>"
    wrapper2="<head><style>table, th, td {border: 1px solid black;border-collapse: collapse;}th, td {padding: 15px;}</style></head><body><table><tr> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> </tr></table></body>"
    for i in range(n):
        if rel[i]=="Direct Neighbor" and sat[i] not in ups:
            rout_ip= str(ip)+" (Router)"
            arrow= "<---- "
            sat_ip= str(sat[i])+" (Satellite "+str(i+1)+")\n"
            whole=wrapper1 %(rout_ip, arrow, sat_ip)
            f.write(whole)

        else:
            for j in range(n):
                if ups[i]==sat[j]:
                    rout_ip= str(ip)+" (Router)"
                    arrow="<----"
                    sat_ip1=str(ups[i])+" (Satellite "+str(j+1)+")"
                    sat_ip2=str(sat[i])+" (Satellite "+str(i+1)+")\n"
                    whole=wrapper2 %(rout_ip, arrow, sat_ip1, arrow, sat_ip2)
                    f.write(whole)
                    break
    f.close()
    """
    for i in range(n):
        if rel[i]=="Direct Neighbor" and sat[i] not in ups:
            fout.write(str(ip)+" (Router)    <----    "+str(sat[i])+" (Satellite "+str(i+1)+")\n")
        else:
            for j in range(n):
                if ups[i]==sat[j]:
                    fout.write(str(ip)+" (Router)    <----    "+str(ups[i])+" (Satellite "+str(j+1)+")    <----    "+str(sat[i])+" (Satellite "+str(i+1)+")\n")
                    break"""
