# encoding:utf-8
from flask import session
from config import ADMIN_USER_ID
from .models import Users


def GetUser():
    return Users.query.get(session.get(ADMIN_USER_ID)) if ADMIN_USER_ID in session else None


def BuildTree(data, pid=0, level=0):
    tree = []
    for row in data:
        if row['pid'] == pid:
            row['level'] = level
            child = BuildTree(data, row['sid'], level + 1)
            row['child'] = child if child else None
            tree.append(row)
    return tree


def BuildTable(data):
    html = ''
    for row in data:
        splice = '├'
        sid = row['sid']
        title = splice * row['level'] + row['tname']
        tr_td = """<option value={sid}>{title}</option>
        """
        if row['child']:
            html += tr_td.format(sid=sid, title=title)
            html += BuildTable(row['child'])
        else:
            html += tr_td.format(sid=sid, title=title)
    return html


def BuildCatList(data):
    for row in data:
        splice = '-- '
        sid = row['sid']
        psort = row['psort']
        title = splice * row['level'] + row['tname']
        description = row['description']
        dirpath = row['dirpath']
        tr_td = """<tr>
        <td align="left"> <a href="product.php?sid={sid}"></a>{title}</td>
        <td>{dirpath}</td>
        <td>{description}</td>
        <td align="center">{psort}</td>
        <td align="center"><a href="../EditProductCatagory/{sid}" >编辑</a>| <a href="../DelProductCatagory/{sid}" onClick="rec();return false">删除</a> </td>
      </tr>
        """
        if row['child']:
            html = tr_td.format(title=title, sid=sid, description=description, dirpath=dirpath, psort=psort)
            html += BuildCatList(row['child'])
        else:
            html = tr_td.format(title=title, sid=sid, description=description, dirpath=dirpath, psort=psort)
    return html
