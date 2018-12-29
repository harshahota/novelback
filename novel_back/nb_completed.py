from db_functions import get_novel_updates
from soup_functions import novel_details,post_chapter
from util_functions import print_log


novelid = 3
novellabel = 'thunder-martial'
novel_latest_update = 516
common_url = 'https://lnmtl.com/chapter/thunder-martial-chapter-'
latest_chapter_number = 3570
print_log("The last update of %s in database is %s"%(novellabel,novel_latest_update),False)
if(common_url != 'None' or latest_chapter_number != 'None'):
    print_log("the latest update of %s is %s"%(novellabel,latest_chapter_number),False)
    if(latest_chapter_number-novel_latest_update > 0):
        for i in range(novel_latest_update+1,latest_chapter_number+1):
            post_chapter(novelid,novellabel,common_url,i)
    else:
        print_log("The chapters for novel %s are up to date"%novellabel,False)
