# Binmaster Purse Parser

**This code will send an embed in a channel of your choosing then update that embed every 30 minutes, allowing you to track the purse of your accounts in an easier way!**

# Steps:

_First go into the config.json file and add a bot token, be sure to enable the Message Content Intent in the discord priveleges tab._
_[Located Here](https://discord.com/developers/applications/)_

* _Then, add the bot to your server and copy the channel id of what channel you want the bot to send messages in._
* _Copy your discord user id and put it in the config.json file._

# Startup:

_First follow the Steps category and put your info in the config.json file._

- _Next run `pip install -r requirements.txt` then run `python3 main.py`_

# DOCS:
* **Run the /update command if you want to update the embed early, it will automatically update every 30 minutes. The bot will tell you how long it will take to parse the data**
* **Run the /purse command if you want a new embed (the bot wont update it)**
* **Run the /ign command to add or remove an ign from the list that it will check**
* **Run the /list command to see what igns are going to be put into the embed**
