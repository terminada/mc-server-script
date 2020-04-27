import pathlib
import platform
import subprocess
import time
from shutil import copyfile

import psutil
import requests
import texteditor
from hurry.filesize import size


# check java function
def checkjava():
    sp = subprocess.Popen(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = str(sp.communicate())
    if output.find("Java(TM)") == -1:
        return False
    else:
        return True


# check OS and memory
def systemcheck():
    systemcheck.OS = platform.system()
    systemcheck.RAM = size(psutil.virtual_memory().available)
    systemcheck.MRAM = size(psutil.virtual_memory().available / 2)


# create the start.bat script
def generatewindowsscript():
    script = "java -Xms" + systemcheck.MRAM + " -Xmx" + systemcheck.RAM + " -jar server.jar"
    print("Command for starting the server:")
    print("Command chay server:")
    print(script)
    open("server/start.bat", 'w+').write(script)


# GET the list of mc versions
def getminecraftversions():
    url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    response = requests.get(url)
    getminecraftversions.json_mc_versions = response.json()


# GET download link for selected version
def getdownloadlink(url):
    response = requests.get(url)
    return response.json()["downloads"]["server"]["url"]


# functions for easy accessing
def latest_mc_release():
    return getminecraftversions.json_mc_versions["latest"]["release"]


def latest_mc_snapshot():
    return getminecraftversions.json_mc_versions["latest"]["snapshot"]


# download function
def download(url):
    print("Downloading server.jar...")
    print("Dang tai server.jar...")
    file = requests.get(url)
    open("server/server.jar", 'wb').write(file.content)
    print("server.jar downloaded!")
    print("Tai server thanh cong!")


# verify yes and no
def yesnoverifier(input):
    if input not in ("Y", "N", "y", "n", "yes", "no"):
        return "wrong"
    if input in ("Y", "y", "yes"):
        return True
    if input in ("N", "n", "no"):
        return False


# welcome
print("Welcome to Minecraft Java Server Creator!")
print("Chao mung ban den voi trinh tao Server Minecraft Java!")
print()
print("Software by HoangTheBoss@IllumiStudios2020")
print()

# check java
if not checkjava():
    print("Java Runtime not found. Download and install at: https://www.java.com/en/download/")
    print("Ban chua cai Java. Tai va cai dat Java tai: https://www.java.com/en/download/")
    print()

# load version list
print("Loading version list...")
print("Dang tai danh sach phien ban...")
print()
getminecraftversions()
print("Done!")
print("Da tai xong danh sach phien ban!")
print()

# pick version
print("Chon phien ban/Pick a version:")
print("1) Release moi nhat/Latest release: ", latest_mc_release())
print("2) Snapshot moi nhat/Latest snapshot: ", latest_mc_snapshot())
print("3) Khác/Other")
print()

while True:
    chosen_ver_num = input("Ghi so phien ban/Type a number: ")
    if chosen_ver_num not in ('1', '2', '3'):
        print("Hay chon lai trong 1,2,3/Pick again in 1,2,3.")
    else:
        break

if chosen_ver_num == "1":
    chosen_ver = latest_mc_release()
elif chosen_ver_num == "2":
    chosen_ver = latest_mc_snapshot()
elif chosen_ver_num == "3":
    chosen_ver = input("Nhap phien ban cu the (X.X.X or snapshot name): ")

print()

# get download link
for i in getminecraftversions.json_mc_versions["versions"]:
    if i["id"] == chosen_ver:
        downloadlink = getdownloadlink(i["url"])

# download
if pathlib.Path('server/server.jar').is_file():
    print("server.jar exists, overwrite?")
    print("File server.jar da ton tai, ban co muon ghi de khong?")
    overwrite = ""
    while yesnoverifier(overwrite) == "wrong":
        overwrite = input("Nhap Y/N: ")
        if yesnoverifier(overwrite) == True:
            pathlib.Path("/server").mkdir(parents=True, exist_ok=True)
            download(downloadlink)
        elif yesnoverifier(overwrite) == False:
            print("Continuing...")
            print("Dang tiep tuc setup...")
            time.sleep(0.5)
else:
    pathlib.Path("/server").mkdir(parents=True, exist_ok=True)
    download(downloadlink)

print()

# eula
print("Agree to Minecraft EULA? (https://account.mojang.com/documents/minecraft_eula)")
print("Dong y voi thoa thuan nguoi dung cua Minecraft? (https://account.mojang.com/documents/minecraft_eula)")
eula = ""
while yesnoverifier(eula) == "wrong":
    eula = input("Nhap Y/N: ")
    if yesnoverifier(eula) == True:
        open("server/eula.txt", 'w+').write("eula=true")
    elif yesnoverifier(eula) == False:
        print("You selected No. Exiting...")
        print("Ban da chon khong dong y. Dang thoat...")
        time.sleep(1)
        exit()

print()

# config
copyfile("./templates/server.properties.templates", "./server/server.properties")
print("Edit server configuration?")
print("Chinh sua cai dat server?")
configserver = ""
while yesnoverifier(configserver) == "wrong":
    configserver = input("Nhap Y/N: ")
    if yesnoverifier(configserver) == True:
        texteditor.open(filename="server/server.properties", encoding="utf_8")
    elif yesnoverifier(configserver) == False:
        print("Continuing...")
        print("Dang tiep tuc setup...")
        time.sleep(0.5)

print()

# checking system and generate scripts
print("Close all other application in order to get the most accurate system info!")
print("Vui long dong moi ung dung de lay thong tin he thong chinh xac nhat!")
input("Nhan ENTER de tiep tuc...")
print()
systemcheck()
print("Hệ điều hành/OS: ", systemcheck.OS)
print("RAM còn trống/Memory Available: ", systemcheck.RAM)
print()
generatewindowsscript()
print()
print("File chạy server/Server starting script: ", pathlib.Path('server/start.bat').absolute())
