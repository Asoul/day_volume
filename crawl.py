#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from lxml import html
import json
import csv
from os import mkdir
from os.path import isdir, isfile, join
from datetime import date, timedelta, datetime
import sys
import math

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def max_ascii(s):
    output = ""
    for i in range(len(s)):
        if is_ascii(s[i]):
            output += s[i]
        else:
            break
    return output

# 今天年月日
today = str(date.today().year).zfill(4)+str(date.today().month).zfill(2)+str(date.today().day).zfill(2)

# 如果資料夾不存在，就開新的一天的資料夾
if not isdir(join('data',today)):
    mkdir(join('data',today))

urls = [line.strip().split(',')[1] for line in open('urls.csv', 'rb')]

for url_idx in range(len(urls)):
    
    rows = []
    page = requests.get('http://jsjustweb.jihsun.com.tw'+urls[url_idx])
    tree = html.fromstring(page.text)
    tr_length = len(tree.xpath('//form[@name="F"]/table/tr/td[1]/table/tr'))
    
    for tr_idx in range(4, tr_length+1):
        tr = tree.xpath('//form[@name="F"]/table/tr/td[1]/table/tr['+str(tr_idx)+']')
        td_length = len(tree.xpath('//form[@name="F"]/table/tr/td[1]/table/tr['+str(tr_idx)+']/td'))
        
        if td_length != 8:
            continue

        for col_idx in range(2):
            if len(tree.xpath('//form[@name="F"]/table/tr/td[1]/table/tr['+str(tr_idx)+']/td['+str(col_idx*4+1)+']/a/text()')) == 0:
                break
            name = max_ascii(tree.xpath('//form[@name="F"]/table/tr/td[1]/table/tr['+str(tr_idx)+']/td['+str(col_idx*4+1)+']/a/text()')[0])
            buy = int(tree.xpath('//form[@name="F"]/table/tr/td[1]/table/tr['+str(tr_idx)+']/td['+str(col_idx*4+2)+']/text()')[0].replace(",",''))
            sell = int(tree.xpath('//form[@name="F"]/table/tr/td[1]/table/tr['+str(tr_idx)+']/td['+str(col_idx*4+3)+']/text()')[0].replace(",",''))
            total = int(tree.xpath('//form[@name="F"]/table/tr/td[1]/table/tr['+str(tr_idx)+']/td['+str(col_idx*4+4)+']/text()')[0].replace(",",''))
            rows.append([name, buy, sell, total])

    rows.sort(key=lambda x: x[0])

    f = open(join('data', today, str(url_idx+1).zfill(3)+'.csv'), 'wb')
    cw = csv.writer(f, delimiter=',')
    for row in rows:
        cw.writerow(row)

