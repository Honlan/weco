# coding:utf-8

'''
	@ weco共创社区开源项目
	@ flask + jinja + angularjs
	@ author by Honlan
	@ last updated 2015-07-28 
'''

from flask import *
from configure_weco import *
import MySQLdb
import MySQLdb.cursors
from functools import wraps
import json
from hashlib import md5
import random
import smtplib  
from email.mime.text import MIMEText
import time
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
# 载入系统配置
app.config.from_object(__name__)
app.secret_key="8E9852FD04BA946D51DE36DFB08E1DB6"

# 数据库连接
db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=DATABASE, port=PORT, charset=CHARSET, cursorclass = MySQLdb.cursors.DictCursor)
db.autocommit(True)
cursor = db.cursor()

# 随机码生成器
def genKey():
	key = ''
	for x in xrange(0, 10):
		key = key + str(random.randint(0, 9))
	key = unicode(md5(key + str(int(time.time()))).hexdigest().upper())
	return key

# 验证api key和token是否属于用户并检测是否有效
def validate(username, apiKey, token):
	count = cursor.execute("select lastActive, TTL from user where username = %s and apiKey = %s and token = %s", [username, apiKey, token])
	if count == 0:
		return False
	else:
		user = cursor.fetchone()
		lastActive = user['lastActive']
		TTL = user['TTL']
		interval = 3600
		if int(time.time()) - int(lastActive) > interval or TTL < 1:
			return False
		else:
			TTL = TTL - 1
			cursor.execute("update user set TTL = %s where username = %s", [str(TTL), username])
			return True


# 验证是否登录
def login_required(fn):
	@wraps(fn)
	def decorated_function(*args, **kwargs):
		if session.get('logged_in') is not True:
			return jsonify(ok=False, login_required=True, msg=str("login_required"))
		return fn(*args, **kwargs)
	return decorated_function

'''
	api路由
	分为user和idea两大块
	分别处理与用户和创意相关的操作
'''

'''
	api用户部分
'''

# 判断用户名是否存在
@app.route('/api/user/existName', methods=['POST'])
def api_user_exist_name():
	data = json.loads(request.data)
	count = cursor.execute("select username from user where username = %s", [data['username']])
	if count > 0:
		return "{'ok': True, 'exist': True}"
	else:
		return "{'ok': True, 'exist': False}"

# 判断邮箱是否存在
@app.route('/api/user/existEmail', methods=['POST'])
def api_user_exist_email():
	data = json.loads(request.data)
	count = cursor.execute("select email from user where email = %s", [data['email']])
	if count > 0:
		return "{'ok': True, 'exist': True}"
	else:
		return "{'ok': True, 'exist': False}"

# 用户注册，注册同时生成固定api key
@app.route('/api/user/register', methods=['POST'])
def api_user_register():
	data = json.loads(request.data)
	username = data['username']
	email = data['email']
	password = unicode(md5(data['password']).hexdigest().upper())
	apiKey = genKey()
	cursor.execute("insert into user(username, password, email, apiKey) values(%s, %s, %s, %s)", [username, password, email, apiKey])
	return "{'ok': True, 'username': " + username + ", 'email': " + email + ", 'apiKey': " + apiKey + "}"

# 用户登录，登陆同时生成动态token，持续时间一个小时，使用次数100
@app.route('/api/user/login', methods=['POST'])
def api_user_login():
	data = json.loads(request.data)
	username = data['username']
	email = username
	password = unicode(md5(data['password']).hexdigest().upper())
	count = cursor.execute("select id from user where username = %s and password = %s", [username, password])
	count = count + cursor.execute("select id from user where email = %s and password = %s", [email, password])
	if count > 0:
		token = genKey()
		TTL = 100
		cursor.execute("update user set token = %s, lastActive = %s, TTL = %s where username = %s", [token, str(int(time.time())), TTL, username])
		cursor.execute("update user set token = %s, lastActive = %s, TTL = %s where email = %s", [token, str(int(time.time())), TTL, email])
		return "{'ok': True, 'token': " + token + "}"
	else:
		return "{'ok': False, 'error': 'wrong login info'}"

# 获取用户的固定apiKey
@app.route('/api/user/apiKey', methods=['POST'])
def api_user_api_key():
	data = json.loads(request.data)
	if data.has_key('username'):
		username = data['username']
		if cursor.execute("select apiKey from user where username = %s", [username]) == 0:
			return "{'ok': False, 'error': 'no such username'}"
		else:
			return "{'ok': True, 'apiKey': " + cursor.fetchone()['apiKey'] + "}"
	if data.has_key('email'):
		email = data['email']
		if cursor.execute("select apiKey from user where email = %s", [email]) == 0:
			return "{'ok': False, 'error': 'no such email'}"
		else:
			return "{'ok': True, 'apiKey': " + cursor.fetchone()['apiKey'] + "}"

# 忘记密码申请
@app.route('/api/user/forgetPwd', methods=['POST'])
def api_user_forget_pwd():
	data = json.loads(request.data)
	email = data['email']
	key = genKey()
	cursor.execute("update user set changePwd = %s where email = %s", [key, email])
	me = "Weco运营团队" + "<" + MAILUSER + "@" + MAILPOSTFIX + ">"
	msg = MIMEText(u"点击以下链接以重置您的密码\n" + key, 'text', 'utf-8')
	msg['Subject'] = '账户密码重置'
	msg['From'] = me
	msg['To'] = email
	server = smtplib.SMTP()
	server.connect(MAILHOST)
	server.login(MAILUSER, MAILPWD)
	server.sendmail(me, [email], msg.as_string())
	server.close() 
	return "{'ok': True, 'key': " + key + "}"

# 忘记密码重置
@app.route('/api/user/resetPwd', methods=['POST'])
def api_user_reset_pwd():
	data = json.loads(request.data)
	email = data['email']
	key = data['key']
	password = data['password']
	if cursor.execute("select id from user where email = %s and changePwd = %s", [email, key]) > 0:
		cursor.execute("update user set password = %s where email = %s", [unicode(md5(password).hexdigest().upper()), email])
		return "{'ok': True, 'msg': 'reset password'}"
	else:
		return "{'ok': False, 'error': 'wrong info to change password'}"

# 根据username获取用户概要非隐私资料
@app.route('/api/user/info', methods=['POST'])
def api_user_info():
	data = json.loads(request.data)
	username = data['username']
	cursor.execute("select username,nickname,email,followUsers,followIdeas,fans,ideas,gender,birthday,constellation,degree,job,skills,tags from user where username = %s", [username])
	user = cursor.fetchone()
	return '{"ok": True, "user": ' + json.dumps(user) + '}'

# 编辑个人信息
# 需要进行api key和token验证
@app.route('/api/user/edit', methods=['POST'])
def api_user_edit():
	data = json.loads(request.data)
	if validate(data['username'], data['apiKey'], data['token']):
		cursor.execute("update user set nickname=%s,gender=%s,birthday=%s,constellation=%s,identity=%s,phone=%s,portrait=%s,degree=%s,job=%s,experiences=%s,skills=%s,tags=%s where username=%s", [data['nickname'],data['gender'],data['birthday'],data['constellation'],data['identity'],data['phone'],data['portrait'],data['degree'],data['job'],data['experiences'],data['skills'],data['tags'],data['username']])
		return "{'ok': True, 'msg':'edit personal profile'}"
	else:
		return "{'ok': False, 'error': 'invalid api key or token'}"

# 修改个人密码
# 需要进行api key和token验证
@app.route('/api/user/changePwd', methods=['POST'])
def api_user_change_pwd():
	data = json.loads(request.data)
	if validate(data['username'], data['apiKey'], data['token']):
		cursor.execute("update user set password = %s where username = %s", [unicode(md5(data['password']).hexdigest().upper()), data['username']])
		return "{'ok': True, 'msg': 'change password'}"
	else:
		return "{'ok': False, 'error': 'invalid api key or token'}" 

# 修改个人邮箱
# 绑定手机号

'''
	activityType说明
	0: 用户关注用户
	1: 用户取消关注用户
	2: 用户关注创意
	3: 用户取消关注创意
	4: 用户发布了创意
	5: 用户加入了创意
	6: 用户离开了创意
	7: 用户点赞了创意
	8: 用户鄙视了创意
	9: 用户评论了创意
'''	

# 关注其他用户
# 需要进行api key和token验证
@app.route('/api/user/follow', methods=['POST'])
def api_user_follow():
	data = json.loads(request.data)
	if validate(data['username'], data['apiKey'], data['token']):
		target = data['target']
		username = data['username']
		activityType = 0
		timestamp = int(time.time())
		cursor.execute("insert into activity(username, target, type, timestamp) values(%s, %s, %s, %s)", [username, target, activityType, timestamp])
		cursor.execute("select followUsers from user where username = %s", [username])
		followUsers = cursor.fetchone()['followUsers']
		followUsers = followUsers + ',' + str(target)
		followUsers = followUsers.lstrip(',')
		cursor.execute("update user set followUsers = %s where username = %s", [followUsers, username])
		return '{"ok": True, "msg": "user follow user"}'
	else:
		return "{'ok': False, 'error': 'invalid api key or token'}"

# 取消关注其他用户
# 需要进行api key和token验证
@app.route('/api/user/unfollow', methods=['POST'])
def api_user_unfollow():
	data = json.loads(request.data)
	if validate(data['username'], data['apiKey'], data['token']):
		target = data['target']
		username = data['username']
		activityType = 1
		timestamp = int(time.time())
		cursor.execute("insert into activity(username, target, type, timestamp) values(%s, %s, %s, %s)", [username, target, activityType, timestamp])
		cursor.execute("select followUsers from user where username = %s", [username])
		followUsers = cursor.fetchone()['followUsers'].split(',')
		temp = ''
		for item in followUsers:
			if not item == str(target):
				temp = temp + item + ','
		cursor.execute("update user set followUsers = %s where username = %s", [temp[:-1], username])
		return '{"ok": True, "msg": "user unfollow user"}'
	else:
		return "{'ok': False, 'error': 'invalid api key or token'}"

'''
	api创意部分
'''

# 发布创意
# 需要进行api key和token验证
@app.route('/api/idea/new', methods=['POST'])
def api_idea_new():
	data = json.loads(request.data)
	if validate(data['username'], data['apiKey'], data['token']):
		cursor.execute("insert into idea(lastUpdate, title, thumbnail, tags, category, description, location, videos, open, needs, team, content, progress, results, owner) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [str(int(time.time())),data['title'],data['thumbnail'],data['tags'],data['category'],data['description'],data['location'],data['videos'],data['open'],data['needs'],data['team'],data['content'],data['progress'],data['results'],data['username']])
		return "{'ok': True, 'title': " + data['title'] + "}"
	else:
		return "{'ok': False, 'error': 'invalid api key or token'}"

# 编辑创意
# 需要进行api key和token验证
@app.route('/api/idea/edit', methods=['POST'])
def api_idea_edit():
	data = json.loads(request.data)
	if validate(data['username'], data['apiKey'], data['token']):
		cursor.execute("update idea set lastUpdate=%s, title=%s, thumbnail=%s, tags=%s, category=%s, description=%s, location=%s, videos=%s, open=%s, needs=%s, team=%s, content=%s, progress=%s, results=%s where id=%s and owner=%s", [str(int(time.time())),data['title'],data['thumbnail'],data['tags'],data['category'],data['description'],data['location'],data['videos'],data['open'],data['needs'],data['team'],data['content'],data['progress'],data['results'],data['id'],data['owner']])
		return "{'ok': True, 'title': " + data['title'] + "}"
	else:
		return "{'ok': False, 'error': 'invalid api key or token'}"

# 用户关注创意
# 需要进行api key和token验证
@app.route('/api/idea/follow', methods=['POST'])
def api_idea_follow():
	data = json.loads(request.data)
	if validate(data['username'], data['apiKey'], data['token']):
		target = data['target']
		username = data['username']
		activityType = 2
		timestamp = int(time.time())
		cursor.execute("insert into activity(username, target, type, timestamp) values(%s, %s, %s, %s)", [username, target, activityType, timestamp])
		cursor.execute("select followIdeas from user where username = %s", [username])
		followIdeas = cursor.fetchone()['followIdeas']
		followIdeas = followIdeas + ',' + str(target)
		followIdeas = followIdeas.lstrip(',')
		cursor.execute("update user set followIdeas = %s where username = %s", [followIdeas, username])
		return '{"ok": True, "msg": "user follow idea"}'
	else:
		return "{'ok': False, 'error': 'invalid api key or token'}"

# 用户取消关注创意
# 需要进行api key和token验证
@app.route('/api/idea/unfollow', methods=['POST'])
def api_idea_unfollow():
	data = json.loads(request.data)
	if validate(data['username'], data['apiKey'], data['token']):
		target = data['target']
		username = data['username']
		activityType = 3
		timestamp = int(time.time())
		cursor.execute("insert into activity(username, target, type, timestamp) values(%s, %s, %s, %s)", [username, target, activityType, timestamp])
		cursor.execute("select followIdeas from user where username = %s", [username])
		followIdeas = cursor.fetchone()['followIdeas'].split(',')
		temp = ''
		for item in followIdeas:
			if not item == str(target):
				temp = temp + item + ','
		cursor.execute("update user set followIdeas = %s where username = %s", [temp[:-1], username])
		return '{"ok": True, "msg": "user unfollow idea"}'
	else:
		return "{'ok': False, 'error': 'invalid api key or token'}"

# 用户评论创意
# 需要进行api key和token验证
@app.route('/api/idea/comment', methods=['POST'])
def api_idea_comment():
	data = json.loads(request.data)
	if validate(data['username'], data['apiKey'], data['token']):
		target = data['target']
		activityType = 9
		timestamp = int(time.time())
		cursor.execute("insert into activity(username, target, type, timestamp) values(%s, %s, %s, %s)", [data['username'], target, activityType, timestamp])
		cursor.execute("insert into comment(ideaId,username,content,timestamp) values(%s,%s,%s,%s)", [target,data['username'],data['content'],timestamp])
		return '{"ok": True, "msg": "user comment idea"}'
	else:
		return "{'ok': False, 'error': 'invalid api key or token'}"

# 用户申请加入团队
# 需要进行api key和token验证
@app.route('/api/idea/join', methods=['POST'])
def api_idea_join():
	data = json.loads(request.data)
	if validate(data['username'], data['apiKey'], data['token']):
		tousername = data['owner']
		fromusername = data['username']
		ideaId = data['ideaId']
		cursor.execute("insert into notice(fromusername,tousername,content,timestamp) values(%s,%s,%s,%s)", [fromusername,tousername,"我想加入你的创意" + str(ideaId),int(time.time())])
		return '{"ok": True, "msg": "user apply for idea"}'
	else:
		return "{'ok': False, 'error': 'invalid api key or token'}"

# 同意加入团队申请

# 用户离开团队

# 用户点赞创意

# 用户鄙视创意

# 获取热门创意

# 搜索创意

'''
	web页面路由
'''

# 主页，展示最新热门创意
@app.route('/')
def index():
	if not session.get('username') == None:
		return render_template('index.html', login=True, username=session['username'])
	else:
		return render_template('index.html', login=False)

# 登陆
@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'GET':
		if not session.get('username') == None:
			return redirect('/')
		else:
			return render_template('login.html', error=error)
	elif request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if cursor.execute("select id from user where username=%s or email=%s", [username,username]) == 0:
			error = u"用户名或邮箱不存在"
			return render_template('login.html', error=error)
		elif cursor.execute("select id from user where username=%s and password=%s", [username,unicode(md5(password).hexdigest().upper())]) + cursor.execute("select id from user where email=%s and password=%s", [username,unicode(md5(password).hexdigest().upper())]) == 0:
			error = u"用户密码错误"
			return render_template('login.html', error=error)
		else:
			token = genKey()
			TTL = 100
			cursor.execute("update user set token = %s, lastActive = %s, TTL = %s where username = %s", [token, str(int(time.time())), TTL, username])
			cursor.execute("update user set token = %s, lastActive = %s, TTL = %s where email = %s", [token, str(int(time.time())), TTL, username])
			cursor.execute("select username from user where username=%s or email=%s", [username,username])
			session['username'] = cursor.fetchone()['username']
			return redirect('/')

# 注销
@app.route('/logout')
def logout():
	if not session.get('username') == None:
		session.pop('username',None)
		return redirect('/login')
	else:
		return redirect('/login') 

# 注册
@app.route('/register', methods=['GET','POST'])
def register():
	if request.method == 'GET':
		if not session.get('username') == None:
			return redirect('/')
		else:
			return render_template('register.html')
	elif request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if cursor.execute("select id from user where username=%s or email=%s", [username,username]) == 0:
			error = u"用户名或邮箱不存在"
			return render_template('login.html', error=error)
		elif cursor.execute("select id from user where username=%s and password=%s", [username,unicode(md5(password).hexdigest().upper())]) + cursor.execute("select id from user where email=%s and password=%s", [username,unicode(md5(password).hexdigest().upper())]) == 0:
			error = u"用户密码错误"
			return render_template('login.html', error=error)
		else:
			token = genKey()
			TTL = 100
			cursor.execute("update user set token = %s, lastActive = %s, TTL = %s where username = %s", [token, str(int(time.time())), TTL, username])
			cursor.execute("update user set token = %s, lastActive = %s, TTL = %s where email = %s", [token, str(int(time.time())), TTL, username])
			cursor.execute("select username from user where username=%s or email=%s", [username,username])
			session['username'] = cursor.fetchone()['username']
			return redirect('/')

if __name__ == '__main__':
	app.run()