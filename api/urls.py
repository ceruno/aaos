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

router_analytics = routers.DefaultRouter()
router_analytics.register(r's1', s1_analytics.ExportViewSet, 'analytics_s1')
router_analytics.register(r's1-debug', s1_analytics.ExportViewSetDebug, 'analytics_s1_debug')

router_exports = routers.DefaultRouter()
router_exports.register(r'bexio', bexio_exports.ExportViewSet, 'exports_bexio')
router_exports.register(r'bexio-debug', bexio_exports.ExportViewSetDebug, 'exports_bexio_debug')
router_exports.register(r'fresh', fresh_exports.ExportViewSet, 'exports_fresh')
router_exports.register(r'fresh-debug', fresh_exports.ExportViewSetDebug, 'exports_fresh_debug')
router_exports.register(r's1', s1_exports.ExportViewSet, 'exports_s1')
router_exports.register(r's1-debug', s1_exports.ExportViewSetDebug, 'exports_s1_debug')

router_licensing = routers.DefaultRouter()
router_licensing.register(r's1', s1_licensing.ExportViewSet, 'licensing_s1')
router_licensing.register(r's1-debug', s1_licensing.ExportViewSetDebug, 'licensing_s1_debug')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(router_main.urls)),
    path('config/', include(router_config.urls)),
    path('analytics/', include(router_analytics.urls)),
    path('exports/', include(router_exports.urls)),
    path('licensing/', include(router_licensing.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += staticfiles_urlpatterns()