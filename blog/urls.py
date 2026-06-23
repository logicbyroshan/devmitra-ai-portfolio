from django.urls import path
from .views import BlogListView, BlogDetailView

app_name = 'blog'

urlpatterns = [
    # Blog Pages
    path('', BlogListView.as_view(), name='blog_list'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
]