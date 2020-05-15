from ftplib import FTP,error_perm
import os
import datetime
#from getpass import getpass

#Check and send
def Files(ftp, path):
    for name in os.listdir(path):
        localpath = os.path.join(path, name)
        if os.path.isfile(localpath):
            ftp.storbinary('STOR ' + name, open(localpath,'rb'))
        elif os.path.isdir(localpath):
            try:
                ftp.mkd(name)
            except error_perm as e:
                if not e.args[0].startswith('550'): 
                    raise
            ftp.cwd(name)
            Files(ftp, localpath)           
            ftp.cwd("..")
        
#Get (File / Folder)
files=input("Folder or File Location:")

#FTP server Login
try:
    ftp=FTP(input("What server:"))
    user=input("User:")
    #passw=getpass('password:')
    passw=input("What Password")
    ftp.login(user,passw)
except ConnectionRefusedError as e:
    print("Connection error does not exist")
    exit()
except error_perm as e:
    print("Username or Password is wrong")
    exit()
except TimeoutError as e:
    print("Server took a long time to respond")
    exit()

#Server folder
print("Folders:")
ftp.dir()
print()

#Entry in folder or creation
folder=input("MKD(New Folder)\nWhat Folder:")
if folder.__contains__('MKD')or folder.__contains__('mkd'):
    folder=input("Folder Name:")
    ftp.mkd(folder)
ftp.cwd(folder)

#Array creation to save data
date=[]
date.insert(0,"")

#Repeat To check (File / Folder) to send to server
while True:    

#File
    if os.path.isfile(files)==True:        
        info=os.stat(files)
        mod=datetime.datetime.fromtimestamp(info.st_mtime)
        time_mod=mod.strftime("%b %d %Y %H:%M:%S")
        if date[0]!=time_mod:
            date.insert(0,time_mod)
            Files(ftp,files)
            print("Updated:",files)

#Folder
    elif os.path.isdir(files)==True:        
        info=os.stat(files)
        mod=datetime.datetime.fromtimestamp(info.st_atime)
        time_mod=mod.strftime("%b %d %Y %H:%M:%S")
        if date[0]!=time_mod:
            date.insert(0,time_mod)
            Files(ftp,files)
            print("Updated:",files)
