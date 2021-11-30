import argparse
import pathlib
import subprocess
import time

import texteditor

import server_configurator as sc
import server_downloader as sd
import server_fetcher as sf
import setup_options as so


# check java function
def check_java():
    sp = subprocess.Popen(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = str(sp.communicate())
    if output.find("Runtime") == -1:
        return False
    return True


# verify yes and no
def yes_no_verifier(inp):
    if inp.lower().startswith("y"):
        return True
    if inp.lower().startswith("n"):
        return False

# # argument handling
# argparser = argparse.ArgumentParser(description="Minecraft Java Server Creator")
# argparser.add_argument("-v", "--version", default="manual", help="Minecraft snapshot/release/custom Version")
# argparser.add_argument("-e", "--eula", default="manual", choices=["y", "n", "manual"], help="Agree to the EULA?")
# argparser.add_argument("-l", "--lithium", default="manual", choices=["y", "n", "manual"],
#                        help="Use Fabric + Lithium for better performance?")
# argparser.add_argument("-m", "--memory", default="manual", help="Amount of RAM to allocate to the server")
# argparser.add_argument("--network", default="manual",
#                        help="The minimum of your Download/Upload Speed in Mbit metrics. manual = prompt, auto = use "
#                             "speedtest, else type numbers only")
# argparser.add_argument("-s", "--slots", default="0", type=int,
#                        help="Number of slots to be available on your server, 0 = manual. Ignore if --network is passed")
# argparser.add_argument("-n", "--name", default="manual", help="Server name, eg. 'Weelux Network'")
# argparser.add_argument("-o", "--overwrite", default="manual", choices=["y", "n", "manual"],
#                        help="Overwrite existing JAR file?")

# args = argparser.parse_args()

# welcome
print("Welcome to Fabric Server Creator! \n")
print("Software by HoangTheBoss. \n")

# check java
if not check_java():
    print("Java Runtime not found. Download and install at: https://www.java.com/en/download/ \n")
    exit()

# load version list
print("Loading version list... \n")

versions_json = sf.getminecraftversions()
latest_release = sf.latest_mc_release(versions_json)
latest_snapshot = sf.latest_mc_snapshot(versions_json)

print("Done! \n")

server_name = so.server_name()

# if args.version == "manual":
# pick version
# chosen_ver_num = so.get_version_option(latest_release, latest_snapshot)
# if chosen_ver_num == 1:
#     chosen_ver = sf.latest_mc_release(versions_json)
# elif chosen_ver_num == 2:
#     chosen_ver = sf.latest_mc_snapshot(versions_json)
# elif chosen_ver_num == 3:
#     chosen_ver = so.get_custom_version()
# while not sf.verify_version(versions_json, chosen_ver):
#     chosen_ver = so.get_custom_version()

options = [
    lambda json: sf.latest_mc_release(json),
    lambda json: sf.latest_mc_snapshot(json),
    lambda json: so.get_custom_version(json)
]

chosen_ver = options[so.get_version_option(latest_release, latest_snapshot)-1](versions_json)

print()

# elif args.version == "release":
#     chosen_ver = latest_release
# elif args.version == "snapshot":
#     chosen_ver = latest_snapshot
# elif sf.verify_version(versions_json, args.version):
#     chosen_ver = args.version
# else:
#     print("ERROR: Invalid --version argument value passed, do -h or --help for more information.")
#     print("Exiting...")
#     exit()

# get download link
for i in versions_json["versions"]:
    if i["id"] == chosen_ver:
        downloadlink = sf.get_download_link(i["url"])

# download
if pathlib.Path('server/server.jar').is_file():
    # if args.overwrite == "manual":
    overwrite = so.overwrite_confirm("server.jar")
    if overwrite:
        sd.download_server(downloadlink)
    else:
        print("Continuing...")
    # elif args.overwrite == "y":
    #     sd.download_server(downloadlink)
    # else:
    #     print("Continuing...")
else:
    sd.download_server(downloadlink)
print()

# use fabric + lithium
# if args.lithium == "manual":
#   lithium_yesno = so.lithium_confirm()
# elif args.lithium == "y":
#     lithium_yesno = True
# else:
#     lithium_yesno = False

fabric_yesno = so.fabric_confirm()

if fabric_yesno:
    if pathlib.Path('server/fabric-server-launch.jar').is_file():
        # if args.overwrite == "manual":
        overwrite = so.overwrite_confirm("fabric-server-launch.jar")
        if overwrite:
            sd.install_fabric(chosen_ver)
        else:
            print("\nContinuing...")
        # elif args.overwrite == "y":
        #     sd.install_fabric(chosen_ver)
    else:
        sd.install_fabric(chosen_ver)
if not fabric_yesno:
    print("Continuing...")

# lithium
print("\nDownload Lithium at https://www.curseforge.com/minecraft/mc-mods/lithium and put it in the mods folder for better server performance! \n")

# eula
# if args.eula == "manual":
eula = so.eula()
# print(eula)  # for testing
if eula:
    sc.eula_true()
elif not eula:
    print("You selected No. Exiting...")
    exit()
print()
# elif args.eula == "y":
#     sc.eula_true()
# elif args.eula == "n":
#     print("You selected to not agree to MC EULA. Exiting...")
#     exit()

# generate config file
sc.generate_config()

# checking system and generate scripts
# if args.memory == "manual":
print("\nClose all other application in order to get the most accurate system info!")
print(input("Press ENTER to continue..."))
print()
system_info = sc.system_check()
print("OS: ", system_info[0])
print("Memory Available: ", system_info[1])
print()
mem = str(system_info[1])
chosen_mem = so.memory_input(mem)
# print(chosen_mem)  # for testing
print()
while (not chosen_mem.endswith("M")) and (not chosen_mem.endswith("G")):
    if chosen_mem.endswith("B"):
        chosen_mem = chosen_mem[:-1]
        break
    else:
        print("Enter a value ends with 'M' or 'G': ")
        chosen_mem = so.memory_input(mem)
# elif args.memory == "auto":
#     system_info = sc.system_check()
#     chosen_mem = system_info[1]
# elif (not args.memory.endswith("M")) and (not args.memory.endswith("G")):
#     system_info = sc.system_check()
#     if args.memory.endswith("B"):
#         chosen_mem = args.memory[:-1]
#     else:
#         print("Invalid --memory argument value passed, do -h or --help for more information.")
#         print("Exiting...")
# else:
#     system_info = sc.system_check()
#     chosen_mem = args.memory

script = sc.generate_script(system_info[1], chosen_mem, fabric_yesno)
print("Command for starting the server: " + script)
print()

# if args.network == "manual":
st_confirm = so.speedtest_confirm()
# print(st_confirm)  # for testing
if st_confirm:
    network_speed = sc.net_speed()
    print("Speed: " + str(network_speed) + "Mbps.")
else:
    network_speed = so.netspeed_manual()
    time.sleep(0.5)
print()
# elif args.network == "auto":
#     network_speed = sc.net_speed()
#     print("Speed: " + str(network_speed))
# else:
#     network_speed = args.network

# config
# if args.slots == 0 and args.network == "manual":
max_player = sc.calc_players(network_speed, chosen_mem)
print("Recommended player slots (max-player in server.properties): " + max_player)
print()
sc.set_properties(max_player=max_player, server_name=server_name)

config_server = so.config_confirm()
# print(configserver)  # for testing
if config_server:
    try:
        texteditor.open(filename="server.properties", encoding="utf_8")
    except:
        print("Failed to open text editor. Consider editing server.properties before first startup of the server.")
else:
    print("Continuing...")
    time.sleep(0.5)
print()
# elif args.slots != 0 and args.network == "manual":
#     sc.set_properties(max_player=args.slots)
# elif args.slots == 0 and args.network != "manual":
#     sc.set_properties(max_player=sc.calc_players(network_speed, chosen_mem))
