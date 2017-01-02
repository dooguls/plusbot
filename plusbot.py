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
#	api_call = sc.api_call("users.list")
#	if api_call.get('ok'):
#		userlist = api_call.get('members')
#		for user in users:
#			if 'name' in user:
#				print("realname is: '" + user['name'] + "' and slackId is: '" + user.get('id') + "'")

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
		# CREATE TABLE users (date text, realname text, slackUname text, score int);
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
	while True:
		for sm in sc.rtm_read():
			text = sm.get("text")
			user = sm.get("user")
			if not text or not user:
				continue
			print("user is:'" + user + "' message is:'" + text + "'")
			# for now it only picks up the first mentioned user's score
			# i need to upgrade the regex so that i find all of the
			# users in a message and then assign points accordingly
			pPlus = re.compile('^.*<@U\w\w\w\w\w\w\w\w>\+\+')
			if pPlus.match(text):
				cur.execute('''UPDATE users SET score = score + 1 WHERE slackUname = ? ''',(user,))
				db_con.commit()
				print(user + " has one more point!")
				continue
			pMinus = re.compile('^.*<@U\w\w\w\w\w\w\w\w>--')
			if pMinus.match(text):
				cur.execute('''UPDATE users SET score = score - 1 WHERE slackUname = ?''',(user,))
				db_con.commit()
				print(user + " has one less point!")
				continue
				
	db_con.close()
if __name__ == "__main__":
	main()
