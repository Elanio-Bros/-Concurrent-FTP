from ftplib import FTP,error_perm
import os
import datetime
#from getpass import getpass

#Check and send
def Files(ftp, path):
    if os.path.isfile(path):
        print("Send file:",path)
        name=os.path.basename(path)
        ftp.storbinary('STOR ' + name, open(path,'rb'))
    elif os.path.isdir(path):
        print("Send Folder:",path)
        name=os.path.dirname(path)
        folder_path=path.replace(name,"")
        try:
            ftp.mkd(folder_path)
            ftp.cwd(folder_path)
            for name in list_files_folder(path):
                Files(ftp, name)
            ftp.cwd("..")
            print("Ok")
        except error_perm as e:
            if not e.args[0].startswith('550'): 
                raise Exception("Erro Server Folder")
            
def list_files_folder(dir):
    res=[]
    for file_path in os.listdir(dir):
        res.append(os.path.join(dir, file_path))
    return res
        
#Get (File / Folder)
files=input("Folder or File Location:")

#FTP server Login
try:
    ftp=FTP(input("What server:"))
    user=input("User:")
    #passw=getpass('password:')
    passw=input("What Password:")
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

# #Server folder
print("Folders:")
ftp.dir()
print()

# #Entry in folder or creation
folder=input("MKD(New Folder)\nWhat Folder:")
if folder.__contains__('MKD')or folder.__contains__('mkd'):
    folder=input("Folder Name:")
    ftp.mkd(folder)
ftp.cwd(folder)

# #Array creation to save data
date=[]
date.insert(0,"")

# Colocar apra mandar apenas uns arquivos escolhidos
#Repeat To check (File / Folder) to send to server
while True:    

#File
    if os.path.isfile(files)==True:        
        info=os.stat(files)
        mod=datetime.datetime.fromtimestamp(info.st_mtime)
        time_mod=mod.strftime("%b %d %Y %H:%M:%S")
        if date[0]<time_mod:
            date.insert(0,time_mod)
            print("Updated File:\n")
            Files(ftp,files)
            print("Updated:",files)

#Mandar apenas os arquivos ou pastas que foram modificados
#Folder
    elif os.path.isdir(files)==True:
        for file in list_files_folder(files):
            info=os.stat(file)
            mod=datetime.datetime.fromtimestamp(info.st_atime)
            time_mod=mod.strftime("%b %d %Y %H:%M:%S")
            if date[0]<time_mod:
                print("Updated Folder:\n")
                date.insert(0,time_mod)
                Files(ftp,file)
                print("Updated:",file)