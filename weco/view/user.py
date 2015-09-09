# coding:utf-8

from flask import *
from weco import app
from weco import connectdb,closedb
from weco.conf.configure import WECOPREFIX
import pprint

# 更新token
def updateToken(username):
	(db,cursor) = connectdb()
	cursor.execute('select token,lastActive from user where username=%s',[username])
	token = cursor.fetchone()
	closedb(db,cursor) 
	if token['lastActive'] > session.get('lastActive') and (not token['token'] == session.get('token')):
		session['token'] = token['token']
		session['lastActive'] = token['lastActive']

# 我的主页
@app.route('/user')
def home():
	if not session.get('username') == None:
		updateToken(session.get('username'))
		(db,cursor) = connectdb()

		# 用户已登陆
		cursor.execute('select * from user where username=%s', [session.get('username')])
		user = cursor.fetchone()

		# 获取所关注的其他用户名单
		followUserStr = user['followUsers']

		# 获取热门标签以供编辑
		hotTags = {}
		cursor.execute("select tag from userTagStat where gender=1 order by count desc limit 10")
		hotTags['male'] = cursor.fetchall()
		cursor.execute("select tag from userTagStat where gender=0 order by count desc limit 10")
		hotTags['female'] = cursor.fetchall()

		# 获取用户的创意
		ideas = user['ideas']
		ideasCount = 0
		if not ideas == '':
			cursor.execute('select id,title,feature from idea where id in (%s) and published=1 and locked=0' % (ideas))
			ideas = cursor.fetchall()
			ideasCount = len(ideas)
		else:
			ideas = None

		# # 获取用户待删除的创意
		# trashs = user['ideas']
		# if not trashs == '':
		# 	cursor.execute('select id,title,feature from idea where id in (%s) and locked=1' % (trashs))
		# 	trashs = cursor.fetchall()
		# else:
		# 	trashs = None

		# 获取用户喜欢的创意
		followIdeas = user['followIdeas']
		followIdeasCount = 0
		if not followIdeas == '':
			cursor.execute('select id,title,feature from idea where id in (%s) and published=1 and locked=0' % (followIdeas))
			followIdeas = cursor.fetchall()
			followIdeasCount = len(followIdeas)
		else:
			followIdeas = None

		# 获取用户关注的其他用户
		followUsers = user['followUsers']
		followUsersCount = 0
		if not followUsers == '':
			followUsers = followUsers.split(',')
			temp = ''
			for item in followUsers:
				temp = temp + '"' + item + '",'
			followUsers = temp[:-1]
			cursor.execute('select username,nickname,portrait,fans from user where username in (%s)' % (followUsers))
			followUsers = cursor.fetchall()
			for item in followUsers:
				temp = item['fans']
				if temp == '':
					temp = 0
				else:
					temp = len(temp.split(','))
				item['fans'] = temp
			followUsersCount = len(followUsers)
		else:
			followUsers = None

		# 获取用户的粉丝
		fans = user['fans']
		fansCount = 0
		if not fans == '':
			fans = fans.split(',')
			temp = ''
			for item in fans:
				temp = temp + '"' + item + '",'
			fans = temp[:-1]
			cursor.execute('select username,nickname,portrait,fans from user where username in (%s)' % (fans))
			fans = cursor.fetchall()
			for item in fans:
				temp = item['fans']
				if temp == '':
					temp = 0
				else:
					temp = len(temp.split(','))
				item['fans'] = temp
			fansCount = len(fans)
		else:
			fans = None

		closedb(db,cursor)

		return render_template('user/home.html', user=user, ideas=ideas, ideasCount=ideasCount, followIdeas=followIdeas, followIdeasCount=followIdeasCount, followUsers=followUsers, followUsersCount=followUsersCount, fans=fans, fansCount=fansCount, followUserStr=followUserStr, hotTags=hotTags)
	
	else:
		# 访问个人主页前需登录
		session['url'] = WECOPREFIX + request.path
		return redirect(url_for('login'))

# 其他用户主页
@app.route('/user/<username>')
def user(username):
	if session.get('username') == username:
		# 访问的就是本人，返回个人主页
		return redirect(url_for('home'))

	else:
		if not session.get('username') == None:
			updateToken(session.get('username'))
		(db,cursor) = connectdb()

		# 访问其他用户
		# cursor.execute('select username,email,nickname,portrait,tags,description,gender,wechat,ideas,followIdeas,fans,followUsers,lastActive from user where username=%s',[username])
		cursor.execute('select username,nickname,portrait,tags,description,gender,wechat,ideas,followIdeas,fans,followUsers,lastActive from user where username=%s',[username])
		user = cursor.fetchone()

		# 获取其他用户的创意
		ideas = user['ideas']
		ideasCount = 0
		if not ideas == '':
			cursor.execute('select id,title,feature from idea where id in (%s) and published=1 and locked=0' % (str(ideas)))
			ideas = cursor.fetchall()
			ideasCount = len(ideas)
		else:
			ideas = None

		# 获取其他用户喜欢的创意
		followIdeas = user['followIdeas']
		followIdeasCount = 0
		if not followIdeas == '':
			cursor.execute('select id,title,feature from idea where id in (%s) and published=1 and locked=0' % (str(followIdeas)))
			followIdeas = cursor.fetchall()
			followIdeasCount = len(followIdeas)
		else:
			followIdeas = None

		# 获取其他用户的关注
		followUsers = user['followUsers']
		followUsersCount = 0
		if not followUsers == '':
			followUsers = followUsers.split(',')
			temp = ''
			for item in followUsers:
				temp = temp + '"' + item + '",'
			followUsers = temp[:-1]
			cursor.execute('select username,nickname,portrait,fans from user where username in (%s)' % (followUsers))
			followUsers = cursor.fetchall()
			for item in followUsers:
				temp = item['fans']
				if temp == '':
					temp = 0
				else:
					temp = len(temp.split(','))
				item['fans'] = temp
			followUsersCount = len(followUsers)
		else:
			followUsers = None

		# 获取其他用户的粉丝
		fans = user['fans']
		fansCount = 0
		if not fans == '':
			fans = fans.split(',')
			temp = ''
			for item in fans:
				temp = temp + '"' + item + '",'
			fans = temp[:-1]
			cursor.execute('select username,nickname,portrait,fans from user where username in (%s)' % (fans))
			fans = cursor.fetchall()
			for item in fans:
				temp = item['fans']
				if temp == '':
					temp = 0
				else:
					temp = len(temp.split(','))
				item['fans'] = temp
			fansCount = len(fans)
		else:
			fans = None

		# 获取当前用户的关注列表
		followUserStr = ''
		me = session.get('username')
		if not me == None:
			cursor.execute('select followUsers from user where username=%s',[me])
			followUserStr = cursor.fetchone()['followUsers']

		closedb(db,cursor)

		return render_template('user/user.html',user=user, ideas=ideas, ideasCount=ideasCount, followIdeas=followIdeas, followIdeasCount=followIdeasCount, followUsers=followUsers, followUsersCount=followUsersCount, fans=fans, fansCount=fansCount, followUserStr=followUserStr)

# 关于weco
@app.route('/about')
def about():
	if not session.get('username') == None:
		return render_template('user/about.html')
	else:
		session['url'] = WECOPREFIX + request.path
		return redirect(url_for('login'))
