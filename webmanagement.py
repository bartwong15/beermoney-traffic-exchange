import time
from selenium import webdriver
from selenium import common
import random

# switch to True to suppress some output
DEBUG = True

def debugPrint(string,override=False):
    ''' if global DEBUG or parameter is true then print '''
    if DEBUG or override:
        print string


def initiateWebdriver(config,initialPage = 'http://www.beermoneytrafficexchange.net63.net'):
    ''' initiates webdriver with settings specified in config file. '''
    print 'Starting webdriver...'
    driver = webdriver.Firefox()
    driver.set_window_position(0,0)
    driver.set_window_size(900,900)
    driver.get(initialPage)
    time.sleep(3)
    #   Make small
    driver.set_window_size(max(100,config['size'][0]),max(200,config['size'][1]))
    #   Set off screen
    driver.set_window_position(config['pos'][0],config['pos'][1])
    #driver.set_window_position(-1000,-1000)

    main_window_handle = driver.current_window_handle
    print main_window_handle
    return (driver, main_window_handle)
    
def enterImgSpice(driver,config,main_window_handle):
    ''' this function just handles the entry page into an ImgSpice site. '''
    print 'Entering ImgSpice site.'
    # initial wait
    time.sleep(4*random.random()+0.2)
    links = driver.find_elements_by_tag_name('a')
    for link in links:
        if 'Continue' in link.text:
            print 'Clicking %s' % link.text
            link.click()
            #   Let popups open
            time.sleep(0.5)
            closeAllWindowsExceptMainScript(driver,main_window_handle)
            break    

def enterShortenedURL(driver,url,config,main_window_handle):     
    ''' this function just handles the entry page into a LinkBucks/Adfly/Adfocus link. '''

    try:
        # determine which shortener was used.
        if 'linkbucks' in url:
            link = driver.find_element_by_id('skiplink')
        if 'adf.ly' in url:
            link = driver.find_element_by_id('skip_button')
        if 'adfoc.us' in url:
            link = driver.find_element_by_class_name('skip')
            
        debugPrint('Clicking Skip button')
        link.click()
        
        #   Let popups open
        time.sleep(.4)
        closeAllWindowsExceptMainScript(driver,main_window_handle)
    except common.exceptions.NoSuchElementException:
        print 'Skip Link not found -- possible Captch required...'
        print 'Moving on to next link.'

def closeAllWindowsExceptMain(driver,main_window_handle):
    ''' Generic close all windows except main window. No script handling '''
    try:
        for handle in driver.window_handles:
            driver.switch_to_window(handle)
            if driver.current_window_handle != main_window_handle:
                driver.close()
    except:
        debugPrint('Failed to close at least one window')
    finally:
        # Always end on main
        driver.switch_to_window(main_window_handle)

def closeAllWindowsExceptMainScript(driver,main_window_handle):
    ''' this function will close all pop-ups and alerts from a linkbucks link '''
    # close all except main window
    for handle in driver.window_handles:
        driver.switch_to_window(handle)
        if driver.current_window_handle != main_window_handle:
            try:
                time.sleep(0.5)
                print driver.current_window_handle
                driver.close()
                # linkbucks usually tries to put some javascript alert in
                # this code should try to get around that.
                try:
                    alert = driver.switch_to_alert()
                    time.sleep(1)
                    alert.accept()
                except common.exceptions.NoAlertPresentException:
                    print 'No Alert present...'
            except common.exceptions.NoSuchWindowException:
                print 'Window already closed'
                
    try:
        # back to main window
        driver.switch_to_window(main_window_handle)
    except:
        print 'whoops'