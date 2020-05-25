import requests


# GET the list of mc versions
def getminecraftversions():
    url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    response = requests.get(url)
    return response.json()


# functions for easy accessing
def latest_mc_release(json):
    return json["latest"]["release"]


def latest_mc_snapshot(json):
    return json["latest"]["snapshot"]


# verify version
def verify_version(json, version):
    for j in json["versions"]:
        if j["id"] == version:
            return True
    return False


# GET download link for selected version
def get_download_link(url):
    response = requests.get(url)
    return response.json()["downloads"]["server"]["url"]


# GET lithium download link
def get_fabric_link():
    url = "https://meta.fabricmc.net/v2/versions/installer"
    response = requests.get(url)
    return response.json()[0]["url"]




