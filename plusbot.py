#!/usr/bin/python3

import re
import os
import datetime
import sqlite3
from slackclient import SlackClient

BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
#BOT_NAME = "plusbot"

# init function
#	pull all the users
#	store all the real names and their slackUnames
#def init_bot():

# plus_minus function
#	get the message and parse for username and score
#	query db for current score
#	increment or decrement score
#	print current score
#def plus_minus():

def main():
    #init connection to database
    # you don't need to check if the database file is there or not, the
    # connect statement will create the file if it doesn't exist.
    # This is what the database table looks like
    # CREATE TABLE users (date text, name text, slackUname text unique, score int, forStatement text);
    db_con = sqlite3.connect('plusbot.db')
    cur = db_con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (date text, name text, slackUname text unique, score int, forStatement text)')
    # init connection to slack
    sc = SlackClient(BOT_TOKEN)
    sc.rtm_connect()
    sc.rtm_send_message("dev", "I'm allive!")

    #init_bot()
    #=========== grab all the users and stuff in database
    api_call = sc.api_call("users.list")
    if api_call.get('ok'):
        userlist = api_call.get('members')
        for userName in userlist:
            if 'name' in userName:
                print("realname is: '" + userName['name'] + "' and slackId is: '" + userName.get('id') + "'")
                timestamp =  datetime.datetime.now().strftime("%Y%m%d%H%M")
                cur.execute("INSERT OR IGNORE INTO users VALUES('{ts}','{rn}','{id}','0','')".format(ts=timestamp,rn=userName['name'],id=userName.get('id')))
        db_con.commit()
	#========== the super big while that listens to new messages
    plusbotSlackUname = 'U3L9KBRU5'
    while True:
        for sm in sc.rtm_read():
            text = sm.get("text")
            user = sm.get("user")
            if not text or not user:
                continue
            print("user is:'" + user + "' message is:'" + text + "'")
            #========== the core ++ and -- functionality
            # for now it only picks up the first mentioned user's score
            # i need to upgrade the regex so that i find all of the
            uNamePlus = re.search('<@U\w\w\w\w\w\w\w\w>\+\+',text)
            if uNamePlus:
                uName = uNamePlus.group(0)[2:11]
                cur.execute('''UPDATE users SET score = score + 1 WHERE slackUname = ? ''',(uName,))
                db_con.commit()
                cur.execute('''SELECT name,score FROM users WHERE slackUname = ? ''',(uName,))
                nameNscore = cur.fetchone()
                #========== adding for statement
                forFound = re.search(' for ',text)
                if forFound:
                    forString = text.split(" for ")
                    print(str(nameNscore[0]) + " has one more point for: " + forString[1] +  " Their total score is: " + str(nameNscore[1]))
                    sc.rtm_send_message("dev", str(nameNscore[0]) + " has one more point for: " + forString[1] + " Their total score is: " + str(nameNscore[1]))
                    cur.execute('''UPDATE users SET forStatement = ? WHERE slackUname = ? ''',(forString[1],uName,))
                    db_con.commit()
                else:
                    print(str(nameNscore[0]) + " has one more point! Their total score is: " + str(nameNscore[1]))
                    sc.rtm_send_message("dev", str(nameNscore[0]) + " has one more point! Their total score is: " + str(nameNscore[1]))
                continue
            #pMinus = re.compile('^.*<@U\w\w\w\w\w\w\w\w>--')
            #if pMinus.match(text):
            uNameMinus = re.search('<@U\w\w\w\w\w\w\w\w>--',text)
            if uNameMinus:
                uName = uNameMinus.group(0)[2:11]
                cur.execute('''UPDATE users SET score = score - 1 WHERE slackUname = ? ''',(uName,))
                db_con.commit()
                cur.execute('''SELECT name,score FROM users WHERE slackUname = ? ''',(uName,))
                nameNscore = cur.fetchone()
                #========== adding for statement
                forFound = re.search(' for ',text)
                if forFound:
                    forString = text.split(" for ")
                    print(str(nameNscore[0]) + " has one less point for: " + forString[1] +  " Their total score is: " + str(nameNscore[1]))
                    sc.rtm_send_message("dev", str(nameNscore[0]) + " has one less point for: " + forString[1] + " Their total score is: " + str(nameNscore[1]))
                    cur.execute('''UPDATE users SET forStatement = ? WHERE slackUname = ? ''',(forString[1],uName,))
                    db_con.commit()
                else:
                    print(str(nameNscore[0]) + " has one less point! Their total score is: " + str(nameNscore[1]))
                    sc.rtm_send_message("dev", str(nameNscore[0]) + " has one less point! Their total score is: " + str(nameNscore[1]))
                continue
            #========== commands to plusbot
            foundPlusBot = re.search(plusbotSlackUname,text)
            if foundPlusBot:
                # === scoreboard command
                scoreCommand = re.search('scoreboard',text)
                if scoreCommand:
                    cur.execute('''SELECT name,score FROM users ORDER BY score DESC''')
                    rows = cur.fetchall()
                    for row in rows:
                        sc.rtm_send_message("dev",str(row[0]) + " has score: " + str(row[1]))
                    continue
                # === check users
                checkCommand = re.search('check',text)
                if checkCommand:
                    try: 
                        print("text::" + text + "::")
                        checkUname = re.search('<@U\w\w\w\w\w\w\w\w>$',text)
                        checkUnameStrip = checkUname.group(0)[2:11]
                        cur.execute('''SELECT name,score From users WHERE slackUname = ? ''',(checkUnameStrip,))
                        row = cur.fetchone()
                        sc.rtm_send_message("dev",str(row[0]) + " has score: " + str(row[1]))
                        continue
                    except AttributeError:
                        sc.rtm_send_message("dev","not a valid user, please try again.")
                # === help
                helpCommand = re.search('help',text)
                if helpCommand:
                    sc.rtm_send_message("dev","to add points to someone type: @validuser++")
                    sc.rtm_send_message("dev","to take points from someone type: @validuser--")
                    sc.rtm_send_message("dev","to check the current scoreboard type: @plusbot scoreboard")
                    sc.rtm_send_message("dev","to check a specific user type: @plusbot check @validuser")
                    sc.rtm_send_message("dev","you can give someone points 'for' something like: @validuser++ for being awesome")
                    sc.rtm_send_message("dev","you can see the help by typing: @plusbot help")
                else:
                    sc.rtm_send_message("dev", "check & scoreboard are the only commands recognized right now.")
                    continue
    db_con.close()
if __name__ == "__main__":
    main()
