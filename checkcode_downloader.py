import urllib2
import time


def main(url,max_num):
    cur_num = 1
    while 1:
        try:
            img = open('checkcode_lib/check_' + str(cur_num) + '.gif', 'wb')
            response = urllib2.urlopen(url)
            img.write(response.read())
            img.close()
            print("The %d check code image done!" %cur_num)
        
        except:
            print("Download failed!")
            
        cur_num += 1
        #time.sleep(1)
        if cur_num > max_num:
            print("\nCompleted!")
            break

if(__name__ == '__main__'):
    url = "http://jwgl.buct.edu.cn/CheckCode.aspx"
    max_num = 1000
    main(url,max_num)