# -*- coding:utf-8 -*-

from django.conf.urls import url
from cdn import views, ajax

admin_urls = [

    # 管理员CDN用户列表页面
    url(r'^admin_cdn_user_list/page/$', views.admin_cdn_user_list_views,
        name='admin_cdn_user_list_views'),

    url(r'^ajax/admin_cdn_user_list/$', ajax.admin_cdn_user_list,
        name='admin_cdn_user_list'),

    # 管理员查看域名列表页面
    url(r'^admin_get_domain_list/page/$', views.admin_get_domain_list_views,
        name='admin_parent_list_views'),

    # 管理员查看域名列表
    url(r'^ajax/admin_get_domain_list/$', ajax.admin_get_domain_list,
        name='admin_get_domain_list'),

    # 管理员添加域名
    url(r'^add_admin_domain/page/$', views.admin_cdn_create_domain_views,
        name='admin_cdn_create_domain_views'),

    # 管理员修改域名配置
    url(r'^modify_admin_domain_configure/page/(?P<domain_id>\S+)/$',
        views.admin_cdn_edit_domain_views,
        name='admin_cdn_edit_domain_views'),

    # 管理员统计
    url(r'^admin_statistics/page/$', views.admin_statistics_views,
        name='admin_statistics_views'),

    # 管理员刷新
    url(r'^admin_refresh/page/$', views.admin_refresh_views,
        name='admin_refresh_views'),

    # 管理员下发刷新
    url(r'^ajax/admin_cdn_domain_refresh/$', ajax.admin_cdn_domain_refresh,
        name='admin_cdn_domain_refresh'),

    # 管理员查询刷新
    url(r'^ajax/admin_cdn_domain_refresh_status/$',
        ajax.admin_cdn_domain_refresh_status,
        name='admin_cdn_domain_refresh_status'),

    # 管理员预加载
    url(r'^admin_preload/page/$', views.admin_preload_views,
        name='admin_preload_views'),

    # 管理员预加载下发
    url(r'^ajax/admin_cdn_domain_preload/$', ajax.admin_cdn_domain_preload,
        name='admin_cdn_domain_preload'),

    # 管理员预加载查询
    url(r'^ajax/admin_cdn_domain_preload_status/$',
        ajax.admin_cdn_domain_preload_status,
        name='admin_cdn_domain_preload_status'),

    # 管理员日志下载页面
    url(r'^admin_log_upload/page/$', views.admin_log_download_views,
        name='admin_log_download_views'),

    # 管理员日志列表
    url(r'^ajax/admin_cdn_domain_log_list/$', ajax.admin_cdn_domain_log_list,
        name='admin_cdn_domain_log_list'),

    # 管理员配置cdn基础信息配置页面
    url(r'^admin_cdn_base_conf/page/(?P<user_id>\S+)/$',
        views.admin_cdn_base_conf_views,
        name='admin_cdn_base_conf_views'),

    # 管理员设置cdn用户基本配置
    url(r'^ajax/admin_cdn_user_set_conf/$', ajax.admin_cdn_user_set_conf,
        name='admin_cdn_user_set_conf'),

    # 管理员创建加速域名页面
    url(r'^admin_cdn_create_domain_views/page/$',
        views.admin_cdn_create_domain_views,
        name='admin_cdn_create_domain_views'),

    # 管理员创建加速域名
    url(r'^ajax/admin_cdn_create_domain/$', ajax.admin_cdn_create_domain,
        name='admin_cdn_create_domain'),

    # 管理员获取证书列表
    url(r'^ajax/admin_cdn_get_cert/$', ajax.admin_cdn_get_cert,
        name='admin_cdn_get_cert'),

    # 管理员修改加速域名
    url(r'^ajax/admin_cdn_edit_domain/$', ajax.admin_cdn_edit_domain,
        name='admin_cdn_edit_domain'),

    # 管理员获取域名配置信息
    url(r'^ajax/admin_cdn_domain_conf/$', ajax.admin_cdn_domain_conf,
        name='admin_cdn_domain_conf'),

    # 管理员报停域名
    url(r'^ajax/admin_cdn_domain_disable/$', ajax.admin_cdn_domain_disable,
        name='admin_cdn_domain_disable'),

    # 管理员激活域名
    url(r'^ajax/admin_cdn_domain_active/$', ajax.admin_cdn_domain_active,
        name='admin_cdn_domain_active'),

    # 管理员获取计费统计数据
    url(r'^ajax/admin_cdn_flux_data/$', ajax.admin_cdn_flux_data,
        name='admin_cdn_flux_data'),

    # 管理员获取请求量统计数据
    url(r'^ajax/admin_cdn_request_data/$', ajax.admin_cdn_request_data,
        name='admin_cdn_request_data'),

    # 管理员获取状态码统计数据
    url(r'^ajax/admin_cdn_status_code_data/$', ajax.admin_cdn_status_code_data,
        name='admin_cdn_status_code_data'),

    # 管理员获取计费统计数据下载
    url(r'^ajax/admin_download_cdn_flux/(?P<start_time>\S+)/(?P<end_time>\S+)'
        r'/(?P<user_id>\S+)/(?P<domain_ids>\S+)/(?P<opts>\S+)/$',
        ajax.admin_download_cdn_flux,
        name='admin_download_cdn_flux'),

    # 管理员获取状态码统计数据下载
    url(r'^ajax/admin_download_status_code/(?P<start_time>\S+)/'
        r'(?P<end_time>\S+)/(?P<user_id>\S+)/(?P<domain_ids>\S+)/'
        r'(?P<opts>\S+)/$',
        ajax.admin_download_status_code,
        name='admin_download_status_code'),

    # 管理员获取状态码趋势统计数据下载
    url(r'^ajax/admin_download_status_code_trend/(?P<start_time>\S+)/'
        r'(?P<end_time>\S+)/(?P<user_id>\S+)/(?P<domain_ids>\S+)'
        r'/(?P<opts>\S+)/$',
        ajax.admin_download_status_code_trend,
        name='admin_download_status_code_trend'),
]


client_urls = [

    # 客户端总览页面
    url(r'^client_cdn_overview/page/$', views.client_cdn_overview_views,
        name='client_cdn_overview_views'),

    # 客户端总览数据
    url(r'^ajax/client_cdn_overview_data/$', ajax.client_cdn_overview_data,
        name='client_cdn_overview_data'),

    # 客户端查看域名列表页面
    url(r'^client_get_domain_list/page/$', views.client_get_domain_list_views,
        name='client_get_domain_list_views'),

    # 客户端添加域名页面
    url(r'^client_cdn_create_domain/page/$',
        views.client_cdn_create_domain_views,
        name='client_cdn_create_domain_views'),

    # 客户端修改域名配置
    url(r'^modify_client_domain_configure/page/(?P<domain_id>\S+)/$',
        views.client_cdn_edit_domain_views,
        name='client_cdn_edit_domain_views'),

    # 客户端创建加速域名
    url(r'^ajax/client_cdn_create_domain/$', ajax.client_cdn_create_domain,
        name='client_cdn_create_domain'),

    # 客户端修改加速域名
    url(r'^ajax/client_cdn_edit_domain/$', ajax.client_cdn_edit_domain,
        name='client_cdn_edit_domain'),

    # 客户端获取证书列表
    url(r'^ajax/client_cdn_get_cert/$', ajax.client_cdn_get_cert,
        name='client_cdn_get_cert'),

    # 客户端统计页面
    url(r'^client_statistics/page/$', views.client_statistics_views,
        name='client_statistics_views'),

    # 客户端刷新页面
    url(r'^client_refresh/page/$', views.client_refresh_views,
        name='client_refresh_views'),

    # 客户端下发刷新
    url(r'^ajax/client_cdn_domain_refresh/$', ajax.client_cdn_domain_refresh,
        name='client_cdn_domain_refresh'),

    # 客户端查询刷新
    url(r'^ajax/client_cdn_domain_refresh_status/$',
        ajax.client_cdn_domain_refresh_status,
        name='client_cdn_domain_refresh_status'),

    # 客户端预加载页面
    url(r'^client_preload/page/$', views.client_preload_views,
        name='client_preload_views'),

    # 客户端预加载下发
    url(r'^ajax/client_cdn_domain_preload/$', ajax.client_cdn_domain_preload,
        name='client_cdn_domain_preload'),

    # 客户端预加载查询
    url(r'^ajax/client_cdn_domain_preload_status/$',
        ajax.client_cdn_domain_preload_status,
        name='client_cdn_domain_preload_status'),

    # 客户端日志下载页面
    url(r'^client_log_upload/page/$', views.client_log_download_views,
        name='client_log_download_views'),

    # 客户端日志列表
    url(r'^ajax/client_cdn_domain_log_list/$', ajax.client_cdn_domain_log_list,
        name='client_cdn_domain_log_list'),

    # 客户端获取域名列表
    url(r'^ajax/client_get_domain_list/$', ajax.client_get_domain_list,
        name='client_get_domain_list'),

    # 客户端报停域名
    url(r'^ajax/client_cdn_domain_disable/$', ajax.client_cdn_domain_disable,
        name='client_cdn_domain_disable'),

    # 客户端激活域名
    url(r'^ajax/client_cdn_domain_active/$', ajax.client_cdn_domain_active,
        name='client_cdn_domain_active'),

    # 客户端获取计费统计数据
    url(r'^ajax/client_cdn_flux_data/$', ajax.client_cdn_flux_data,
        name='client_cdn_flux_data'),

    # 客户端获取请求量统计数据
    url(r'^ajax/client_cdn_request_data/$', ajax.client_cdn_request_data,
        name='client_cdn_request_data'),

    # 客户端获取计费统计数据下载
    url(r'^ajax/client_download_cdn_flux/(?P<start_time>\S+)/(?P<end_time>\S+)'
        r'/(?P<domain_ids>\S+)/$',
        ajax.client_download_cdn_flux,
        name='client_download_cdn_flux'),

    # 客户端获取状态码统计数据
    url(r'^ajax/client_cdn_status_code_data/$',
        ajax.client_cdn_status_code_data,
        name='client_cdn_status_code_data'),

    # 客户端获取状态码统计数据下载
    url(r'^ajax/client_download_status_code/(?P<start_time>\S+)/'
        r'(?P<end_time>\S+)/(?P<domain_ids>\S+)/$',
        ajax.client_download_status_code,
        name='client_download_status_code'),

    # 客户端获取状态码趋势统计数据下载
    url(r'^ajax/client_download_status_code_trend/(?P<start_time>\S+)/'
        r'(?P<end_time>\S+)/(?P<domain_ids>\S+)/$',
        ajax.client_download_status_code_trend,
        name='client_download_status_code_trend'),


]


urlpatterns = [


]

urlpatterns.extend(admin_urls)
urlpatterns.extend(client_urls)
