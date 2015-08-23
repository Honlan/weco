# coding:utf-8

from flask import *
from weco import app
from weco import cursor

# 判断用户名是否存在
@app.route('/api/user/existName', methods=['POST'])
def api_user_exist_name():
	data = request.form
	count = cursor.execute("select username from user where username = %s", [data['username']])
	if count > 0:
		return json.dumps({"ok": True, "exist": True})
	else:
		return json.dumps({"ok": True, "exist": False})