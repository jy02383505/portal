from django.contrib import admin

# Register your models here.
from base.models import *


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'create_time', 'remark')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'remark')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'remark')


class StrategyAdmin(admin.ModelAdmin):
    list_display = ('provider', 'product', 'service')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')


class PermAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'code', 'content_type', 'desc',
        'level', 'order', 'is_menu', 'url', 'type_name')


class PermGroupAdmin(admin.ModelAdmin):
    list_display = ('group',)


class PermUserAdmin(admin.ModelAdmin):
    list_display = ('user',)


class PermStrategyAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator_username', 'strategy_type', 'remark')


class GroupProfileAdmin(admin.ModelAdmin):
    list_display = ('group', 'creator_name', 'create_time', 'desc', 'remark')


admin.site.register(Provider, ProviderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Strategy, StrategyAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Perm, PermAdmin)

admin.site.register(PermGroup, PermGroupAdmin)
admin.site.register(PermUser, PermUserAdmin)
admin.site.register(PermStrategy, PermStrategyAdmin)
admin.site.register(GroupProfile, GroupProfileAdmin)
