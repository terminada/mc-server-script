from __future__ import print_function, unicode_literals
from InquirerPy import prompt
from InquirerPy.exceptions import InvalidArgument
from InquirerPy.validator import PathValidator


def get_version_option(release, snapshot):
    questions = [
        {
            "type": "list",
            "name": "version_option",
            "message": "Pick a version:",
            "choices": ["Latest release: " + release, "Latest snapshot: " + snapshot, "Other version"],
            "default": 1
        }

    ]
    answer = prompt(questions, vi_mode=True)
    if "release" in answer["version_option"]:
        return 1
    if "snapshot" in answer["version_option"]:
        return 2
    return 3


def get_custom_version(json):
    versions = []
    for j in json["versions"]:
        versions.append(j["id"])

    questions = [
        {
            "type": "fuzzy",
            "name": "custom_version",
            "message": "Type custom version:",
            "choices": versions,
            "max_height": "70%"
        }
    ]
    answer = prompt(questions, vi_mode=True)
    return answer["custom_version"]


def overwrite_confirm(filename):
    questions = [
        {
            "type": "confirm",
            "name": "overwrite_confirm",
            "message": filename + " exist, do you want to overwrite?",
            "default": False
        }
    ]
    answer = prompt(questions, vi_mode=True)
    return answer["overwrite_confirm"]


def fabric_confirm():
    questions = [
        {
            "type": "confirm",
            "name": "fabric_confirm",
            "message": "Use fabric for better server performance?",
            "default": True
        }
    ]
    answer = prompt(questions, vi_mode=True)
    return answer["fabric_confirm"]


def server_name():
    questions = [
        {
            "type": "input",
            "name": "server_name",
            "message": "Your server name:"
        }
    ]
    answer = prompt(questions, vi_mode=True)
    return answer["server_name"]


def eula():
    questions = [
        {
            "type": "confirm",
            "name": "eula",
            "message": "Agree to Minecraft's End-User License Agreement?",
            "default": True
        }
    ]
    answer = prompt(questions, vi_mode=True)
    return answer["eula"]


def memory_input(default):
    questions = [
        {
            "type": "input",
            "name": "memory_input",
            "message": "How much RAM do you want to allocate to the server?",
            "default": default
        }
    ]
    answer = prompt(questions, vi_mode=True)
    return answer["memory_input"]


def speedtest_confirm():
    questions = [
        {
            "type": "confirm",
            "name": "speedtest_confirm",
            "message": "Do you want to run network speedtest?",
            "default": True
        }
    ]
    answer = prompt(questions, vi_mode=True)
    return answer["speedtest_confirm"]


def netspeed_manual():
    questions = [
        {
            "type": "input",
            "name": "download_speed",
            "message": "Download speed (Mbps)",
            "validate": lambda text: len(text) > 0 or "Please input"
        },
        {
            "type": "input",
            "name": "upload_speed",
            "message": "Upload speed (Mbps)",
            "validate": lambda text: len(text) > 0 or "Please input"
        }
    ]
    answer = prompt(questions, vi_mode=True)
    return min(answer["download_speed"], answer["upload_speed"])


def config_confirm():
    questions = [
        {
            "type": "confirm",
            "name": "config_confirm",
            "message": "Edit server configuration?",
            "default": True
        }
    ]
    answer = prompt(questions, vi_mode=True)
    return answer["config_confirm"]