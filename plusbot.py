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
	sc = SlackClient(BOT_TOKEN)
	sc.rtm_connect()
	sc.rtm_send_message("dev", "I'm allive!")

	#init_bot()
	api_call = sc.api_call("users.list")
	if api_call.get('ok'):
		# CREATE TABLE users (date text, name text, slackUname text unique, score int);
		db_con = sqlite3.connect('plusbot.db')
		cur = db_con.cursor()
		userlist = api_call.get('members')
		for userName in userlist:
			if 'name' in userName:
				print("realname is: '" + userName['name'] + "' and slackId is: '" + userName.get('id') + "'")
				timestamp =  datetime.datetime.now().strftime("%Y%m%d%H%M")
				cur.execute("INSERT OR IGNORE INTO users VALUES('{ts}','{rn}','{id}','0')".format(ts=timestamp,rn=userName['name'],id=userName.get('id')))
		db_con.commit()
	#plus_minus()
	plusbotSlackUname = 'U3L9KBRU5'
	while True:
		for sm in sc.rtm_read():
			text = sm.get("text")
			user = sm.get("user")
			if not text or not user:
				continue
			print("user is:'" + user + "' message is:'" + text + "'")
			# for now it only picks up the first mentioned user's score
			# i need to upgrade the regex so that i find all of the
			uNamePlus = re.search('<@U\w\w\w\w\w\w\w\w>\+\+',text)
			if uNamePlus:
				uName = uNamePlus.group(0)[2:11]
				cur.execute('''UPDATE users SET score = score + 1 WHERE slackUname = ? ''',(uName,))
				db_con.commit()
				cur.execute('''SELECT name,score FROM users WHERE slackUname = ? ''',(uName,))
				nameNscore = cur.fetchone()
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
				print(str(nameNscore[0]) + " has one less point! Their total score is: " + str(nameNscore[1]))
				sc.rtm_send_message("dev", str(nameNscore[0]) + " has one less point! Their total score is: " + str(nameNscore[1]))
				continue
			foundPlusBot = re.search(plusbotSlackUname,text)
			if foundPlusBot:
				scoreCommand = re.search('scoreboard',text)
				if scoreCommand:
					cur.execute('''SELECT name,score FROM users ORDER BY score DESC''')
					rows = cur.fetchall()
					for row in rows:
						sc.rtm_send_message("dev",str(row[0]) + " has score: " + str(row[1]))
					continue
				checkCommand = re.search('check',text)
				if checkCommand:
					checkUname = re.search('<@U\w\w\w\w\w\w\w\w>$',text)
					checkUnameStrip = checkUname.group(0)[2:11]
					cur.execute('''SELECT name,score From users WHERE slackUname = ? ''',(checkUnameStrip,))
					row = cur.fetchone()
					sc.rtm_send_message("dev",str(row[0]) + " has score: " + str(row[1]))
					continue
				else:
					sc.rtm_send_message("dev", "scoreboard is the only command recognized right now.")
					continue
	db_con.close()
if __name__ == "__main__":
	main()
