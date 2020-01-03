# -*- coding:utf-8 -*-

from django.conf.urls import url
from security import views, ajax


admin_urls = [

    # 管理员安全CDN频道统计
    url(r'^admin_sec_overview/page/$',
        views.admin_sec_overview_views,
        name='admin_sec_overview_views'),

    # 管理员安全CDN客户列表
    url(r'^admin_sec_user_list/page/$', views.admin_sec_user_list_views,
        name='admin_sec_user_list_views'),

    # 管理员获取安全用户列表
    url(r'^ajax/admin_sec_user_list/$', ajax.admin_sec_user_list,
        name='admin_sec_user_list'),
    # 管理员添加安全客户
    url(r'^ajax/admin_create_sec_user/$', ajax.admin_create_sec_user,
        name='admin_create_sec_user'),


    # 管理员安全CDN频道列表页面
    url(r'^admin_sec_domain_list/page/$',
        views.admin_sec_domain_list_views,
        name='admin_sec_domain_list_views'),

    # 管理员获取安全CDN频道列表
    url(r'^ajax/admin_get_sec_domain_list/$',
        ajax.admin_get_sec_domain_list,
        name='admin_get_sec_domain_list'),

    # 管理员安全域名配置页面
    url(r'^admin_sec_domain_conf/page/(?P<domain_id>\S+)/$',
        views.admin_sec_domain_conf_views,
        name='admin_sec_domain_conf_views'),

    # 管理员添加安全频道获取cms频道列表
    url(r'^ajax/admin_get_cms_channel_list/$',
        ajax.admin_get_cms_channel_list,
        name='admin_get_cms_channel_list'),

    # 管理员添加安全频道
    url(r'^ajax/admin_create_sec_domain/$',
        ajax.admin_create_sec_domain,
        name='admin_create_sec_domain'),

    # 管理员安全CDN频道告警
    url(r'^admin_alarm_list/page/$', views.admin_alarm_list,
        name='admin_alarm_list'),

    # 管理员waf开通首页
    url(r'^admin_domain_waf_create_index/page/$',
        views.admin_domain_waf_create_index_views,
        name='admin_domain_waf_create_index_views'),

    # 管理员检查域名waf状态
    url(r'^ajax/admin_check_domain_waf_status/$',
        ajax.admin_check_domain_waf_status,
        name='admin_check_domain_waf_status'),

    # 管理员绑定域名
    url(r'^ajax/admin_domain_waf_binding/$',
        ajax.admin_domain_waf_binding,
        name='admin_domain_waf_binding'),

    # 管理员waf注册页面(绑定)
    url(r'^admin_domain_waf_register/page/(?P<domain_id>\S+)/$',
        views.admin_domain_waf_register_views,
        name='admin_domain_waf_register_views'),

    # 管理员创建域名
    url(r'^ajax/admin_domain_waf_create/$',
        ajax.admin_domain_waf_create,
        name='admin_domain_waf_create'),

    # 管理员waf注册页面(创建)
    url(r'^admin_domain_waf_create/page/(?P<domain_id>\S+)/$',
        views.admin_domain_waf_create_views,
        name='admin_domain_waf_create_views'),

    # 管理员同步waf配置
    url(r'^ajax/admin_sync_domain_waf_conf/$',
        ajax.admin_sync_domain_waf_conf,
        name='admin_sync_domain_waf_conf'),


    # 管理员waf配置失败or创建中
    url(r'^admin_domain_waf_conf_fail/page/$',
        views.admin_domain_waf_conf_fail_views,
        name='admin_domain_waf_conf_fail_views'),

    # 管理员waf CDN配置页面
    url(r'^admin_domain_waf_cdn_conf/page/(?P<domain_id>\S+)/$',
        views.admin_domain_waf_cdn_conf_views,
        name='admin_domain_waf_cdn_conf_views'),

    # 管理员waf 基本信息配置
    url(r'^ajax/admin_set_domain_waf_conf/$',
        ajax.admin_set_domain_waf_conf,
        name='admin_set_domain_waf_conf'),

    # 管理员waf 设置CDN
    url(r'^ajax/admin_domain_waf_set_cdn/$',
        ajax.admin_domain_waf_set_cdn,
        name='admin_domain_waf_set_cdn'),

    # 管理员上传waf证书
    url(r'^ajax/admin_upload_waf_cert/$',
        ajax.admin_upload_waf_cert,
        name='admin_upload_waf_cert'),

    # 管理员开关waf
    url(r'^ajax/admin_domain_set_waf/$',
        ajax.admin_domain_set_waf,
        name='admin_domain_set_waf'),

    # 管理员删除waf
    url(r'^ajax/admin_domain_del_waf/$',
        ajax.admin_domain_del_waf,
        name='admin_domain_del_waf'),

    # 管理员获取waf默认规则
    url(r'^ajax/admin_get_waf_default_rule/$',
        ajax.admin_get_waf_default_rule,
        name='admin_get_waf_default_rule'),

    # 管理员获取waf自定义规则
    url(r'^ajax/admin_get_waf_self_rule/$',
        ajax.admin_get_waf_self_rule,
        name='admin_get_waf_self_rule'),

    # 管理员设置全部默认规则开关
    url(r'^ajax/admin_reset_default_rule/$',
        ajax.admin_reset_default_rule,
        name='admin_reset_default_rule'),

    # 管理员设置默认规则
    url(r'^ajax/admin_enable_default_rule/$',
        ajax.admin_enable_default_rule,
        name='admin_enable_default_rule'),

    # 管理员设置自定义规则
    url(r'^ajax/admin_enable_self_rule/$',
        ajax.admin_enable_self_rule,
        name='admin_enable_self_rule'),

    # 管理员安全统计页面
    url(r'^admin_sec_overview/page/(?P<domain_id>\S+)/$',
        views.admin_sec_overview_views,
        name='admin_sec_overview_views'),

    # 管理员获取waf日志
    url(r'^ajax/admin_get_log_list/$',
        ajax.admin_get_log_list,
        name='admin_get_log_list'),

    # 管理员获取waf日志详情
    url(r'^ajax/admin_get_log_detail/$',
        ajax.admin_get_log_detail,
        name='admin_get_log_detail'),

    # 管理员下载日志
    url(r'^ajax/admin_download_log/(?P<domain_id>\S+)/(?P<atk_ip>\S+)/'
        r'(?P<start_time>\S+)/(?P<end_time>\S+)/(?P<log_rows>\S+)/$',
        ajax.admin_download_log,
        name='admin_download_log'),

    # 管理员获取waf统计数据
    url(r'^ajax/admin_get_waf_statistics/$',
        ajax.admin_get_waf_statistics,
        name='admin_get_waf_statistics'),

    # 管理员下载拦截攻击次数
    url(r'^ajax/admin_download_time_cnt/'
        r'(?P<domain_id>\S+)/(?P<start_time>\S+)/(?P<end_time>\S+)/$',
        ajax.admin_download_time_cnt,
        name='admin_download_time_cnt'),

    # 管理员下载攻击来源
    url(r'^ajax/admin_download_ip_list/'
        r'(?P<domain_id>\S+)/(?P<start_time>\S+)/(?P<end_time>\S+)/$',
        ajax.admin_download_ip_list,
        name='admin_download_ip_list'),

    # 管理员下载攻击方式
    url(r'^ajax/admin_download_rule_list/'
        r'(?P<domain_id>\S+)/(?P<start_time>\S+)/(?P<end_time>\S+)/$',
        ajax.admin_download_rule_list,
        name='admin_download_rule_list'),

]


client_urls = [

    # 父账号安全域名配置页面
    url(r'^parent_sec_domain_conf/page/(?P<domain_id>\S+)/$',
        views.parent_sec_domain_conf_views,
        name='parent_sec_domain_conf_views'),

    # 父账号安全CDN频道列表页面
    url(r'^parent_sec_domain_list/page/$',
        views.parent_sec_domain_list_views,
        name='parent_sec_domain_list_views'),
    # 父账号安全域名列表
    url(r'^ajax/parent_get_sec_domain_list/$',
        ajax.parent_get_sec_domain_list,
        name='parent_get_sec_domain_list'),

    # 父账号获取waf基础配置信息
    url(r'^ajax/parent_get_waf_default_rule/$',
        ajax.parent_get_waf_default_rule,
        name='parent_get_waf_default_rule'),

    # 父账号获取waf自定义规则配置信息
    url(r'^ajax/parent_get_waf_self_rule/$',
        ajax.parent_get_waf_self_rule,
        name='parent_get_waf_self_rule'),

    # 父账号获取waf基础信息
    url(r'^ajax/parent_get_waf_base_conf/$',
        ajax.parent_get_waf_base_conf,
        name='parent_get_waf_base_conf'),

    # 父账号设置防御模式
    url(r'^ajax/parent_set_defense_mode/$',
        ajax.parent_set_defense_mode,
        name='parent_set_defense_mode'),

    # 父账号全部开启或者关闭默认规则
    url(r'^ajax/parent_reset_default_rule/$',
        ajax.parent_reset_default_rule,
        name='parent_reset_default_rule'),

    # 父账号开关指定默认规则
    url(r'^ajax/parent_enable_default_rule/$',
        ajax.parent_enable_default_rule,
        name='parent_enable_default_rule'),

    # 父账号开关指定自定义规则
    url(r'^ajax/parent_enable_self_rule/$',
        ajax.parent_enable_self_rule,
        name='parent_enable_self_rule'),

    # 父账号安全统计页面
    url(r'^parent_sec_overview/page/(?P<domain_id>\S+)/$',
        views.parent_sec_overview_views,
        name='parent_sec_overview_views'),

    # 父账号获取waf日志
    url(r'^ajax/parent_get_log_list/$',
        ajax.parent_get_log_list,
        name='parent_get_log_list'),

    # 父账号获取waf日志详情
    url(r'^ajax/parent_get_log_detail/$',
        ajax.parent_get_log_detail,
        name='parent_get_log_detail'),

    # 父账号下载日志
    url(r'^ajax/parent_download_log/(?P<domain_id>\S+)/(?P<atk_ip>\S+)/'
        r'(?P<start_time>\S+)/(?P<end_time>\S+)/(?P<log_rows>\S+)/$',
        ajax.parent_download_log,
        name='parent_download_log'),

    # 父账号获取waf统计数据
    url(r'^ajax/parent_get_waf_statistics/$',
        ajax.parent_get_waf_statistics,
        name='parent_get_waf_statistics'),

    # 父账号下载拦截攻击次数
    url(r'^ajax/parent_download_time_cnt/'
        r'(?P<domain_id>\S+)/(?P<start_time>\S+)/(?P<end_time>\S+)/$',
        ajax.parent_download_time_cnt,
        name='parent_download_time_cnt'),

    # 父账号下载攻击来源
    url(r'^ajax/parent_download_ip_list/'
        r'(?P<domain_id>\S+)/(?P<start_time>\S+)/(?P<end_time>\S+)/$',
        ajax.parent_download_ip_list,
        name='parent_download_ip_list'),

    # 父账号下载攻击方式
    url(r'^ajax/parent_download_rule_list/'
        r'(?P<domain_id>\S+)/(?P<start_time>\S+)/(?P<end_time>\S+)/$',
        ajax.parent_download_rule_list,
        name='parent_download_rule_list'),

]


urlpatterns = [


]

urlpatterns.extend(admin_urls)
urlpatterns.extend(client_urls)

