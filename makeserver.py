import argparse
import os
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
def check_java():
    sp = subprocess.Popen(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = str(sp.communicate())
    if output.find("Java(TM)") == -1:
        return False
    return True


# check OS and memory
def system_check():
    return platform.system(), size(psutil.virtual_memory().available)


# create the start.bat script
def generate_script(os, inputmem, lithium):
    if not lithium:
        generated_script = "java -Xms" + inputmem + " -Xmx" + inputmem + " -jar server.jar"
    elif lithium:
        generated_script = "java -Xms" + inputmem + " -Xmx" + inputmem + " -jar fabric-server-launch.jar"
    if os == "Windows":
        open("server/start.bat", 'w+').write(generated_script)
        print("File chay server/Server starting script: ", pathlib.Path('server/start.bat').absolute())
    elif os == "Linux":
        open("server/start.sh", 'w+').writelines(["#!/bin/sh", generated_script])
        print("File chay server/Server starting script: ", pathlib.Path('server/start.sh').absolute())
    elif os == "MacOS":
        open("server/start.sh", 'w+').writelines(["#!/bin/sh", generated_script])
        print("File chay server/Server starting script: ", pathlib.Path('server/start.sh').absolute())
    return generated_script


# GET the list of mc versions
def getminecraftversions():
    url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    response = requests.get(url)
    return response.json()


# GET download link for selected version
def get_download_link(url):
    response = requests.get(url)
    return response.json()["downloads"]["server"]["url"]


# GET lithium download link
def get_fabric_link():
    url = "https://meta.fabricmc.net/v2/versions/installer"
    response = requests.get(url)
    return response.json()[0]["url"]


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


# download fabric
def download_fabric(url):
    pathlib.Path("server").mkdir(parents=True, exist_ok=True)
    print("Downloading fabric_installer.jar...")
    print("Dang tai fabric_installer.jar...")
    obj = SmartDL(url, "server/fabric_installer.jar")
    obj.start()
    print("fabric_installer.jar downloaded!")
    print("Tai fabric thanh cong!")


# verify yes and no
def yes_no_verifier(inp):
    if inp.lower().startswith("y"):
        return True
    if inp.lower().startswith("n"):
        return False


# verify version
def verify_version(json, version):
    for j in json["versions"]:
        if j["id"] == version:
            return True
    return False


# network speedtest
def net_speed():
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


# argument handling
argparser = argparse.ArgumentParser(description="Minecraft Java Server Creator")
argparser.add_argument("-v", "--version", default="manual", help="Minecraft snapshot/release/custom Version")
argparser.add_argument("-e", "--eula", default="manual", choices=["y", "n", "manual"], help="Agree to the EULA?")
argparser.add_argument("-l", "--lithium", default="manual", choices=["y", "n", "manual"],
                       help="Use Fabric + Lithium for better performance?")
argparser.add_argument("-m", "--memory", default="manual", help="Amount of RAM to allocate to the server")
argparser.add_argument("-n", "--network", default="manual",
                       help="The minimum of your Download/Upload Speed in Mbit metrics. manual = prompt, auto = use "
                            "speedtest, else type numbers only")
argparser.add_argument("-s", "--slots", default="0", type=int,
                       help="Number of slots to be available on your server, 0 = manual. Ignore if --network is passed")
argparser.add_argument("-o", "--overwrite", default="manual", choices=["y", "n", "manual"],
                       help="Overwrite existing JAR file?")

args = argparser.parse_args()

# welcome
print("Welcome to Minecraft Java Server Creator!")
print("Chao mung ban den voi trinh tao Server Minecraft Java! \n")
print("Software by HoangTheBoss@IllumiStudios2020 \n")

# check java
if not check_java():
    print("Java Runtime not found. Download and install at: https://www.java.com/en/download/")
    print("Ban chua cai Java. Tai va cai dat Java tai: https://www.java.com/en/download/")

# load version list
print("Loading version list...")
print("Dang tai danh sach phien ban... \n")

versions_json = getminecraftversions()
print("Done!")
print("Da tai xong danh sach phien ban! \n")

if args.version == "manual":
    # pick version
    print("Chon phien ban/Pick a version:")
    print("1) Release moi nhat/Latest release: ", latest_mc_release(versions_json))
    print("2) Snapshot moi nhat/Latest snapshot: ", latest_mc_snapshot(versions_json))
    print("3) Khac/Other \n")

    while True:
        chosen_ver_num = input("Ghi so phien ban/Type a number: ")
        # print(chosen_ver_num)  # for testing
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
        while not verify_version(versions_json, chosen_ver):
            chosen_ver = input("Phien ban khong dung, xin hay nhap lai/Try again: ")

    print()

elif args.version == "release":
    chosen_ver = latest_mc_release(versions_json)
elif args.version == "snapshot":
    chosen_ver = latest_mc_snapshot(versions_json)
elif verify_version(versions_json, args.version):
    chosen_ver = args.version
else:
    print("Invalid --version argument value passed, do -h or --help for more information.")
    print("Exiting...")
    exit()

# get download link
for i in versions_json["versions"]:
    if i["id"] == chosen_ver:
        downloadlink = get_download_link(i["url"])

# download
if pathlib.Path('server/server.jar').is_file():
    if args.overwrite == "manual":
        print("server.jar exists, overwrite? [y/N]")
        overwrite = input("File server.jar da ton tai, ban co muon ghi de khong? [y/N]")
        if overwrite == "":
            print("Continuing...")
            print("Dang tiep tuc setup...")
            time.sleep(0.5)
        else:
            while True:
                if yes_no_verifier(overwrite):
                    download(downloadlink)
                    break
                elif not yes_no_verifier(overwrite):
                    print("Continuing...")
                    print("Dang tiep tuc setup...")
                    time.sleep(0.5)
                    break
                else:
                    overwrite = input("Nhap Y/N: ")
    elif args.overwrite == "y":
        download(downloadlink)
else:
    download(downloadlink)
print()

# use fabric + lithium
if args.lithium == "manual":
    print("Use fabric and lithium for better server performance? [Y/n]")
    lithium_yesno = input("Su dung fabric va lithium de giam lag server? [Y/n]")
    print()
    if lithium_yesno == "":
        lithium_yesno = "y"
elif args.lithium == "y":
    lithium_yesno = "y"
else:
    lithium_yesno = "n"

while True:
    if yes_no_verifier(lithium_yesno):
        if pathlib.Path('server/fabric-server-launch.jar').is_file():
            if args.overwrite == "manual":
                print("fabric-server-launch.jar exists, overwrite? [y/N]")
                overwrite = input("File fabric-server-launch.jar da ton tai, ban co muon ghi de khong? [y/N]")
                if overwrite == "":
                    print("Continuing...")
                    print("Dang tiep tuc setup...")
                    time.sleep(0.5)
                    break
                else:
                    while True:
                        if yes_no_verifier(overwrite):
                            fabric_link = get_fabric_link()
                            download_fabric(fabric_link)
                            os.system("java -jar server/fabric_installer.jar server -dir server -mcversion " +
                                      chosen_ver)
                            break
                        elif not yes_no_verifier(overwrite):
                            print("Continuing...")
                            print("Dang tiep tuc setup...")
                            time.sleep(0.5)
                            break
                        else:
                            overwrite = input("Nhap Y/N: ")
            elif args.overwrite == "y":
                fabric_link = get_fabric_link()
                download_fabric(fabric_link)
                os.system("java -jar server/fabric_installer.jar server -dir server -mcversion " + chosen_ver)
                break
        else:
            fabric_link = get_fabric_link()
            download_fabric(fabric_link)
            os.system("java -jar server/fabric_installer.jar server -dir server -mcversion " + chosen_ver)
        print()
    elif not yes_no_verifier(lithium_yesno):
        print("Continuing...")
        print("Dang tiep tuc setup...")
        time.sleep(0.5)
        break
    else:
        lithium_yesno = input("Nhap Y/N: ")

# eula
if args.eula == "manual":
    print("Agree to Minecraft EULA? [Y/n] (https://account.mojang.com/documents/minecraft_eula)")
    eula = input("Dong y voi thoa thuan nguoi dung cua Minecraft? [Y/n] ("
                 "https://account.mojang.com/documents/minecraft_eula)")
    # print(eula)  # for testing
    if eula == "":
        pathlib.Path("server").mkdir(parents=True, exist_ok=True)
        open("server/eula.txt", 'w+').write("eula=true")
    else:
        while True:
            if yes_no_verifier(eula):
                pathlib.Path("server").mkdir(parents=True, exist_ok=True)
                open("server/eula.txt", 'w+').write("eula=true")
                break
            elif not yes_no_verifier(eula):
                print("You selected No. Exiting...")
                print("Ban da chon khong dong y. Dang thoat...")
                time.sleep(1)
                exit()
            else:
                eula = input("Nhap Y/N: ")

    print()

elif args.eula == "y":
    pathlib.Path("server").mkdir(parents=True, exist_ok=True)
    open("server/eula.txt", 'w+').write("eula=true")
elif args.eula == "n":
    print("You selected to not agree to MC EULA. Exiting...")
    exit()

# checking system and generate scripts
if args.memory == "manual":
    print("Close all other application in order to get the most accurate system info!")
    print("Vui long dong moi ung dung de lay thong tin he thong chinh xac nhat!")
    print(input("Nhan ENTER de tiep tuc..."))
    print()
    system_info = system_check()
    print("He dieu hanh/OS: ", system_info[0])
    print("RAM con trong/Memory Available: ", system_info[1])
    print()
    mem = str(system_info[1])
    print("How much RAM do you want to allocate to the server? [" + mem + "]")
    chosen_mem = input("Ban muon cho server bao nhieu RAM? [" + mem + "]:")
    # print(chosen_mem)  # for testing
    print()
    if chosen_mem == "":
        chosen_mem = system_info[1]
    else:
        while (not chosen_mem.endswith("M")) and (not chosen_mem.endswith("G")):
            if chosen_mem.endswith("B"):
                chosen_mem = chosen_mem[:-1]
                break
            else:
                print("Enter a value ends with 'M' or 'G': ")
                chosen_mem = input("Hay nhap so ket thuc boi 'M' hoac 'G': ")
elif args.memory == "auto":
    system_info = system_check()
    chosen_mem = system_info[1]
elif (not args.memory.endswith("M")) and (not args.memory.endswith("G")):
    system_info = system_check()
    if args.memory.endswith("B"):
        chosen_mem = args.memory[:-1]
    else:
        print("Invalid --memory argument value passed, do -h or --help for more information.")
        print("Exiting...")
else:
    system_info = system_check()
    chosen_mem = args.memory

script = generate_script(system_info[1], chosen_mem, yes_no_verifier(lithium_yesno))
print("Command for starting the server:")
print("Command chay server: " + script)
print()

if args.network == "manual":
    print("Do you want to run network speedtest? [Y/n]")
    st_confirm = input("Ban co muon do toc do mang? [Y/n]")
    # print(st_confirm)  # for testing
    if st_confirm == "":
        network_speed = net_speed()
        print("Toc do/Speed: " + str(network_speed))
    else:
        while True:
            if yes_no_verifier(st_confirm):
                network_speed = net_speed()
                print("Toc do/Speed: " + str(network_speed))
                break
            elif not yes_no_verifier(st_confirm):
                manual_down = input("Nhap toc do tai xuong/Download speed (Mbps): ")
                manual_up = input("Nhap toc do tai len/Upload speed (Mbps): ")
                network_speed = min(manual_down, manual_up)
                time.sleep(0.5)
                break
            else:
                config_server = input("Nhap Y/N: ")
    print()
elif args.network == "auto":
    network_speed = net_speed()
    print("Toc do/Speed: " + str(network_speed))
else:
    network_speed = args.network

# config
if args.slots == 0 and args.network == "manual":
    max_player = calc_players(network_speed, chosen_mem)
    print("Recommended player slots (max-player in server.properties): " + max_player)
    print("So slot duoc khuyen cao (max-player trong server.properties): " + max_player)
    print()
    copyfile("./templates/server.properties.templates", "./server/server.properties")
    with open("server/server.properties", "r", encoding="utf8") as file:
        fileout = file.read().replace("max-players=20", ("max-players=" + max_player))
    with open("server/server.properties", "w", encoding="utf8") as file:
        file.write(fileout)

    print("Edit server configuration? [Y/n]")
    config_server = input("Chinh sua cai dat server? [Y/n]")
    # print(configserver)  # for testing
    if config_server == "":
        texteditor.open(filename="server/server.properties", encoding="utf_8")
    else:
        while True:
            if yes_no_verifier(config_server):
                texteditor.open(filename="server/server.properties", encoding="utf_8")
                break
            elif not yes_no_verifier(config_server):
                print("Continuing...")
                print("Dang tiep tuc setup...")
                time.sleep(0.5)
                break
            else:
                config_server = input("Nhap Y/N: ")
    print()
elif args.slots != 0 and args.network == "manual":
    max_player = args.slots
    copyfile("./templates/server.properties.templates", "./server/server.properties")
    with open("server/server.properties", "r", encoding="utf8") as file:
        fileout = file.read().replace("max-players=20", ("max-players=" + max_player))
    with open("server/server.properties", "w", encoding="utf8") as file:
        file.write(fileout)
elif args.slots == 0 and args.network != "manual":
    max_player = calc_players(network_speed, chosen_mem)
    copyfile("./templates/server.properties.templates", "./server/server.properties")
    with open("server/server.properties", "r", encoding="utf8") as file:
        fileout = file.read().replace("max-players=20", ("max-players=" + max_player))
    with open("server/server.properties", "w", encoding="utf8") as file:
        file.write(fileout)
