import os
import time
import random
from basicftp import *

# switch to True to suppress some output
DEBUG = True

def debugPrint(string,override=False):
    ''' if global DEBUG or parameter is true then print '''
    if DEBUG or override:
        print string
        
class site:
    def __init__(self,credentials,url):
        self.user= credentials
        self.url = url
        self.visit = 0

def loadSites(user,url,filename = 'twitter-site-list.txt',LOADLOCALLIST=True,localFile='testlinks.txt'):
    ''' Load sites from file from FTP or a local source   '''
    needToUpdate = True
    pullLinks(filename=filename,directory='/links/')
    
    if DEBUG and LOADLOCALLIST: openfile = open(localFile,'r')
    else:   openfile = open(filename,'r')
    
    with openfile as sitesFile:
        sites = []
        for line in sitesFile:
            debugPrint(line)
            [tmpUser,tmpURL] = line.split(',')
            if tmpUser != user:           
                sites.append(site(tmpUser,tmpURL))
            elif tmpUser==user and tmpURL==url:
                needToUpdate=False
    if needToUpdate:
        sites.append(site(user,url))
        newUserFile=user+'.site.txt'
        with open(newUserFile,'w') as updateUser:
            updateUser.write(','.join([user,url])+'\n')
        pushFile(filename=newUserFile,directory='/new_users/')
        os.remove(newUserFile)
            
    #   Mix up sites -- no favorites.
    random.shuffle(sites)
    
    return sites
    
def checkConfig(config):
    ''' Just check before proceeding that we have everything we need. '''
    requiredValues = ['user','waittime','size','pos','site']
    for i in requiredValues:
        if i not in config.keys():
            print '%s required in config file!' % i
            return False
    
    
def loadConfig():
    ''' 
        load '=' separated file.  
        Required: user, site, size, pos 
    '''
    with open('config.txt') as configFile:
        config = dict()
        for line in configFile:
            try:
                if '=' in line and line[0] != '#':
                    x = line.split('=')
                    if x[0].strip() in ['waittime','pos','size']:
                        config[x[0].strip()] = [int(y) for y in x[1].strip().split(',')]
                    else:
                        config[x[0].strip()] = x[1].strip() 
            except:
                print 'Problem loading config.'
        
        # Show for now.
        debugPrint(config)

    return config

def initiateCreditFile(creditFileName,header,config):
    #   try to load current credit file from ftp
    try:
        pullLinks(filename=creditFileName,directory='/status/')
        with open(creditFileName,'a') as creditFile:
            creditFile.write(header + ",0\n")
    
    #   create new credit file.
    except:
        with open(creditFileName,'w') as creditFile:
            header = str(time.mktime(time.localtime())) + ',' + time.strftime("%x %X")
            creditFile.write(header + ",0\n")    
