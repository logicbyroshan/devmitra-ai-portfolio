from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from portfolio.sitemaps import (
    StaticViewSitemap,
    ProjectSitemap,
    ExperienceSitemap,
    AchievementSitemap,
)
from blog.sitemaps import BlogSitemap

# Sitemap configuration
sitemaps = {
    "static": StaticViewSitemap,
    "blogs": BlogSitemap,
    "projects": ProjectSitemap,
    "experiences": ExperienceSitemap,
    "achievements": AchievementSitemap,
}

urlpatterns = [
    path("panel/", include("dashboard.urls", namespace="dashboard")),
    path("auth/", include("authentication.urls", namespace="authentication")),
    path("", include("portfolio.urls")),
    path("blogs/", include("blog.urls")),
    path("ai/", include("ai.urls")),
    path("", include("roshan.urls")),
    # SEO URLs
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler400 = 'portfolio.views.custom_bad_request'
handler403 = 'portfolio.views.custom_permission_denied'
handler404 = 'portfolio.views.custom_page_not_found'
handler500 = 'portfolio.views.custom_server_error'
