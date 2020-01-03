
import random
import string
import hashlib
import requests

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import login as auth_login, authenticate

from base.models import UserProfile
from base.functions import get_menu_tree, create_user
from common.feed import AccountsFeed as af


def admin_login(request):
    """管理员登录页面"""
    if request.user.is_authenticated:
        redirect_to = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
        return HttpResponseRedirect(redirect_to)

    res = {
        'sso_name': settings.SSO_NAME
    }

    return render(request, 'base/admin_login.html', res)


def customer_login(request):
    """客户登录页面"""

    if request.user.is_authenticated:
        redirect_to = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
        return HttpResponseRedirect(redirect_to)

    return render(request, 'base/customer_login.html')


@login_required
def logout(request):
    """退出"""

    is_staff = False
    if request.user.is_staff:
        is_staff = True

    if 'fake_user' in request.session:
        del request.session['fake_user']
        if is_staff:
            return redirect(reverse('admin_login_page'))
        else:
            return redirect(reverse('customer_login_page'))

    auth_logout(request)
    if is_staff:
        return redirect(reverse('admin_login_page'))
    else:
        return redirect(reverse('customer_login_page'))


# @login_required
def base(request):
    """base
    0: 登录成功 //该状态码不返回
    1: 该账户不存在
    2: 密码错误
    3: 账户不能为空
    4：该账户已被锁定
    5：该账户需要重新登录（由于登陆已过期）
    6：密码不能为空
    11：该系统未在 SSO系统 注册
    12：无效的Token
    13：请求不合法
    21：服务器不可用，请稍后再试
    30：未知的错误状态
    """
    eoss = request.GET.get("eoss")

    if eoss:
        if eoss == 1:
            err_msg = af.USER_ERROR
        elif eoss == 2:
            err_msg = af.USER_ERROR
        elif eoss == 4:
            err_msg = af.USER_LOCKING
        else:
            err_msg = af.USER_ERROR

        res = {
            'msg': err_msg,
            'sso_name': settings.SSO_NAME
        }

        return render(request, 'base/admin_login.html', res)
    else:
        menus, perm_user = get_menu_tree(request.user)

        res = {
            'menus': menus,
            'perm_user': perm_user
        }

        return render(request, 'base/base.html', res)


@login_required
def reset_password_views(request):
    """重置密码"""
    return render(request, 'user/rest_password.html', {})


@login_required
def reset_password_views(request):
    """重置密码"""
    return render(request, 'user/rest_password.html', {})


@login_required
def product_prompt_views(request, menu_code):
    """产品提示页面"""
    res = {
        'menu_code': menu_code
    }

    return render(request, 'base/product_prompt_views.html', res)


@require_GET
def get_sso_token(request):
    """退出
    {"hasLogon":true,"type":1,"account":"xinkai.zhang@chinacache.com",
    "cdate":1558602246000,"adate":1558602246000,"err":0,"ec":0}
    {"hasLogon":false,"type":-1,"account":"",
    "cdate":null,"adate":null,"err":12,"ec":0}

    """

    backend_path = 'django.contrib.auth.backends.AllowAllUsersModelBackend'

    token = request.GET.get("ioss")

    if token:
        md5 = hashlib.md5()

        md5.update((settings.SSO_NAME + token + "CssoC").encode('utf-8'))

        url = (
            "https://sso.chinacache.com:443/queryByTokenId?"
            "clientName={}"
            "&tokenId={}"
            "&md5Hash={}"
        ).format(settings.SSO_NAME, token, md5.hexdigest())

        res = requests.get(url)
        has_login = res.json().get('hasLogon', False)

        user = None
        if has_login:
            username = res.json().get('account', '')
            user = UserProfile.objects.filter(username=username).first()
            if not user:
                identity = 'is_admin'
                # 管理员登录通过sso校验,系统生成随机密码不需要记录
                password = "".join(random.sample(
                    string.ascii_letters + string.digits, 10))
                group = Group.objects.filter(name='客服').first()
                user = create_user(username, password, group, identity)
        if user:
            user.backend = backend_path
            auth_login(request, user)

    return HttpResponseRedirect('/base/base/', {})


@login_required
def help_online(request):
    """帮助文档"""

    return render(request, 'base/11.pdf', {})
