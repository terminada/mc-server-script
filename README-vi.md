<h1 align="center">Script setup server Minecraft Java</h1>

> For English version please check [README.md](README.md)

[![Build Status](https://travis-ci.com/terminada/mc-server-script.svg?branch=master)](https://travis-ci.com/terminada/mc-server-script)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/terminada/mc-server-script/?ref=repository-badge)

![IllumiStudios](https://img.shields.io/badge/Powered%20by-IllumiStudios-black)
[![ApexHosting](https://img.shields.io/badge/Host%20your%20server%20on-Apex%20Hosting-critical)](https://billing.apexminecrafthosting.com/aff.php?aff=2786)


Script [setup](https://minecraft.gamepedia.com/Tutorials/Setting_up_a_server) server cho nền tảng Windows, MacOSX, Ubuntu, Debian, CentOS, Fedora... sử dụng Python.

### Mục lục
1. [Demo](#demo)
2. [Hướng dẫn cài đặt và sử dụng](#cài-đặt-và-sử-dụng)
3. [Phần phụ thuộc](#phần-phụ-thuộc)
4. [Đóng góp](#đóng-góp)

## Demo
![screenshot-1](demos/screenshot-1.png "Screenshot 1")

## Cài đặt và sử dụng

__Dành riêng cho Windows 10:__ 

- Tải file `.zip` mới nhất tại [Releases](https://github.com/hoangtheboss/mc-server-script/releases)
- Chạy `windows-easy.bat` 

Để cài thủ công, bạn cần [__Python 3.7__](https://www.python.org/downloads/release/python-377/) và [__GIT__](https://git-scm.com/downloads), sau đó nhập dòng lệnh vào Terminal (cmd):

```shell
git clone https://github.com/HoangTheBoss/mc-server-script.git
cd mc-server-script
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 makeserver.py
```

__Chú ý__: Sử dụng `python3` trên Windows 8/10 có khả năng sẽ mở __Store__, trong trường hợp đó sử dụng `python` thay cho `python3`

## Phần phụ thuộc
Check [requirements.txt](https://github.com/HoangTheBoss/mc-server-script/blob/master/requirements.txt) để cập nhật thông tin mới nhất
```
hurry.filesize == 0.9
psutil == 5.7.0
requests == 2.23.0
text_editor == 1.0.5
speedtest_cli == 2.1.2
pySmartDL == 1.3.3
```

## Đóng góp
Bạn có thể đóng góp cho dự án bằng cách mở __Issues__ và __Pull Requests__.

## Bạn muốn chơi server nhưng không có máy để host?
Host server giá rẻ tại [Apex Hosting](https://billing.apexminecrafthosting.com/aff.php?aff=2786)!


