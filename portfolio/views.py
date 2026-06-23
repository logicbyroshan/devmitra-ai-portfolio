from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

# Import all models from your models.py
from .models import (
    Technology,
    Experience,
    Project,
    FAQ,
    Category,
    NewsletterSubscriber,
    Achievement,
    SiteConfiguration,
    Resume,
    VideoResume,
    ContactSubmission,
)

# Import all forms from your forms.py
from .forms import ContactForm, NewsletterForm


# =========================================================================
# HOME PAGE VIEW
# =========================================================================
class HomeView(TemplateView):
    """View for the homepage. Gathers context from multiple models."""

    template_name = "portfolio-home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["skills"] = Technology.objects.all().order_by("name")
        context["experiences"] = Experience.objects.order_by("-start_date")[:3]
        context["projects"] = Project.objects.order_by("-created_date")[:3]
        context["achievements"] = Achievement.objects.order_by("-date_issued")[:3]
        from blog.models import Blog

        context["blogs"] = Blog.objects.order_by("-created_date")[:3]
        return context


# =========================================================================
# PROJECT VIEWS
# =========================================================================
class ProjectListView(ListView):
    """View for the main projects list page with filtering and pagination."""

    model = Project
    template_name = "projects-list.html"
    context_object_name = "projects"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_published=True)
        category_slug = self.request.GET.get("category")
        if category_slug and category_slug != "all":
            queryset = queryset.filter(
                categories__slug=category_slug, categories__category_type="PRO"
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
            category_type=Category.CategoryType.PROJECT
        )
        return context


class ProjectDetailView(DetailView):
    """View for a single project detail page."""

    model = Project
    template_name = "project-detail.html"
    context_object_name = "project"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Project.objects.filter(is_published=True)


# =========================================================================
# EXPERIENCE VIEWS
# =========================================================================
class ExperienceListView(ListView):
    """View for the main experience list page."""

    model = Experience
    template_name = "experience-list.html"
    context_object_name = "experiences"
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        exp_type = self.request.GET.get("category")
        if exp_type and exp_type != "all":
            queryset = queryset.filter(experience_type=exp_type)

        sort_by = self.request.GET.get("sort", "newest")
        if sort_by == "oldest":
            queryset = queryset.order_by("start_date")
        else:
            queryset = queryset.order_by("-start_date")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["experience_types"] = Category.objects.filter(
            category_type=Category.CategoryType.EXPERIENCE
        )
        return context


class ExperienceDetailView(DetailView):
    """View for a single experience dtl page."""

    model = Experience
    template_name = "experience-detail.html"
    context_object_name = "experience"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experience = self.get_object()
        # Get related experiences (excluding current one, limit to 3)
        context["related_experiences"] = Experience.objects.exclude(
            id=experience.id
        ).order_by("-start_date")[:3]
        return context


# =========================================================================
# FORM HANDLING & API-LIKE VIEWS
# =========================================================================
class ContactSubmissionView(View):
    """Handles the submission of the main contact form."""

    @method_decorator(ratelimit(key="ip", rate="5/m", method="POST", block=True))
    def post(self, request, *args, **kwargs):
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {
                        "status": "success",
                        "message": "Thank you for your message! I'll get back to you soon.",
                    }
                )
            else:
                errors = []
                for field, field_errors in form.errors.items():
                    for error in field_errors:
                        errors.append(f"{field}: {error}")
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Please check the fields: " + ", ".join(errors),
                    },
                    status=400,
                )
        else:
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Thank you for your message! I'll get back to you soon."
                )
            else:
                messages.error(
                    request,
                    "There was an error. Please check the fields and try again.",
                )
            return redirect(reverse("portfolio:home") + "#contact")


class NewsletterSubscribeHomeView(View):
    """Handles the submission of the newsletter form on the homepage."""

    @method_decorator(ratelimit(key="ip", rate="5/m", method="POST", block=True))
    def post(self, request, *args, **kwargs):
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            form = NewsletterForm(request.POST)
            if form.is_valid():
                subscriber, created = NewsletterSubscriber.objects.get_or_create(
                    email=form.cleaned_data["email"]
                )
                if created:
                    return JsonResponse(
                        {
                            "status": "success",
                            "message": "Thanks for subscribing! You'll receive updates soon.",
                        }
                    )
                else:
                    return JsonResponse(
                        {"status": "info", "message": "You are already subscribed!"}
                    )
            else:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Please provide a valid email address.",
                    },
                    status=400,
                )
        else:
            form = NewsletterForm(request.POST)
            if form.is_valid():
                subscriber, created = NewsletterSubscriber.objects.get_or_create(
                    email=form.cleaned_data["email"]
                )
                if created:
                    messages.success(request, "Thanks for subscribing!")
                else:
                    messages.info(request, "You are already subscribed!")
            else:
                messages.error(request, "Please provide a valid email address.")
            return redirect(reverse("portfolio:home") + "#newsletter")


class NewsletterSubscribeAjaxView(View):
    """Handles AJAX requests for newsletter subscriptions from the modal."""

    @method_decorator(ratelimit(key="ip", rate="5/m", method="POST", block=True))
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email", "").strip()
        try:
            validate_email(email)
        except DjangoValidationError:
            return JsonResponse(
                {"success": False, "message": "Please enter a valid email address."},
                status=400,
            )

        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)

        if created:
            message = "Thank you for subscribing!"
        else:
            message = "You are already subscribed!"

        return JsonResponse({"success": True, "message": message})


class AchievementListView(ListView):
    model = Achievement
    template_name = "achievements-list.html"
    context_object_name = "achievements"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.GET.get("category")
        if category and category != "all":
            queryset = queryset.filter(category__id=category)

        sort_by = self.request.GET.get("sort", "newest")
        if sort_by == "oldest":
            queryset = queryset.order_by("date_issued")
        else:
            queryset = queryset.order_by("-date_issued")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["achievement_categories"] = Category.objects.filter(
            category_type=Category.CategoryType.ACHIEVEMENT
        )
        return context


# ======================= CUSTOM ERROR HANDLERS =======================


def custom_bad_request(request, exception=None):
    """
    Custom 400 Bad Request error handler.
    """
    return render(request, "400.html", status=400)


def custom_permission_denied(request, exception=None):
    """
    Custom 403 Permission Denied error handler.
    """
    return render(request, "403.html", status=403)


def custom_page_not_found(request, exception=None):
    """
    Custom 404 Page Not Found error handler.
    """
    return render(request, "404.html", status=404)


def custom_server_error(request):
    """
    Custom 500 Server Error handler.
    """
    return render(request, "500.html", status=500)
