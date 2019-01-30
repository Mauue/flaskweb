from flask import  render_template, redirect, request, flash, url_for, g, session
from . import blog
from ..auth.views import login_required
from app.db import get_db
import pymysql
import time
import math,bleach
from markdown import markdown


@blog.route('/')
def index():
    return render_template('blog/index.html')