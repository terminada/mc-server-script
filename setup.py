import pathlib
import requests
import subprocess
import time
import json


# check java function
def checkjava():
    sp = subprocess.Popen(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = str(sp.communicate())
    if output.find("Java(TM)") == -1:
        return False
    else:
        return True


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
    file = requests.get(url)
    open("server/server.jar", 'wb').write(file.content)


# welcome
print("Welcome to Minecraft Java Server Creator!")
print("Chào mừng bạn đến với trình tạo Server Minecraft Java!")
print()
print("Software by HoangTheBoss@IllumiStudios2020")
print()

# check java
if not checkjava():
    print("Java Runtime not found. Download and install at: https://www.java.com/en/download/")
    print("Bạn chưa cài Java. Tải và cài đặt Java tại: https://www.java.com/en/download/")

# load version list
print("Loading version list...")
print("Đang tải danh sách phiên bản...")
getminecraftversions()
print("Done!")
print("Đã tải xong danh sách phiên bản!")
print()

# pick version
print("Chọn phiên bản:")
print("1) Release mới nhất: ", latest_mc_release())
print("2) Snapshot mới nhất: ", latest_mc_snapshot())
print("3) Khác/Other")

while True:
    chosen_ver_num = input("Chọn số phiên bản: ")
    if chosen_ver_num not in ('1', '2', '3'):
        print("Hãy chọn lại trong 1,2,3.")
    else:
        break

if chosen_ver_num == "1":
    chosen_ver = latest_mc_release()
elif chosen_ver_num == "2":
    chosen_ver = latest_mc_snapshot()
elif chosen_ver_num == "3":
    chosen_ver = input("Nhập phiên bản cụ thể (X.X.X hoặc tên snapshot): ")

# get download link
for i in getminecraftversions.json_mc_versions["versions"]:
    if i["id"] == chosen_ver:
        downloadlink = getdownloadlink(i["url"])

# download
# print()
# pathlib.Path("/server").mkdir(parents=True, exist_ok=True)
# download(downloadlink)

# eula
print("Đồng ý với thỏa thuận người dùng của Minecraft? (https://account.mojang.com/documents/minecraft_eula)")
eula = ""
while eula not in ("Y", "N", "y", "n", "yes", "no"):
    eula = input("Nhập Y/N: ")
    if eula in ("Y", "y", "yes"):
        break
    elif eula in ("N", "n", "no"):
        print("Bạn đã chọn không đồng ý. Đang thoát...")
        time.sleep(1)
        exit()
