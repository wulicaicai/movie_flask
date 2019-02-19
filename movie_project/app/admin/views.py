#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: wulicaicai
# IDE PyCharm
import os
import uuid
import datetime
from . import admin
from flask import render_template, redirect, url_for, flash, session, request, abort
from app.admin.forms import LoginForm, TagForm, AdminForm, MovieForm, PreviewForm, PwdForm, AuthForm, \
    RoleForm  # 导入登陆表单类
from app.models import Admin, Tag, Movie, Preview, User, Comment, Moviecol, Oplog, Adminlog, Userlog, Auth, Role
from functools import wraps  # 装饰器
from app import db, app
from werkzeug.utils import secure_filename  # secure_filename　如果不添加secure_filename　无法获取中文文件名
from werkzeug.security import generate_password_hash


# 上下文应用处理器
# 上下文处理器的装饰器
@admin.context_processor
def tpl_extra():
    data = dict(
        online_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    return data


# 定义登录判断装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # session不存在时请求登录
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 权限控制判断装饰器
def admin_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin = Admin.query.join(
            Role
        ).filter(
            Role.id == Admin.role_id,
            Admin.id == session['admin_id']
        ).first()
        auths = admin.role.auths
        auths = list(map(lambda v: int(v), auths.split(",")))
        auth_list = Auth.query.all()
        urls = [v.url for v in auth_list for val in auths if val == v.id]
        rule = request.url_rule
        if str(rule) not in urls:
            abort(404)
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


# 管理系统主页面
@admin.route('/')
@admin_login_req
def index():
    return redirect(url_for('admin.movie_list',page=1))


# 管理页面登陆页面
@admin.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # 验证
        data = form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        print(admin.pwd)
        if not admin.check_pwd(data['pwd']):
            flash('密码错误或用户错误! ', 'err')
            return redirect(url_for('admin.login'))
        session['admin'] = data['account']
        session['admin_id'] = admin.id
        adminlogin = Adminlog(
            admin_id=admin.id,
            ip=request.remote_addr,
        )
        db.session.add(adminlogin)
        db.session.commit()
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html', form=form)


# 管理退出页面
@admin.route('/logout/')
@admin_login_req
def logout():
    session.pop('admin', None)
    session.pop('admin_id', None)
    return redirect(url_for('admin.login'))


# 管理员修改密码
@admin.route('/pwd/', methods=["GET", "POST"])
@admin_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=session['admin']).first()
        if not admin.check_pwd(data['old_pwd']):
            flash('旧密码不正确,请重新输入', 'err')
            return render_template('admin/pwd.html', form=form)
        else:
            admin.pwd = generate_password_hash(data['new_pwd'])
            db.session.add(admin)
            db.session.commit()
            flash('修改密码成功,请重新登陆', 'ok')
            oplog = Oplog(
                admin_id=session['admin_id'],
                ip=request.remote_addr,
                reason='%s修改密码' % session['admin']
            )
            db.session.add(oplog)
            db.session.commit()
            return redirect(url_for('admin.logout'))
    return render_template('admin/pwd.html', form=form)


# 添加标签处理
@admin.route('/tag/add/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data['name']).count()
        if tag == 1:
            flash('名称已经存在!', 'err')
            return redirect(url_for('admin.tag_add'))
        tag = Tag(
            name=data['name']
        )
        db.session.add(tag)
        db.session.commit()
        flash('添加标签成功!', 'ok')
        oplog = Oplog(
            admin_id=session['admin_id'],
            ip=request.remote_addr,
            reason='添加 %s 标签' % data['name']
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html', form=form)


# 编辑标签处理
@admin.route('/tag/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_conut = Tag.query.filter_by(name=data['name']).count()
        if tag.name != data['name'] and tag_conut == 1:
            flash('标签已经存在!', 'err')
            return redirect(url_for('admin.tag_edit', id=id))
        tag_name = tag.name
        tag.name = data['name']
        db.session.add(tag)
        db.session.commit()
        flash('修改标签成功!', 'ok')
        oplog = Oplog(
            admin_id=session['admin_id'],
            ip=request.remote_addr,
            reason='标签" %s "修改为" %s "' % (tag_name, data['name'])
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.tag_edit', id=id))
    return render_template('admin/tag_edit.html', form=form, tag=tag)


# 标签列表
@admin.route('/tag/list/<int:page>/', methods=["GET"])
@admin_login_req
@admin_auth
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)  # 按照时间查询
    return render_template('admin/tag_list.html', page_data=page_data)


# 标签删除
@admin.route('/tag/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def tag_del(id):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('删除标签成功!', 'ok')
    oplog = Oplog(
        admin_id=session['admin_id'],
        ip=request.remote_addr,
        reason='删除 %s 标签' % (tag.name)
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.tag_list', page=1))


# 添加电影
@admin.route('/movie/add/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):  # 创建文件夹
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        url = change_filename(file_url)  # 修改文件名
        logo = change_filename(file_logo)
        form.url.data.save(app.config['UP_DIR'] + url)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        movie = Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            playnum=0,
            commentnum=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            release_time=data['release_time'],
            length=data['length'],

        )
        db.session.add(movie)
        db.session.commit()
        flash('电影添加成功', 'ok')
        oplog = Oplog(
            admin_id=session['admin_id'],
            ip=request.remote_addr,
            reason='添加 %s 电影' % (data['title'])
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie_add.html', form=form)


# 电影列表
@admin.route('/movie/list/<int:page>/', methods=["GET"])
@admin_login_req
@admin_auth
def movie_list(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)  # 按照时间查询
    return render_template('admin/movie_list.html', page_data=page_data)


# 删除电影
@admin.route('/movie/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def movie_del(id):
    movie = Movie.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    flash('删除电影成功!', 'ok')
    oplog = Oplog(
        admin_id=session['admin_id'],
        ip=request.remote_addr,
        reason='删除 %s 电影' % (movie.title)
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.movie_list', page=1))


# 修改电影
@admin.route('/movie/edit/<int:id>/', methods=["GET", "POST"])
@admin_login_req
def movie_edit(id=None):
    form = MovieForm()
    form.url.validators = []
    form.logo.validators = []
    movie = Movie.query.get_or_404(int(id))
    if request.method == 'GET':
        # form.title.flags.required = False
        form.url.flags.required = False
        form.logo.flags.required = False
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star
    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(title=data['title']).count()
        if movie_count == 1 and movie.title != data['title']:
            flash('片名已经存在', 'err')
            return redirect(url_for('admin.movie_edit', id=movie.id))

        if not os.path.exists(app.config['UP_DIR']):  # 创建文件夹
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')

        if form.url.data != '':
            file_url = secure_filename(form.url.data.filename)
            movie.url = change_filename(file_url)  # 修改文件名
            form.url.data.save(app.config['UP_DIR'] + movie.url)

        if form.logo.data != '':
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + movie.logo)

        movie.star = data['star']
        movie.tag_id = data['tag_id']
        movie.info = data['info']
        movie.title = data['title']
        movie.area = data['area']
        movie.length = data['length']
        movie.release_time = data['release_time']
        db.session.add(movie)
        db.session.commit()
        flash('电影修改成功', 'ok')
        oplog = Oplog(
            admin_id=session['admin_id'],
            ip=request.remote_addr,
            reason='修改 %s 电影' % (movie.title)
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.movie_edit', id=movie.id))
    return render_template('admin/movie_edit.html', form=form, movie=movie)


# 编辑上映电影
@admin.route('/preview/add/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):  # 创建文件夹
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        logo = change_filename(file_logo)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        preview = Preview(
            title=data['title'],
            logo=logo,
        )
        db.session.add(preview)
        db.session.commit()
        flash('预告上传成功', 'ok')
        oplog = Oplog(
            admin_id=session['admin_id'],
            ip=request.remote_addr,
            reason='添加 %s 上映预告' % data['title']
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.preview_add'))
    return render_template('admin/preview_add.html', form=form)


# 上映预告列表
@admin.route('/preview/list/<int:page>/', methods=["GET"])
@admin_login_req
@admin_auth
def preview_list(page):
    if page is None:
        page = 1
    page_data = Preview.query.order_by(
        Preview.addtime.desc()
    ).paginate(page=page, per_page=10)  # 按照时间查询
    return render_template('admin/preview_list.html', page_data=page_data)


# 删除上映预告列表
@admin.route('/preview/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def preview_del(id=None):
    preview = Preview.query.get_or_404(int(id))
    db.session.delete(preview)
    db.session.commit()
    flash('删除预告成功!', 'ok')
    oplog = Oplog(
        admin_id=session['admin_id'],
        ip=request.remote_addr,
        reason='删除 %s 上映预告' % preview.title
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.preview_list', page=1))


# 编辑预告
@admin.route('/preview/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def preview_edit(id):
    form = PreviewForm()
    form.logo.validators = []
    preview = Preview.query.get_or_404(int(id))
    if request.method == "GET":
        form.title.data = preview.title
    if form.validate_on_submit():
        data = form.data

        if form.logo.data.filename != '':
            file_logo = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + preview.logo)

        preview.title = data['title']
        db.session.add(preview)
        db.session.commit()
        flash('修改预告成功', 'ok')
        oplog = Oplog(
            admin_id=session['admin_id'],
            ip=request.remote_addr,
            reason='修改 %s 上映预告' % data['title']
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.preview_edit', id=id))
    return render_template('admin/preview_edit.html', form=form, preview=preview)


# 会员列表
@admin.route('/user/list/<int:page>/', methods=["GET"])
@admin_login_req
@admin_auth
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.addtime.desc()
    ).paginate(page=page, per_page=10)  # 按照时间查询
    return render_template('admin/user_list.html', page_data=page_data)


# 查看会员
@admin.route('/user/view/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def user_view(id=None):
    user = User.query.get_or_404(int(id))
    return render_template('admin/user_view.html', user=user)


# 删除会员
@admin.route('/user/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def user_del(id=None):
    user = User.query.get_or_404(int(id))
    user_name = user.name
    db.session.delete(user)
    db.session.commit()
    flash('删除成功!', 'ok')
    oplog = Oplog(
        admin_id=session['admin_id'],
        ip=request.remote_addr,
        reason='删除 %s 用户' % user_name
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.user_list', page=1))


# 评论列表
@admin.route('/comment/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def comment_list(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)  # 按照时间查询
    return render_template('admin/comment_list.html', page_data=page_data)


# 删除评论
@admin.route('/comment/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def comment_del(id=None):
    comment = Comment.query.get_or_404(int(id))
    db.session.delete(comment)
    db.session.commit()
    flash('删除成功!', 'ok')
    comments = comment.user_id
    name = User.query.get_or_404(int(comments))
    oplog = Oplog(
        admin_id=session['admin_id'],
        ip=request.remote_addr,
        reason='删除 <%s> 用户评论的内容:< %s >' % (name.name, comment.content)
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.comment_list', page=1))


# 收藏列表
@admin.route('/moviecol/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def moviecol_list(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Moviecol.movie_id,
        User.id == Moviecol.user_id
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)  # 按照时间查询
    return render_template('admin/moviecol_list.html', page_data=page_data)


# 删除收藏
@admin.route('/moviecol/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def moviecol_del(id=None):
    moviecol = Moviecol.query.get_or_404(int(id))
    moviecol_user = moviecol.user_id
    username = User.query.get_or_404(int(moviecol_user))
    moviecol_movie = moviecol.movie_id
    moviename = Movie.query.get_or_404(int(moviecol_movie))
    db.session.delete(moviecol)
    db.session.commit()
    flash('删除成功!', 'ok')
    oplog = Oplog(
        admin_id=session['admin_id'],
        ip=request.remote_addr,
        reason='删除 <%s> 用户收藏的电影 <%s>' % (username.name, moviename.title)
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.moviecol_list', page=1))


# 操作日志列表
@admin.route('/oplog/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def oplog_list(page=None):
    if page is None:
        page = 1
    page_data = Oplog.query.join(
        Admin
    ).filter(
        Admin.id == Oplog.admin_id,
    ).order_by(
        Oplog.addtime.desc()
    ).paginate(page=page, per_page=10)  # 按照时间查询
    return render_template('admin/oplog_list.html', page_data=page_data)


# 管理员登录日志列表
@admin.route('/adminloginlog/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def adminloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Adminlog.query.join(
        Admin
    ).filter(
        Admin.id == Adminlog.admin_id,
    ).order_by(
        Adminlog.addtime.desc()
    ).paginate(page=page, per_page=10)  # 按照时间查询
    return render_template('admin/adminloginlog_list.html', page_data=page_data)


# 会员登录日志列表
@admin.route('/userloginlog/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def userloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.join(
        User
    ).filter(
        User.id == Userlog.user_id,
    ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=10)  # 按照时间查询
    return render_template('admin/userloginlog_list.html', page_data=page_data)


# 添加角色
@admin.route('/role/add/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        print(data)
        role = Role(
            name=data['name'],
            auths=','.join(map(lambda v: str(v), data['auths']))
        )
        db.session.add(role)
        db.session.commit()
        flash('添加角色成功', 'ok')
    return render_template('admin/role_add.html', form=form)


# 编辑角色
@admin.route('/role/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def role_edit(id=None):
    form = RoleForm()
    role = Role.query.get_or_404(id)
    if request.method == "GET":
        auths = role.auths
        form.auths.data = list(map(lambda v: int(v), auths.split(',')))
    if form.validate_on_submit():
        data = form.data
        role.name = data['name']
        role.auths = ','.join(map(lambda v: str(v), data['auths']))
        db.session.add(role)
        db.session.commit()
        flash('修改角色成功!', 'ok')
        oplog = Oplog(
            admin_id=session['admin_id'],
            ip=request.remote_addr,
            reason='修改" %s "权限' % (data['name'])
        )
        db.session.add(oplog)
        db.session.commit()
    return render_template('admin/role_edit.html', form=form, role=role)


# 角色列表
@admin.route('/role/list/<int:page>', methods=['GET'])
@admin_login_req
@admin_auth
def role_list(page):
    if page is None:
        page = 1
    page_data = Role.query.order_by(
        Role.addtime.desc()
    ).paginate(page=page, per_page=10)  # 按照时间查询
    return render_template('admin/role_list.html', page_data=page_data)


# 删除角色列表
@admin.route('/role/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def role_del(id):
    role = Role.query.filter_by(id=id).first_or_404()
    db.session.delete(role)
    db.session.commit()
    flash('删除角色成功!', 'ok')
    oplog = Oplog(
        admin_id=session['admin_id'],
        ip=request.remote_addr,
        reason='删除 %s 权限' % (role.name))
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.role_list', page=1))


# 添加权限
@admin.route('/auth/add/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(
            title=data["name"],
            url=data["url"],
        )
        db.session.add(auth)
        db.session.commit()
        flash("添加权限成功！", "ok")
        oplog = Oplog(
            admin_id=session['admin_id'],
            ip=request.remote_addr,
            reason='添加 %s 权限' % (data["name"]))
        db.session.add(oplog)
        db.session.commit()
    return render_template('admin/auth_add.html', form=form)


# 权限列表
@admin.route('/auth/list/<int:page>/', methods=["GET"])
@admin_login_req
@admin_auth
def auth_list(page=None):
    if page is None:
        page = 1
    page_data = Auth.query.order_by(
        Auth.addtime.desc()
    ).paginate(page=page, per_page=10)  # 按照时间查询
    return render_template('admin/auth_list.html', page_data=page_data)


# 删除权限列表
@admin.route('/auth/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def auth_del(id):
    auth = Auth.query.filter_by(id=id).first_or_404()
    db.session.delete(auth)
    db.session.commit()
    flash('删除权限成功!', 'ok')
    oplog = Oplog(
        admin_id=session['admin_id'],
        ip=request.remote_addr,
        reason='删除 %s 权限' % (auth.title)
    )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for('admin.auth_list', page=1))


# 编辑权限处理
@admin.route('/auth/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def auth_edit(id=None):
    form = AuthForm()
    auth = Auth.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        auth.url = data['url']
        auth.title = data['name']
        db.session.add(auth)
        db.session.commit()
        flash('修改权限成功!', 'ok')
        oplog = Oplog(
            admin_id=session['admin_id'],
            ip=request.remote_addr,
            reason='修改" %s "权限' % (data['name'])
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.auth_edit', id=id))
    return render_template('admin/auth_edit.html', form=form, auth=auth)


# 添加管理员
@admin.route('/admin/add/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def admin_add():
    form = AdminForm()
    from werkzeug.security import generate_password_hash
    if form.validate_on_submit():
        data = form.data
        admin = Admin(
            name=data["name"],
            pwd=generate_password_hash(data['pwd']),
            role_id=data['role_id'],
            is_super=1,
        )
        db.session.add(admin)
        db.session.commit()
        flash("添加管理员成功！", "ok")
        oplog = Oplog(
            admin_id=session['admin_id'],
            ip=request.remote_addr,
            reason='添加 %s 管理员' % (data["name"]))
        db.session.add(oplog)
        db.session.commit()
    return render_template('admin/admin_add.html', form=form)


# 管理员列表
@admin.route('/admin/list/<int:page>/', methods=["GET"])
@admin_login_req
@admin_auth
def admin_list(page=None):
    if page is None:
        page = 1
    page_data = Admin.query.join(Role).filter(
        Role.id == Admin.role_id
    ).order_by(
        Admin.addtime.desc()
    ).paginate(page=page, per_page=10)
    page_data1 = Admin.query.join(Role).filter(
        Role.id == Admin.role_id
    ).order_by(
        Admin.addtime.desc()
    ).count()
    # 按照时间查询
    print(page_data1)
    return render_template('admin/admin_list.html', page_data=page_data)


# 测试
@admin.route('/admin/hello/<int:id>/', methods=["GET"])
@admin_login_req
def hello(id=None):
    return render_template('admin/hello.html')
