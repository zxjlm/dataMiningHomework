# -*- coding: utf-8 -*-
__author__ = 'xiejdm'

from App import db


class Diagnosis(db.Model):
    __tablename__ = 'diagnosis'
    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(64))
    prescription = db.Column(db.String(500))
    sta_prescription = db.Column(db.String(500))

    def text(self):
        return "%s %s" % (self.province, self.id)

    def __repr__(self):
        return '<Diagnosis %r %r>' % (self.id, self.province, self.prescription, self.sta_prescription)


class HerbInfo(db.Model):
    __tablename__ = 'herb_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    process_name = db.Column(db.String(500))
    standard_name = db.Column(db.String(500))
    xing = db.Column(db.String(500))
    wei = db.Column(db.String(500))
    guijing = db.Column(db.String(500))
    remark = db.Column(db.String(500))

    def __repr__(self):
        return '<HerbInfo %r %r>' % (self.standard_name, self.xing)

