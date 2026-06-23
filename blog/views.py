from django.views.generic import ListView, DetailView

from .models import Blog
from portfolio.models import Category


class BlogListView(ListView):
    """View for the main blog list page with filtering and pagination."""

    model = Blog
    template_name = "blog-list.html"
    context_object_name = "blogs"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get("category")
        if category_slug and category_slug != "all":
            queryset = queryset.filter(
                categories__slug=category_slug, categories__category_type="BLG"
            )

        sort_by = self.request.GET.get("sort", "newest")
        if sort_by == "oldest":
            queryset = queryset.order_by("created_date")
        else:
            queryset = queryset.order_by("-created_date")

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(
            category_type=Category.CategoryType.BLOG
        )
        return context


class BlogDetailView(DetailView):
    """View for a single blog post detail page."""

    model = Blog
    template_name = "blog-detail.html"
    context_object_name = "blog"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        post_categories = post.categories.all()
        context["suggested_posts"] = (
            Blog.objects.filter(categories__in=post_categories)
            .exclude(pk=post.pk)
            .distinct()
            .order_by("-created_date")[:2]
        )
        return context
