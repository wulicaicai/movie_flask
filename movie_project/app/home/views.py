#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: wulicaicai
# IDE PyCharm

import datetime, json, os
from . import home

from flask import render_template, redirect, url_for, flash, session, request, Response
from app.home.forms import RegisForm, LoginForm, UserdetailForm, PwdForm, CommentForm
from app.models import Moviecol, User, Userlog, Preview, Tag, Movie, Comment
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import uuid
from functools import wraps
from app import db, app, rd


# 定义登录判断装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # session不存在时请求登录
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 修改文件名称
def change_filename(filename):
    suffix = filename[-3:]
    if suffix == 'peg':
        suffix = 'jpeg'
        # fileinfo = os.path.splitext(filename)
        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex + '.' + suffix
        return filename
    else:
        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex + '.' + suffix
        return filename


# 登陆页面
@home.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        if not user:
            flash('账户或错误', 'err')
        else:
            if not user.check_pwd(data['pwd']):
                flash('账户或错误', 'err')
                return redirect(url_for('home.login'))
            session['user'] = user.name
            session['user_id'] = user.id
            userlog = Userlog(
                user_id=user.id,
                ip=request.remote_addr,
            )
            db.session.add(userlog)
            db.session.commit()
            return redirect(url_for('home.user'))
    return render_template('home/login.html', form=form)


@home.route('/logout/')  # 退出登陆
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('home.login'))


# 会员注册页面
@home.route('/regist/', methods=['GET', 'POST'])
def regist():
    form = RegisForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            pwd=generate_password_hash(data['pwd']),
            uuid=uuid.uuid4().hex,
        )
        db.session.add(user)
        db.session.commit()
        flash('注册成功!', 'ok')
        return redirect(url_for("home.login"))
    return render_template('home/regist.html', form=form)


# 会员中心
@home.route('/user/', methods=['GET', 'POST'])
@user_login_req
def user():
    form = UserdetailForm()
    user = User.query.get(int(session['user_id']))
    form.face.validators = []
    if request.method == "GET":
        form.face.flags.required = False
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data

        if not os.path.exists(app.config['FC_DIR']):  # 创建文件夹
            os.makedirs(app.config['FC_DIR'])
            os.chmod(app.config['FC_DIR'], 'rw')

        if form.face.data != '':
            file_face = secure_filename(form.face.data.filename)  # 说是这行没有filename属性
            user.face = change_filename(file_face)
            form.face.data.save(app.config['FC_DIR'] + user.face)

        name_count = User.query.filter_by(name=data['name']).count()
        if data['name'] != user.name and name_count == 1:
            flash('昵称已存在', 'err')
            return redirect(url_for('home.user'))
        email_count = User.query.filter_by(email=data['email']).count()

        if data['email'] != user.email and email_count == 1:
            flash('邮箱已存在', 'err')
            return redirect(url_for('home.user'))
        phone_count = User.query.filter_by(phone=data['phone']).count()

        if data['phone'] != user.phone and phone_count == 1:
            flash('手机号码已存在', 'err')
            return redirect(url_for('home.user'))

        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']

        db.session.add(user)
        db.session.commit()
        flash('修改成功', 'ok')
        # return redirect(url_for('home.user'))
    return render_template('home/user.html', form=form, user=user)


# 修改密码
@home.route('/pwd/', methods=['GET', 'POST'])
@user_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session['user']).first()
        if not user.check_pwd(data['old_pwd']):
            flash('旧密码不正确,请重新输入', 'err')
            return render_template('home/pwd.html', form=form)
        else:
            user.pwd = generate_password_hash(data['new_pwd'])
            db.session.add(user)
            db.session.commit()
            flash('修改密码成功,请重新登陆', 'ok')
            return redirect(url_for('home.logout'))
    return render_template('home/pwd.html', form=form)


@home.route('/comments/<int:page>/')  # 评论页面
@user_login_req
def comments(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Comment.movie_id,
        User.id == session['user_id'],
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/comments.html', page_data=page_data)


# 会员登陆日志
@home.route('/loginlog/<int:page>/', methods=['GET'])
@user_login_req
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.filter_by(
        user_id=int(session['user_id'])
    ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/loginlog.html', page_data=page_data)


# 添加电影收藏
@home.route('/moviecol/add/', methods=["GET"])
@user_login_req
def moviecol_add():
    uid = request.args.get('uid', '')
    mid = request.args.get('mid', '')
    moviecol_ = Moviecol.query.filter_by(
        user_id=int(uid),
        movie_id=int(mid),
    ).count()
    if moviecol_ == 1:
        data = dict(ok=0)
    if moviecol_ == 0:
        moviecol_ = Moviecol(
            user_id=int(uid),
            movie_id=int(mid),
        )
        db.session.add(moviecol_)
        db.session.commit()
        data = dict(ok=1)
    import json
    return json.dumps(data)


# 电影收藏
@home.route('/moviecol/<int:page>/')
@user_login_req
def moviecol(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Moviecol.movie_id,
        User.id == session['user_id'],
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/moviecol.html', page_data=page_data)


@home.route('/<int:page>/', methods=['GET', 'POST'])  # 主页面
def index(page=None):
    tags = Tag.query.all()

    page_data = Movie.query

    # 标签
    tid = request.args.get('tid', 0)
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id=int(tid))

    # 星级
    star = request.args.get('star', 0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))

    # 时间
    time = request.args.get('time', 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.addtime.asc()
            )

    # 播放量
    pm = request.args.get('pm', 0)
    if int(pm) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(
                Movie.playnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.playnum.asc()
            )

    # 评论量
    cm = request.args.get('cm', 0)
    if int(cm) != 0:
        if int(cm) == 1:
            page_data = page_data.order_by(
                Movie.commentnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.commentnum.asc()
            )

    # 分页
    if page is None:
        page = 1
    page_data = page_data.paginate(page=int(page), per_page=10)
    p = dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm,
    )
    return render_template('home/index.html', tags=tags, p=p, page_data=page_data)


# 上映预告轮播图
@home.route('/animation/')
def animation():
    data = Preview.query.order_by(Preview.addtime.desc()).all()
    return render_template('home/animation.html', data=data)


# 搜索页面
@home.route('/search/<int:page>/')
def search(page=None):
    if page is None:
        page = 1
    key = request.args.get('key', '')
    movie_count = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')).count()
    page_data = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    page_data.key = key
    return render_template('home/search.html', key=key, movie_count=movie_count, page_data=page_data)


@home.route('/play/<int:id>/<int:page>/', methods=['GET', 'POST'])  # 搜索页面
def play(id=None, page=None):
    movie = Movie.query.join().filter(
        Tag.id == Movie.tag_id,
        Movie.id == int(id),
    ).first_or_404()
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == movie.id,
        User.id == Comment.user_id,
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    movie.playnum = movie.playnum + 1

    form = CommentForm()
    if 'user' in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data['content'],
            movie_id=movie.id,
            user_id=session['user_id']
        )
        db.session.add(comment)
        db.session.commit()
        movie.commentnum = movie.commentnum + 1
        flash('添加评论成功', 'ok')
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('home.play', id=movie.id, page=1))
    db.session.add(movie)
    db.session.commit()
    return render_template('home/play.html', movie=movie, form=form, page_data=page_data)


@home.route('/video/<int:id>/<int:page>/', methods=['GET', 'POST'])  # 搜索页面
def video(id=None, page=None):
    movie = Movie.query.join().filter(
        Tag.id == Movie.tag_id,
        Movie.id == int(id),
    ).first_or_404()
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == movie.id,
        User.id == Comment.user_id,
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    movie.playnum = movie.playnum + 1

    form = CommentForm()
    if 'user' in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data['content'],
            movie_id=movie.id,
            user_id=session['user_id']
        )
        db.session.add(comment)
        db.session.commit()
        movie.commentnum = movie.commentnum + 1
        flash('添加评论成功', 'ok')
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('home.video', id=movie.id, page=1))
    db.session.add(movie)
    db.session.commit()
    return render_template('home/video.html', movie=movie, form=form, page_data=page_data)


@home.route("/tm//v3/", methods=["GET", "POST"])
def tm():
    if request.method == "GET":
        # 获取弹幕消息队列
        id = request.args.get("id")
        global key
        key = "movie" + str(id)
        if rd.llen(key):
            msgs = rd.lrange(key, 0, 2999)
            res = {
                "code": 0,
                "data": [eval(v.decode("utf8")) for v in msgs]
            }
        else:
            res = {
                "code": 0,
                "data": []
            }
        resp = json.dumps(res)
    if request.method == "POST":
        # 添加弹幕
        data = json.loads(request.get_data())
        msg = [data["time"], data["type"], data["color"], data["author"], data["text"], request.remote_addr,
               datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex]
        res = {
            "code": 0,
            "data": msg
        }
        resp = json.dumps(res)
        rd.lpush(key, json.dumps(msg))
    return Response(resp, mimetype="application/json")
