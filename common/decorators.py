from django.http import HttpResponseRedirect
from base.models import PermUser, PermUserObj, PermGroup, UserPermStrategy


def rights_required(perm_code, obj_name=None, redirect_url='/base/login/'):
    """
    Decorator for views that checks whether a user has a service permission
    enabled, redirecting to the redirect page if necessary.
    """

    def wrapper(f):
        def decorate(request, *arg, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseRedirect(redirect_url)

            user = request.user

            # 超级用户
            if user.is_superuser:
                check_result = True
            # 公司职员
            elif user.is_staff:
                group = user.groups.first()
                check_result = PermGroup.has_perm(perm_code, group)
            # 客户账号
            else:
                if obj_name:
                    obj_id = request.POST.get('obj_id', '')
                    if not obj_id:
                        return HttpResponseRedirect(redirect_url)
                    check_result = PermUserObj.has_perm(
                        perm_code, obj_name, obj_id, user)
                else:
                    if user.is_parent:
                        check_result = PermUser.has_perm(perm_code, user)
                    elif user.is_child:
                        check_result = UserPermStrategy.has_perm(
                            perm_code, user)

            if check_result:
                return f(request, *arg, **kwargs)
            else:
                return HttpResponseRedirect(redirect_url)

        return decorate

    return wrapper

