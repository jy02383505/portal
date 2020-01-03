import copy

from django.db.models import Q
from django.contrib.auth.models import Group

from base.models import (UserProfile, Perm, PermGroup, PermUser, PermStrategy,
                         UserPermStrategy)
from common.functions import int_check
from common.feed import AccountsFeed as af, APIUrl


def create_user(
        username, password, group, identity, mobile='', company='', email='',
        creator_username='', linkman='', remark='', reset_password=False,
        is_api=False):
    """
    :param username: 用户名
    :param password: 密码
    :param group: 角色
    :param identity: 身份 管理员is_admin/父账号is_parent/子账号is_child
    :param mobile: 电话
    :param company: 公司
    :param email: 邮箱
    :param creator_username: 创建者名称
    :param linkman: 联系人
    :param remark: 备注
    :param reset_password: 是否重置密码
    :param is_api: 是否设置api
    :return: user(obj)
    """
    user = None

    try:

        user = UserProfile.objects.create_user(username, email, password)
        parent_username = ''

        # 创建管理员
        if identity == 'is_admin':
            user.is_staff = True

        # 创建父账号
        elif identity == 'is_parent':
            user.is_parent = True

        # 创建子账号
        elif identity == 'is_child':
            parent_username = creator_username
            user.is_child = True

        # 创建代理账号
        elif identity == 'is_agent':
            user.is_parent = True
            user.is_agent = True

        if reset_password:
            user.reset_password = True

        if creator_username:
            user.creator_username = creator_username

        if mobile:
            user.mobile = mobile

        if company:
            user.company = company

        if linkman:
            user.linkman = linkman

        if remark:
            user.remark = remark

        if parent_username:
            user.parent_username = parent_username

        user.save()

        body = {
            'username': username,
            'user_id': user.id,
        }

        if is_api:
            body['is_api'] = True

        api_res = APIUrl.post_link('create_user', body)
        if api_res.get('return_code') != 0:
            user.delete()
            assert False

        group.user_set.add(user)
        group.user_set.add
        group.save()

    except Exception as e:
        print(e)

    return user


def create_domain():
    """创建域名"""


def get_menu_tree(user):
    """
    :param user: 通过用户获取权限
    :return:
    """
    menu_tree = []
    user_code_list = []
    user_perm = []
    try:
        if user.is_staff:
            group = user.groups.first()
            perm_group = PermGroup.objects.filter(group=group).first()

            all_user_perm = perm_group.perm.all()

            perm_list = all_user_perm.filter(is_menu=True)
            user_code_list = [i.code for i in perm_list]

            user_perm_opt = all_user_perm.filter(is_menu=False)
            user_perm = [i.code for i in user_perm_opt]

        elif user.is_parent:
            perm_user = PermUser.objects.filter(user=user).first()

            all_user_perm = perm_user.perm.all()

            user_perm_menu_list = all_user_perm.filter(is_menu=True)
            user_code_list = [i.code for i in user_perm_menu_list]
            perm_list = Perm.objects.filter(
                is_menu=True, content_type__contains='CLIENT',
                code__in=user_code_list)

            user_perm_opt = all_user_perm.filter(is_menu=False)
            user_perm = [i.code for i in user_perm_opt]

        elif user.is_child:
            user_perm_strategy = UserPermStrategy.objects.filter(
                user=user).first()

            for i in user_perm_strategy.perm_strategy.all():
                for j in i.perm.all():
                    if j.code not in user_code_list:
                        user_code_list.append(j.code)

            perm_list = Perm.objects.filter(
                is_menu=True, content_type__contains='CLIENT')


            user_perm_opt = Perm.objects.filter(
                is_menu=False, content_type__contains='CLIENT')
            user_perm = [i.code for i in user_perm_opt]

        level_1_menus = perm_list.filter(level=1)

        for i in level_1_menus:
            level_2_menus = perm_list.filter(level=2, parent_code=i.code)

            level_1_menu = i.dict_info

            child_list = []
            for j in level_2_menus:

                menu_info = copy.deepcopy(j.dict_info)

                if j.code not in user_code_list:
                    menu_info['url'] = '/base/product_prompt/page/%s/' \
                                       % j.parent_code

                child_list.append(menu_info)

            child_list = sorted(child_list, key=lambda x: x['order'])

            level_1_menu['child'] = child_list

            menu_tree.append(level_1_menu)
    except Exception as e:
        print(e)

    if menu_tree:
        menu_tree = sorted(menu_tree, key=lambda x: x['order'])

    return menu_tree, user_perm


def handle_perm(all_perm):
    """处理权限结构"""

    perm = {}
    perm_type = []

    menu_level_1_list = all_perm.filter(level=1)

    for i in menu_level_1_list:
        type_dict = {
            'id': i.code,
            'name': i.type_name
        }

        perm_type.append(type_dict)

        p_perm_query = all_perm.filter(parent_code=i.code)
        p_perm = [
            {'id': i.code, 'name': i.name} for i in p_perm_query
        ]
        perm[i.code] = p_perm

    return perm, perm_type


def get_user_perm_strategy_list(request):
    """获取用户权限列表"""
    name = request.POST.get('name', '')
    strategy_type = request.POST.get('strategy_type', '')

    perm_strategy_list = PermStrategy.objects.filter(
        Q(creator_username=request.user.username) |
        Q(strategy_type=PermStrategy.SYSTEM_NUM))

    if name:
        perm_strategy_list = PermStrategy.objects.filter(name=name)

    msg = ''
    perm_strategy_dict_list = []
    try:
        if strategy_type:
            strategy_type = int_check(strategy_type)
            if strategy_type is None:
                msg = af.PARAME_ERROR
                assert False

            perm_strategy_list = perm_strategy_list.filter(
                strategy_type=strategy_type)

        for i in perm_strategy_list:
            strategy_dict = {
                'id': i.id,
                'name': i.name,
                'strategy_type_name': i.strategy_type_name,
                'remark': i.remark
            }
            perm_strategy_dict_list.append(strategy_dict)
    except AssertionError:
        pass

    return msg, perm_strategy_dict_list
