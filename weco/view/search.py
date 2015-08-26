# coding:utf-8

from flask import *
from weco import app
from weco import cursor
import time
import math

# 搜索创意
@app.route('/search')
def search():
	recent = None
	hot = None

	if not session.get('username') == None:
		# 获取当前用户的最近搜索记录
		cursor.execute("select * from search where username=%s and keyword!='' group by keyword,target order by timestamp desc limit 10",[session.get('username')])
		recent = cursor.fetchall()
	
	# 获取热门搜索记录
	cursor.execute("select keyword, target, count(*) as count from search where timestamp > %s and keyword!='' group by keyword,target order by count(*) desc limit 10",[int(time.time())-3600*24*7])
	hot = cursor.fetchall();

	# 获取各个类别的创意数量
	cursor.execute("select count(id) as count, category from idea where published=1 and locked=0 group by category")
	categoryStat = cursor.fetchall()
	temp = {}
	for item in categoryStat:
		temp[item['category']] = item['count']
	categoryStat = temp
	return render_template('search/search.html',recent=recent,hot=hot,categoryStat=categoryStat)

# 关键词搜索
@app.route('/search/keyword')
def search_keyword():
	target = request.args.get('target')
	keyword = request.args.get('keyword')
	key = keyword
	pageId = request.args.get('pageId')
	numPerPage = 10
	pageId = int(pageId)

	# 记录本次搜索
	keyword = keyword.split(' ')
	if session.get('username') == None:
		username = ''
	else:
		username = session.get('username')

	# 存储搜索结果
	result = []
	if target == 'idea':
		# 搜索的是创意
		for item in keyword:
			cursor.execute("insert into search(username,target,keyword,timestamp) values(%s,%s,%s,%s)",[username,target,item,str(int(time.time()))])
			cursor.execute("select * from idea where published=1 and locked=0 and (title like '%%%s%%' or tags like '%%%s%%' or category like '%%%s%%')" % (item,item,item))
			ideas = cursor.fetchall()
			for i in ideas:
				temp = int(time.time()) - int(i['timestamp'])
				if temp < 60:
					temp = str(temp) + 's'
				elif temp < 3600:
					temp = str(temp/60) + 'm'
				elif temp < 3600 * 24:
					temp = str(temp/3600) + 'h'
				else:
					temp = str(temp/(3600*24)) + 'd'
				i['timestamp'] = temp
				result.append(i)
		result = sorted(result, key=lambda x:(x['praise'], x['timestamp']), reverse=True)
	elif target == 'user': 
		# 搜索的是用户
		for item in keyword:
			cursor.execute("insert into search(username,target,keyword,timestamp) values(%s,%s,%s,%s)",[username,target,item,str(int(time.time()))])
			cursor.execute("select username,nickname,portrait,tags,description,fans,lastActive from user where username!='None' and (nickname like '%%%s%%' or tags like '%%%s%%' or description like '%%%s%%')" % (item,item,item))
			users = cursor.fetchall()
			for i in users:
				if i['fans'] == '':
					i['fans'] = 0
				else:
					i['fans'] = len(i['fans'].split(','))
				result.append(i)
		result = sorted(result, key=lambda x:(x['lastActive']), reverse=True)

	# 计算分页信息，截取结果
	count = len(result)
	result = result[pageId*numPerPage:pageId*numPerPage+numPerPage]
	start = int(pageId) - 3
	end = int(pageId) + 3
	total = int(math.ceil(float(count) / numPerPage)) - 1
	if start < 0:
		start = 0
	if end > total:
		end = total
	pages = []
	for i in xrange(start, end + 1):
		pages.append(i)

	# 关键词搜索无返回结果时查看当前热门搜索
	cursor.execute("select keyword, target, count(*) as count from search where timestamp > %s and keyword!='' group by keyword,target order by count(*) desc limit 10",[int(time.time())-3600*24*7])
	hot = cursor.fetchall();

	return render_template('search/search_keyword.html', target=target, keyword=key, count=count, start=start, end=end, current=int(pageId), pages=pages, total=total, result=result, hot=hot)

# 根据分类返回创意
@app.route('/search/category')
def search_category():
	category = request.args.get('category')
	pageId = request.args.get('pageId')
	numPerPage = 10

	# 计算该分类的创意数量
	cursor.execute('select count(*) as count from idea where category=%s and published=1 and locked=0',[category])
	count = cursor.fetchone()['count']

	# 获取该分类的创意并分页
	cursor.execute('select * from idea where category=%s and published=1 and locked=0 order by praise desc, timestamp desc limit %s,%s',[category,int(pageId)*numPerPage,numPerPage])
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

	# 计算分页信息
	start = int(pageId) - 3
	end = int(pageId) + 3
	total = int(math.ceil(float(count) / numPerPage)) - 1
	if start < 0:
		start = 0
	if end > total:
		end = total
	pages = []
	for i in xrange(start, end + 1):
		pages.append(i)

	return render_template('search/search_category.html', category=category, count=count, start=start, end=end, current=int(pageId), pages=pages, total=total, ideas=ideas)
