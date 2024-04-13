from ftplib import FTP,error_perm
import os
import datetime
#from getpass import getpass

#Array creation to save data
format_date="%b %d %Y %H:%M:%S"
date=[]
date.insert(0,datetime.date.today().strftime(format_date))

#Check and send
def File(ftp, path):
        print("Send file:",path)
        name=os.path.basename(path)
        ftp.storbinary('STOR ' + name, open(path,'rb'))

def Dir(ftp,path):
    print("Send Folder:",path)
    name=os.path.dirname(path)
    folder_path=path.replace(name+"\\","")
    try:
        ftp.mkd(folder_path)
    except error_perm as e:
        if not e.args[0].startswith('550'): 
            raise Exception("Erro Server Folder")
    ftp.cwd(folder_path)
    print("Ok")

def Dir_close(ftp):
        ftp.cwd("..")
        print("Close")
            
def list_files_folder(dir):
    res=[]
    for file_path in os.listdir(dir):
        res.append(os.path.join(dir, file_path))
    return res

def verify_file(file):
    info=os.stat(file)
    mod=datetime.datetime.fromtimestamp(info.st_mtime)
    time_mod=mod.strftime(format_date)
    # print(time_mod,date[0]);
    if date[0]<=time_mod:
        date.insert(0,time_mod)
        print("Updated File:\n")
        File(ftp,file)
        print("Updated:",file)

def verify_dir(dir,ignore):
    # info=os.stat(dir)
    # mod=datetime.datetime.fromtimestamp(info.st_mtime)
    # time_mod=mod.strftime(format_date)
    # date[0]<time_mod and 
    for path in list_files_folder(dir):
        if not any(argument in path for argument in ignore):
            if os.path.isfile(path):
                verify_file(path)
            elif os.path.isdir(path):
                Dir(ftp,path)
                verify_dir(path,ignore)
                Dir_close(ftp)

#Get (File / Folder)
files=input("Folder or File Location:")

#FTP server Login
try:
    server=input("What server:")
    ftp=FTP(server)
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
folder=input("MKD (Create new Folder)\nWhat Folder:")
if folder.__contains__('MKD') or folder.__contains__('mkd'):
    folder=input("Folder Name:")
    ftp.mkd(folder)
ftp.cwd(folder)

# Colocar para mandar apenas uns arquivos escolhidos
# Mandar apenas os arquivos ou pastas que foram modificados
#Repeat To check (File / Folder) to send to server
while True:
#File
    if os.path.isfile(files):      
        verify_file(files)
#Folder
    elif os.path.isdir(files):      
        ignore_folders=[".git"]
        verify_dir(files,ignore_folders)