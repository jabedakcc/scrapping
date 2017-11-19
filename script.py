# -*- coding: utf8 -*-
#author :-   Jabed
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
import csv
from multiprocessing import Pool
import sys
import time
import re
import os
import subprocess
from datetime import datetime
start = time.time()

def decodeEmail(e):
    de = ""
    k = int(e[:2], 16)
    for i in range(2, len(e)-1, 2):
        de += chr(int(e[i:i+2], 16)^k)
    return de

g = open('link.txt')        #Reads from text file
ab = g.readlines()
bc = [z.strip(' \t\n\r') for z in ab]
print ("Total" + " " + str(len(bc)) + " " + "link.\n")
datestring = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
outputFile = open('final--' + datestring + '.csv', 'w', newline='', encoding="utf8")
outputWriter = csv.writer(outputFile)

for idx, i in enumerate(bc):
    print ("Get data from link -- " + str(idx))
    req = urllib.request.Request(i, headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    html = urllib.request.urlopen(req)
    soup = str(BeautifulSoup(html, 'html.parser'))
    time.sleep(10)
    name = re.findall('<tr class="text-right">(.*?)</tr>', soup, re.DOTALL)
    title = str(re.findall('[^>]+</small></h1>', soup, re.DOTALL)).replace(')', '').replace('(', '').replace('</small></h1>', '').replace('\'', '').replace(']', '').replace('[', '')
    for tit in name:
        tit = str(tit)
        try:
            cname = str(re.findall('<td class="text-left">(.*?)<', tit, re.DOTALL)).replace('\\n', '').replace('\\t', '').replace('\n', '').replace(']', '').replace('[', '').replace(',', '').replace(' ', '-')
            ime = cname.split("-")
            ime = str(ime[1] +"-"+ ime[0] +"-"+ ime[2]).replace('\'', '')
            cname = time.mktime(datetime.strptime(ime, '%d-%b-%Y').timetuple())
        except:
            cname = "n/a"
        title += ""   
        Open = str(re.findall('<td>(.*?)</td>', tit, re.DOTALL)[0]).replace('\\n', '').replace('\\t', '').replace('\n', '').replace(']', '').replace('[', '').replace(' ', '-')
        High = str(re.findall('<td>(.*?)</td>', tit, re.DOTALL)[1]).replace('\\n', '').replace('\\t', '').replace('\n', '').replace(']', '').replace('[', '').replace(' ', '-')
        Low = str(re.findall('<td>(.*?)</td>', tit, re.DOTALL)[2]).replace('\\n', '').replace('\\t', '').replace('\n', '').replace(']', '').replace('[', '').replace(' ', '-')
        Close = str(re.findall('<td>(.*?)</td>', tit, re.DOTALL)[3]).replace('\\n', '').replace('\\t', '').replace('\n', '').replace(']', '').replace('[', '').replace(' ', '-')
        Volume = str(re.findall('<td>(.*?)</td>', tit, re.DOTALL)[4]).replace('\\n', '').replace('\\t', '').replace('\n', '').replace(']', '').replace('[', '').replace(' ', '-')
        MarketCap = str(re.findall('<td>(.*?)</td>', tit, re.DOTALL)[5]).replace('\\n', '').replace('\\t', '').replace('\n', '').replace(']', '').replace('[', '').replace(' ', '-')
        outputWriter.writerow([title,cname,Open,High,Low,Close,Volume,MarketCap])
outputFile.close()

