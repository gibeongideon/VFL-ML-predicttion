from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd
options = Options()
options.add_argument('--headless')
#options.add_argument('--disable-gpu') # 
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def countD(n,str1="Next job in {} S"):
    countDown = n
    while (countDown >= 0):
        cc=[]
        if countDown != 0:
            cc.append(countDown)
            print(str1.format(cc[0]),end='\r')
            sleep(1)
            cc.clear()
            countDown = countDown - 1
        else:
            break

valz = []
season = []
nvall =[]
def soupg(html,flak):  # function to extract the much needed SEASON VALUE and NUMBER
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())
    #print('YES BITCH')

    if flak == 0:
        
        for lin in soup.find_all("li", class_="sb-option "):

            match = re.search(r"5_(\d+),", str(lin))
            seasn = lin.text.strip()


            if match  is not None:
                for vall in match.groups():
                  #  print(lin)
                    valz.append((vall,seasn))
                
    elif flak == 1:
        
        va33 = soup.find("li", class_="active first")
        #match1 = re.search(r"10_(\d+),(\d+)_(\d+)", str(va33))
        match1 = re.search(r"10_(\d+),", str(va33))
        nval, = match1.groups()
        nvall.append(nval)
        

        #print(lin)
                
                
   # print(valz)# valz
    #return valz

def lData2(pageSource,driver,sis):##not being used here
    #print( 'Saving BIZ begins bitches!,')
    try:
        sleep(1)
        table = pd.read_html(pageSource)

        #for n in range(len(tables)):

           # round  = [n+1,n+1,n+1,n+1,n+1,n+1,n+1,n+1,]# for round adding
        siss = [sis,sis,sis,sis,sis,sis,sis,sis,sis,sis,sis,sis,sis,sis,sis,sis]

        dF=table[0]
        #dF['ROUND'] = pd.Series(round)# for round adding
        dF['SEASON'] = pd.Series(siss)# for round adding
        with open('/home/ideon/Desktop/DataMineCode/STORAGE/Table89.csv', 'a') as f:
            dF.to_csv(f, index=False, header=False)

        print('SAVING TABLES DONE')
        driver.close()

    except:
        pass
        print('Saving err')
        driver.close()
       


        
def reload(link,driver,sis = '000000',flag = 0):
        print('loading results page')
        sleep(1)
        driver.get(link)
        print('getting results page-')
        sleep(2)
        if flag == 3:
            flak = 1
        else:
            flak = 0
        #wait = WebDriverWait(driver, 60)
        
        seas = sis
        
        pageSource=(driver.page_source).encode('utf-8')
        if flag == 1 or flag == 3:
            soupg(pageSource,flak)
        elif flag == 2:
            lData1(pageSource,driver)
        elif flag == 4:
            lData2(pageSource,driver,seas)
     
        else:
            lData(pageSource,driver,seas)
link1 = 'https://vfl3.betradar.com/s4/?clientid=500&language=en&vsportid=1#2_1,3_800,22_7,5_1489868,9_overview'
l_URL = [link1,]           
def latest_URL(valz):
    base_http =  'https://vfl3.betradar.com/s4/?clientid=500&language=en&vsportid=1#2_1,3_800,22_7,5_QQQQQQ,9_overview'
    vas , sis = valz[0]
    n_http = base_http.replace('QQQQQQ',vas)
    l_URL.append(n_http)
    print(l_URL)
    
    
def cdriver():
    driver = webdriver.Chrome(executable_path="/home/ideon/Desktop/DataMineCode/chromedriver",options=options)
    return driver




link = l_URL[-1] 


driver = cdriver()

reload(link,driver,flag = 1)
r_linkS=[]
base_http =  'https://vfl3.betradar.com/s4/?clientid=500&language=en&vsportid=1#2_1,3_800,22_7,5_QQQQQQ,9_overview,25_1,10_PPPPPP,26_5,24_ZZ'
mcount = 0
for vas1 in valz:
    mcount = mcount +1
    reload(link,driver,flag = 3)
   #print(nvall)
    vas , sis = vas1
    gen_http = base_http.replace('QQQQQQ',vas)
    print("Main count", mcount ,"of 30")
    count = 0
    for n in range(30):
        count=count + 1
        gen_http2 = gen_http.replace('PPPPPP',nvall[-1])
        gen_http3 = gen_http2.replace('ZZ',str(n+1))
        r_linkS.append((gen_http3,sis))



count1 = 0
st = 500
for lin in r_linkS[st:]:
    link ,sis = lin
    try:

        driver = cdriver()
        sleep(1)
        count1=count1+1
        print("COUNT:",count1,'of ',len(r_linkS) - st )
        reload(link,driver,sis,flag = 4)

    except: 
        print('am here')
        reload(link,driver,sis ,flag = 4)
        #sleep(2)


latest_URL(valz)
r_linkS.clear()  # clear list 
valz.clear()



print('To resume in 68hrs ','DONT INTERFERE!!!!')
countD(255000,str1="Next RESULT  in {} S")



