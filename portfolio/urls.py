from django.urls import path
from .views import (
    # Page Views
    HomeView,
    ProjectListView,
    ProjectDetailView,
    ExperienceListView,
    ExperienceDetailView,
    AchievementListView,
    # Form/API Views
    ContactSubmissionView,
    NewsletterSubscribeHomeView,
    NewsletterSubscribeAjaxView,
)

app_name = "portfolio"

urlpatterns = [
    # Home Page
    path("", HomeView.as_view(), name="home"),
    # Project Pages
    path("projects/", ProjectListView.as_view(), name="project_list"),
    path("projects/<slug:slug>/", ProjectDetailView.as_view(), name="project_detail"),
    # Experience Pages
    path("experiences/", ExperienceListView.as_view(), name="experience_list"),
    path(
        "experience/<int:pk>/", ExperienceDetailView.as_view(), name="experience_detail"
    ),
    # Form Submission URLs
    path("contact-submit/", ContactSubmissionView.as_view(), name="contact_submit"),
    path(
        "subscribe-home/", NewsletterSubscribeHomeView.as_view(), name="subscribe_home"
    ),
    path("subscribe/", NewsletterSubscribeAjaxView.as_view(), name="subscribe_ajax"),
    path("achievements/", AchievementListView.as_view(), name="achievements_list"),
]
