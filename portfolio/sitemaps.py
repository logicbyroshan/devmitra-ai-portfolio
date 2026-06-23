from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project, Achievement, Experience


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""

    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "portfolio:home",
            "portfolio:project_list",
            "portfolio:experience_list",
            "portfolio:achievements_list",
        ]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    """Sitemap for projects"""

    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Project.objects.all().order_by("-created_date")

    def lastmod(self, obj):
        return obj.created_date

    def location(self, obj):
        return reverse("portfolio:project_detail", kwargs={"slug": obj.slug})


class ExperienceSitemap(Sitemap):
    """Sitemap for experiences"""

    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Experience.objects.all().order_by("-start_date")

    def lastmod(self, obj):
        return obj.start_date

    def location(self, obj):
        return reverse("portfolio:experience_detail", kwargs={"pk": obj.pk})


class AchievementSitemap(Sitemap):
    """Sitemap for achievements"""

    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Achievement.objects.all().order_by("-date_issued")

    def lastmod(self, obj):
        return obj.date_issued

    def location(self, obj):
        # Achievements might not have detail pages, but include in sitemap for list page filtering
        return reverse("portfolio:achievements_list") + f"?achievement={obj.id}"
