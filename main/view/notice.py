# coding:utf-8

from flask import *
from main import app
from main import cursor
import time

# 通知提醒
@app.route('/notice')
def notice():
	if session.get('username') == None:
		# 用户尚未登录
		return redirect(url_for('login'))
	else:
		# 获取和当前用户有关的动态
		username = session.get('username')
		cursor.execute("select * from activity where me=%s and checked=0 order by timestamp desc",[username])
		activities = cursor.fetchall()
		activityCount = len(activities)
		for item in activities:
			item['weekday'] = time.localtime(float(item['timestamp'])).tm_wday
			if item['weekday'] == 0:
				item['weekday'] = '星期一'
			elif item['weekday'] == 1:
				item['weekday'] = '星期二'
			elif item['weekday'] == 2:
				item['weekday'] = '星期三'
			elif item['weekday'] == 3:
				item['weekday'] = '星期四'
			elif item['weekday'] == 4:
				item['weekday'] = '星期五'
			elif item['weekday'] == 5:
				item['weekday'] = '星期六'
			elif item['weekday'] == 6:
				item['weekday'] = '星期日'
			item['timestamp'] = time.strftime('%m-%d', time.localtime(float(item['timestamp'])))
		cursor.execute("update activity set checked=1 where me=%s",[username])

		# 获取和当前用户有关的聊天信息
		cursor.execute("select source,sourceNickname,count(*) as count,content,timestamp from chat where target=%s and source!=%s and checked=0 group by source order by timestamp desc",[username,username])
		chats = cursor.fetchall()
		for item in chats:
			item['timestamp'] = time.strftime('%m-%d %H:%M', time.localtime(float(item['timestamp'])))
			cursor.execute("select portrait from user where username=%s",[item['source']])
			item['portrait'] = cursor.fetchone()['portrait']
		chatsCount = len(chats)

		return render_template('notice/notice.html',activities=activities,activityCount=activityCount,chats=chats,chatsCount=chatsCount)

# 私信界面
@app.route('/chat/<username>')
def chat(username):
	if session.get('username') == None:
		# 用户尚未登录
		return redirect(url_for('login'))
	else:
		# 用户已经登陆，获取所有聊天记录
		me = session.get('username')
		cursor.execute("select * from chat where (source=%s and target=%s) or (source=%s and target=%s) order by timestamp desc limit 100",[username,me,me,username])
		chats = cursor.fetchall()
		chats = sorted(chats, key=lambda x:(x['timestamp']))

		# 合并聊天时间戳
		currentTime = 0
		for item in chats:
			temp = float(item['timestamp'])
			if not currentTime == 0 and float(item['timestamp']) - currentTime < 600:
				item['timestamp'] = ''
			else:
				item['timestamp'] = (time.strftime('%m月%d日 %H:%M', time.localtime(float(item['timestamp'])))).lstrip('0')
			currentTime = temp

		# 将消息设置为已读
		cursor.execute('update chat set checked=1 where source=%s and target=%s',[username,me])

		# 获取用户头像和昵称
		cursor.execute("select portrait from user where username=%s",[me])
		myPortrait = cursor.fetchone()['portrait']
		cursor.execute("select nickname,portrait from user where username=%s",[username])
		portrait = cursor.fetchone()
		targetNickname = portrait['nickname']
		portrait = portrait['portrait']

		return render_template('notice/chat.html',target=username,targetNickname=targetNickname,chats=chats,myPortrait=myPortrait,portrait=portrait)