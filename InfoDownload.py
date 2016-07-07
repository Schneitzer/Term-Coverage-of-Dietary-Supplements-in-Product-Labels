import csv
import urllib
import urllib.request as UR
import urllib.error as UE
import os, os.path


#set the URL constant#
CONST_INFO_URL = 'http://www.dsld.nlm.nih.gov/dsld/prdInfo_download.jsp?id='
CONST_DSF_URL = 'http://www.dsld.nlm.nih.gov/dsld/prdDSF_download.jsp?id='
CONST_STATE_URL = 'http://www.dsld.nlm.nih.gov/dsld/prdStatements_download.jsp?id='
CONST_CONTACT_URL = 'http://www.dsld.nlm.nih.gov/dsld/prdContact_download.jsp?id='

#make the subfolders#
curMainDir = os.path.dirname(os.path.abspath(__file__))
infoPath = os.path.join(curMainDir, 'info')
dsfPath = os.path.join(curMainDir, 'dsf')
statePath = os.path.join(curMainDir, 'statement')
contactPath = os.path.join(curMainDir, 'contact')
os.makedirs(infoPath, exist_ok=True)
os.makedirs(dsfPath, exist_ok=True)
os.makedirs(statePath, exist_ok=True)
os.makedirs(contactPath, exist_ok=True)

#download the files#
with open('lstProducts.csv',encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        fileid = row['DSLD ID']
        req = UR.Request(CONST_INFO_URL + fileid)
        try:
            response = UR.urlopen(req)
        except UE.URLError as e:
            if hasattr(e, 'reason'):
                print('Error downloading the data. Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('Error downloading the data due to HTTP error. Error code: ', e.code)
            continue
        UR.urlretrieve(CONST_INFO_URL + fileid, os.path.join(infoPath, fileid) + '_info.csv')
        UR.urlretrieve(CONST_DSF_URL + fileid,  os.path.join(dsfPath, fileid) + '_dsf.csv')
        UR.urlretrieve(CONST_STATE_URL + fileid, os.path.join(statePath, fileid) + '_state.csv')
        UR.urlretrieve(CONST_CONTACT_URL + fileid, os.path.join(contactPath, fileid) + '_contact.csv')
        # input()
    csvfile.close()
