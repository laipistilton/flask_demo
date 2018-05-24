# coding:utf8
from . import admin


@admin.route("/")
def index():
    return '<h1 style="color:red" >Admin</h1>'