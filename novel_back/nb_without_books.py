from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from config import drivers_location
chrome_driver_path = drivers_location + '/chromedriver'
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

from db_functions import get_novel_updates,insert_single_chapter,insert_missed_chapter
from soup_functions import novel_details,post_chapter
from util_functions import print_log

myresult = get_novel_updates()
for result in myresult:
    novelid = result[0]
    novellabel = result[1]
    novel_latest_update = result[2]
    print_log("The last update of %s in database is %s"%(novellabel,novel_latest_update),False)
    common_url,latest_chapter_number = novel_details(novellabel)
    # latest_chapter_number = 40
    if(common_url != 'None' or latest_chapter_number != 'None'):
        print_log("the latest update of %s is %s"%(novellabel,latest_chapter_number),False)
        if(latest_chapter_number-novel_latest_update > 0):
            driver = webdriver.Chrome(chrome_driver_path,chrome_options=chrome_options)

            for chapter_no in range(novel_latest_update+1,latest_chapter_number+1):
                # post_chapter(novelid,novellabel,common_url,chapter_no)
                tries = 3
                for j in range(tries):
                    try:
                        url = common_url+str(chapter_no)
                        driver.get(url)
                        texts = driver.find_elements_by_class_name('translated')
                        finaltext = ""
                        for text in texts:
                            unedited = text.text.replace('„','“')
                            # unedited = bytes(unedited, 'utf-8').decode('utf-8', 'ignore')
                            finaltext += unedited + "\n"
                        insert_single_chapter(novelid,novellabel,chapter_no,finaltext)
                    except (AttributeError,NoSuchElementException) as e:
                        if j < tries - 1: # i is zero indexed
                            continue
                        else:
                            insert_missed_chapter(novelid,novellabel,chapter_no)
                            print_log("error page not loaded %s"%e,True)
                            pass
                    break
            driver.close()
        else:
            print_log("The chapters for novel %s are up to date"%novellabel,False)
