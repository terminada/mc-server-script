import pathlib
import platform
import subprocess
import time
from shutil import copyfile

import psutil
import requests
import speedtest
import texteditor
from hurry.filesize import size
from pySmartDL import SmartDL


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
    return platform.system(), size(psutil.virtual_memory().available)


# create the start.bat script
def generatescript(os, inputmem):
    generated_script = "java -Xms" + inputmem + " -Xmx" + inputmem + " -jar server.jar"
    if os == "Windows":
        open("server/start.bat", 'w+').write(generated_script)
    elif os == "Linux":
        open("server/start.sh", 'w+').writelines(["#!/bin/sh", generated_script])
    elif os == "MacOS":
        open("server/start.sh", 'w+').writelines(["#!/bin/sh", generated_script])
    return generated_script


# GET the list of mc versions
def getminecraftversions():
    url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    response = requests.get(url)
    return response.json()


# GET download link for selected version
def getdownloadlink(url):
    response = requests.get(url)
    return response.json()["downloads"]["server"]["url"]


# functions for easy accessing
def latest_mc_release(json):
    return json["latest"]["release"]


def latest_mc_snapshot(json):
    return json["latest"]["snapshot"]


# download function
def download(url):
    pathlib.Path("server").mkdir(parents=True, exist_ok=True)
    print("Downloading server.jar...")
    print("Dang tai server.jar...")
    obj = SmartDL(url, "server/server.jar")
    obj.start()
    # file = requests.get(url)
    # open("server/server.jar", 'wb').write(file.content)
    print("server.jar downloaded!")
    print("Tai server thanh cong!")


# verify yes and no
def yesnoverifier(inp):
    if inp.lower().startswith("y"):
        return True
    if inp.lower().startswith("n"):
        return False


# verify version
def verifyversion(json, version):
    for i in json["versions"]:
        if i["id"] == version:
            return True
    return False


# network speedtest
def netspeed():
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download(threads=8)
    s.upload(threads=8)
    results_dict = s.results.dict()
    return round((min(results_dict["download"], results_dict["upload"])) / 1048576)


# calculations
def calc_players(net, ram):
    if ram.endswith("G"):
        ram_int = int(ram[:-1]) * 1024
    else:
        ram_int = int(ram[:-1])
    net_players = int(net) / 0.33
    ram_players = (ram_int * 0.75) / 64
    max_player = round(min(ram_players, net_players))
    return str(max_player)


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
versions_json = getminecraftversions()
print("Done!")
print("Da tai xong danh sach phien ban!")
print()

# pick version
print("Chon phien ban/Pick a version:")
print("1) Release moi nhat/Latest release: ", latest_mc_release(versions_json))
print("2) Snapshot moi nhat/Latest snapshot: ", latest_mc_snapshot(versions_json))
print("3) Khac/Other")
print()

while True:
    chosen_ver_num = input("Ghi so phien ban/Type a number: ")
    if chosen_ver_num not in ('1', '2', '3'):
        print("Hay chon lai trong 1,2,3/Pick again in 1,2,3.")
    else:
        break

if chosen_ver_num == "1":
    chosen_ver = latest_mc_release(versions_json)
elif chosen_ver_num == "2":
    chosen_ver = latest_mc_snapshot(versions_json)
elif chosen_ver_num == "3":
    chosen_ver = input("Nhap phien ban cu the (X.X.X or snapshot name): ")
    while not verifyversion(versions_json, chosen_ver):
        chosen_ver = input("Phien ban khong dung, xin hay nhap lai/Try again: ")

print()

# eula
print("Agree to Minecraft EULA? [Y/n] (https://account.mojang.com/documents/minecraft_eula)")
eula = input("Dong y voi thoa thuan nguoi dung cua Minecraft? [Y/n] ("
             "https://account.mojang.com/documents/minecraft_eula)")
if eula == "":
    pathlib.Path("server").mkdir(parents=True, exist_ok=True)
    open("server/eula.txt", 'w+').write("eula=true")
else:
    while True:
        if yesnoverifier(eula):
            pathlib.Path("server").mkdir(parents=True, exist_ok=True)
            open("server/eula.txt", 'w+').write("eula=true")
            break
        elif not yesnoverifier(eula):
            print("You selected No. Exiting...")
            print("Ban da chon khong dong y. Dang thoat...")
            time.sleep(1)
            exit()
        else:
            eula = input("Nhap Y/N: ")

print()

# checking system and generate scripts
print("Close all other application in order to get the most accurate system info!")
print("Vui long dong moi ung dung de lay thong tin he thong chinh xac nhat!")
input("Nhan ENTER de tiep tuc...")
print()
systeminfo = systemcheck()
print("He dieu hanh/OS: ", systeminfo[0])
print("RAM con trong/Memory Available: ", systeminfo[1])
print()
ram = str(systeminfo[1])
print("How much RAM do you want to allocate to the server? [" + ram + "]")
chosen_mem = input("Ban muon cho server bao nhieu RAM? [" + ram + "]:")
print()
if chosen_mem == "":
    chosen_mem = systeminfo[1]
else:
    while (not chosen_mem.endswith("M")) and (not chosen_mem.endswith("G")):
        if chosen_mem.endswith("B"):
            chosen_mem = chosen_mem[:-1]
            break
        else:
            print("Enter a value ends with 'M' or 'G': ")
            chosen_mem = input("Hay nhap so ket thuc boi 'M' hoac 'G': ")
script = generatescript(systeminfo[1], chosen_mem)
print("Command for starting the server:")
print("Command chay server: " + script)
print("File chay server/Server starting script: ", pathlib.Path('server/start.bat').absolute())
print()

print("Do you want to run network speedtest? [Y/n]")
st_confirm = input("Ban co muon do toc do mang? [Y/n]")
if st_confirm == "":
    network_speed = netspeed()
    print("Toc do/Speed: " + str(network_speed))
else:
    while True:
        if yesnoverifier(st_confirm):
            network_speed = netspeed()
            print("Toc do/Speed: " + netspeed())
            break
        elif not yesnoverifier(st_confirm):
            manual_down = input("Nhap toc do tai xuong/Download speed (Mbps): ")
            manual_up = input("Nhap toc do tai len/Upload speed (Mbps): ")
            network_speed = min(manual_down, manual_up)
            time.sleep(0.5)
            break
        else:
            configserver = input("Nhap Y/N: ")
print()

# config
print("Recommended player slots (max-player): " + calc_players(network_speed, chosen_mem))
print("So slot duoc khuyen cao (max-player): " + calc_players(network_speed, chosen_mem))
print()
copyfile("./templates/server.properties.templates", "./server/server.properties")
print("Edit server configuration? [Y/n]")
configserver = input("Chinh sua cai dat server? [Y/n]")
if configserver == "":
    texteditor.open(filename="server/server.properties", encoding="utf_8")
else:
    while True:
        if yesnoverifier(configserver):
            texteditor.open(filename="server/server.properties", encoding="utf_8")
            break
        elif yesnoverifier(configserver) == False:
            print("Continuing...")
            print("Dang tiep tuc setup...")
            time.sleep(0.5)
            break
        else:
            configserver = input("Nhap Y/N: ")
print()

# get download link
for i in versions_json["versions"]:
    if i["id"] == chosen_ver:
        downloadlink = getdownloadlink(i["url"])

# download
if pathlib.Path('server/server.jar').is_file():
    print("server.jar exists, overwrite? [y/N]")
    overwrite = input("File server.jar da ton tai, ban co muon ghi de khong? [y/N]")
    if overwrite == "":
        print("Continuing...")
        print("Dang tiep tuc setup...")
        time.sleep(0.5)
    else:
        while True:
            if yesnoverifier(overwrite):
                download(downloadlink)
                break
            elif not yesnoverifier(overwrite):
                print("Continuing...")
                print("Dang tiep tuc setup...")
                time.sleep(0.5)
                break
            else:
                overwrite = input("Nhap Y/N: ")
else:
    download(downloadlink)
print()
