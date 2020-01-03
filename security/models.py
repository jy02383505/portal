from django.db import models

ACCESS_TYPE = [
    ('上层-waf-源站', 1),
    ('边缘-waf-上层', 2),
]

ORIGIN_TYPE = [
    ('IP回源', 1),
    ('域名回源', 2),
]

defense_type = [
    ('普通防御模式', 1),
    ('高级防御模式', 2),
]

status = [
    ('WAF未配置', 0),
    ('WAF配置中', 1),
    ('WAF配置成功', 2),
    ('接入CDN成功', 3),
    ('WAF配置失败', -1),
]

# waf表
task_obj = {
    'domain': 'www.baidu.com',
    'access_point': 'HK',
    'access_point_cname': 'cc-waf-rim.ccgslb.com.cn',
    'access_type': 2,
    'status': 0,
    'confirm_cdn_preload': False,
    'confirm_cdn_http_layered': False,
    'confirm_cdn_https_layered': False,
    'err_msg': ''
}

# 证书表
cert_info = {
    'cert': '',
    'key': '',
    'domain': '',
    'QINGSONG_id': '青松id',
    'CC_id': '青松id',
    'name': '',
    'user_id': 4,
    'desc': '',
}

update = {
    'domain': '域名',
    'access_point': '接入点',
    'access_point_cname': '接入点对应cname',
    'access_type': 'waf接入方式 目前是 2',
    'src_type': '1 ip回源 & 2 域名回源',
    'src_address': '回源值 域名回源就是域名,ip回源就是ip',
    'src_port': '回源端口',
    'src_host': '回源host',
    'is_https': '是否启用https',
    'cert_name': '证书名称',
    'default_waf_mode': '默认规则防御模式',
    'self_waf_mode': '自定义规则防御模式',
}
