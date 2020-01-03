"""fuse_nova URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.views.generic import TemplateView

from django.views.i18n import JavaScriptCatalog
from django.conf.urls.i18n import i18n_patterns
from django.urls import path

urlpatterns = [

    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),

    url(r'^$',
        TemplateView.as_view(template_name='base/customer_login.html'),
        name='home'),

    url(r'^admin/', admin.site.urls),

    # 基础功能
    url(r'^base/', include('base.urls')),
    # 安全
    url(r'^sec/', include('security.urls')),
    # 证书
    url(r'^cert/', include('cert.urls')),
    # cdn功能
    url(r'^cdn/', include('cdn.urls')),
    # (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^i18n/', include('django.conf.urls.i18n')),

]


