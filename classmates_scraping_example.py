#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 11:53:57 2018

@author: taylormattia
"""

###Copy curl command system
import requests
import re
import pandas as pd

#Defining cookies and headers to scrape AJAX database 
cookies = {
    'sbi_debug': 'false',
    'ML_VISITOR': '3cb72b8c72290bb2b004049aa25dff577b940ff420180803094138',
    'CMBeta.memorylane': '1,57,notForced',
    's_fid': '4F7B193C68A70D6C-2E8CD190AC672584',
    '__gads': 'ID=fc6a950f5f6185f4:T=1533314513:S=ALNI_MZ4txkRPsFukEGB0b2vqA1gPI6HQA',
    '_ga': 'GA1.2.1273884201.1533314514',
    '_1ci_7ag23o86kjasbfd': '2bba1f10-973c-11e8-82f9-f5565561aba3',
    'onboarding': '2018-08-06 08:02:06.143',
    '__qca': 'P0-196150204-1534448523316',
    'bafp': '66973160-a18f-11e8-b727-5d72356e37a4',
    '__g_c': 'a%3A0%7Cr%3A%7Cb%3A2%7Cc%3A91959816955473%7Cd%3A2%7Ce%3A0%7Cf%3A1%7Ch%3A0',
    '__g_u': '91959816955473_2_0_1_5_1535228704927_0',
    's_cc': 'true',
    'regComplete': '0',
    'sccssCnfrm': '0',
    'pt': 'brt2',
    '__zlcmid': 'o7hbJ6JDCZXB6D',
    'acq': '1535984530256&7000009753',
    'session': '2&AED217F45B224499834CD8AD501BE343',
    'remember': '1',
    'regStart': '0',
    'site_tour': 'done',
    'sbi_user_sync_complete': 'true',
    'sm_dapi_session': '1',
    '__insp_wid': '5287141',
    '__insp_slim': '1537811552044',
    '__insp_nv': 'true',
    '__insp_targlpu': 'aHR0cDovL3d3dy5jbGFzc21hdGVzLmNvbS9zaXRldWkvcGVvcGxlL2Fubi1jaGFwcGVsbC84NzA2NjcyNzAzP3JlZ2lzdHJhdGlvbklkPTg3MDY2NzI3MDM%3D',
    '__insp_targlpt': 'QW5uIChIYWxsKSBDaGFwcGVsbCwgQ2xhc3Mgb2YgMTk3OCAtIERvbmRlcm8gSGlnaCBTY2hvb2wgLSBDbGFzc21hdGVz',
    '__insp_norec_sess': 'true',
    '_gid': 'GA1.2.249854995.1538321817',
    'FP_stickynav': '{"code_audit_test_link":1538597587}',
    'gomezIncludeScript.sticky': '1,3,not_forced',
    '_litra_ses.fa39': '*',
    's_lv_s': 'Less%20than%201%20day',
    's_vnum': '1596386513770%26vn%3D75',
    's_invisit': 'true',
    'bfp_sn_rf_8b2087b102c9e3e5ffed1c1478ed8b78': '1538577137_448524895959_8b2087b102c9e3e5ffed1c1478ed8b78_Direct',
    'bfp_sn_pl': '1538577137_448524895959',
    'gpv_p1': 'K12%20Member%20List',
    '_litra_id.fa39': 'a-00zj--9aa1e101-d237-46a1-ab1d-89c516918de9.1533314521.77.1538582113.1538512524.4e0632ef-153f-4169-a321-e7ddcd035f17',
    'session_depth': 'www.classmates.com%3D139%7C174660702%3D43%7C971443307%3D66%7C347560335%3D30',
    's_ppv': '-%2C93%2C24%2C2136.4000244140625',
    'PageViewCounter': '3347',
    'ident': '1538582139203&cfdec7207c8c242e98eb5058e64772ff24652c63',
    's_lv': '1538582140377',
    's_nr2': '1538582140383-Repeat',
    's_sq': 'memorylaneprod%3D%2526pid%253DK12%252520Member%252520List%2526pidt%253D1%2526oid%253Djavascript%25253A%25253B%2526ot%253DA%26memorylanedev%3D%2526pid%253Dhttp%25253A%25252F%25252Fwww.classmates.com%25252Famember%25252Flogin.php%2526oid%253Dhttp%25253A%25252F%25252Fwww.classmates.com%25252F%25253Fmiscj%25253DCMHeader%2526ot%253DA',
}

headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Accept': 'text/html, */*; q=0.01',
    'Referer': 'http://www.classmates.com/places/school/Treasure-Coast-High-School/7001661806',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

#Pages 1 - 31
#Setting up page numbers
page_num = list(range(1, 32, 1))
page_num = [str(x) for x in page_num]

#Defining length and parameters
b = len(page_num)
params = [[] for i in range(b)]

for num in range(0, b):
    params[num] = (
        ('communityId', '7001661806'),
        ('communityType', '1'),
        ('startYear', '1960'),
        ('endYear', '2025'),
        ('gradYear', '2011'),
        ('tab', 'yearsAttended'),
        ('sort', 'lastname'),
        ('days', ''),
        ('firstLetter', ''),
        ('ugcIcon', ''),
        ('loadUgcCounts', 'false'),
        ('page', page_num[num]),
        ('_', '1538582140419'),
    )

#Getting response for each group 
response = [[] for i in range(b)]  
for num in range(0,b):
    response[num] = requests.get('http://www.classmates.com/places/ajax/ajax_defaultClassList', headers=headers, params=params[num], cookies=cookies)
    
    
#Getting classmates links
start = 'data-viewFullProfileLink="'
end = '"  rel'

classmates_links = [[] for i in range(b)] 

#Get websites from pages 2 - n
for num in range(0,b):
    classmates_links[num] = re.findall('%s(.*)%s' % (start, end), response[num].text)
    classmates_links[num] = list(set(classmates_links[num])) 
    
#Reducing to one list 
classmates_links = [item for items in classmates_links for item in items]    

#Parse each page
c = len(classmates_links)
page = [[] for i in range(c)]


#Loading modules for multiprocessing
from multiprocessing.dummy import Pool as ThreadPool

#Instantiating Pool objects
pool = ThreadPool()

#Sets Pool size to 8 (or number of cores on the device)
pool = ThreadPool(8)

#Open urls in own threads and return results
from requests.packages.urllib3.util.retry import Retry

#Establishing session
s = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = requests.adapters.HTTPAdapter(max_retries=retry)
s.mount('http://', adapter)
s.mount('https://', adapter)

results = pool.map(s.get, classmates_links)

#First name
first_name = []
first_start = '<input name="firstName" value="'
first_end = '" type="hidden"/>'

for num in range(0, c):
    first_name.append(results[num].text.split(first_start)[-1].split(first_end)[0])


#Last name
last_name = []
last_start = '<input name="lastName" value="'
last_end = '" type="hidden"/> <input type="hidden"'

for num in range(0,c):
    last_name.append(results[num].text.split(last_start)[-1].split(last_end)[0])


#Grad Year
grad_year = []
grad_start = 'Class of '
grad_end = ' </div> <div class'

for num in range(0,c):
    grad_year.append(results[num].text.split(grad_start)[-1].split(grad_end)[0])


#Converting to pandas data frame
df = pd.DataFrame({'classmates_links': classmates_links,
                  'first_name': first_name,
                  'last_name': last_name,
                  'grad_year': grad_year})

#Saving as .csv
df.to_csv('school_120177004148_links.csv')

