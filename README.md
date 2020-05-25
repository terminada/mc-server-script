<h1 align="center">Minecraft JE Server creation script</h1>

> Phiên bản tiếng Việt tại [README-vi.md](README-vi.md)

[![Build Status](https://travis-ci.com/HoangTheBoss/mc-server-script.svg?branch=master)](https://travis-ci.com/HoangTheBoss/mc-server-script)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/HoangTheBoss/mc-server-script/?ref=repository-badge)

![IllumiStudios](https://img.shields.io/badge/Powered%20by-IllumiStudios-black)
[![ApexHosting](https://img.shields.io/badge/Host%20your%20server%20on-Apex%20Hosting-critical)](https://billing.apexminecrafthosting.com/aff.php?aff=2786)


Minecraft Server [setup](https://minecraft.gamepedia.com/Tutorials/Setting_up_a_server) script for Windows, MacOSX, Ubuntu, Debian, CentOS, Fedora... (Not Solaris at the moment), using Python and some dependencies.

### Table of Contents
1. [Demo](#demo)
2. [Installation and usage](#installation-and-usage)
3. [Dependencies](#dependencies)
4. [Contribute](#contribute)

## Demo
![screenshot-1](demos/screenshot-1.png "Screenshot 1")

## Installation and usage

For __Windows 10 only__: 

- Download the latest `.zip` file at [Releases](https://github.com/hoangtheboss/mc-server-script/releases)
- Run `windows-easy.bat` to download Python (embedded version/if not installed), install dependencies and execute the script.

Alternatively you will have to install __Python 3.7__ by yourself, then use the command line:

```
git clone https://github.com/HoangTheBoss/mc-server-script.git
cd mc-server-script
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 makeserver.py
```

__Note__: Using `python3` on Windows 8/10 may open the __Store__, in that case use `python`

## Dependencies
Better check [requirements.txt](https://github.com/HoangTheBoss/mc-server-script/blob/master/requirements.txt) for more updated contents
```
hurry.filesize == 0.9
psutil == 5.7.0
requests == 2.23.0
text_editor == 1.0.5
speedtest_cli == 2.1.2
pySmartDL == 1.3.3
```

## Contribute
Do what you can to help the project. Issues and pull requests are welcome.

## I want to run my own MC server but don't have a dedicated machine for that
You can host your server at [Apex Hosting](https://billing.apexminecrafthosting.com/aff.php?aff=2786) for cheap!


