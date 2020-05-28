#encoding:utf-8
from sqlobject import connectionForURI, sqlhub
USERNAME = 'yangjm'
PASSWORD = 'yjm1062'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'defaultDB'
DB_URI = f'mysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8'
connection = connectionForURI(DB_URI)
sqlhub.processConnection = connection