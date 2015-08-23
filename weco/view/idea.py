# coding:utf-8

from flask import *
from weco import app
from weco import cursor
import time
import random
from hashlib import md5
from werkzeug import secure_filename
import os
from weco.conf.configure import WECOROOT

# 随机码生成器
def genKey():
	key = ''
	for x in xrange(0, 10):
		key = key + str(random.randint(0, 9))
	key = unicode(md5(key + str(int(time.time()))).hexdigest().upper())
	return key

# 主页，展示热门创意
@app.route('/')
def index():
	cursor.execute('select * from idea where locked=0 order by praise desc, timestamp desc limit 10')

	# 转换时间戳
	ideas = cursor.fetchall()
	for item in ideas:
		temp = int(time.time()) - int(item['timestamp'])
		if temp < 60:
			temp = str(temp) + 's'
		elif temp < 3600:
			temp = str(temp/60) + 'm'
		elif temp < 3600 * 24:
			temp = str(temp/3600) + 'h'
		else:
			temp = str(temp/(3600*24)) + 'd'
		item['timestamp'] = temp

	return render_template('index/index.html', ideas=ideas, hot=True)

# 主页，展示最新创意
@app.route('/<mode>')
def index_latest(mode):
	if mode == 'latest':
		cursor.execute('select * from idea where locked=0 order by timestamp desc, praise desc limit 10')

		# 转换时间戳
		ideas = cursor.fetchall()
		for item in ideas:
			temp = int(time.time()) - int(item['timestamp'])
			if temp < 60:
				temp = str(temp) + 's'
			elif temp < 3600:
				temp = str(temp/60) + 'm'
			elif temp < 3600 * 24:
				temp = str(temp/3600) + 'h'
			else:
				temp = str(temp/(3600*24)) + 'd'
			item['timestamp'] = temp

		return render_template('index/index.html', ideas=ideas, hot=False)

# 发布创意
@app.route('/idea/new',methods=['GET','POST'])
def idea_new():
	if request.method == 'GET':
		# 用户已经登陆
		if not session.get('username') == None:
			# 获取热门标签
			category = ['社会','设计','生活','城市','娱乐','健康','旅行','教育','运动','产品','艺术','科技','工程','广告','其他']
			hotTags = {}
			for item in category:
				cursor.execute("select tag from ideaTagStat where category=%s order by count desc limit 10",[item])
				hotTags[item] = cursor.fetchall()

			return render_template('idea/idea_new.html',hotTags=hotTags)

		# 用户尚未登录
		else:
			return redirect(url_for('login'))

	elif request.method == 'POST':
		# 用户已经登陆
		if not session.get('username') == None:
			# 新增创意数据
			username = session.get('username')
			title = request.form['title']
			category = request.form['category']
			tags = request.form['tags']
			timestamp = str(int(time.time()))
			cursor.execute('select nickname from user where username=%s',[username])
			nickname = cursor.fetchone()['nickname']
			cursor.execute('insert into idea(title,category,tags,timestamp,owner,nickname) values(%s,%s,%s,%s,%s,%s)',[title,category,tags,timestamp,username,nickname])
			
			# 获取新增创意id
			cursor.execute('select id from idea where title=%s and category=%s and tags=%s and timestamp=%s and owner=%s and nickname=%s',[title,category,tags,timestamp,username,nickname])
			ideaId = cursor.fetchone()['id']

			# 将该id添加至用户的创意列表中
			cursor.execute('select ideas from user where username=%s',[username])
			ideas = cursor.fetchone()['ideas']
			ideas = ideas + ',' + str(ideaId)
			ideas = ideas.lstrip(',')
			cursor.execute('update user set ideas=%s where username=%s',[ideas,username])

			# 统计创意tag次数
			for tag in tags.split(' '):
				if tag == '':
					continue
				cursor.execute("select count from ideaTagStat where tag=%s and category=%s",[tag,category])
				record = cursor.fetchone()
				if record == None:
					cursor.execute("insert into ideaTagStat(tag,category,count) values(%s,%s,1)",[tag,category])
				else:
					count = int(record['count']) + 1
					cursor.execute("update ideaTagStat set count=%s where tag=%s and category=%s",[count,tag,category])
			return redirect(url_for('idea',ideaId=ideaId))

		# 用户尚未登录
		else:
			return redirect(url_for('login'))

# 创意主页
@app.route('/idea/<ideaId>')
def idea(ideaId):
	# 如果创意已被锁定，则给出错误提示
	# TO DO

	# 缓存该创意的阅读、点赞等用户行为
	if session.get('ideas') == None:
		session['ideas'] = {}

	# 阅读量＋1
	if not session['ideas'].has_key(str(ideaId)):
		cursor.execute('select readCount from idea where id=%s', [ideaId])
		readCount = int(cursor.fetchone()['readCount']) + 1
		cursor.execute('update idea set readCount=%s where id=%s', [readCount,ideaId])
		session['ideas'][str(ideaId)] = 0
	
	# 获取创意信息
	cursor.execute('select * from idea where id=%s', [ideaId])
	idea = cursor.fetchone()
	idea['timestamp'] = time.strftime('%m-%d %H:%M', time.localtime(float(idea['timestamp'])))

	# 判断当前用户是否已经喜欢该创意
	liked = False
	username = session.get('username')
	if (not username == None) and (not username == idea['owner']):
		cursor.execute('select followIdeas from user where username=%s',[username])
		if ideaId in cursor.fetchone()['followIdeas'].split(','):
			liked = True
		else:
			liked = False

	# 获取该创意所有附件
	cursor.execute("select * from attachment where ideaId=%s order by timestamp asc",[ideaId])
	attachments = cursor.fetchall()
	for item in attachments:
		item['timestamp'] = time.strftime('%m-%d %H:%M', time.localtime(float(item['timestamp'])))

	# 获取该创意所有评论
	cursor.execute("select * from comment where ideaId=%s order by praise desc, timestamp desc", [ideaId])
	comments = cursor.fetchall()
	for item in comments:
		item['timestamp'] = time.strftime('%m-%d %H:%M', time.localtime(float(item['timestamp'])))
	commentsCount = len(comments)
	
	# 获取该创意发起人粉丝人数
	cursor.execute("select fans from user where username=%s",[idea['owner']])
	fans = len(cursor.fetchone()['fans'].split(','))

	# 获取热门标签以供编辑
	category = ['社会','设计','生活','城市','娱乐','健康','旅行','教育','运动','产品','艺术','科技','工程','广告','其他']
	hotTags = {}
	for item in category:
		cursor.execute("select tag from ideaTagStat where category=%s order by count desc limit 10",[item])
		hotTags[item] = cursor.fetchall()

	if not session.get('username') == None:
		cursor.execute("update user set TTL=100 where username=%s",[session.get('username')])

	return render_template('idea/idea.html', idea=idea, liked=liked, attachments=attachments, comments=comments, commentsCount=commentsCount, fans=fans, hotTags=hotTags)

# 为创意添加文本内容
@app.route('/idea/addText/<ideaId>',methods=['POST'])
def idea_add_text(ideaId):
	if not session.get('username') == None:
		text = request.form['content']
		cursor.execute("insert into attachment(ideaId,fileType,url,timestamp,username) values(%s,%s,%s,%s,%s)",[ideaId,0,text,str(int(time.time())), session.get('username')])
		return redirect(url_for('idea', ideaId=ideaId))
	else:
		return redirect(url_for('login'))

# 为创意添加视频内容
@app.route('/idea/addVideo/<ideaId>', methods=['POST'])
def idea_add_video(ideaId):
	if not session.get('username') == None:
		image = request.files['content']
		today = time.strftime('%Y%m%d', time.localtime(time.time()))
		filename = today + '_' + secure_filename(genKey()[:10] + '_' + image.filename)
		UPLOAD_FOLDER = '/static/uploads/video'
		filepath = os.path.join(WECOROOT + UPLOAD_FOLDER, filename)
		relapath = os.path.join(UPLOAD_FOLDER, filename)
		image.save(filepath)
		cursor.execute("insert into attachment(ideaId,fileType,url,timestamp,username) values(%s,%s,%s,%s,%s)",[ideaId,2,relapath,str(int(time.time())), session.get('username')])
		return redirect(url_for('idea', ideaId=ideaId))
	else:
		return redirect(url_for('login'))
