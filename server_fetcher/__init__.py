import requests


# GET the list of mc versions
def getminecraftversions():
    url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    response = requests.get(url)
    return response.json()


# functions for easy accessing
def latest_mc_release(data):
    return data["latest"]["release"]


def latest_mc_snapshot(data):
    return data["latest"]["snapshot"]


# verify version
def verify_version(data, version):
    for j in data["versions"]:
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


# # GET lithium versions
# def get_lithium_versions():
#     url = "https://api.github.com/repos/jellysquid3/lithium-fabric/tags"
#     response = requests.get(url)
#     return response.json()
#
#
# # GET Lithium download link
# def get_lithium_asset_link(tag):
#     url = "https://api.github.com/repos/jellysquid3/lithium-fabric/releases/tags/" + tag
#     print(url)
#     response = requests.get(url)
#     assets = response.json()["assets"]
#     jar_name = ""
#     jar_link = ""
#     for j in assets:
#         if jar_name != "" and (j["name"]) < len(jar_name):
#             jar_link = j["browser_download_url"]
#     return jar_link
#
#
# # search for matching lithium version
# def get_lithium_link(mc_version):
#     lithium_versions = get_lithium_versions()
#     for j in range(1, len(mc_version)-3):
#         for k in lithium_versions:
#             if mc_version[:-j] in k["name"]:
#                 return get_lithium_asset_link(k["name"])
#             #print("NONE: ", j["name"])

