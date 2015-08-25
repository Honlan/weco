# coding:utf-8

from flask import *
from weco import app
from weco import cursor
import time
import base64
import random
from hashlib import md5
import os
from weco.conf.configure import WECOROOT

'''
	动态类别说明：
	1. 其他用户关注了我
	2. 其他用户喜欢了我的创意
	3. 其他用户评论了我的创意
'''

# 随机码生成器
def genKey():
	key = ''
	for x in xrange(0, 10):
		key = key + str(random.randint(0, 9))
	key = unicode(md5(key + str(int(time.time()))).hexdigest().upper())
	return key

# 验证token是否属于用户并检测是否有效
def validate(username, token):
	count = cursor.execute("select lastActive, TTL from user where username = %s and token = %s", [username, token])
	if count == 0:
		return False
	else:
		return True
		user = cursor.fetchone()
		lastActive = user['lastActive']
		TTL = user['TTL']
		interval = 3600*24*7
		# token有效期为7天，调用次数为100
		if int(time.time()) - int(lastActive) > interval or TTL < 1:
			return False
		else:
			TTL = TTL - 1
			cursor.execute("update user set TTL = %s where username = %s", [str(TTL), username])
			return True

# 根据offset获取热门创意
@app.route('/api/idea/hot', methods=['POST'])
def api_idea_hot():
	offset = int(request.form['offset'])
	cursor.execute('select * from idea where locked=0 order by praise desc, timestamp desc limit ' + str(offset*10) + ',10')
	ideas = cursor.fetchall()

	# 转换时间戳
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

	return json.dumps({"ok": True, "ideas": ideas})

# 根据offset获取最新创意
@app.route('/api/idea/latest', methods=['POST'])
def api_idea_latest():
	offset = int(request.form['offset'])
	cursor.execute('select * from idea where locked=0 order by timestamp desc, praise desc limit ' + str(offset*10) + ',10')
	ideas = cursor.fetchall()

	# 转换时间戳
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

	return json.dumps({"ok": True, "ideas": ideas})

# 关注创意
# 需要进行token验证
@app.route('/api/idea/follow', methods=['POST'])
def api_idea_follow():
	data = request.form

	if validate(data['username'], data['token']):
		# 验证通过
		ideaId = data['ideaId']
		username = data['username']
		cursor.execute("select nickname,followIdeas from user where username = %s", [username])
		nickname = cursor.fetchone()
		followIdeas = nickname['followIdeas']
		nickname = nickname['nickname']

		# 更新关注创意列表
		followIdeas = followIdeas.split(',')
		if not ideaId in followIdeas:
			followIdeas.append(ideaId)
		temp = ''
		for item in followIdeas:
			if item == '':
				continue
			temp = temp + item + ','
		followIdeas = temp[:-1]
		cursor.execute("update user set followIdeas = %s where username = %s", [followIdeas, username])
		
		# 添加类别2动态，我的创意被别人关注了
		cursor.execute("select title,owner from idea where id=%s",[ideaId])
		owner = cursor.fetchone()
		ideaTitle = owner['title']
		owner = owner['owner']
		cursor.execute("insert into activity(me,other,otherNickname,ideaId,ideaTitle,activityType,timestamp) values(%s,%s,%s,%s,%s,%s,%s)",[owner,username,nickname,ideaId,ideaTitle,2,str(int(time.time()))])
		return json.dumps({"ok": True})

	else:
		# 验证失败
		return json.dumps({"ok": False, "error": "invalid token"})

# 用户取消关注创意
# 需要进行token验证
@app.route('/api/idea/disfollow', methods=['POST'])
def api_idea_disfollow():
	data = request.form

	if validate(data['username'], data['token']):
		# 验证通过
		ideaId = data['ideaId']
		username = data['username']
		cursor.execute("select followIdeas from user where username = %s", [username])
		followIdeas = cursor.fetchone()['followIdeas']
		followIdeas = followIdeas.split(',')

		# 更新关注创意列表
		if ideaId in followIdeas:
			followIdeas.remove(ideaId)
		temp = ''
		for item in followIdeas:
			if item == '':
				continue
			temp = temp + item + ','
		followIdeas = temp[:-1]
		cursor.execute("update user set followIdeas = %s where username = %s", [followIdeas, username])

		return json.dumps({"ok": True})

	else:
		# 验证失败
		return json.dumps({"ok": False, "error": "invalid token"})

# 用户待删除创意
# 需要进行token验证
@app.route('/api/idea/trash', methods=['POST'])
def api_idea_trash():
	data = request.form

	if validate(data['username'], data['token']):
		# 验证通过
		ideaId = data['ideaId']
		username = data['username']

		cursor.execute("select owner from idea where id=%s",[ideaId])
		owner = cursor.fetchone()['owner']

		# 创意确实属于用户
		if owner == username:
			cursor.execute("update idea set locked=1 where id=%s",[ideaId])
			return json.dumps({"ok": True})

		else:
			return json.dumps({"ok": False, "error": "invalid token"})

	else:
		# 验证失败
		return json.dumps({"ok": False, "error": "invalid token"})

# 用户恢复创意
# 需要进行token验证
@app.route('/api/idea/recover', methods=['POST'])
def api_idea_recover():
	data = request.form

	if validate(data['username'], data['token']):
		# 验证通过
		ideaId = data['ideaId']
		username = data['username']

		cursor.execute("select owner from idea where id=%s",[ideaId])
		owner = cursor.fetchone()['owner']

		# 创意确实属于用户
		if owner == username:
			cursor.execute("update idea set locked=0 where id=%s",[ideaId])
			return json.dumps({"ok": True})

		else:
			return json.dumps({"ok": False, "error": "invalid token"})

	else:
		# 验证失败
		return json.dumps({"ok": False, "error": "invalid token"})

# 用户永久删除创意
# 需要进行token验证
@app.route('/api/idea/delete', methods=['POST'])
def api_idea_delete():
	data = request.form

	if validate(data['username'], data['token']):
		# 验证通过
		ideaId = data['ideaId']
		username = data['username']

		cursor.execute("select owner from idea where id=%s",[ideaId])
		owner = cursor.fetchone()['owner']

		# 创意确实属于用户
		if owner == username:
			cursor.execute("delete from idea where id=%s",[ideaId])
			cursor.execute("select ideas from user where username=%s",[username])
			ideas = cursor.fetchone()['ideas'].split(',')

			if ideaId in ideas:
				ideas.remove(ideaId)
			temp = ''
			for item in ideas:
				if item == '':
					continue
				temp = temp + item + ','
			ideas = temp[:-1]
			cursor.execute("update user set ideas = %s where username = %s", [ideas, username])

			return json.dumps({"ok": True})

		else:
			return json.dumps({"ok": False, "error": "invalid token"})

	else:
		# 验证失败
		return json.dumps({"ok": False, "error": "invalid token"})

# 用户点赞创意
@app.route('/api/idea/praise', methods=['POST'])
def api_idea_praise():
	ideaId = request.form['ideaId']
	if (not session.get('ideas') == None) and (not session['ideas'].get(str(ideaId)) == None):
		if session['ideas'][str(ideaId)] == 0:
			# 点赞
			cursor.execute('select praise from idea where id=%s', [ideaId])
			praise = int(cursor.fetchone()['praise']) + 1
			cursor.execute('update idea set praise=%s where id=%s', [praise,ideaId])
			session['ideas'][str(ideaId)] = 1

			return json.dumps({"ok": True, "praise": praise, "action": "increase"})

		else:
			# 取消赞
			cursor.execute('select praise from idea where id=%s', [ideaId])
			praise = int(cursor.fetchone()['praise']) - 1
			cursor.execute('update idea set praise=%s where id=%s', [praise,ideaId])
			session['ideas'][str(ideaId)] = 0

			return json.dumps({"ok": True, "praise": praise, "action": "decrease"})

	else:
		return json.dumps({"ok": False})

# 用户点赞评论
@app.route('/api/comment/praise', methods=['POST'])
def api_comment_praise():
	commentId = request.form['commentId']

	if session.get('comments') == None:
		session['comments'] = {}

	if session['comments'].get(str(commentId)) == None:
		# 点赞评论
		session['comments'][str(commentId)] = True
		cursor.execute('select praise from comment where id=%s', [commentId])
		praise = int(cursor.fetchone()['praise']) + 1
		cursor.execute('update comment set praise=%s where id=%s', [praise,commentId])
		return json.dumps({"ok": True, "praise": praise, "action": "increase"})

	else:
		# 取消赞评论
		session['comments'].pop(str(commentId), None)
		cursor.execute('select praise from comment where id=%s', [commentId])
		praise = int(cursor.fetchone()['praise']) - 1
		cursor.execute('update comment set praise=%s where id=%s', [praise,commentId])
		return json.dumps({"ok": True, "praise": praise, "action": "decrease"})

# 为创意添加图片内容
# 需要进行token验证
@app.route('/api/idea/addImg', methods=['POST'])
def api_idea_addImg():
	data = request.form
	if validate(data['username'], data['token']):
		# 验证通过
		ideaId = data['ideaId']
		cursor.execute("select owner from idea where id=%s",[ideaId])

		# 用户和创意匹配
		if cursor.fetchone()['owner'] == data['username']:
			# 添加图片并保存至上传路径
			imgBase = data['image']
			imgBase = imgBase[imgBase.find('base64')+7:]
			imageData = base64.b64decode(imgBase)
			today = time.strftime('%Y%m%d%H', time.localtime(time.time()))
			filename = today + '_' + genKey()[:10] + '.jpg'
			UPLOAD_FOLDER = '/static/uploads/img'
			filepath = os.path.join(WECOROOT + UPLOAD_FOLDER, filename)
			relapath = os.path.join(UPLOAD_FOLDER, filename)
			imageFile = open(filepath,'wb')
			imageFile.write(imageData)
			imageFile.close()
			cursor.execute("insert into attachment(ideaId,fileType,url,timestamp,username) values(%s,%s,%s,%s,%s)",[ideaId,1,relapath,str(int(time.time())), data['username']])
			return json.dumps({"ok": True})

		else:
			return json.dumps({"ok": False, "error": "invalid token"})

	else:
		# 验证失败
		return json.dumps({"ok": False, "error": "invalid token"})

# 删除创意附件
# 需要进行token验证
@app.route('/api/attachment/remove',methods=['POST'])
def api_attachment_remove():
	data = request.form
	if validate(data['username'], data['token']):
		# 验证通过
		attachmentId = data['attachmentId']
		cursor.execute("select * from attachment where id=%s",[attachmentId])
		attachment = cursor.fetchone()

		if attachment['username'] == data['username']:
			# 附件确实属于该用户
			if (not attachment['fileType'] == 0) and (os.path.exists(WECOROOT + attachment['url'])):
				# 附件类型为图片或视频，则同时删除文件
				os.remove(WECOROOT + attachment['url'])
			
			# 删除创意记录
			cursor.execute('delete from attachment where id=%s', [attachmentId])

			return json.dumps({"ok": True})

		else:
			return json.dumps({"ok": False, "error": "invalid token"})

	else:
		# 验证失败
		return json.dumps({"ok": False, "error": "invalid token"})

# 编辑创意
# 需要进行token验证
@app.route('/api/idea/edit', methods=['POST'])
def api_idea_edit():
	data = request.form
	if validate(data['username'], data['token']):
		# 验证通过
		ideaId = data['ideaId']
		cursor.execute("select owner from idea where id=%s",[ideaId])

		# 创意确实属于用户
		if cursor.fetchone()['owner'] == data['username']:
			# 更新创意信息
			cursor.execute("update idea set title=%s,tags=%s,category=%s where id=%s",[data['title'],data['tags'],data['category'],ideaId])
			
			# 统计创意tag次数
			for tag in data['tags'].split(' '):
				if tag == '':
					continue
				cursor.execute("select count from ideaTagStat where tag=%s and category=%s",[tag,data['category']])
				record = cursor.fetchone()
				if record == None:
					cursor.execute("insert into ideaTagStat(tag,category,count) values(%s,%s,1)",[tag,data['category']])
				else:
					count = int(record['count']) + 1
					cursor.execute("update ideaTagStat set count=%s where tag=%s and category=%s",[count,tag,data['category']])
			
			# 处理创意缩略图
			if data.has_key('thumbnail'):
				imgBase = data['thumbnail']
				imgBase = imgBase[imgBase.find('base64')+7:]
				imageData = base64.b64decode(imgBase)
				today = time.strftime('%Y%m%d%H', time.localtime(time.time()))
				temp = genKey()[:10]
				filename = today + '_' + temp + '.jpg'
				UPLOAD_FOLDER = '/static/uploads/img'
				filepath = os.path.join(WECOROOT + UPLOAD_FOLDER, filename)
				relapath = os.path.join(UPLOAD_FOLDER, filename)
				imageFile = open(filepath,'wb')
				imageFile.write(imageData)
				imageFile.close()

				imgBase = data['feature']
				imgBase = imgBase[imgBase.find('base64')+7:]
				imageData = base64.b64decode(imgBase)
				filename = today + '_' + temp + '_thumb.jpg'
				filepath = os.path.join(WECOROOT + UPLOAD_FOLDER, filename)
				relapath1 = os.path.join(UPLOAD_FOLDER, filename)
				imageFile = open(filepath,'wb')
				imageFile.write(imageData)
				imageFile.close()

				# 删除旧缩略图并更新新缩略图路径
				cursor.execute('select thumbnail,feature from idea where id=%s',[ideaId])
				oldthumb = cursor.fetchone()
				oldfeature = oldthumb['feature']
				oldthumb = oldthumb['thumbnail']
				if (not oldthumb == '/static/img/idea.jpg') and (os.path.exists(WECOROOT + oldthumb)):
					os.remove(WECOROOT + oldthumb)
				if (not oldfeature == '/static/img/idea.jpg') and (os.path.exists(WECOROOT + oldfeature)):
					os.remove(WECOROOT + oldfeature)

				print oldthumb,oldfeature
				print relapath,relapath1,ideaId

				cursor.execute("update idea set thumbnail=%s,feature=%s where id=%s",[relapath,relapath1,ideaId])

			return json.dumps({"ok": True})

		# 创意不属于该用户
		else:
			return json.dumps({"ok": False, "error": "invalid token"})
	
	else:
		# 验证失败
		return json.dumps({"ok": False, "error": "invalid token"})

# 用户评论创意
# 需要进行token验证
@app.route('/api/idea/comment', methods=['POST'])
def api_idea_comment():
	data = request.form
	if validate(data['username'], data['token']):
		# 验证通过
		ideaId = data['ideaId']
		username = data['username']
		timestamp = str(int(time.time()))
		content = data['content']
		cursor.execute('select nickname,portrait from user where username=%s', [username])
		nickname = cursor.fetchone()
		portrait = nickname['portrait']
		nickname = nickname['nickname']

		# 新增评论记录
		cursor.execute("insert into comment(username,nickname,portrait,ideaId,timestamp,content) values(%s,%s,%s,%s,%s,%s)", [username,nickname,portrait,ideaId,timestamp,content])
		cursor.execute("select commentCount from idea where id=%s",[ideaId])
		commentCount = int(cursor.fetchone()['commentCount']) + 1
		cursor.execute("update idea set commentCount=%s where id=%s",[commentCount,ideaId])
		
		# 添加类别3动态，我的创意被别人评论了
		cursor.execute("select title,owner from idea where id=%s",[ideaId])
		owner = cursor.fetchone()
		ideaTitle = owner['title']
		owner = owner['owner']
		cursor.execute("insert into activity(me,other,otherNickname,ideaId,ideaTitle,comment,activityType,timestamp) values(%s,%s,%s,%s,%s,%s,%s,%s)",[owner,username,nickname,ideaId,ideaTitle,content,3,str(int(time.time()))])
		return json.dumps({"ok": True})
	
	else:
		# 验证失败
		return json.dumps({"ok": False, "error": "invalid token"})

