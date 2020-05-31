# encoding:utf-8
from extends import db


class ProductCatagory(db.Model):
    self_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, nullable=False)
    type_name = db.Column(db.String(20), nullable=False)
    keywords = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)
    product_sort = db.Column(db.Integer, nullable=True)
    visable = db.Column(db.Integer, nullable=False, default=1)
    dirPath = db.Column(db.String(80), nullable=False)