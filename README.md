plusbot is a little slack-bot, written in python-3,  which adds points to users with @username++ and takes points away with @username--. It stores the results in an sqlite database and can run on any linux box connected to the Internet.

Install instructions
#0 apt-get install sqlite3
#1 apt-get install python3
#2 apt-get install python3-pip
#3 python3 -m pip install slackclient
#4 export SLACK_BOT_TOKEN='your slack api token here'
#5 sqlite3 plusbot.db (and then quit with .quit)
#6 invite the bot to your channel for it to work.

Current Features:
* ++ and -- add one point and subtract one point

Future Features:
* print out report of current scores in highest score order
* add or subtract points to more than one user in a message
