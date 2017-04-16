*plusbot* is a little slack-bot, written in python-3,  which adds points to users with @username++ and takes points away with @username--. It stores the results in an sqlite database and can run on any linux box connected to the Internet.

This bot is a written from scratch clone of https://plusplus.chat b/c I didn't want my information going to some other service in the cloud.

### Install instructions (assuming ubuntu or some form of debian)
0. apt-get install sqlite3
1. apt-get install python3
2. apt-get install python3-pip
3. python3 -m pip install slackclient
4. export SLACK_BOT_TOKEN='your slack api token here'
5. invite the bot to your channel for it to work.

### Current Features:
* ++ and -- add one point and subtract one point like: '@validuser++' or '@validuser--' or can have a space like '@validuser ++' or '@validuser --'
* command 'scoreboard' prints out report of current scores highest to lowest. To use the command type: '@plusbot scoreboard'
* command 'check' to query on someone's current score. To use it type: '@plusbot check @somevaliduser'
* 'for' statement as in: "@username++ for being awesome"
* help statement tells all the commands as in: '@plusbot help'

### Future Features:
* add or subtract points to more than one user in a message
* add weekly honors concept. Where on Fridays at 0800 EST/EDT the bot announces the score and says something clever about the top spot and something derogatory about the bottom person
* remove all of the hard coded stuff for channel name, bot name, and whatnot
