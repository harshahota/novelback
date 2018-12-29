import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from db_functions import insert_single_chapter,insert_missed_chapter
from util_functions import print_log

import math

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
tries = 3

dir_path=os.path.dirname(os.path.realpath(__file__))
chrome_driver_path = dir_path + '/drivers/chromedriver'
chrome_options = Options()
chrome_options.add_argument("--headless")

def no_of_digits(num):
    return int(math.log10(num))+1

def novel_details(label):
    for i in range(tries):
        try:
            driver = webdriver.Chrome(chrome_driver_path,chrome_options=chrome_options)
            baseurl = 'https://lnmtl.com/novel/'
            url = baseurl+label
            driver.get(url)
            chapter = driver.find_element_by_class_name('chapter-link')
            latest_link = chapter.get_attribute("href")
            latest_chapter_number = int(chapter.find_element_by_tag_name('span').text[1:])
            common_url = latest_link[:-no_of_digits(latest_chapter_number)]
            driver.close()
            return common_url,latest_chapter_number
        except (AttributeError, NoSuchElementException) as e:
            driver.close()
            if i < tries - 1: # i is zero indexed
                continue
            else:
                print_log("error page not loaded %s"%e,True)
                pass
        break

def post_chapter(id,label,common_url,chapter_no):
    for i in range(tries):
        try:
            driver = webdriver.Chrome(chrome_driver_path,chrome_options=chrome_options)
            url = common_url+str(chapter_no)
            driver.get(url)
            texts = driver.find_elements_by_class_name('translated')
            finaltext = ""
            for text in texts:
                unedited = text.text.replace('„','“')
                # unedited = bytes(unedited, 'utf-8').decode('utf-8', 'ignore')
                finaltext += unedited + "\n"
            print(finaltext[329])
            driver.close()
            insert_single_chapter(id,label,chapter_no,finaltext)
        except (AttributeError,NoSuchElementException) as e:
            driver.close()
            if i < tries - 1: # i is zero indexed
                continue
            else:
                insert_missed_chapter(id,label,chapter_no)
                print_log("error page not loaded %s"%e,True)
                pass
        break
