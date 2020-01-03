import os
import xlwt
import datetime

from django.conf import settings
from urllib.parse import urlparse

from common.feed import CDNConf, APIUrl
from base.models import Domain
from common.functions import datetime_to_str


def get_cdn_type_from_name(name):
    """通过名称获取加速类型"""

    cdn_type = 0
    for i in CDNConf.CDN_TYPE:
        check_name = i['check_name']
        if check_name in name:
            cdn_type = i['id']
            break

    return cdn_type


def make_base_excel(excel_name, sheet_name, domain_list, start_time, end_time):
    """生成基础excel"""

    # 判断目录是否存在,不存在则创建新目录
    cwd = os.path.join(settings.BASE_DIR, 'excel')
    if not os.path.exists(cwd):
        os.makedirs(cwd)

    # 判断文件是否存在,存在则删除
    excel_path = os.path.join(cwd, excel_name)
    if os.path.exists(excel_path):
        os.remove(excel_path)

    # 创建excel文件
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet(sheet_name)

    row = 0
    worksheet.write(row, 0, label='Statistical time')
    worksheet.write(row, 1, label='%s - %s' % (start_time, end_time))

    row = 1
    worksheet.write(row, 0, label='Statistical domain')

    for domain in domain_list:
        worksheet.write(row, 1, label=domain)
        row += 1

    return row, excel_path, worksheet, workbook


def detect_domain(user_id, urls):
    """加速url检测"""

    check_url = []
    for url in urls:
        if url:
            url_info = urlparse(url)

            domain_obj = Domain.objects.filter(
                protocol=url_info.scheme,
                domain=url_info.netloc, user__id=user_id
            ).first()

            if domain_obj:
                check_url.append(url)

    return check_url


def get_effective_contract(user):
    """获取用户有效合同"""
    body = {
        'username_list': [user.username]
    }

    res = APIUrl.post_link('user_query', body)
    user_query = res.get('user_query', {})

    now = datetime_to_str(datetime.datetime.now(), _format='%Y-%m-%d')


    username = user.username

    user_info = user_query.get(username, {})

    contract = user_info.get('contract', {})

    contract_name = ''
    try:

        if not user_info or not contract:
            assert False

        contract_name = ''
        product_cdn_type = []

        for c in contract:

            start_time = contract[c]['start_time']
            end_time = contract[c]['end_time']

            if start_time <= now <= end_time:
                product_list = contract[c]['product']
                for p in product_list:
                    product_name = p['product_name']

                    if CDNConf.NOVA_TYPE in product_name:
                        product_cdn_type = CDNConf.NOVA_TYPE_LIST
                        continue

                    p_cdn_type = get_cdn_type_from_name(product_name)
                    product_cdn_type.append(p_cdn_type)

                contract_name = c

                break

        if not contract_name:
            assert False

    except AssertionError:
        pass

    return contract_name