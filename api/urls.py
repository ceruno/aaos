"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from rest_framework import routers
from configuration import views
from s1_export import views as s1_views


router_main = routers.DefaultRouter()
router_main.register(r'users', views.UserViewSet)
router_main.register(r'groups', views.GroupViewSet)

router_config = routers.DefaultRouter()
router_config.register(r's1', views.SentinelOneViewSet)
router_config.register(r'elastic', views.ElasticViewSet)
router_config.register(r'fresh', views.FreshServiceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router_main.urls)),
    path('config/', include(router_config.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('test/', s1_views.agents)
]

urlpatterns += staticfiles_urlpatterns()