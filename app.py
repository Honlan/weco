# coding:utf-8

'''
	@ weco共创社区开源项目
	@ flask + jinja + angularjs
	@ author by Honlan
	@ last updated 2015-07-28 
'''

from flask import *
from configure_weco import *

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
	app.run()