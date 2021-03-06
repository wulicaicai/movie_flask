#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: wulicaicai
# IDE PyCharm

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, \
    SelectMultipleField  # 多选
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Admin, Tag, Auth, Role

tags = Tag.query.all()
auths_list = Auth.query.all()
role_list = Role.query.all()


# 管理员登陆
class LoginForm(FlaskForm):
    '''
    管理员登陆表单
    '''
    account = StringField(
        label='账号',
        validators=[DataRequired('请输入账号')

                    ],  # 验证
        description="账号",
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入账号！',
            # 'required': 'required',  # 这项必须填写
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码!')
        ],
        description='密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入密码！',
            # 'required': 'required',  # 这项必须填写
        }
    )
    submit = SubmitField(
        '登陆',
        render_kw={
            'class': 'btn btn-primary btn-block btn-flat',
        }
    )

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError('账号不存在!')


# 标签
class TagForm(FlaskForm):
    name = StringField(
        label='名称',
        validators=[
            DataRequired('请输入标签!')
        ],
        description='标签',
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！",
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            'class': 'btn btn-primary',
        }
    )


# 电影表单
class MovieForm(FlaskForm):
    """电影表单"""
    title = StringField(
        label="片名",
        validators=[
            DataRequired("请输入片名！")
        ],
        description="片名",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "autofocus": "",
            "placeholder": "请输入片名！"
        }
    )
    url = FileField(
        label="文件",
        validators=[
            DataRequired("请上传文件！")
        ],
        description="文件",
        render_kw={
            "id": "input_url"
        }
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介！")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": 10,
            "id": "input_info"
        }
    )
    logo = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面！")
        ],
        description="封面",
        render_kw={
            "id": "input_logo"
        }
    )
    star = SelectField(
        label="星级",
        validators=[
            DataRequired("请选择星级！")
        ],
        coerce=int,
        choices=[(0, "未选择"), (1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        description="星级",
        render_kw={
            "class": "form-control",
            "id": "input_star"
        }
    )
    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择标签！")
        ],
        coerce=int,
        choices=[(0, "未选择")] + [(v.id, v.name) for v in Tag.query.all()],
        description="标签",
        render_kw={
            "class": "form-control",
            "id": "input_tag_id"
        }
    )
    area = StringField(
        label="地区",
        validators=[
            DataRequired("请输入地区！")
        ],
        description="地区",
        render_kw={
            "class": "form-control",
            "id": "input_area",
            "placeholder": "请输入地区！"
        }
    )
    length = StringField(
        label="片长",
        validators=[
            DataRequired("请输入片长！")
        ],
        description="片长",
        render_kw={
            "class": "form-control",
            "id": "input_length",
            "placeholder": "请输入片长！"
        }
    )
    release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("请选择上映时间！")
        ],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "id": "input_release_time",
            "placeholder": "请选择上映时间！"
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 预告
class PreviewForm(FlaskForm):
    title = StringField(
        label="预告标题",
        validators=[
            DataRequired("请输入预告标题！")
        ],
        description="预告标题",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "autofocus": "",
            "placeholder": "请输入预告标题！"
        }

    )
    logo = FileField(
        label="预告标题",
        validators=[
            DataRequired("请上传预告封面！")
        ],
        description="预告标题",
        render_kw={
            "id": "input_url"
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 　密码
class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label='旧密码',
        validators=[
            DataRequired('请输入旧密码! ')
        ],
        description='旧密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入旧密码',

        }
    )
    new_pwd = PasswordField(
        label='新密码',
        validators=[
            DataRequired('请输入新密码! ')
        ],
        description='新密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入新密码',

        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            "class": "btn btn-primary"
        }
    )
    #
    # def validata_old_pwd(self, field):
    #     from flask import session
    #     pwd = field.data
    #     name = session['admin']
    #     admin = Admin.query.filter_by(
    #         name=name
    #     ).first()
    #     if not admin.check_pwd(pwd):
    #         raise ValidationError('旧密码错误!')  #imoocmovie


# 权限
class AuthForm(FlaskForm):
    name = StringField(
        label='权限名称',
        validators=[
            DataRequired('请输入权限名称!')
        ],
        description='权限名称',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限名称！",
        }
    )
    url = StringField(
        label='权限地址',
        validators=[
            DataRequired('请输入权限地址!')
        ],
        description='权限地址',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限地址！",
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-primary',
        }
    )


# 角色
class RoleForm(FlaskForm):
    name = StringField(
        label='角色名称',
        validators=[
            DataRequired('请输入角色名称!')
        ],
        description='角色名称',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入角色名称！",
        }
    )
    auths = SelectMultipleField(
        label='权限列表',
        validators=[
            DataRequired('请选择权限!')
        ],
        coerce=int,
        choices=[(v.id, v.title) for v in auths_list],
        description='权限名称',
        render_kw={
            "class": "form-control",

        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-primary',
        }
    )


class AdminForm(FlaskForm):
    name = StringField(
        label='管理员名称',
        validators=[
            DataRequired('请输入管理员名称')

        ],  # 验证
        description="管理员名称",
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入管理员名称！',
        }
    )
    pwd = PasswordField(
        label='管理员密码',
        validators=[
            DataRequired('请输入管理员密码!')
        ],
        description='管理员密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入管理员密码！',
        }
    )
    repwd = PasswordField(
        label='管理员重复密码',
        validators=[
            DataRequired('请输入管理员重复密码!'),
            EqualTo('pwd',message='两次密码不一致!')
        ],
        description='管理员重复密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入管理员重复密码！',
        }
    )
    role_id = SelectField(
        label='所属角色',
        coerce=int,
        choices=[(v.id, v.name) for v in role_list],
        render_kw={
            'class': 'form-control',
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-primary',
        }
    )
