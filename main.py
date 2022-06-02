import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import time
import os
import sys
import pandas as pd
import csv
import base64
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







# sourcery skip: do-not-use-bare-except
filz = open("searchterms.csv", "r")
csvFile = csv.DictReader(filz)


for line in csvFile:
    clean_title = cleanFilename(line["terms"]).replace("  "," ")
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
    text_2 = line["terms"].replace(")", "").replace("(", "").replace("&","").replace("-","").lower()
    chosen_img = []
    chosen_score= []
    for img in all_images:
        img_text = cleanFilename(img.get_attribute("alt")).lower()
        score = fuzz.ratio(text_2, img_text)
        if score > 50:
            chosen_img.append(img)
            chosen_score.append(score)
    if chosen_img:
        chosen_score = sorted(chosen_score, reverse=True)
        lucky_score = chosen_score[0]
        lucky_img = chosen_img[chosen_score.index(lucky_score)]
        try:
            lucky_img.click()
            time.sleep(5)
            full_image = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img")))
        except:
            print("no image")
            continue
        try:
            img_src = full_image.get_attribute("src")
            print(lucky_score, line["terms"], img_src)
            ext = getExtension(img_src)
            img_name = cleanFilename(line["terms"]) + "." + ext
            if img_src.startswith("data:image"):
                try:
                    decode_img = base64.b64decode(img_src.split(",")[1])
                    img_path = f"dataimages/{img_name}"
                    with open(img_path, "wb") as f:
                        f.write(decode_img)
                    
                except:
                    print("bad image")
            else:
                try:
                    downloadObj.downloadFile(img_src, "images/" + img_name)
                except:
                    print("bad image")
        except:
            print("no full image")
    else:
        print("no image")
    
    


