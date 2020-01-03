# -*- coding:utf-8 -*-

from django.conf.urls import url
from base import views, ajax


admin_urls = [

    # 管理员查询父账号页面
    url(r'^admin_parent_list/page/$', views.admin_parent_list_views,
        name='admin_parent_list_views'),
    # 管理员父账号列表
    url(r'^ajax/admin_get_parent_list/$', ajax.admin_get_parent_list,
        name='admin_get_parent_list'),

    # 管理员创建父账号页面
    url(r'^create_parent_user/page/$', views.create_parent_user_views,
        name='create_parent_user_views'),
    # 创建父账号
    url(r'^ajax/create_parent_user/$', ajax.admin_create_parent_user,
        name='admin_create_parent_user'),

    # 创建管查看父账号详情
    url(r'^admin_parent_details/page/(?P<user_id>\S+)/$',
        views.admin_parent_details_views,
        name='admin_parent_details_views'),
    # 修改父账号
    url(r'^ajax/edit_parent_user/$', ajax.admin_edit_parent_user,
        name='admin_edit_parent_user'),

    # 给用户开通api
    url(r'^ajax/admin_open_parent_api/$', ajax.admin_open_parent_api,
        name='admin_open_parent_api'),

    # 管理员设置父账号api状态
    url(r'^ajax/admin_set_parent_api_status/$',
        ajax.admin_set_parent_api_status,
        name='admin_set_parent_api_status'),

    # 管理员删除父账号api使用
    url(r'^ajax/admin_set_parent_api_remove/$',
        ajax.admin_set_parent_api_remove,
        name='admin_set_parent_api_remove'),


    # 管理员查看父账号操作日志页面
    url(r'^admin_parent_opt_log/page/$', views.admin_parent_opt_log_views,
        name='admin_parent_opt_log_views'),
    # 管理员查看父账号操作日志列表
    url(r'^ajax/admin_get_parent_opt_log_list/$',
        ajax.admin_get_parent_opt_log_list,
        name='admin_get_parent_opt_log_list'),

    # 管理员绑定CMS账号
    url(r'^admin_bind_cms_parent/page/$', views.admin_bind_cms_parent_views,
        name='admin_bind_cms_parent_views'),

    # 管理员查看管理员账号页面
    url(r'^admin_admin_list/page/$', views.admin_admin_list_views,
        name='admin_admin_list_views'),
    # 管理员获取管理员账号列表
    url(r'^ajax/admin_get_admin_list/$', ajax.admin_get_admin_list,
        name='admin_get_admin_list'),

    # 管理员创建管理员页面
    url(r'^create_admin_user/page/$', views.create_admin_user_views,
        name='create_admin_user_views'),
    # 创建管理员账号
    url(r'^ajax/create_admin_user/$', ajax.create_admin_user,
        name='create_admin_user'),

    # 创建管查看管理员账号详情
    url(r'^admin_admin_details/page/(?P<user_id>\S+)/$',
        views.admin_admin_details_views,
        name='admin_admin_details_views'),
    # 修改管理员账号
    url(r'^ajax/edit_admin_user/$', ajax.edit_admin_user,
        name='edit_admin_user'),

    # 管理员查看管理员操作日志页面
    url(r'^admin_admin_opt_log/page/$', views.admin_admin_opt_log_views,
        name='admin_parent_opt_log_views'),
    # 管理员查看管理员操作日志列表
    url(r'^ajax/admin_get_admin_opt_log_list/$',
        ajax.admin_get_admin_opt_log_list,
        name='admin_get_admin_opt_log_list'),

    # 管理员角色管理页面
    url(r'^admin_group_manage/page/$', views.admin_group_manage_views,
        name='admin_group_manage_views'),
    # 管理员角色列表
    url(r'^ajax/admin_get_group_list/$', ajax.admin_get_group_list,
        name='admin_get_group_list'),

    # 管理员角色创建页面
    url(r'^admin_group_create/page/$', views.admin_group_create_views,
        name='admin_group_create_views'),
    # 管理员角色创建
    url(r'^ajax/admin_group_create/$', ajax.admin_group_create,
        name='admin_group_create'),
    # 管理员角色详情
    url(r'^admin_group_details_views/page/(?P<group_id>\S+)/$',
        views.admin_group_details_views,
        name='admin_group_details_views'),
    # 管理员修改角色
    url(r'^ajax/admin_group_edit/$', ajax.admin_group_edit,
        name='admin_group_edit'),
    # 管理员删除角色
    url(r'^ajax/admin_group_delete/$', ajax.admin_group_delete,
        name='admin_group_delete'),

    # 管理员获取绑定的cms账号
    url(r'^ajax/admin_get_parent_cms_list/$', ajax.admin_get_parent_cms_list,
        name='admin_get_parent_cms_list'),
    # 管理员cms客户详情页面
    url(r'^admin_cms_details/page/(?P<user_id>\S+)/$',
        views.admin_cms_details_views,
        name='admin_cms_details_views'),

    # 管理员绑定设置用户三方平台基础信息页面
    url(r'^admin_set_user_strategy/page/(?P<user_id>\S+)/$',
        views.admin_set_user_strategy_views,
        name='admin_set_user_strategy_views'),


    # 管理员创建cms客户绑定关系
    url(r'^admin_create_binding/page/$', views.admin_create_binding_views,
        name='admin_create_binding_views'),

    # 管理员创建cms客户绑定关系执行
    url(r'^ajax/admin_user_binding/$', ajax.admin_user_binding,
        name='admin_user_binding'),

    # 管理员解除cms客户绑定关系执行
    url(r'^ajax/admin_user_relieve_binding/$', ajax.admin_user_relieve_binding,
        name='admin_user_relieve_binding'),

    # 管理员绑定设置用户三方平台基础信息
    url(r'^ajax/admin_set_user_strategy_conf/$',
        ajax.admin_set_user_strategy_conf,
        name='admin_set_user_strategy_conf'),

    # 管理员同步合同信息
    url(r'^ajax/admin_sync_contract_info/$',
        ajax.admin_sync_contract_info,
        name='admin_sync_contract_info'),

    # 管理员绑定合同
    url(r'^ajax/admin_binding_user_contract/$',
        ajax.admin_binding_user_contract,
        name='admin_binding_user_contract'),

    # 管理员解除绑定合同
    url(r'^ajax/admin_user_relieve_contract/$',
        ajax.admin_user_relieve_contract,
        name='admin_user_relieve_contract'),

]


client_urls = [

    # 子账号重置密码
    url(r'^reset_password/page/$', views.reset_password_views,
        name='reset_password_views'),

    # 父账号管理子账号页面
    url(r'^parent_child_list/page/$', views.parent_child_list_views,
        name='parent_child_list_views'),
    # 父账号获取子账号列表
    url(r'^ajax/parent_get_child_list/$', ajax.parent_get_child_list,
        name='parent_get_child_list'),

    # 父账号获取子账号详情
    url(r'^parent_child_details_views/page/(?P<user_id>\S+)/$',
        views.parent_child_details_views,
        name='parent_child_details_views'),
    # 父账号修改子账号&权限修改
    url(r'^ajax/edit_child_user/$', ajax.edit_child_user,
        name='edit_child_user'),

    # 父账号创建子账号页面
    url(r'^create_child_user/page/$', views.create_child_user_views,
        name='create_child_user_views'),
    # 父账号创建子账号
    url(r'^ajax/create_child_user/$', ajax.create_child_user,
        name='create_child_user'),

    # 父账号策略管理页面
    url(r'^parent_get_perm_strategy/page/$',
        views.parent_get_perm_strategy_views,
        name='parent_perm_strategy_views'),
    # 父账号获取子策略列表
    url(r'^ajax/parent_get_perm_strategy_list/$',
        ajax.parent_get_perm_strategy_list,
        name='parent_get_perm_strategy_list'),

    # 父账号创建权限策略页面
    url(r'^parent_create_perm_strategy/page/$',
        views.parent_create_perm_strategy_views,
        name='parent_create_perm_strategy_views'),
    # 父账号创建权限策略接口
    url(r'^ajax/create_perm_strategy/$',
        ajax.create_perm_strategy,
        name='create_perm_strategy'),


    # 父账号查看策略详情
    url(r'^parent_perm_strategy_details/page/(?P<perm_strategy_id>\S+)/$',
        views.parent_perm_strategy_details_views,
        name='parent_perm_strategy_details_views'),
    # 父账号修改权限策略接口
    url(r'^ajax/edit_perm_strategy/$',
        ajax.edit_perm_strategy,
        name='edit_perm_strategy'),
    # 父账号删除权限策略接口
    url(r'^ajax/delete_perm_strategy/$',
        ajax.delete_perm_strategy,
        name='delete_perm_strategy'),

    # 用户账号信息
    url(r'^parent_user_info/page/$', views.parent_user_info_views,
        name='parent_user_info_views'),

    # 用户访问秘钥
    url(r'^parent_secret_info/page/$', views.parent_secret_info_views,
        name='parent_secret_info_views'),

    # 客户端开通api使用
    url(r'^ajax/client_open_parent_api/$', ajax.client_open_parent_api,
        name='client_open_parent_api'),

    # 客户端设置api使用状态
    url(r'^ajax/client_set_parent_api_status/$',
        ajax.client_set_parent_api_status,
        name='client_set_parent_api_status'),

    # 客户端删除api使用
    url(r'^ajax/client_set_parent_api_remove/$',
        ajax.client_set_parent_api_remove,
        name='client_set_parent_api_remove'),

    # 用户修改密码页面
    url(r'^parent_change_password/page/$', views.parent_change_password_views,
        name='parent_change_password_views'),

    # 用户修改密码
    url(r'^ajax/client_reset_password/$', ajax.client_reset_password,
        name='client_reset_password'),



]


urlpatterns = [

    # 基础页面
    url(r'^base/$', views.base, name='base'),

    # 登录页面
    url(r'^admin_login/$', views.admin_login, name='admin_login_page'),

    # 登录页面
    url(r'^customer_login/$', views.customer_login, name='customer_login_page'),

    # 登录校验
    url(r'^ajax/login/$', ajax.login, name='login'),

    # 账号退出
    url(r'^logout/$', views.logout, name='logout'),

    # 账号退出
    url(r'^product_prompt/page/(?P<menu_code>\S+)/$',
        views.product_prompt_views, name='product_prompt_views'),

    # 账号退出
    url(r'^get_sso_token/$',
        views.get_sso_token, name='get_sso_token'),


]

urlpatterns.extend(admin_urls)
urlpatterns.extend(client_urls)
