# coding:utf-8

# 加载需要使用的包
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from flask import *
import MySQLdb
import MySQLdb.cursors

# import smtplib  
# from email.mime.text import MIMEText

import warnings
warnings.filterwarnings("ignore")

# 加载配置文件
from conf.configure import *

# 载入系统配置
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "1DA2DG3HYK9KU1T6WRSFSF2GCSG6GSDSYL9UL1Q2S3X4A1"

# 数据库连接
db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=DATABASE, port=PORT, charset=CHARSET, cursorclass = MySQLdb.cursors.DictCursor)
db.autocommit(True)
cursor = db.cursor()

# 加载其他模块代码
from weco.api import user
import weco.api.idea
import weco.view.auth
import weco.view.idea
import weco.view.user
import weco.view.search
import weco.view.notice