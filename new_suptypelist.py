# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 03:58:08 2016

@author: Schneitzer
"""

import os, os.path
import csv
import re
import unicodedata

curMainDir = os.path.dirname(os.path.abspath(__file__))
dsfPath = os.path.join(curMainDir, 'dsf')
csvName = os.path.join(curMainDir, 'ingrTypeStat.csv')

filter1 = [r"\borganic\b",r"\bstandardi(s|z)ed\b",r"\bcertified\b",r"\band\b"]
filter2 = [r"\bextract\w*\b",r"\bfruit\w*\b",r"\bpowder\w*\b",r"\bberr\w*\b",r"\bliquid\w*\b",r"\bconc\b",r"\bconcentrate\w*\b",r"freeze-dried",r"\bfreeze\b",r"\bdried\b",r"\bjuice\b", r"\bfluid\b", r"\bcomplex\b", r"\bblend\b",r"\bherb\b",r"\bsprout\w*\b",r"\bseed\w*\b",r"\baqueous\b",r"\bgel\b",r"\bsupercritical\b"]
brandpattern = r'[(]TM[)]|[(]R[)]'
linneausPattern = r'([(])(\b[A-Z][a-z]+\b) (\b[a-z]+\b)( L\.)?([)])'
#typepattern = r'(.*)(\[)(A[0-9]{4})(\])'
numberpattern = r'\b[0-9]+(?!_)'
dosepattern = r'([Mm][Cc]?[Gg]|[Oo][Zz])\.?'
extracharpattern = r'([\[\]\"\{\}\.\,\%\:])|((?<!\w)\'(?!\w))'
amperpattern = r'\&'
hyphenpattern = r'-'
underpattern = r'_'
htmlpattern = r'(\<p.*?\>)(.*?)(\;\<\/p>)'
parpattern = r'[(].*[)]'

typelist = []
ingrset= [set() for i in range(1,21)]
ingrcompare = [[] for i in range(1,21)]
ingrcounter = [0 for i in range(1,21)]

files = [open('IngrType%i.csv' %i, 'w', encoding='utf-8-sig') for i in range(1,21)]
#for f in files:
#    f.close()
with open('ingrTypeStat.csv',encoding='utf-8-sig') as typefile:
    reader = csv.DictReader(typefile)
    for row in reader:
        if row['Type']:
            typelist.append(row['Type'])

with open('lstProducts.csv',encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        ingrlinn = ""
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
                        ingr = row['Dietary Ingredient (Synonym/Source)'] # extract the ingredient information
                        original = ingr
                        ingr = re.sub(brandpattern, '', ingr)
                        ingr = re.sub(htmlpattern, r'\2,',ingr)
                        ingr = re.sub(extracharpattern, '&', ingr)
                        ingr = re.sub(amperpattern, ' ', ingr)
                        ingr = re.sub(dosepattern, '', ingr) # remove all redundant information
                        ingr = re.sub(hyphenpattern, '_', ingr)
                        ingr = re.sub(numberpattern,'',ingr)
                        #linntag = re.search(linneausPattern, ingr)
                        ingr = re.sub(parpattern, '', ingr)
                        ingr = re.sub(underpattern, '-', ingr)
                        #if linntag:
                            #ingrlinn = " ".join([linntag.group(2)]+[linntag.group(3)]+[linntag.group(4)])
                            #ingrlinn = ingrlinn.lower()
                        ingr = ingr.lower() # make every character lowercase for easier preprocessing
                        
                        for pattern in filter1:
                            ingr = re.sub(pattern, '', ingr) #remove "organic" and "standardized"
                        for pattern in filter2:
                            ingr = re.sub(pattern, '', ingr)
                        ingrsplit = ingr.split()
                        ingr = " ".join(ingrsplit) # remove redundant white space
                        if not row['DSLD Ingredient Categories']:
                            ingrType = "default"
                        else:
                            ingrType = row['DSLD Ingredient Categories']
                        if ingrType in typelist:
                            fileindex = typelist.index(ingrType)
                            ingrset[fileindex].add(ingr)
                            ingrcompare[fileindex] += [(original,ingr)]
                            #if ingrlinn:                            
                                #ingrset[fileindex].add(ingrlinn)               
        except OSError as e:
            pass
#==============================================================================
#     for s in ingrset:
#         outputlist = list(s)
#         fileindex = ingrset.index(s)
#         typewriter = csv.writer(files[fileindex], quoting = csv.QUOTE_NONE, quotechar = '')
#         for ing in sorted(outputlist):
#             try:
#                 typewriter.writerow([ing])
#             except csv.Error as e:
#                 print(ing)
#                 continue
#==============================================================================
    for t in ingrcompare:
        fileindex = ingrcompare.index(t)
        typewriter = csv.writer(files[fileindex], quoting = csv.QUOTE_MINIMAL, quotechar = '|')
        typewriter.writerow(["Original Name"]+["Processed Name"])
        for inggroup in t:
            try:
                typewriter.writerow([inggroup[0]]+[inggroup[1]])
            except csv.Error as e:
                print(inggroup[0],inggroup[1])
                continue
            
    for f in files:
        f.close()
        fileindex = files.index(f)
        newname = typelist[fileindex] + '_new.txt'
        os.rename(f.name,newname)    
        