# -*- coding:utf-8 -*-

from django.conf.urls import url
from cert import views, ajax


admin_urls = [

    # 管理员查看证书管理页面
    url(r'^admin_cert_ssl_manage/page/$', views.admin_cert_ssl_manage_views,
        name='admin_cert_ssl_manage_views'),

    # 管理员查看证书列表
    url(r'^ajax/admin_cert_list/$', ajax.admin_cert_list,
        name='admin_cert_list'),

    # 管理员创建证书页面
    url(r'^admin_cert_create/page/$', views.admin_cert_create_views,
        name='admin_cert_create_views'),

    # 管理员证书的上传与修改
    url(r'^ajax/admin_cert_create_or_edit/$', ajax.admin_cert_create_or_edit,
        name='admin_cert_create_or_edit'),

    # 管理员证书删除
    url(r'^ajax/admin_cert_delete/$', ajax.admin_cert_delete,
        name='admin_cert_delete'),

    # 管理员修改证书页面
    url(r'^admin_cert_edit/page/(?P<cert_name>\S+)/(?P<user_id>\S+)/$',
        views.admin_cert_edit_views,
        name='admin_cert_edit_views'),

    # 管理员证书详情页面
    url(r'^admin_cert_detail/page/(?P<cert_name>\S+)/(?P<user_id>\S+)/$',
        views.admin_cert_detail_views,
        name='admin_cert_detail'),
]


client_urls = [

    # 客户端查看证书管理页面
    url(r'^client_cert_ssl_manage/page/$', views.client_cert_ssl_manage_views,
        name='client_cert_ssl_manage_views'),

    # 客户端查看证书列表
    url(r'^ajax/client_cert_list/$', ajax.client_cert_list,
        name='client_cert_list'),

    # 客户端创建证书页面
    url(r'^client_cert_create/page/$', views.client_cert_create_views,
        name='client_cert_create_views'),

    # 客户端证书的上传与修改
    url(r'^ajax/client_cert_create_or_edit/$', ajax.client_cert_create_or_edit,
        name='client_cert_create_or_edit'),

    # 客户端证书删除
    url(r'^ajax/client_cert_delete/$', ajax.client_cert_delete,
        name='client_cert_delete'),

    # 客户端修改证书页面
    url(r'^client_cert_edit/page/(?P<cert_name>\S+)/(?P<user_id>\S+)/$',
        views.client_cert_edit_views,
        name='client_cert_edit_views'),

    # 客户端证书详情页面
    url(r'^client_cert_detail/page/(?P<cert_name>\S+)/(?P<user_id>\S+)/$',
        views.client_cert_detail_views,
        name='client_cert_detail'),

]


urlpatterns = [


]

urlpatterns.extend(admin_urls)
urlpatterns.extend(client_urls)
