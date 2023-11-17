from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from config import views
from analytics.sentinelone import views as s1_analytics
from exports.sentinelone import views as s1_exports
from exports.freshservice import views as fresh_exports
from exports.bexio import views as bexio_exports
from exports.postgres import views as postgres_exports
from exports.jira import views as jira_exports
from licensing.sentinelone import views as s1_licensing
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


def redirect_to_docs(request):
    return redirect("/docs/")


admin.site.site_header = "AAOS"
admin.site.site_title = "AAOS"
admin.site.index_title = "Welcome"

router_main = routers.DefaultRouter()
router_main.register(r"users", views.UserViewSet)
router_main.register(r"groups", views.GroupViewSet)

router_config = routers.DefaultRouter()
router_config.register(r"s1", views.SentinelOneViewSet)
router_config.register(r"elastic", views.ElasticViewSet)
router_config.register(r"fresh", views.FreshServiceViewSet)
router_config.register(r"bexio", views.BexioViewSet)
router_config.register(r"sharepoint", views.SharePointViewSet)
router_config.register(r"loki", views.LokiViewSet)
router_config.register(r"dataset", views.DataSetViewSet)
router_config.register(r"postgres", views.PostgresViewSet)
router_config.register(r"jira", views.JiraViewSet)
router_config.register(r"crontabschedule", views.CrontabScheduleViewSet)
router_config.register(r"intervalschedule", views.IntervalScheduleViewSet)
router_config.register(r"periodictask", views.PeriodicTaskViewSet)

router_analytics = routers.DefaultRouter()
router_analytics.register(r"s1", s1_analytics.ExportViewSet, "analytics_s1")
router_analytics.register(
    r"s1-debug", s1_analytics.ExportViewSetDebug, "analytics_s1_debug"
)

router_exports = routers.DefaultRouter()
router_exports.register(r"bexio", bexio_exports.ExportViewSet, "exports_bexio")
router_exports.register(
    r"bexio-debug", bexio_exports.ExportViewSetDebug, "exports_bexio_debug"
)
router_exports.register(r"fresh", fresh_exports.ExportViewSet, "exports_fresh")
router_exports.register(
    r"fresh-debug", fresh_exports.ExportViewSetDebug, "exports_fresh_debug"
)
router_exports.register(r"s1", s1_exports.ExportViewSet, "exports_s1")
router_exports.register(r"postgres", postgres_exports.ExportViewSet, "exports_postgres")
router_exports.register(r"jira", jira_exports.ExportViewSet, "exports_jira")

router_licensing = routers.DefaultRouter()
router_licensing.register(r"s1", s1_licensing.ExportViewSet, "licensing_s1")
router_licensing.register(
    r"s1-debug", s1_licensing.ExportViewSetDebug, "licensing_s1_debug"
)

urlpatterns = [
    path("", redirect_to_docs, name="redirect-to-docs"),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("users/", include(router_main.urls)),
    path("config/", include(router_config.urls)),
    path("analytics/", include(router_analytics.urls)),
    path("exports/", include(router_exports.urls)),
    path("licensing/", include(router_licensing.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "openapi",
        get_schema_view(
            title="AAOS",
            description="Analysis, Automation and Orchestration System",
            version="0.1.8",
        ),
        name="openapi-schema",
    ),
    path(
        "swagger-ui/",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
