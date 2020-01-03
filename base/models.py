
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.contenttypes.models import ContentType

from common.feed import AccountsFeed as af


class Provider(models.Model):

    name = models.CharField(
        verbose_name='供应商名称',
        max_length=255,
        null=True,
        blank=True
    )

    code = models.CharField(
        verbose_name='代码标识',
        max_length=255,
        null=True,
        blank=True
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='添加时间',
    )

    remark = models.CharField(
        verbose_name='备注',
        max_length=255,
        default='',
    )

    class Meta:
        verbose_name = '供应商'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s>>%s' % (self.name, self.code)


class Product(models.Model):

    name = models.CharField(
        verbose_name='产品名称',
        max_length=255,
        null=True,
        blank=True
    )

    code = models.CharField(
        verbose_name='产品标识',
        max_length=255,
        null=True,
        blank=True
    )

    remark = models.CharField(
        verbose_name='备注',
        max_length=255,
        default='',
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='添加时间',
    )

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s>>%s' % (self.name, self.code)


class Service(models.Model):

    name = models.CharField(
        verbose_name='服务名称',
        max_length=255,
        null=True,
        blank=True
    )

    code = models.CharField(
        verbose_name='代码标识',
        max_length=255,
        null=True,
        blank=True
    )

    remark = models.CharField(
        verbose_name='备注',
        max_length=255,
        default='',
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='添加时间',
    )

    class Meta:
        verbose_name = '服务策略'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s>>%s' % (self.name, self.code)


class Strategy(models.Model):

    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='添加时间',
    )

    class Meta:
        verbose_name = '策略'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s>>%s>>%s' % (
            self.provider.name, self.product.name, self.service.name)

    @property
    def code(self):
        return '%s_%s_%s' % (
            self.provider.code, self.product.code, self.service.code)

    @classmethod
    def get_obj_from_property(cls, provider_code, product_code, service_code):
        obj = cls.objects.filter(
            provider__code=provider_code,
            product__code=product_code,
            service__code=service_code
        ).first()

        return obj


class UserProfile(AbstractUser):

    mobile = models.CharField(
        default='',
        verbose_name='手机号',
        max_length=11,
        null=True,
        blank=True
    )

    company = models.CharField(
        default='',
        verbose_name='公司名称',
        max_length=255,
        null=True,
        blank=True
    )

    is_parent = models.BooleanField(
        verbose_name='父账号标识',
        default=False
    )

    is_child = models.BooleanField(
        verbose_name='子账号标识',
        default=False
    )

    is_agent = models.BooleanField(
        verbose_name='代理商标识',
        default=False
    )

    parent_username = models.CharField(
        verbose_name='父账号',
        default='',
        max_length=255,
        blank=True
    )

    creator_username = models.CharField(
        max_length=255,
        default='admin',
        verbose_name='创建者',
    )

    read_only = models.ManyToManyField(
        Product,
        related_name='产品读取权限',
        blank=True
    )

    add_only = models.ManyToManyField(
        Product,
        related_name='产品添加权限',
        blank=True
    )

    edit_only = models.ManyToManyField(
        Product,
        related_name='产品修改权限',
        blank=True
    )

    delete_only = models.ManyToManyField(
        Product,
        related_name='产品删除权限',
        blank=True
    )

    strategy_list = models.ManyToManyField(
        Strategy,
        related_name='服务列表',
        blank=True
    )

    product_list = models.ManyToManyField(
        Product,
        related_name='user_product',
        blank=True
    )

    reset_password = models.BooleanField(
        verbose_name='重置密码标识',
        default=False
    )

    remark = models.CharField(
        max_length=255,
        default='',
        verbose_name='备注',
        blank=True
    )

    linkman = models.CharField(
        max_length=255,
        default='',
        verbose_name='联系人',
        blank=True
    )

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s>>%s" % (self.username, self.id)

    @property
    def creator(self):
        """创建者"""
        obj = UserProfile.objects.filter(username=self.creator_username).first()
        return obj

    @property
    def parent(self):
        """父账号"""
        obj = UserProfile.objects.filter(username=self.parent_username).first()
        return obj

    @property
    def type_name(self):
        """用户;类别名称"""
        name = ''
        if self.is_parent:
            name = af.COMMON_CUSTOMER
        elif self.is_agent:
            name = af.AGENT_CUSTOMER
        elif self.is_child:
            name = af.CHILD_CUSTOMER
        elif self.is_staff:
            name = af.ADMIN

        return name

    @classmethod
    def create_admin(cls, creator):
        """创建管理员"""
        user = cls(creator_username=creator.username)
        user.is_staff = True
        user.save()

    @classmethod
    def create_parent(cls, creator):
        """创建父账号"""
        user = cls(creator_username=creator.username)
        user.is_parent = True
        user.save()
        user.user_permissions.clear()

    @classmethod
    def create_child(cls, creator):
        """创建子账号"""
        user = cls(creator_username=creator.username)
        user.is_child = True
        user.save()
        user.user_permissions.clear()


class GroupProfile(models.Model):

    ADMIN_ID = 1
    CUSTOMER_SERVICE_ID = 2
    COMMON_STAFF_ID = 3
    CUSTOMER_ID = 4
    CUSTOMER_CHILD_ID = 5

    ADMIN = '管理员'
    CUSTOMER_SERVICE = '客服'
    COMMON_STAFF = '普通员工'
    CUSTOMER = '客户'
    CUSTOMER_CHILD = '客户子账号'

    GROUP_BASE = (
        (ADMIN_ID, ADMIN),
        (CUSTOMER_SERVICE_ID, CUSTOMER_SERVICE),
        (COMMON_STAFF_ID, COMMON_STAFF),
        (CUSTOMER_ID, CUSTOMER),
        (CUSTOMER_CHILD_ID, CUSTOMER_CHILD)
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )

    creator_name = models.CharField(
        default='admin',
        verbose_name='创建者名称',
        max_length=255,
        blank=True
    )

    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )

    desc = models.CharField(
        max_length=255,
        default='',
        verbose_name='描述信息',
        blank=True
    )

    remark = models.CharField(
        max_length=255,
        default='',
        verbose_name='备注',
        blank=True
    )

    class Meta:
        verbose_name = '角色扩展'
        verbose_name_plural = verbose_name

    @classmethod
    def group_views(cls, only_admin=True):
        """获取角色列表"""
        res = []
        for i in cls.objects.all():

            if only_admin:
                if i.group.name in [cls.CUSTOMER, cls.CUSTOMER_CHILD]:
                    continue
            temp = {
                'id': i.id,
                'group_id': i.group.id,
                'name': i.group.name
            }
            res.append(temp)

        return res


class Perm(models.Model):

    name = models.CharField(
        verbose_name='名称',
        max_length=255,
    )

    code = models.CharField(
        verbose_name='标识',
        max_length=255,
    )

    content_type = models.CharField(
        verbose_name='类型',
        max_length=255,
    )

    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )

    desc = models.CharField(
        max_length=255,
        default='',
        verbose_name='描述信息'
    )

    level = models.CharField(
        max_length=255,
        default='',
        verbose_name='菜单等级'
    )

    parent_code = models.CharField(
        max_length=255,
        default='',
        verbose_name='父级菜单名称'
    )

    order = models.CharField(
        max_length=255,
        default='',
        verbose_name='菜单顺序'
    )

    is_menu = models.BooleanField(
        default=False,
        verbose_name='是否是菜单'
    )

    url = models.CharField(
        max_length=255,
        default='',
        verbose_name='访问地址'
    )

    type_name = models.CharField(
        max_length=255,
        default='',
        verbose_name='类别名称'
    )

    en_code = models.CharField(
        max_length=255,
        default='',
        verbose_name='英文'
    )

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = verbose_name

    @property
    def dict_info(self):
        """字典格式"""

        info = {
            'name': self.name,
            'code': self.code,
            'order': self.order,
            'url': self.url,
            'en_code': self.en_code,
        }
        return info

    def __str__(self):
        return '%s>%s>%s' % (self.level, self.name, self.desc)


class PermGroup(models.Model):

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )

    perm = models.ManyToManyField(
        Perm,
    )

    class Meta:
        verbose_name = '组权限'
        verbose_name_plural = verbose_name

    @classmethod
    def assign_perm(cls, code_or_obj, group):

        perm_group, is_new = PermGroup.objects.get_or_create(group=group)
        if is_new:
            perm_group.save()

        if isinstance(code_or_obj, str):
            perm = Perm.objects.filter(code=code_or_obj).first()
            if perm:
                perm_group.perm.add(perm)

        elif isinstance(code_or_obj, Perm):
            perm = code_or_obj
            perm_group.perm.add(perm)

    @classmethod
    def has_perm(cls, perm_code, group):

        perm_group = PermGroup.objects.filter(group=group).first()
        if perm_group:
            check_obj = perm_group.perm.all().filter(code=perm_code)
        else:
            check_obj = None
        res = True if check_obj else False
        return res


class PermUser(models.Model):

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
    )

    perm = models.ManyToManyField(
        Perm,
        blank=True
    )

    class Meta:
        verbose_name = '用户权限'
        verbose_name_plural = verbose_name

    @classmethod
    def assign_perm(cls, code_or_obj, user):
        perm_user, is_new = cls.objects.get_or_create(user=user)
        if is_new:
            perm_user.save()

        if isinstance(code_or_obj, str):
            perm = Perm.objects.filter(code=code_or_obj).first()
            check_result = perm_user.perm.filter(code=code_or_obj)
            if not check_result and perm:
                perm_user.perm.add(perm)
        elif isinstance(code_or_obj, Perm):
            perm = code_or_obj
            check_result = perm_user.perm.filter(code=code_or_obj.code)
            if not check_result:
                perm_user.perm.add(perm)

    @classmethod
    def has_perm(cls, perm_code, user):
        res = True if cls.objects.filter(
            perm__code=perm_code, user=user).first() else False

        return res

    @classmethod
    def user_perm(cls, user, is_code=True):
        perm_user = cls.objects.filter(user=user).first()

        perm_list = []
        if perm_user:
            if is_code:
                perm_list = [i.code for i in perm_user.perm.all()]
            else:
                perm_list = perm_user

        return perm_list


class PermUserObj(models.Model):

    perm = models.ForeignKey(
        Perm,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    obj_id = models.IntegerField(
        verbose_name='对象id',
    )

    class Meta:
        verbose_name = '用户对象权限'
        verbose_name_plural = verbose_name

    @classmethod
    def has_perm(cls, perm_code, content_type, obj_id, user):
        res = True if cls.objects.filter(
            perm__code=perm_code,
            content_type__model=content_type,
            obj_id=obj_id,
            user=user).first() else False

        return res

    @classmethod
    def get_obj_from_perm(cls, perm_code, content_type_model,
                          user, result_id=True):
        """获取对应权限对象"""
        content_type = ContentType.objects.filter(
            model=content_type_model).first()

        perm_user_obj = cls.objects.filter(
            perm__code=perm_code,
            content_type__model=content_type, user=user)
        obj_id_list = [i.obj_id for i in perm_user_obj]

        result = []

        if result_id:
            result = obj_id_list
        else:

            obj_model = content_type.model_class()

            result = obj_model.objects.filter(id__in=obj_id_list)

        return result


class PermStrategy(models.Model):

    SYSTEM_NUM = 1
    PARENT_NUM = 2

    GROUP_BASE = (
        (SYSTEM_NUM, af.SYSTEM_PERM_STRATEGY),
        (PARENT_NUM, af.PARENT_PERM_STRATEGY),
    )

    name = models.CharField(
        max_length=200,
        default='',
        verbose_name='名称',
    )

    creator_username = models.CharField(
        max_length=200,
        default='',
        verbose_name='操作用户',
        null=True,
        blank=True
    )

    strategy_type = models.IntegerField(
        default=SYSTEM_NUM,
        choices=GROUP_BASE,
        verbose_name='策略类型',
    )

    perm = models.ManyToManyField(
        Perm,
        related_name='权限集合',
        blank=True
    )

    remark = models.CharField(
        max_length=200,
        default='',
        verbose_name='备注',
        blank=True
    )

    class Meta:
        verbose_name = '权限策略'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s>>%s' % (
            self.name, self.creator_username
            if self.creator_username else 'system')

    @property
    def strategy_type_name(self):
        name = ''
        for i in self.GROUP_BASE:
            if self.strategy_type == i[0]:
                name = i[1]
                break
        return name

    @classmethod
    def strategy_type_dict(cls):
        type_list = []
        for i in cls.GROUP_BASE:
            type_list.append({'id': i[0], 'name': i[1]})
        return type_list


class UserPermStrategy(models.Model):

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
    )

    perm_strategy = models.ManyToManyField(
        PermStrategy,
        blank=True
    )

    class Meta:
        verbose_name = '用户权限策略关系'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % self.user.username

    @classmethod
    def assign_perm(cls, perm_strategy_ids, user):
        perm_strategy_list = PermStrategy.objects.filter(
            id__in=perm_strategy_ids)
        user_perm_strategy, is_new = cls.objects.get_or_create(user=user)
        if not is_new:
            user_perm_strategy.perm_strategy.clear()

        user_perm_strategy.save()

        for i in perm_strategy_list:
            user_perm_strategy.perm_strategy.add(i)

    @classmethod
    def has_perm(cls, perm_code, user):
        res = False
        user_perm_strategy = cls.objects.filter(user=user).first()

        for i in user_perm_strategy.perm_strategy.all():
            check_perm = i.perm.filter(code=perm_code)
            if check_perm:
                res = True
                break
        return res


class OperateLog(models.Model):

    user = models.ForeignKey(
        UserProfile,
        verbose_name='操作用户',
        on_delete=models.CASCADE
    )

    user_type = models.CharField(
        max_length=200,
        default='',
        verbose_name='操作用户',
        db_index=True
    )

    flag = models.CharField(
        max_length=20,
        verbose_name='功能标记',
    )

    info = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='描述',
    )

    from_ip = models.CharField(
        max_length=19,
        default='',
        verbose_name='操作ip',
    )

    ua = models.CharField(
        max_length=200,
        default='',
        verbose_name='浏览器信息',
    )

    add_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )

    class Meta:
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name

        index_together = ["user", "add_time"]

    def __str__(self):
        return '%s--%s' % (self.user.username, self.info)

    @staticmethod
    def write_operate_log(request, flag, info):
        """
        操作记录
        :param flag: 模块名称
        :param request: views request object
        :param info: 操作记录
        :return:
        """
        try:
            user = request.user

            user_type = ''
            if user.is_staff:
                user_type = 'is_admin'
            elif user.is_parent:
                user_type = 'is_parent'
            elif user.is_child:
                user_type = 'is_child'

            from_ip = request.META['REMOTE_ADDR']
            ua = request.META['HTTP_USER_AGENT']
            log = OperateLog(
                user=user, flag=flag, info=info, from_ip=from_ip, ua=ua,
                user_type=user_type)
            log.save()
        except Exception as e:
            print(e, request)
            pass

    @classmethod
    def get_operator_logs(cls, user_type='', username='',
                          start_time=None, end_time=None):
        """获取日志列表"""
        print(22222, user_type, username, start_time, end_time)
        import time
        start = time.time()
        if user_type:
            operator_logs = OperateLog.objects.filter(
                user_type=user_type)

        filter_dict = dict()
        if username:
            filter_dict['user__username'] = username

        if start_time and end_time:
            filter_dict['add_time__gte'] = start_time
            filter_dict['add_time__lte'] = end_time

        if filter_dict:
            operator_logs = operator_logs.filter(**filter_dict)

        operator_logs = operator_logs.order_by('-add_time')

        print(operator_logs)
        print(333333333, time.time()-start)

        operator_log_dict_list = []
        for i in operator_logs:
            print(111112233, i.id)
            log_dict = {
                'user': i.user.username,
                'flag': i.flag,
                'info': i.info,
                'from_ip': i.from_ip,
                'ua': i.ua,
                'add_time': str(i.add_time)[:19],
            }
            operator_log_dict_list.append(log_dict)
        
        print(444444444, time.time()-start)
        print(operator_log_dict_list)

        return operator_log_dict_list


class Domain(models.Model):

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='域名所属用户',
    )

    domain = models.CharField(
        max_length=255,
        blank=False,
        verbose_name=u'域名',
    )

    protocol = models.CharField(
        verbose_name=u'协议',
        max_length=255,
    )

    def __str__(self):
        return "%s>>%s" % (self.user.username, self.domain)

    class Meta:
        verbose_name = '域名信息'
        verbose_name_plural = verbose_name

    @classmethod
    def get_domain_query_by_user(cls, user):
        """获取域名列表"""

        # 管理员
        if user.is_staff:
            domain_query = cls.objects.all()

        # 父账号
        elif user.is_parent:
            child_list = UserProfile.objects.filter(
                parent_username=user.username)
            check_user_list = [i for i in child_list]
            check_user_list.append(user)
            domain_query = cls.objects.filter(user__in=check_user_list)
        # 子账号
        elif user.is_child:
            content_type_model = 'domain'
            perm_code = 'client_cdn_domain_list'
            domain_id_list = PermUserObj.get_obj_from_perm(
                perm_code, content_type_model, user)

            domain_query = cls.objects.filter(user=user)
            temp_id_list = [i.id for i in domain_query]
            domain_id_list.extend(temp_id_list)
            domain_id_list = list(set(domain_id_list))

            domain_query = cls.objects.filter(id__in=domain_id_list)

        return domain_query

    @property
    def channel(self):
        """频道"""
        return '%s://%s' % (self.protocol, self.domain)


class DomainStrategy(models.Model):

    domain = models.ForeignKey(
        Domain,
        on_delete=models.CASCADE,
        related_name='域名',
    )

    strategy = models.ForeignKey(
        Strategy,
        on_delete=models.CASCADE,
        related_name='策略',
    )

    def __str__(self):
        return "%s>>%s" % (self.domain.domain, self.strategy.id)

    class Meta:
        verbose_name = '域名策略关系'
        verbose_name_plural = verbose_name
