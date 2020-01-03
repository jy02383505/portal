from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required


from common.feed import AccountsFeed as af, APIUrl
from base.models import (UserPermStrategy, UserProfile, PermStrategy, Perm,
                         PermUser)
from common.decorators import rights_required
from base.functions import handle_perm, get_user_perm_strategy_list
from  common.functions import timestamp_to_str


@login_required
@rights_required('child_create')
def create_child_user_views(request):
    """父账号创建子账号页面"""

    _, perm_strategy_dict_list = get_user_perm_strategy_list(request)

    res = {
        'perm_strategy_list': perm_strategy_dict_list,
        'strategy_type_dict': PermStrategy.strategy_type_dict()
    }
    return render(request, 'user/create_user_management.html', res)


@login_required
@rights_required('child_manage')
def parent_child_list_views(request):
    """父账号管理子账号页面"""

    _, perm_strategy_dict_list = get_user_perm_strategy_list(request)

    res = {
        'perm_strategy_list': perm_strategy_dict_list,
        'strategy_type_dict': PermStrategy.strategy_type_dict()
    }
    return render(request, 'user/user_management_list.html', res)


@login_required
@rights_required('child_manage')
def parent_child_details_views(request, user_id):
    """父账号获取子账号详情"""
    child = UserProfile.objects.filter(id=user_id).first()

    _, perm_strategy_dict_list = get_user_perm_strategy_list(request)

    user_perm_strategy = UserPermStrategy.objects.filter(user=child).first()

    user_perm_strategy_dict_list = []

    if user_perm_strategy:
        for i in user_perm_strategy.perm_strategy.all():
            perm_strategy_dict = {
                'id': i.id,
                'name': i.name,
                'remark': i.remark,
                'strategy_type_name': i.strategy_type_name
            }
            user_perm_strategy_dict_list.append(perm_strategy_dict)

    res = {
        'user': child,
        'perm_strategy_list': perm_strategy_dict_list,
        'user_perm_strategy_list': user_perm_strategy_dict_list,
        'strategy_type_dict': PermStrategy.strategy_type_dict()
    }
    return render(request, 'user/user_management_details.html', res)


@login_required
@rights_required('access_manage_menu')
def parent_get_perm_strategy_views(request):
    """父账号策略管理页面"""

    _, perm_strategy_dict_list = get_user_perm_strategy_list(request)

    res = {
        'perm_strategy_list': perm_strategy_dict_list,
        'strategy_type_dict': PermStrategy.strategy_type_dict()
    }
    return render(request, 'user/parent_get_perm_strategy_views.html', res)


@login_required
@rights_required('perm_strategy_create')
def parent_create_perm_strategy_views(request):
    """父账号策略创建页面"""

    _, perm_strategy_dict_list = get_user_perm_strategy_list(request)

    perm_user = PermUser.objects.filter(user=request.user).first()
    user_perm = {}
    user_perm_type = []
    if perm_user and perm_user.perm.all():
        user_perm, user_perm_type = handle_perm(perm_user.perm.all())

    res = {
        'user_perm': user_perm,
        'user_perm_type': user_perm_type,
        'perm_strategy_list': perm_strategy_dict_list,
        'strategy_type_dict': PermStrategy.strategy_type_dict()
    }

    return render(request, 'user/parent_create_perm_strategy_views.html', res)


@login_required
@rights_required('access_manage_menu')
def parent_perm_strategy_details_views(request, perm_strategy_id):
    """父账号策略详情"""

    perm_strategy = PermStrategy.objects.filter(id=perm_strategy_id).first()
    parent_perm = {}
    parent_perm_type = []
    if perm_strategy:
        parent_perm, parent_perm_type = handle_perm(perm_strategy.perm.all())

    all_perm = Perm.objects.filter(content_type__contains='CLIENT')
    all_perm, all_perm_type = handle_perm(all_perm)
    res = {
        'all_perm': all_perm,
        'all_perm_type': all_perm_type,
        'perm_strategy': perm_strategy,

        'parent_perm': parent_perm,
        'parent_perm_type': parent_perm_type,
        'strategy_type_dict': PermStrategy.strategy_type_dict()
    }
    return render(request, 'user/strategy_management_details.html', res)


@login_required
@rights_required('client_user_info')
def parent_user_info_views(request):
    """用户账号信息"""
    res = {
        'user': request.user
    }
    return render(request, 'user/user_info_details.html', res)


@login_required
@rights_required('client_api_info')
def parent_secret_info_views(request):
    """用户秘钥信息信息"""
    user = request.user
    body = {
        'username_list': [user.username]
    }

    res = APIUrl.post_link('user_query', body)
    user_query = res.get('user_query', {})
    user_info = user_query.get(user.username, {})

    secret_id = user_info.get('api_secret_id', '')
    secret_key = user_info.get('api_secret_key', '')
    api_create_time = user_info.get('api_create_time', '')
    if api_create_time:
        api_create_time = timestamp_to_str(api_create_time)
    api_open = user_info.get('api_open', 0)

    api_info = list()

    if secret_id and secret_key:
        api_info_dict = {
            'secret_id': secret_id,
            'secret_key': secret_key,
            'create_time': api_create_time,
            'status': api_open,
            'type': _(af.COMMON)
        }
        api_info.append(api_info_dict)

    user.api_info = api_info

    res = {
        'user': user
    }
    return render(request, 'user/user_secret_info_details.html', res)


@login_required
@rights_required('client_change_password')
def parent_change_password_views(request):
    """用户修改密码"""
    res = {

    }
    return render(request, 'user/user_change_password.html', res)
