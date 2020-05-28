import os
import pathlib
from pySmartDL import SmartDL

import server_fetcher as sf


# download server jar
def download_server(url):
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


# install fabric
def install_fabric(chosen_ver):
    fabric_link = sf.get_fabric_link()
    download_fabric(fabric_link)
    os.system("java -jar server/fabric_installer.jar server -dir server -mcversion " + chosen_ver)
