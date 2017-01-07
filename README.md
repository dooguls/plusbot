*plusbot* is a little slack-bot, written in python-3,  which adds points to users with @username++ and takes points away with @username--. It stores the results in an sqlite database and can run on any linux box connected to the Internet.

This bot is a written from scratch clone of https://plusplus.chat b/c I didn't want my information going to some other service in the cloud.

### Install instructions
0. apt-get install sqlite3
1. apt-get install python3
2. apt-get install python3-pip
3. python3 -m pip install slackclient
4. export SLACK_BOT_TOKEN='your slack api token here'
5. sqlite3 plusbot.db (and then quit with .quit)
6. invite the bot to your channel for it to work.

### Current Features:
* ++ and -- add one point and subtract one point
* command 'scoreboard' prints out report of current scores highest to lowest. To use the command type: '@plusbot scoreboard'
* command 'check' to query on someone's current score. To use it type: '@plusbot check @somevaliduser'

### Future Features:
* add or subtract points to more than one user in a message
* add 'for' statement as in: "@username++ for being awesome"
* add weekly honors concept. Where on Fridays at 0800 EST/EDT the bot announces the score and says something clever about the top spot and something derogatory about the bottom person
* add feature for software to create database first time it's run instead of creating the database outside of the script.
* remove all of the hard coded stuff for channel name, bot name, and whatnot
