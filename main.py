import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import os
import sys
import pandas as pd
import csv
import json

import re

from wget import download
import mimetypes

all_imgtyp = ["jpg", "png", "gif", "webp",  "png",  "jpeg"]
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

product_data={"title":[], "imagename": [], "img_url": [],"SellerSku": []}
download_manual = {"title":[], "img_url": [],"SellerSku": []}



class downloader:

        
    # Create a downloadfile method
    # Accepting the url and the file storage location
    # Set the location to an empty string by default.

    def downloadFile(self, url, location=""):
         # Download file and with a custom progress bar
        download(url, out = location)


downloadObj = downloader()

def cleanFilename(s):
    if not s:
        return ''
    badchars = ["/",":","?","<",">","|","#","\\",",",".","^",";","(",")","-","&","%","$","@","!","'","+","=","*"]
    for c in badchars:
        s = s.replace(c, '')
    return s



def getExtension(img_src):
    f_type = mimetypes.guess_type(img_src, strict=True)[0]
    if f_type is None:
        return "jpg"
    elif f_type.split("/")[1] == "jpeg":
        return "jpg"
    else:
        return f_type.split("/")[1]







filz = open("tunahama.csv", "r")
csvFile = csv.DictReader(filz)


for line in csvFile:
    clean_title = cleanFilename(line["title"]).replace("  "," ")
    query = clean_title.replace(" ","+")
    print(query)
    driver.get(
    "https://www.google.com/search?q="
    + query
    + "&source=lnms&tbm=isch"
    + "&sclient=img"
    )

    time.sleep(2)
    try:
        all_images = driver.find_elements(By.CSS_SELECTOR,"#islrg > div.islrc > div > a.wXeWr.islib.nfEiy > div.bRMDJf.islir > img")
    except:
        print("bad search term")
    # get first row images

    first_five = all_images[:30]
    for i in range(len(first_five)):
        img_alt =  first_five[i].get_attribute("alt")
        text_1 = img_alt.lower().split(" ")
        print(text_1)
        # print(text_1)
        text_2 = line["title"].replace(")", "").replace("(", "").replace("&","").replace("-","").lower().split(" ")
        for txc in text_2:
            if txc in ["", "brand"]:
                text_2.remove(txc)

        print(text_2)
        matches = [text for text in text_1 if text in text_2]
        print(matches)
        # print(matches , len(matches), len(text_1), len(text_2))
        if len(matches) >= (len(text_2) /2):
            try:
                element = first_five[i]
                element.click()
                time.sleep(10)
                full_image = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img")))
                img_src = full_image.get_attribute("src")
                print(img_src, line["title"])

            except:
                print("no full image")
                img_src = ""
            if (
                    img_src.startswith("data:image")    
                ):
                    print("invalid link")
            elif ("cdnprod.mafretailproxy.com" in img_src
                or "copia.co.ke" in img_src or "msuper.co.ke" in img_src or "e-mart.co.ke" in img_src or "ke.jumia.is/unsafe" in img_src or "www.sangyug.com" in img_src):
                    try:
                        download_manual["title"].append(line["title"])
                        download_manual["img_url"].append(img_src)
                        download_manual["SellerSku"].append(line["SellerSku"])
                    except:
                        print("error")
            else:
                ext = getExtension(img_src)
                try:
                    downloadObj.downloadFile(img_src, f"remaining/{clean_title}.{ext}")
                    product_data["title"].append(line["title"])
                    product_data["imagename"].append(f"{clean_title}.{ext}")
                    product_data["SellerSku"].append(line["SellerSku"])
                    product_data["img_url"].append(img_src)
                except:
                    print("error")
        with open('upload.json', 'w') as f:
            json.dump(product_data, f)
        with open('download.json', 'w') as f:
            json.dump(download_manual, f)
        break
                
               
            
        



      