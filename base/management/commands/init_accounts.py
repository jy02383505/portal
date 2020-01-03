# -*- coding:utf-8 -*-

"""
初始化项目权限系统
"""
import os
import shutil

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from base.models import *


def init_group():
    """
    创建资源云平台初始化角色
        供应商: supplier
        管理员: admin
        客户: customer
    :return:
    """

    groups = Group.objects.all()
    groups.delete()

    for i in GroupProfile.GROUP_BASE:

        name = i[1]
        _id = i[0]

        group, is_new = Group.objects.get_or_create(id=_id, name=name)

        if is_new:
            group_profile, is_new = GroupProfile.objects.get_or_create(
                group=group)

            if not is_new:
                continue

            group_profile.save()


def init_service():
    """初始化服务"""

    providers = Provider.objects.all()
    providers.delete()
    products = Product.objects.all()
    products.delete()
    strategy = Strategy.objects.all()
    strategy.delete()
    services = Service.objects.all()
    services.delete()

    base_provider = [
        {'name': '蓝汛',
         'code': 'CC',
         },
        {'name': '腾讯',
         'code': 'TENCENT',
         },
        {'name': '青松',
         'code': 'QINGSONG',
         },
    ]

    for i in base_provider:

        name = i['name']
        code = i['code']

        provider, is_new = Provider.objects.get_or_create(name=name, code=code)

        if is_new:
            print('provider', provider.name, 'has be save')

    base_product = [
        {
            'name': 'CDN',
            'code': 'CDN',
        },

        {
            'name': '安全服务',
            'code': 'SECURITY',
        },

    ]

    for i in base_product:

        name = i['name']
        code = i['code']

        product, is_new = Product.objects.get_or_create(name=name, code=code)

        if is_new:
            print('provider', product.name, 'has be save')

    base_service = [
        {'name': '内容分发',
         'code': 'CDN',
         },
        {'name': 'waf',
         'code': 'WAF',
         },
        {'name': 'CC',
         'code': 'CC',
         },
    ]

    for i in base_service:

        name = i['name']
        code = i['code']

        service, is_new = Service.objects.get_or_create(name=name, code=code)

        if is_new:
            print('service', service.name, 'has be save')

    base_strategy = [
        {
            'provider': 'CC',
            'product': 'CDN',
            'service': 'CDN',
        },
        {
            'provider': 'TENCENT',
            'product': 'CDN',
            'service': 'CDN',
        },
        {
            'provider': 'QINGSONG',
            'product': 'SECURITY',
            'service': 'WAF',
        },
        {
            'provider': 'CC',
            'product': 'SECURITY',
            'service': 'CC',
        },
    ]

    for i in base_strategy:

        provider = i['provider']
        product = i['product']
        service = i['service']

        provider = Provider.objects.get(code=provider)
        product = Product.objects.get(code=product)
        service = Service.objects.get(code=service)

        strategy, is_new = Strategy.objects.get_or_create(
            provider=provider, product=product, service=service)

        if is_new:
            print(strategy, 'has be save')


def init_permissions():
    """初始化权限"""

    # perms = Perm.objects.all()
    # perms.delete()

    base_perm = [
        {
            'name': '用户账号管理',
            'code': 'all_parent_menu',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端父账号管理一级菜单',
            'parent_code': '',
            'level': 1,
            'order': 1,
            'is_menu': True,
            'url': '-',
            'type_name': '用户账号管理',
            'en_code': 'User Management'
        },

        {
            'name': '管理员账号管理',
            'code': 'all_admin_menu',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端管理员账号管理一级菜单',
            'parent_code': '',
            'level': 1,
            'order': 2,
            'is_menu': True,
            'url': '-',
            'type_name': '管理员账号管理',
            'en_code': 'Administrator Management'
        },

        {
            'name': 'CDN业务管理',
            'code': 'admin_cdn_menu',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端管理员CDN管理一级菜单',
            'parent_code': '',
            'level': 1,
            'order': 3,
            'is_menu': True,
            'url': '-',
            'type_name': 'CDN业务管理',
            'en_code': 'CDN Service Management'
        },
        {
            'name': '安全CDN',
            'code': 'admin_security_menu',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端管理员安全管理一级菜单',
            'parent_code': '',
            'level': 1,
            'order': 4,
            'is_menu': True,
            'url': '-',
            'type_name': '安全业务管理',
            'en_code': 'Secure CDN service'
        },

        {
            'name': 'SSL证书',
            'code': 'admin_ssl_cert_menu',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端管理员SSL证书管理一级菜单',
            'parent_code': '',
            'level': 1,
            'order': 5,
            'is_menu': True,
            'url': '-',
            'type_name': 'SSL证书管理',
            'en_code': 'SSL Certificate'
        },

        {
            'name': '用户账号列表',
            'code': 'all_parent_views',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端管理员查看父账号列表二级菜单',
            'parent_code': 'all_parent_menu',
            'level': 2,
            'order': 1,
            'is_menu': True,
            'url': '/base/admin_parent_list/page/',
            'en_code': 'User Account List',
        },

        {
            'name': '用户操作记录',
            'code': 'all_parent_opt_log_views',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端管理员查看父账号操作记录二级菜单',
            'parent_code': 'all_parent_menu',
            'level': 2,
            'order': 2,
            'is_menu': True,
            'url': '/base/admin_parent_opt_log/page/',
            'en_code': 'User Operation Record'
        },

        {
            'name': 'CMS客户绑定',
            'code': 'bind_parent_CMS_views',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端绑定CMS客户账号与系统账号关系',
            'parent_code': 'all_parent_menu',
            'level': 2,
            'order': 3,
            'is_menu': True,
            'url': '/base/admin_bind_cms_parent/page/',
            'en_code': 'ChinaCache User Binding',
        },

        {
            'name': '管理员账户列表',
            'code': 'all_admin_views',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端管理员查看管理员账号列表二级菜单',
            'parent_code': 'all_admin_menu',
            'level': 2,
            'order': 1,
            'is_menu': True,
            'url': '/base/admin_admin_list/page/',
            'en_code': 'Administrator List',
        },

        {
            'name': '管理员操作记录',
            'code': 'all_admin_opt_log_views',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端管理员查看管理员操作记录二级菜单',
            'parent_code': 'all_admin_menu',
            'level': 2,
            'order': 2,
            'is_menu': True,
            'url': '/base/admin_admin_opt_log/page/',
            'en_code': 'Administrator Operation Record'
        },

        {
            'name': '角色管理',
            'code': 'group_manage',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端管理员角色管理录二级菜单',
            'parent_code': 'all_admin_menu',
            'level': 2,
            'order': 3,
            'is_menu': True,
            'url': '/base/admin_group_manage/page/',
            'en_code': 'Role Management'
        },

        {
            'name': '创建管理员',
            'code': 'admin_create',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端管理员创建管理员',
            'parent_code': 'all_admin_menu',
            'level': 3,
            'order': 1,
            'is_menu': False,
            'url': '-'
        },

        {
            'name': '创建角色',
            'code': 'group_create',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端管理员创建角色',
            'parent_code': 'all_admin_menu',
            'level': 3,
            'order': 1,
            'is_menu': False,
            'url': '-'
        },

        {
            'name': '创建父账号',
            'code': 'parent_create',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端管理员创建父账号',
            'parent_code': 'all_parent_menu',
            'level': 3,
            'order': 1,
            'is_menu': False,
            'url': '-'
        },

        {
            'name': 'CDN用户列表',
            'code': 'admin_cdn_user_list',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端cdn服务用户列表',
            'parent_code': 'admin_cdn_menu',
            'level': 2,
            'order': 1,
            'is_menu': True,
            'url': '/cdn/admin_cdn_user_list/page/',
            'type_name': 'CDN用户列表',
            'en_code': 'CDN User List'
        },

        {
            'name': '域名列表',
            'code': 'admin_cdn_domain_list',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端cdn服务查看域名列表',
            'parent_code': 'admin_cdn_menu',
            'level': 2,
            'order': 2,
            'is_menu': True,
            'url': '/cdn/admin_get_domain_list/page/',
            'type_name': '域名列表',
            'en_code': 'Domain List'
        },

        {
            'name': '统计',
            'code': 'admin_cdn_domain_statistical',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端cdn服务查看域名统计',
            'parent_code': 'admin_cdn_menu',
            'level': 2,
            'order': 3,
            'is_menu': True,
            'url': '/cdn/admin_statistics/page/',
            'type_name': '统计',
            'en_code': 'Statistics'
        },

        {
            'name': '刷新',
            'code': 'admin_cdn_domain_refresh',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端cdn服务查看域名刷新',
            'parent_code': 'admin_cdn_menu',
            'level': 2,
            'order': 4,
            'is_menu': True,
            'url': '/cdn/admin_refresh/page/',
            'type_name': '刷新',
            'en_code': 'Refresh'
        },

        {
            'name': '预加载',
            'code': 'admin_cdn_domain_preload',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端cdn服务查看域名预加载',
            'parent_code': 'admin_cdn_menu',
            'level': 2,
            'order': 5,
            'is_menu': True,
            'url': '/cdn/admin_preload/page/',
            'type_name': '预加载',
            'en_code': 'Preload'
        },

        {
            'name': '下载日志',
            'code': 'admin_cdn_domain_log',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端cdn服务查看域名日志',
            'parent_code': 'admin_cdn_menu',
            'level': 2,
            'order': 6,
            'is_menu': True,
            'url': '/cdn/admin_log_upload/page/',
            'type_name': '日志',
            'en_code': 'Log Download'
        },

        {
            'name': '概览',
            'code': 'admin_security_overview',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端安全cdn概览',
            'parent_code': 'admin_security_menu',
            'level': 2,
            'order': 1,
            'is_menu': False,
            'url': '/sec/admin_sec_overview/page/',
            'type_name': '概览',
            'en_code': 'Overview'
        },

        {
            'name': '安全CDN客户列表',
            'code': 'admin_security_user_list',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端安全cdn客户列表',
            'parent_code': 'admin_security_menu',
            'level': 2,
            'order': 2,
            'is_menu': True,
            'url': '/sec/admin_sec_user_list/page/',
            'type_name': '安全CDN客户列表',
            'en_code': 'Secure CDN customer list'
        },

        {
            'name': '安全CDN频道列表',
            'code': 'admin_security_domain_list',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端安全cdn频道列表',
            'parent_code': 'admin_security_menu',
            'level': 2,
            'order': 3,
            'is_menu': True,
            'url': '/sec/admin_sec_domain_list/page/',
            'type_name': '安全CDN频道列表',
            'en_code': 'Secure CDN domain list'
        },

        {
            'name': '管理员添加安全CDN频道',
            'code': 'admin_add_security_domain',
            'content_type': 'ADMIN_BASE',
            'desc': '管理员添加安全CDN频道',
            'parent_code': 'admin_security_menu',
            'level': 3,
            'order': 0,
            'is_menu': False,
            'url': '',
            'type_name': '添加安全频道',
            'en_code': ''
        },

        {
            'name': '管理员添加安全用户',
            'code': 'admin_add_security_user',
            'content_type': 'ADMIN_BASE',
            'desc': '管理员添加安全用户',
            'parent_code': 'admin_security_menu',
            'level': 3,
            'order': 0,
            'is_menu': False,
            'url': '',
            'type_name': '添加安全用户',
            'en_code': ''
        },

        {
            'name': '添加域名',
            'code': 'admin_cdn_create_domain',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端cdn服务添加域名',
            'parent_code': 'admin_cdn_menu',
            'level': 3,
            'order': 0,
            'is_menu': False,
            'url': '',
            'type_name': '添加域名',
            'en_code': ''
        },

        {
            'name': '证书管理',
            'code': 'admin_cdn_cert_manage',
            'content_type': 'ADMIN_BASE',
            'desc': '管理端证书管理页面',
            'parent_code': 'admin_ssl_cert_menu',
            'level': 2,
            'order': 0,
            'is_menu': True,
            'url': '/cert/admin_cert_ssl_manage/page/',
            'type_name': '证书管理',
            'en_code': 'Certificate Management'
        },

    ]

    for i in base_perm:

        check_p = Perm.objects.filter(code=i['code']).first()
        if not check_p:
            check_p = Perm(**i)
        else:
            check_p.name = i['name']
            check_p.content_type = i['content_type']
            check_p.desc = i['desc']
            check_p.parent_code = i['parent_code']
            check_p.level = i['level']
            check_p.order = i['order']
            check_p.is_menu = i['is_menu']
            check_p.url = i['url']
            check_p.type_name = i.get('type_name', '')
            check_p.en_code = i.get('en_code', '')

        check_p.save()

    client_menu = [
        {
            'name': 'CDN',
            'code': 'client_cdn_menu',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端cdn服务一级菜单',
            'parent_code': '',
            'level': 1,
            'order': 1,
            'is_menu': True,
            'url': '-',
            'type_name': 'CDN',
            'en_code': 'CDN'
        },

        {
            'name': '安全CDN服务',
            'code': 'client_security_menu',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端安全服务一级菜单',
            'parent_code': '',
            'level': 1,
            'order': 2,
            'is_menu': True,
            'url': '-',
            'type_name': '安全服务',
            'en_code': 'Secure CDN service',
        },

        {
            'name': 'SSL证书管理',
            'code': 'client_ssl_cert_menu',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端SSL证书管理一级菜单',
            'parent_code': '',
            'level': 1,
            'order': 3,
            'is_menu': True,
            'url': '-',
            'type_name': 'SSL证书管理',
            'en_code': 'SSL Certificate '
        },

        {
            'name': '访问管理',
            'code': 'access_manage_menu',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端访问控制一级菜单',
            'parent_code': '',
            'level': 1,
            'order': 4,
            'is_menu': True,
            'url': '-',
            'type_name': '访问管理',
            'en_code': 'Access Management'
        },

        {
            'name': '我的账号',
            'code': 'client_user_menu',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端账号信息一级菜单',
            'parent_code': '',
            'level': 1,
            'order': 5,
            'is_menu': True,
            'url': '-',
            'type_name': '我的账号',
            'en_code': 'My Account'
        },

        {
            'name': '用户管理',
            'code': 'child_manage',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端用户子账号管理二级菜单',
            'parent_code': 'access_manage_menu',
            'level': 2,
            'order': 1,
            'is_menu': True,
            'url': '/base/parent_child_list/page/',
            'en_code': 'User Management'
        },

        {
            'name': '策略管理',
            'code': 'child_strategy_manage',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端用户子账号策略管理二级菜单',
            'parent_code': 'access_manage_menu',
            'level': 2,
            'order': 2,
            'is_menu': True,
            'url': '/base/parent_get_perm_strategy/page/',
            'en_code': 'Policy management',
        },

        {
            'name': '创建子账号',
            'code': 'child_create',
            'content_type': 'CLIENT_BASE',
            'desc': '客户账号可以创建子账号',
            'parent_code': 'access_manage_menu',
            'level': 3,
            'order': 1,
            'is_menu': False,
            'url': '-',
            'en_code': ''
        },

        {
            'name': '创建权限策略',
            'code': 'perm_strategy_create',
            'content_type': 'CLIENT_BASE',
            'desc': '客户账号可以创建创建权限策略',
            'parent_code': 'access_manage_menu',
            'level': 3,
            'order': 1,
            'is_menu': False,
            'url': '-',
            'en_code': ''
        },

        {
            'name': '总览',
            'code': 'client_cdn_overview',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端cdn服务总览',
            'parent_code': 'client_cdn_menu',
            'level': 2,
            'order': 1,
            'is_menu': True,
            'url': '/cdn/client_cdn_overview/page/',
            'type_name': '总览',
            'en_code': 'Overview'
        },

        {
            'name': '域名列表',
            'code': 'client_cdn_domain_list',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端cdn服务查看域名列表',
            'parent_code': 'client_cdn_menu',
            'level': 2,
            'order': 2,
            'is_menu': True,
            'url': '/cdn/client_get_domain_list/page/',
            'type_name': '域名列表',
            'en_code': 'Domain List'
        },

        {
            'name': '统计',
            'code': 'client_cdn_domain_statistical',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端cdn服务查看统计',
            'parent_code': 'client_cdn_menu',
            'level': 2,
            'order': 3,
            'is_menu': True,
            'url': '/cdn/client_statistics/page/',
            'type_name': '统计',
            'en_code': 'Statistics'
        },


        {
            'name': '刷新',
            'code': 'client_cdn_domain_refresh',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端cdn服务查看域名刷新',
            'parent_code': 'client_cdn_menu',
            'level': 2,
            'order': 4,
            'is_menu': True,
            'url': '/cdn/client_refresh/page/',
            'type_name': '刷新',
            'en_code': 'Refresh'
        },

        {
            'name': '预加载',
            'code': 'client_cdn_domain_preload',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端cdn服务查看域名预加载',
            'parent_code': 'client_cdn_menu',
            'level': 2,
            'order': 5,
            'is_menu': True,
            'url': '/cdn/client_preload/page/',
            'type_name': '预加载',
            'en_code': 'Preload'
        },

        {
            'name': '日志下载',
            'code': 'client_cdn_domain_log',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端cdn服务查看域名日志',
            'parent_code': 'client_cdn_menu',
            'level': 2,
            'order': 6,
            'is_menu': True,
            'url': '/cdn/client_log_upload/page/',
            'type_name': '日志',
            'en_code': 'Log Download'
        },

        {
            'name': '安全CDN频道',
            'code': 'client_security_domain_list',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端安全查看频道列表',
            'parent_code': 'client_security_menu',
            'level': 2,
            'order': 1,
            'is_menu': True,
            'url': '/sec/parent_sec_domain_list/page/',
            'type_name': '域名列表',
            'en_code': 'Secure CDN channel',
        },

        {
            'name': '证书管理',
            'code': 'client_cdn_cert_manage',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端证书管理页面',
            'parent_code': 'client_ssl_cert_menu',
            'level': 2,
            'order': 0,
            'is_menu': True,
            'url': '/cert/client_cert_ssl_manage/page/',
            'type_name': '证书管理',
            'en_code': 'Certificate Management'
        },

        {
            'name': '添加域名',
            'code': 'client_cdn_create_domain',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端cdn服务添加域名',
            'parent_code': 'client_cdn_menu',
            'level': 3,
            'order': 0,
            'is_menu': False,
            'url': '',
            'type_name': '添加域名',
            'en_code': ''
        },

        {
            'name': '账号信息',
            'code': 'client_user_info',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端查看账号信息',
            'parent_code': 'client_user_menu',
            'level': 2,
            'order': 0,
            'is_menu': True,
            'url': '/base/parent_user_info/page/',
            'type_name': '我的账号',
            'en_code': 'Account Information'
        },
        {
            'name': '访问秘钥',
            'code': 'client_api_info',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端查看API信息',
            'parent_code': 'client_user_menu',
            'level': 2,
            'order': 1,
            'is_menu': True,
            'url': '/base/parent_secret_info/page/',
            'type_name': '我的账号',
            'en_code': 'Access secret key'
        },
        {
            'name': '修改密码',
            'code': 'client_change_password',
            'content_type': 'CLIENT_BASE',
            'desc': '客户端查看账号信息',
            'parent_code': 'client_user_menu',
            'level': 2,
            'order': 2,
            'is_menu': True,
            'url': '/base/parent_change_password/page/',
            'type_name': '我的账号',
            'en_code': 'Change Password'
        },

    ]

    for i in client_menu:

        check_p = Perm.objects.filter(code=i['code']).first()
        if not check_p:
            check_p = Perm(**i)
        else:
            check_p.name = i['name']
            check_p.content_type = i['content_type']
            check_p.desc = i['desc']
            check_p.parent_code = i['parent_code']
            check_p.level = i['level']
            check_p.order = i['order']
            check_p.is_menu = i['is_menu']
            check_p.url = i['url']
            check_p.type_name = i.get('type_name', '')
            check_p.en_code = i.get('en_code', '')

        check_p.save()


def init_perm_group():
    """初始化组权限"""
    admin_group = Group.objects.get(name='管理员')
    client_group = Group.objects.get(name='客户')

    admin_perm = [
        'all_parent_menu', 'all_admin_menu', 'admin_cdn_menu',
        'admin_security_menu', 'all_parent_views', 'all_parent_opt_log_views',
        'all_admin_views', 'all_admin_opt_log_views', 'group_manage'

    ]

    for i in admin_perm:
        print(i)
        p = Perm.objects.get(code=i)
        pg, is_new = PermGroup.objects.get_or_create(group=admin_group)
        pg.perm.add(p)
        pg.save()


def init_perm_user():
    """初始化用户权限"""

    client_perm = [
        'access_manage', 'client_cdn_menu', 'client_security_menu',
        'child_manage', 'child_strategy_manage'
    ]
    user = UserProfile.objects.get(username='test')

    for i in client_perm:
        print(i)
        p = Perm.objects.get(code=i)
        pg = PermUser(perm=p, user=user)
        pg.save()


def init_admins():
    """初始化多个管理员"""

    # base_user_list = ['admin1', 'admin2', 'admin3', 'admin4', 'admin5']
    # base_email = 'xx@xx.xx'
    # password = ''

    admin_group = Group.objects.get(name='客户')

    user = UserProfile.objects.get(username='test')
    user.save()
    admin_group.user_set.add(user)
    admin_group.save()


class Command(BaseCommand):

    def handle(self, *args, **options):
        # excel_dir = os.path.join(settings.BASE_DIR, 'excel')
        # shutil.rmtree(excel_dir)
        # os.makedirs(excel_dir)

        # init_group()
        # init_service()
        init_permissions()

        # init_permissions()
