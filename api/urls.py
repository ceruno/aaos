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
from config import views
from analytics.sentinelone import views as s1_analytics
from exports.sentinelone import views as s1_exports
from exports.freshservice import views as fresh_exports
from exports.bexio import views as bexio_exports
from licensing.sentinelone import views as s1_licensing
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


router_main = routers.DefaultRouter()
router_main.register(r'users', views.UserViewSet)
router_main.register(r'groups', views.GroupViewSet)

router_config = routers.DefaultRouter()
router_config.register(r's1', views.SentinelOneViewSet)
router_config.register(r'elastic', views.ElasticViewSet)
router_config.register(r'fresh', views.FreshServiceViewSet)
router_config.register(r'bexio', views.BexioViewSet)
router_config.register(r'sharepoint', views.SharePointViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(router_main.urls)),
    path('config/', include(router_config.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('analytics/s1', s1_analytics.main),
    path('analytics/s1-debug', s1_analytics.debug),
    path('exports/s1', s1_exports.main),
    path('exports/s1-debug', s1_exports.debug),
    path('exports/fresh', fresh_exports.main),
    path('exports/fresh-debug', fresh_exports.debug),
    path('exports/bexio', bexio_exports.main),
    path('exports/bexio-debug', bexio_exports.debug),
    path('licensing/s1', s1_licensing.main),
    path('licensing/s1-debug', s1_licensing.debug),
]

urlpatterns += staticfiles_urlpatterns()