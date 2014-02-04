import os,sys, traceback, getopt
import time
from selenium import webdriver
from selenium import common
import random

####################################################
# these 3 files contain the meat of this program   #
####################################################
from basicftp import *          # basic functions for uploading/downloading from FTP server
from webmanagement import *     # functions for navigating around the sites
from initiateexchange import *  # helper functions for getting everything setup/shutdown
####################################################

def debugPrint(string,override=False):
    ''' if global DEBUG or parameter is true then print '''
    if DEBUG or override:
        print string
        
        
# switch to True to suppress some output
DEBUG = True

# This is the probability of not entering a shortened page.
# this is to mimic a fickle human -- may not be necessary, but 
# can be added in
SITEENTERPROB = 1

# Users stay on the page for at least this long.
MINWAITTIME = 3

# load page
initialPage = 'http://www.beermoneytrafficexchange.net63.net'

# public ftp site for retreiving site list.
pub_server_ftp = 'yodelaeu.net76.net'
pub_server_user='a3672348'
pub_server_pass='crackerjack1'

# for easy loading of specific test sites.
LOADLOCALLIST=True
localFile = 'testlinks.txt'



    
def main():        
    print 'Loading Config...'
    config = loadConfig()
    (driver,main_window_handle) = initiateWebdriver(config,initialPage=initialPage)
    
    numVisits = 0
     
    #   Create file to keep track if people are using program.
    debugPrint('initiating status file...')
    
    #   open credit file
    creditFileName = config['user'] + '.txt'
    header = str(time.mktime(time.localtime())) + ',' + time.strftime("%x %X")
    initiateCreditFile(creditFileName,header,config)
    
    #   Load sites to be used.
    debugPrint('loading sites...')
    sites = loadSites(user=config['user'],url=config['site'],LOADLOCALLIST=LOADLOCALLIST,localFile=localFile)
    
    # window needs to be wide because 'skip' link needs to be 'visible.'
    driver.set_window_size(max(1200,config['size'][0]),max(400,config['size'][1]))
      
    try:    
        for site in sites:
            driver.get(site.url)
            
            # wait at least 5 seconds for shortener skip link.
            time.sleep(2*random.random() + 8)
            # Consider shorteners first.
            if 'linkbucks' in site.url or 'adf.ly' in site.url or 'adfoc.us' in site.url:
                debugPrint('Attempting a Shortened link.')
                debugPrint(site.url)
                enterShortenedURL(driver,site.url,config,main_window_handle)
                
            # regardless of where we started, if we are at an ImgSpice site, enter.
            if 'imgspice' in driver.current_url:
                enterImgSpice(driver,config,main_window_handle)
                
            # try and keep track of how many sites we've gone to.
            numVisits = numVisits + 1
            debugPrint('Went to %s' % site.url)
            
            # wait
            if DEBUG:
                time.sleep(random.random()+1)
            else:
                time.sleep(max(random.randint(config['waittime'][0],config['waittime'][0]),MINWAITTIME))
    except: 
        print 'Here\' the error:'
        traceback.print_exc()
        print 'Done error'

    finally:
        debugPrint('went to ' + str(numVisits) + ' sites.')
        driver.close()
        debugPrint('Done surfing.  Updating credit file...')
        with open(creditFileName,'a') as creditFile:
            creditFile.write(header + "," + str(numVisits)+ '\n') 
        pushFile(filename=creditFileName,directory='/status/')
        os.remove(creditFileName)

if __name__ == '__main__':
    main()
    
    