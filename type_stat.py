# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 12:34:31 2016

@author: Schneitzer
"""

import os, os.path
import csv
import collections
import re

typeStat = collections.defaultdict(int)
des = {}
curMainDir = os.path.dirname(os.path.abspath(__file__))
csvName = os.path.join(curMainDir, 'TypeStat.csv')
pattern = r'(.*)(\[A[0-9]{4}\])'

with open('SupType.csv',encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    with open(csvName, 'w', encoding = 'utf-8-sig') as writefile:
        fieldnames = ['Type', 'Description', 'Total']
        writer = csv.DictWriter(writefile, fieldnames, quoting = csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in reader:
            if row['Type']:
                tag = re.search(pattern,row['Type'])
                key = tag.group(2)
                des[key] = tag.group(1)
                typeStat[key] += 1
        for k,v in typeStat.items():
            typeStatPrint = collections.defaultdict(list)
            tmp = []
            tmp.append(('Type',k))
            tmp.append(('Total',v))
            tmp.append(('Description',des[k]))
            print(tmp)
            for k,v in tmp:
                typeStatPrint[k].append(v)
            writer.writerow(typeStatPrint)
            print(typeStatPrint)
        
                
                