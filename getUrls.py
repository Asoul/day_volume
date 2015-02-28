#!/bin/python
# -*- coding: utf-8 -*-

import requests
import csv

page = requests.get('http://jsjustweb.jihsun.com.tw/Z/ZG/ZGB/ZGB.djhtm')
f = open('urls.csv', 'wb')
names = []
fn = open('names', 'rb')
for name in csv.reader(fn):
    names.append(name)
cw = csv.writer(f, delimiter=',')
tagEnd = 0
i = 0
while True:
    urlStart = page.text.find('/z/zg/zgb', tagEnd)
    if urlStart == -1:
        break
    tagEnd = page.text.find('</a>', urlStart)
    # 1636, 1662, 1664~1679
    i += 1
    cw.writerow([i, page.text[urlStart:urlStart+27]])
