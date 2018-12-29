from db_functions import get_novel_updates
from soup_functions import novel_details,post_chapter
from util_functions import print_log

myresult = get_novel_updates()
for result in myresult:
    novelid = result[0]
    novellabel = result[1]
    novel_latest_update = result[2]
    print_log("The last update of %s in database is %s"%(novellabel,novel_latest_update),False)
    common_url,latest_chapter_number = novel_details(novellabel)
    # latest_chapter_number = 20
    if(common_url != 'None' or latest_chapter_number != 'None'):
        print_log("the latest update of %s is %s"%(novellabel,latest_chapter_number),False)
        if(latest_chapter_number-novel_latest_update > 0):
            for i in range(novel_latest_update+1,latest_chapter_number+1):
                post_chapter(novelid,novellabel,common_url,i)
        else:
            print_log("The chapters for novel %s are up to date"%novellabel,False)
