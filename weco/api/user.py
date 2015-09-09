# coding:utf-8

from flask import *
from weco import app
from weco import connectdb,closedb
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
	(db,cursor) = connectdb()

	count = cursor.execute("select lastActive, TTL from user where username = %s and token = %s", [username, token])
	if count == 0:
		closedb(db,cursor)
		return False
	else:
		closedb(db,cursor)
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

# 注册时判断用户名是否存在
@app.route('/api/user/existName', methods=['POST'])
def api_user_exist_name():
	(db,cursor) = connectdb()

	data = request.form
	count = cursor.execute("select username from user where username = %s", [data['username']])

	closedb(db,cursor)
	
	if count > 0:
		return json.dumps({"ok": True, "exist": True})
	else:
		return json.dumps({"ok": True, "exist": False})

# 注册时判断手机号是否存在
@app.route('/api/user/existEmail', methods=['POST'])
def api_user_exist_email():
	(db,cursor) = connectdb()

	data = request.form
	count = cursor.execute("select email from user where email = %s", [data['email']])

	closedb(db,cursor)

	if count > 0:
		return json.dumps({"ok": True, "exist": True})
	else:
		return json.dumps({"ok": True, "exist": False})

# 用户编辑个人信息
# 需要进行token验证
@app.route('/api/user/edit', methods=['POST'])
def api_user_edit():
	data = request.form
	if validate(data['username'], data['token']):
		(db,cursor) = connectdb()

		# 验证成功
		nickname = data['nickname']
		gender = data['gender']
		tags = data['tags']
		description = data['description']
		email = data['email']
		wechat = data['wechat']
		hobby = data['hobby']
		location = data['location']

		# 统计用户tag次数
		for tag in tags.split(' '):
			if tag == '':
				continue
			cursor.execute("select count from userTagStat where tag=%s and gender=%s",[tag,gender])
			record = cursor.fetchone()
			if record == None:
				cursor.execute("insert into userTagStat(tag,gender,count) values(%s,%s,1)",[tag,gender])
			else:
				count = int(record['count']) + 1
				cursor.execute("update userTagStat set count=%s where tag=%s and gender=%s",[count,tag,gender])
		
		cursor.execute("update user set nickname=%s, gender=%s,tags=%s,description=%s,email=%s,wechat=%s,hobby=%s,location=%s where username=%s", [nickname,gender,tags,description,email,wechat,hobby,location,data['username']])
		
		# 处理用户头像
		if data.has_key('portrait'):
			# 生成新的头像图片
			portrait = data['portrait']
			portrait = portrait[portrait.find('base64')+7:]
			imageData = base64.b64decode(portrait)
			today = time.strftime('%Y%m%d%H', time.localtime(time.time()))
			filename = today + '_' + genKey()[:10] + '.jpg'
			UPLOAD_FOLDER = '/static/uploads/img'
			filepath = os.path.join(WECOROOT + UPLOAD_FOLDER, filename)
			relapath = os.path.join(UPLOAD_FOLDER, filename)
			imageFile = open(filepath,'wb')
			imageFile.write(imageData)
			imageFile.close()

			# 删除旧的头像图片
			cursor.execute('select portrait from user where username=%s',[data['username']])
			oldportrait = cursor.fetchone()['portrait']
			if (not oldportrait == '/static/img/user.png') and (os.path.exists(WECOROOT + oldportrait)):
				os.remove(WECOROOT + oldportrait)
			cursor.execute("update user set portrait=%s where username=%s",[relapath,data['username']])

			# 更新该用户所有创意的头像路径
			cursor.execute("select ideas from user where username=%s",[data['username']])
			myIdeas = cursor.fetchone()['ideas'].split(',')
			for item in myIdeas:
				if item == '':
					continue
				cursor.execute("update idea set portrait=%s where id=%s",[relapath,item])

			# 更新该用户所有评论的头像路径
			cursor.execute("update comment set portrait=%s where username=%s",[relapath,data['username']])

		closedb(db,cursor)

		return json.dumps({"ok": True})

	else:
		# 验证失败
		return json.dumps({"ok": False, "error": "invalid token"})

# 用户关注其他用户
# 需要进行token验证
@app.route('/api/user/follow', methods=['POST'])
def api_user_follow():
	data = request.form
	if validate(data['source'], data['token']):
		(db,cursor) = connectdb()

		# 验证通过
		source = data['source']
		target = data['target']
		cursor.execute("select nickname,followUsers from user where username = %s", [source])
		nickname = cursor.fetchone()
		followUsers = nickname['followUsers']
		nickname = nickname['nickname']
		followUsers = followUsers.split(',')

		# 更新双方关注用户列表
		if not target in followUsers:
			followUsers.append(target)
		temp = ''
		for item in followUsers:
			if item == '':
				continue
			temp = temp + item + ','
		followUsers = temp[:-1]
		cursor.execute("update user set followUsers = %s where username = %s", [followUsers, source])
		cursor.execute("select fans from user where username = %s", [target])
		fans = cursor.fetchone()['fans']
		fans = fans.split(',')
		if not source in fans:
			fans.append(source)
		temp = ''
		for item in fans:
			if item == '':
				continue
			temp = temp + item + ','
		fans = temp[:-1]
		cursor.execute("update user set fans = %s where username = %s", [fans, target])
		
		# 添加类别1动态，我被别人关注了
		cursor.execute("insert into activity(me,other,otherNickname,activityType,timestamp) values(%s,%s,%s,%s,%s)",[target,source,nickname,1,str(int(time.time()))])

		closedb(db,cursor)

		return json.dumps({"ok": True})

	else:
		# 验证失败
		return json.dumps({"ok": False, "error": "invalid token"})

# 用户取消关注其他用户
# 需要进行token验证
@app.route('/api/user/disfollow', methods=['POST'])
def api_user_disfollow():
	data = request.form
	if validate(data['source'], data['token']):
		(db,cursor) = connectdb()

		# 验证成功
		source = data['source']
		target = data['target']

		# 更新双方关注列表
		cursor.execute("select followUsers from user where username = %s", [source])
		followUsers = cursor.fetchone()['followUsers']
		followUsers = followUsers.split(',')
		if target in followUsers:
			followUsers.remove(target)
		temp = ''
		for item in followUsers:
			if item == '':
				continue
			temp = temp + item + ','
		followUsers = temp[:-1]
		cursor.execute("update user set followUsers = %s where username = %s", [followUsers, source])
		cursor.execute("select fans from user where username = %s", [target])
		fans = cursor.fetchone()['fans']
		fans = fans.split(',')
		if source in fans:
			fans.remove(source)
		temp = ''
		for item in fans:
			if item == '':
				continue
			temp = temp + item + ','
		fans = temp[:-1]
		cursor.execute("update user set fans = %s where username = %s", [fans, target])

		closedb(db,cursor)

		return json.dumps({"ok": True})

	else:
		# 验证失败
		return json.dumps({"ok": False, "error": "invalid token"})

# 发送聊天消息
# 需要进行token验证
@app.route('/api/chat/send', methods=['POST'])
def api_chat_send():
	data = request.form
	if validate(data['source'], data['token']):
		(db,cursor) = connectdb()

		# 验证成功
		source = data['source']
		target = data['target']
		content = data['content']
		timestamp = str(int(time.time()))
		cursor.execute("select nickname from user where username=%s",[target])
		targetNickname = cursor.fetchone()['nickname']
		cursor.execute("select nickname from user where username=%s",[source])
		sourceNickname = cursor.fetchone()['nickname']
		cursor.execute("insert into chat(source,sourceNickname,target,targetNickname,content,timestamp) values(%s,%s,%s,%s,%s,%s)",[source,sourceNickname,target,targetNickname,content,timestamp])

		closedb(db,cursor)

		return json.dumps({"ok": True})

	else:
		# 验证失败
		return json.dumps({"ok": False, "error": "invalid token"})

