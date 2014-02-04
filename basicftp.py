''' Handle basic FTP functions. '''
import ftplib

def pullLinks(filename='twitter-site-list.txt',ftpserver='yodelaeu.net76.net',ftpuser='a3672348',ftppass='crackerjack1',directory=None):
    ''' Pull Links from server '''
    print 'Pulling Links from server...'
    session = ftplib.FTP(ftpserver,ftpuser,ftppass)
    with open(filename ,'wb') as localFile: 
        if directory != None:
            session.cwd(directory)    
        session.retrbinary('RETR %s' % filename,localFile.write )
        session.quit()

def pushFile(filename='file.txt',ftpserver='yodelaeu.net76.net',ftpuser='a3672348',ftppass='crackerjack1',directory=None):
    ''' Push status file to server '''
    session = ftplib.FTP(ftpserver,ftpuser,ftppass)
    with open(filename ,'rb') as statusFile:
        if directory != None:
            session.cwd(directory)            
        session.storbinary('STOR ' + filename,statusFile)
        session.quit()