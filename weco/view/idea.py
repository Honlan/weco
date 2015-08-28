# coding:utf-8

from flask import *
from weco import app
from weco import connectdb,closedb
import time
import base64
import random
from hashlib import md5
from werkzeug import secure_filename
import os
from weco.conf.configure import WECOROOT, WECOPREFIX

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
	(db,cursor) = connectdb()
	cursor.execute('select * from idea where published=1 and locked=0 order by praise desc, timestamp desc limit 10')

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

	closedb(db,cursor)

	return render_template('index/index.html', ideas=ideas, hot=True)

# 主页，展示最新创意
@app.route('/<mode>')
def index_latest(mode):
	if mode == 'latest':
		(db,cursor) = connectdb()
		cursor.execute('select * from idea where published=1 and locked=0 order by timestamp desc, praise desc limit 10')

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

		closedb(db,cursor)

		return render_template('index/index.html', ideas=ideas, hot=False)

# 发布创意
@app.route('/idea/new',methods=['GET','POST'])
def idea_new():
	if request.method == 'GET':
		# 用户已经登陆
		if not session.get('username') == None:
			# 获取热门标签
			category = ['社会创新','设计','生活','城市','娱乐','健康','旅行','教育','运动','产品','艺术','科技','工程','广告','其他']
			hotTags = {}
			(db,cursor) = connectdb()
			for item in category:
				cursor.execute("select tag from ideaTagStat where category=%s order by count desc limit 10",[item])
				hotTags[item] = cursor.fetchall()

			closedb(db,cursor)

			return render_template('idea/idea_new.html',hotTags=hotTags)

		# 用户尚未登录
		else:
			session['url'] = WECOPREFIX + request.path
			return redirect(url_for('login'))

	elif request.method == 'POST':
		# 用户已经登陆
		if not session.get('username') == None:
			# 新增创意数据
			(db,cursor) = connectdb()
			username = request.form['username']
			title = request.form['title']
			category = request.form['category']
			tags = request.form['tags']
			# content = request.form['content']
			timestamp = str(int(time.time()))
			cursor.execute('select nickname,portrait from user where username=%s',[username])
			portrait = cursor.fetchone()
			nickname = portrait['nickname']
			portrait = portrait['portrait']

			# 保存封面图片
			# imgBase = request.form['thumbnail']
			# imgBase = imgBase[imgBase.find('base64')+7:]
			# imageData = base64.b64decode(imgBase)
			# today = time.strftime('%Y%m%d%H', time.localtime(time.time()))
			# temp = genKey()[:10]
			# filename = today + '_' + temp + '.jpg'
			# UPLOAD_FOLDER = '/static/uploads/img'
			# filepath = os.path.join(WECOROOT + UPLOAD_FOLDER, filename)
			# relapath = os.path.join(UPLOAD_FOLDER, filename)
			# imageFile = open(filepath,'wb')
			# imageFile.write(imageData)
			# imageFile.close()

			# imgBase = request.form['feature']
			# imgBase = imgBase[imgBase.find('base64')+7:]
			# imageData = base64.b64decode(imgBase)
			# filename = today + '_' + temp + '_thumb.jpg'
			# filepath = os.path.join(WECOROOT + UPLOAD_FOLDER, filename)
			# relapath1 = os.path.join(UPLOAD_FOLDER, filename)
			# imageFile = open(filepath,'wb')
			# imageFile.write(imageData)
			# imageFile.close()

			# 新增创意并添加内容
			# cursor.execute('insert into idea(title,category,tags,timestamp,owner,nickname,portrait,thumbnail,feature) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',[title,category,tags,timestamp,username,nickname,portrait,relapath,relapath1])
			cursor.execute('insert into idea(title,category,tags,timestamp,owner,nickname,portrait) values(%s,%s,%s,%s,%s,%s,%s)',[title,category,tags,timestamp,username,nickname,portrait])

			# 获取新增创意id
			cursor.execute('select id from idea where title=%s and category=%s and tags=%s and timestamp=%s and owner=%s',[title,category,tags,timestamp,username])
			ideaId = cursor.fetchone()['id']

			# cursor.execute("insert into attachment(ideaId,fileType,url,timestamp,username) values(%s,%s,%s,%s,%s)",[ideaId,0,content,str(int(time.time())), username])

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

			closedb(db,cursor)
			
			return json.dumps({"ideaId": ideaId})

		# 用户尚未登录
		else:
			session['url'] = WECOPREFIX + request.path
			return redirect(url_for('login'))

# 创意主页
@app.route('/idea/<ideaId>')
def idea(ideaId):
	# 如果创意已被锁定，则给出错误提示
	# TO DO

	(db,cursor) = connectdb()

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
		if item['fileType'] == 0:
			item['url'] = item['url'].split('\n')
			temp = []
			for i in item['url']:
				i = i.strip()
				if not i == '':
					temp.append(i)
			item['url'] = temp

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
	category = ['社会创新','设计','生活','城市','娱乐','健康','旅行','教育','运动','产品','艺术','科技','工程','广告','其他']
	hotTags = {}
	for item in category:
		cursor.execute("select tag from ideaTagStat where category=%s order by count desc limit 10",[item])
		hotTags[item] = cursor.fetchall()

	if not session.get('username') == None:
		cursor.execute("update user set TTL=100 where username=%s",[session.get('username')])

	closedb(db,cursor)

	return render_template('idea/idea.html', idea=idea, liked=liked, attachments=attachments, comments=comments, commentsCount=commentsCount, fans=fans, hotTags=hotTags)

# 为创意添加文本内容
@app.route('/idea/addText/<ideaId>',methods=['POST'])
def idea_add_text(ideaId):
	if not session.get('username') == None:
		(db,cursor) = connectdb()
		text = request.form['content']
		cursor.execute("insert into attachment(ideaId,fileType,url,timestamp,username) values(%s,%s,%s,%s,%s)",[ideaId,0,text,str(int(time.time())), session.get('username')])
		closedb(db,cursor)
		return redirect(url_for('idea', ideaId=ideaId))
	else:
		session['url'] = WECOPREFIX + request.path
		return redirect(url_for('login'))

# 为创意添加视频内容
@app.route('/idea/addVideo/<ideaId>', methods=['POST'])
def idea_add_video(ideaId):
	if not session.get('username') == None:
		(db,cursor) = connectdb()
		image = request.files['content']
		today = time.strftime('%Y%m%d', time.localtime(time.time()))
		filename = today + '_' + secure_filename(genKey()[:10] + '_' + image.filename)
		UPLOAD_FOLDER = '/static/uploads/video'
		filepath = os.path.join(WECOROOT + UPLOAD_FOLDER, filename)
		relapath = os.path.join(UPLOAD_FOLDER, filename)
		image.save(filepath)
		cursor.execute("insert into attachment(ideaId,fileType,url,timestamp,username) values(%s,%s,%s,%s,%s)",[ideaId,2,relapath,str(int(time.time())), session.get('username')])
		closedb(db,cursor)
		return redirect(url_for('idea', ideaId=ideaId))
	else:
		session['url'] = WECOPREFIX + request.path
		return redirect(url_for('login'))

