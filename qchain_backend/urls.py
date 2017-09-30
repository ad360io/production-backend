"""qchain_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
import qchain_backend.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', qchain_backend.views.login3210, name='loginass1234'),
    url(r'^dashboard-stats/$', qchain_backend.views.dashboard_stats, name='dashboard-stats'),
    url(r'^dashboard-tables/$', qchain_backend.views.dashboard_tables, name='dashboard-tables'),
    url(r'^dashboard-charts/', qchain_backend.views.dashboard_charts, name='dashboard-charts'),
    url(r'^display-marketplace/$', qchain_backend.views.display_marketplace, name='display-marketplace'),
    url(r'^create-adspace/$', qchain_backend.views.create_adspace, name='create-adspace'),
    #url(r'^sites/(?P<web_id>[0-9]+)/$', qchain_backend.views.ad_list, name='ad_list'),
    #url(r'^api-token-auth/', obtain_jwt_token),

]

