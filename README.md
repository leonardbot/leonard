Sheldon bot
===================
[![Build Status](https://travis-ci.org/Shamoi/sheldon.svg?branch=master)](https://travis-ci.org/Shamoi/sheldon)

Sheldon is a powerful modules-based bot for chats. Right now Sheldon can work with VK and Telegram, but that list will be expand soon.

----------


Install
-------------
```bash
git clone https://github.com/Shamoi/sheldon.git
cd sheldon
pip install -r requirements.txt
```

----------


Run
-------------------

###VK adapter
VK Adapter - adapter for popular russian social network VK.com
```bash
export VK_LOGIN=your_vk_login
export VK_PASSWORD=your_password
```
And run bot:
```bash
python start.py en vk
```
or
```bash
python start.py ru vk
```
###Telegram adapter
Telegram adapter - adapter to Telegram messenger. You need to install tg (https://github.com/vysheng/tg) and pytg (https://github.com/luckydonald/pytg) first.
```bash
export TG_PATH=/full/path/to/your/tg/folder/
```
And run bot:
```bash
python start.py en telegram
```
or
```bash
python start.py ru telegram
```
----------

Running tests
-------------------

To run tests you need to add main directory of Sheldon to $PYTHONPATH
```bash
export PYTHONPATH=.
```
Then just run:
```bash
py.test .
```

----------


Avaliable commands
--------------------
Updated version of commands you can get by '!help' оr '!помощь'

![bot's commands](http://i.imgur.com/av9kHJQ.png)
