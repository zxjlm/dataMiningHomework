#导入依赖
from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
#创建一个服务
app = Flask(__name__)

#配置app属性
# 设置连接数据库的URL
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://xiejdm:xuexi@127.0.0.1:3306/movie'

# 设置每次请求结束后会自动提交数据库的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 查询时显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = False

#response显示中文json,
app.config['JSON_AS_ASCII']=False

#生成一个sqlalchemy对象
db = SQLAlchemy(app)

#创建模型，在python中通过Role类映身roles表
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email=db.Column(db.String(64))

    def __repr__(self):
        return '<Role %r %r>' % (self.name, self.email)

#获取model名

#验证
#使用filter_by动态查询查询
filters={'name':'lisa'}
# filter_by用于查询简单的列名，不支持比较运算符
obj = Role.query.filter_by(**filters).all()
print(obj)
filters={'name':'lisa', 'email':'xxx'}
obj = Role.query.filter_by(**filters).all()
print(obj)

# filter比filter_by的功能更强大，支持比较运算符，支持or_、in_等语法
filters = {Role.name == 'lisa', Role.id <= 1}
obj = Role.query.filter(*filters).all()
print(obj)


obj = Role.query(Role.id, func.count('*').label('name')).filter(Role.name == 'lisa').group_by(Role.name).all()
print(obj)

