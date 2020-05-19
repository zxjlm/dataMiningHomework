# -*- coding: utf-8 -*-
__author__ = 'xiejdm'

from secure import sql_url

UPLOAD_FOLDER = '/home/xiejdm/PycharmProjects/data_analysis/App/uploads/'
ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx', 'tsv', 'csvz', 'tsvz'])

XING_LIST = ['寒', '温', '凉', '热', '平', '湿']
WEI_LIST = ['酸', '苦', '甘', '辛', '咸', '淡']
GUIJING_LIST = ['心', '肝', '脾', '肺', '肾', '胃', '大肠', '小肠', '膀胱', '胆', '心包', '三焦']

SECRET_KEY = '1111111111111111'
DEBUG = True
# SQLALCHEMY
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = sql_url
# 显示SQL语句
SQLALCHEMY_ECHO = False

# 设置每次请求结束后会自动提交数据库的改动
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
# SQLALCHEMY_TRACK_MODIFICATIONS = True
