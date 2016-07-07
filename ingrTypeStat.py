# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 01:54:54 2016

@author: Schneitzer
"""

import os, os.path
import csv
import unicodedata

curMainDir = os.path.dirname(os.path.abspath(__file__))
dsfPath = os.path.join(curMainDir, 'dsf')
csvName = os.path.join(curMainDir, 'ingrTypeStat.csv')
ingrTypeCount = {}

with open('lstProducts.csv',encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    with open(csvName, 'w', encoding = 'utf-8-sig') as writefile:
        writer = csv.writer(writefile, quoting = csv.QUOTE_NONE, quotechar = '')
        writer.writerow(["Type"] + ["Total"])
        for row in reader:
            if row['DSLD ID']:
                fileid = row['DSLD ID']
            dsfName = os.path.join(dsfPath, fileid) + '_dsf.csv'
            try:
                with open(dsfName, encoding = 'utf-8-sig') as dsffile:
                    dsfRead = csv.DictReader(dsffile)
                    for row in dsfRead:
                        for k in row:
                            knew = unicodedata.normalize("NFKD",k)
                            row[knew] = row.pop(k)
                        if row['Dietary Ingredient (Synonym/Source)']:
                            if not row['DSLD Ingredient Categories']:
                                ingrType = "default"
                            else:
                                ingrType = row['DSLD Ingredient Categories']
                                ingrType = ingrType.lower()
                            if ingrType not in ingrTypeCount:
                                ingrTypeCount[ingrType] = 1
                            else:
                                ingrTypeCount[ingrType] += 1
                        
            except OSError as e:
                pass
        for k in ingrTypeCount:
            writer.writerow([k]+[ingrTypeCount[k]])
            