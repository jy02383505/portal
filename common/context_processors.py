# -*- coding=utf-8 -*-

from base.functions import get_menu_tree


def user_perm(request):
    """A context processor that provides service list of user."""
    user = request.user

    if 'AnonymousUser' == str(user):
        return {}

    if not user:
        return {}

    _, user_perm_list = get_menu_tree(user)

    res = {
        'user_perm': user_perm_list
    }

    return res



