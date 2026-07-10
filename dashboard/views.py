"""
Custom admin dashboard views.
All views are protected by @login_required.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from django_ratelimit.decorators import ratelimit

from portfolio.models import (
    Project, ProjectImage, Experience, Achievement,
    Category, Technology, SiteConfiguration, Resume, VideoResume,
    FAQ, ContactSubmission, NewsletterSubscriber,
)
from blog.models import Blog
from roshan.models import (
    AboutMeConfiguration, Resource, ResourceCategory, ResourcesConfiguration,
)
from ai.models import AIQuery, AIContext
from notifications.models import ContactNotification, NotificationSettings, EmailTemplate
from .forms import (
    ProjectForm, ProjectImageFormSet, BlogForm, ExperienceForm,
    SkillForm, FAQForm, AchievementForm, ResourceForm, ResourceCategoryForm,
    CategoryForm, BlogCategoryForm, AIContextForm, SiteConfigurationForm,
    AboutMeForm, ResumeForm, VideoResumeForm, NotificationSettingsForm,
    EmailTemplateForm, ResourcesConfigForm, DashboardLoginForm, TechnologyForm,
)


# ═══════════════════════════════════════════════════════════════
# AUTHENTICATION
# ═══════════════════════════════════════════════════════════════

@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    form = DashboardLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user is not None and user.is_staff:
            auth_login(request, user)
            return redirect(request.GET.get('next') or 'dashboard:index')
        messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'dashboard/login.html', {'form': form})


@require_POST
@login_required(login_url='dashboard:login')
def dashboard_logout(request):
    auth_logout(request)
    return redirect('dashboard:login')


# ═══════════════════════════════════════════════════════════════
# DASHBOARD HOME
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='dashboard:login')
def dashboard_index(request):
    total_messages = ContactSubmission.objects.count()
    unread_messages = ContactSubmission.objects.filter(is_read=False).count()
    stats = {
        'projects': Project.objects.count(),
        'blogs': Blog.objects.count(),
        'experiences': Experience.objects.count(),
        'skills': Technology.objects.count(),
        'achievements': Achievement.objects.count(),
        'resources': Resource.objects.count(),
        'ai_queries': AIQuery.objects.count(),
        'messages': total_messages,
        'unread_messages': unread_messages,
        'newsletter': NewsletterSubscriber.objects.count(),
    }
    recent_projects = Project.objects.only(
        'pk', 'title', 'is_published', 'created_date'
    ).order_by('-created_date')[:5]
    recent_blogs = Blog.objects.only(
        'pk', 'title', 'is_published', 'reading_time', 'created_date'
    ).order_by('-created_date')[:5]
    recent_messages = ContactSubmission.objects.only(
        'pk', 'name', 'email', 'message', 'submitted_date', 'is_read'
    ).order_by('-submitted_date')[:5]
    context = {
        'stats': stats,
        'recent_projects': recent_projects,
        'recent_blogs': recent_blogs,
        'recent_messages': recent_messages,
        'active_nav': 'dashboard',
    }
    return render(request, 'dashboard/index.html', context)


# ═══════════════════════════════════════════════════════════════
# PROJECTS
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='dashboard:login')
def projects_list(request):
    projects = Project.objects.prefetch_related('technologies', 'categories').order_by('-created_date')
    return render(request, 'dashboard/projects/list.html', {
        'projects': projects, 'active_nav': 'projects',
    })


@login_required(login_url='dashboard:login')
def project_create(request):
    form = ProjectForm(request.POST or None, request.FILES or None)
    image_formset = ProjectImageFormSet(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid() and image_formset.is_valid():
        project = form.save()
        image_formset.instance = project
        image_formset.save()
        messages.success(request, f'Project "{project.title}" created successfully.')
        return redirect('dashboard:projects_list')
    return render(request, 'dashboard/projects/form.html', {
        'form': form, 'image_formset': image_formset, 'active_nav': 'projects',
    })


@login_required(login_url='dashboard:login')
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, request.FILES or None, instance=project)
    image_formset = ProjectImageFormSet(request.POST or None, request.FILES or None, instance=project)
    if request.method == 'POST' and form.is_valid() and image_formset.is_valid():
        form.save()
        image_formset.save()
        messages.success(request, f'Project "{project.title}" updated.')
        return redirect('dashboard:projects_list')
    return render(request, 'dashboard/projects/form.html', {
        'form': form, 'image_formset': image_formset, 'project': project, 'active_nav': 'projects',
    })


@login_required(login_url='dashboard:login')
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f'Project "{title}" deleted.')
        return redirect('dashboard:projects_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'Project', 'object_label': project.title,
        'cancel_url': reverse('dashboard:projects_list'),
        'active_nav': 'projects',
    })


@require_POST
@login_required(login_url='dashboard:login')
def project_toggle_published(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.is_published = not project.is_published
    project.save(update_fields=['is_published'])
    return JsonResponse({'status': 'ok', 'is_published': project.is_published})


# ═══════════════════════════════════════════════════════════════
# BLOG
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='dashboard:login')
def blog_list(request):
    posts = Blog.objects.prefetch_related('categories').order_by('-created_date')
    return render(request, 'dashboard/blog/list.html', {
        'posts': posts, 'active_nav': 'blog',
    })


@login_required(login_url='dashboard:login')
def blog_create(request):
    form = BlogForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save()
        messages.success(request, f'Article "{post.title}" created.')
        return redirect('dashboard:blog_list')
    return render(request, 'dashboard/blog/form.html', {
        'form': form, 'active_nav': 'blog',
    })


@login_required(login_url='dashboard:login')
def blog_edit(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    form = BlogForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Article "{post.title}" updated.')
        return redirect('dashboard:blog_list')
    return render(request, 'dashboard/blog/form.html', {
        'form': form, 'post': post, 'active_nav': 'blog',
    })


@login_required(login_url='dashboard:login')
def blog_delete(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f'Article "{title}" deleted.')
        return redirect('dashboard:blog_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'Blog Post', 'object_label': post.title,
        'cancel_url': reverse('dashboard:blog_list'),
        'active_nav': 'blog',
    })


@require_POST
@login_required(login_url='dashboard:login')
def blog_toggle_published(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.is_published = not post.is_published
    post.save(update_fields=['is_published'])
    return JsonResponse({'status': 'ok', 'is_published': post.is_published})


@login_required(login_url='dashboard:login')
def blog_categories_list(request):
    categories = Category.objects.filter(category_type='BLG').order_by('name')
    return render(request, 'dashboard/blog/categories_list.html', {
        'categories': categories, 'active_nav': 'blog_categories',
    })


@login_required(login_url='dashboard:login')
def blog_category_create(request):
    form = BlogCategoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cat = form.save()
        messages.success(request, f'Category "{cat.name}" created.')
        return redirect('dashboard:blog_categories_list')
    return render(request, 'dashboard/blog/category_form.html', {
        'form': form, 'active_nav': 'blog_categories',
    })


@login_required(login_url='dashboard:login')
def blog_category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk, category_type='BLG')
    form = BlogCategoryForm(request.POST or None, instance=category)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Category "{category.name}" updated.')
        return redirect('dashboard:blog_categories_list')
    return render(request, 'dashboard/blog/category_form.html', {
        'form': form, 'category': category, 'active_nav': 'blog_categories',
    })


@login_required(login_url='dashboard:login')
def blog_category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, category_type='BLG')
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('dashboard:blog_categories_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'Blog Category', 'object_label': category.name,
        'cancel_url': reverse('dashboard:blog_categories_list'),
        'active_nav': 'blog_categories',
    })


# ═══════════════════════════════════════════════════════════════
# EXPERIENCE
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='dashboard:login')
def experience_list(request):
    experiences = Experience.objects.select_related('experience_type').prefetch_related('technologies').order_by('-start_date')
    return render(request, 'dashboard/experience/list.html', {
        'experiences': experiences, 'active_nav': 'experience',
    })


@login_required(login_url='dashboard:login')
def experience_create(request):
    form = ExperienceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        exp = form.save()
        messages.success(request, f'Experience at {exp.company_name} created.')
        return redirect('dashboard:experience_list')
    return render(request, 'dashboard/experience/form.html', {
        'form': form, 'active_nav': 'experience',
    })


@login_required(login_url='dashboard:login')
def experience_edit(request, pk):
    exp = get_object_or_404(Experience, pk=pk)
    form = ExperienceForm(request.POST or None, instance=exp)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Experience at {exp.company_name} updated.')
        return redirect('dashboard:experience_list')
    return render(request, 'dashboard/experience/form.html', {
        'form': form, 'exp': exp, 'active_nav': 'experience',
    })


@login_required(login_url='dashboard:login')
def experience_delete(request, pk):
    exp = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        exp.delete()
        messages.success(request, 'Experience deleted.')
        return redirect('dashboard:experience_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'Experience',
        'object_label': f'{exp.role} at {exp.company_name}',
        'cancel_url': reverse('dashboard:experience_list'),
        'active_nav': 'experience',
    })


@require_POST
@login_required(login_url='dashboard:login')
def experience_toggle_visible(request, pk):
    exp = get_object_or_404(Experience, pk=pk)
    exp.is_visible = not exp.is_visible
    exp.save(update_fields=['is_visible'])
    return JsonResponse({'status': 'ok', 'is_visible': exp.is_visible})


# ═══════════════════════════════════════════════════════════════
# SKILLS
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='dashboard:login')
def skills_list(request):
    skills = Technology.objects.order_by('name')
    return render(request, 'dashboard/skills/list.html', {
        'skills': skills, 'active_nav': 'skills',
    })


@login_required(login_url='dashboard:login')
def skill_create(request):
    form = SkillForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        skill = form.save()
        messages.success(request, f'Skill "{skill.name}" created.')
        return redirect('dashboard:skills_list')
    return render(request, 'dashboard/skills/form.html', {
        'form': form, 'active_nav': 'skills',
    })


@login_required(login_url='dashboard:login')
def skill_edit(request, pk):
    skill = get_object_or_404(Technology, pk=pk)
    form = SkillForm(request.POST or None, request.FILES or None, instance=skill)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Skill "{skill.name}" updated.')
        return redirect('dashboard:skills_list')
    return render(request, 'dashboard/skills/form.html', {
        'form': form, 'skill': skill, 'active_nav': 'skills',
    })


@login_required(login_url='dashboard:login')
def skill_delete(request, pk):
    skill = get_object_or_404(Technology, pk=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted.')
        return redirect('dashboard:skills_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'Skill', 'object_label': skill.name,
        'cancel_url': reverse('dashboard:skills_list'),
        'active_nav': 'skills',
    })


@login_required(login_url='dashboard:login')
def faq_list(request):
    faqs = FAQ.objects.order_by('order')
    return render(request, 'dashboard/skills/faq_list.html', {
        'faqs': faqs, 'active_nav': 'faqs',
    })


@login_required(login_url='dashboard:login')
def faq_create(request):
    form = FAQForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'FAQ created.')
        return redirect('dashboard:faq_list')
    return render(request, 'dashboard/skills/faq_form.html', {
        'form': form, 'active_nav': 'faqs',
    })


@login_required(login_url='dashboard:login')
def faq_edit(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    form = FAQForm(request.POST or None, instance=faq)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'FAQ updated.')
        return redirect('dashboard:faq_list')
    return render(request, 'dashboard/skills/faq_form.html', {
        'form': form, 'faq': faq, 'active_nav': 'faqs',
    })


@login_required(login_url='dashboard:login')
def faq_delete(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        faq.delete()
        messages.success(request, 'FAQ deleted.')
        return redirect('dashboard:faq_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'FAQ', 'object_label': faq.question[:80],
        'cancel_url': reverse('dashboard:faq_list'),
        'active_nav': 'faqs',
    })


# ═══════════════════════════════════════════════════════════════
# ACHIEVEMENTS
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='dashboard:login')
def achievements_list(request):
    achievements = Achievement.objects.select_related('category').order_by('-date_issued')
    return render(request, 'dashboard/achievements/list.html', {
        'achievements': achievements, 'active_nav': 'achievements',
    })


@login_required(login_url='dashboard:login')
def achievement_create(request):
    form = AchievementForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        ach = form.save()
        messages.success(request, f'Achievement "{ach.title}" created.')
        return redirect('dashboard:achievements_list')
    return render(request, 'dashboard/achievements/form.html', {
        'form': form, 'active_nav': 'achievements',
    })


@login_required(login_url='dashboard:login')
def achievement_edit(request, pk):
    ach = get_object_or_404(Achievement, pk=pk)
    form = AchievementForm(request.POST or None, request.FILES or None, instance=ach)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Achievement "{ach.title}" updated.')
        return redirect('dashboard:achievements_list')
    return render(request, 'dashboard/achievements/form.html', {
        'form': form, 'ach': ach, 'active_nav': 'achievements',
    })


@login_required(login_url='dashboard:login')
def achievement_delete(request, pk):
    ach = get_object_or_404(Achievement, pk=pk)
    if request.method == 'POST':
        ach.delete()
        messages.success(request, 'Achievement deleted.')
        return redirect('dashboard:achievements_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'Achievement', 'object_label': ach.title,
        'cancel_url': reverse('dashboard:achievements_list'),
        'active_nav': 'achievements',
    })


@require_POST
@login_required(login_url='dashboard:login')
def achievement_toggle_visible(request, pk):
    ach = get_object_or_404(Achievement, pk=pk)
    ach.is_visible = not ach.is_visible
    ach.save(update_fields=['is_visible'])
    return JsonResponse({'status': 'ok', 'is_visible': ach.is_visible})


# ═══════════════════════════════════════════════════════════════
# RESOURCES
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='dashboard:login')
def resources_list(request):
    resources = Resource.objects.prefetch_related('categories').order_by('order', '-created_date')
    return render(request, 'dashboard/resources/list.html', {
        'resources': resources, 'active_nav': 'resources',
    })


@login_required(login_url='dashboard:login')
def resource_create(request):
    form = ResourceForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        resource = form.save()
        messages.success(request, f'Resource "{resource.title}" created.')
        return redirect('dashboard:resources_list')
    return render(request, 'dashboard/resources/form.html', {
        'form': form, 'active_nav': 'resources',
    })


@login_required(login_url='dashboard:login')
def resource_edit(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    form = ResourceForm(request.POST or None, request.FILES or None, instance=resource)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Resource "{resource.title}" updated.')
        return redirect('dashboard:resources_list')
    return render(request, 'dashboard/resources/form.html', {
        'form': form, 'resource': resource, 'active_nav': 'resources',
    })


@login_required(login_url='dashboard:login')
def resource_delete(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        resource.delete()
        messages.success(request, 'Resource deleted.')
        return redirect('dashboard:resources_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'Resource', 'object_label': resource.title,
        'cancel_url': reverse('dashboard:resources_list'),
        'active_nav': 'resources',
    })


@require_POST
@login_required(login_url='dashboard:login')
def resource_toggle_active(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    resource.is_active = not resource.is_active
    resource.save(update_fields=['is_active'])
    return JsonResponse({'status': 'ok', 'is_active': resource.is_active})


@require_POST
@login_required(login_url='dashboard:login')
def resource_toggle_featured(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    resource.is_featured = not resource.is_featured
    resource.save(update_fields=['is_featured'])
    return JsonResponse({'status': 'ok', 'is_featured': resource.is_featured})


@login_required(login_url='dashboard:login')
def resource_categories_list(request):
    categories = ResourceCategory.objects.order_by('order', 'name')
    return render(request, 'dashboard/resources/categories_list.html', {
        'categories': categories, 'active_nav': 'resource_categories',
    })


@login_required(login_url='dashboard:login')
def resource_category_create(request):
    form = ResourceCategoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cat = form.save()
        messages.success(request, f'Category "{cat.name}" created.')
        return redirect('dashboard:resource_categories_list')
    return render(request, 'dashboard/resources/category_form.html', {
        'form': form, 'active_nav': 'resource_categories',
    })


@login_required(login_url='dashboard:login')
def resource_category_edit(request, pk):
    category = get_object_or_404(ResourceCategory, pk=pk)
    form = ResourceCategoryForm(request.POST or None, instance=category)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Category "{category.name}" updated.')
        return redirect('dashboard:resource_categories_list')
    return render(request, 'dashboard/resources/category_form.html', {
        'form': form, 'category': category, 'active_nav': 'resource_categories',
    })


@login_required(login_url='dashboard:login')
def resource_category_delete(request, pk):
    category = get_object_or_404(ResourceCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('dashboard:resource_categories_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'Resource Category', 'object_label': category.name,
        'cancel_url': reverse('dashboard:resource_categories_list'),
        'active_nav': 'resource_categories',
    })


# ═══════════════════════════════════════════════════════════════
# TAXONOMY
# ═══════════════════════════════════════════════════════════════

@require_POST
@login_required(login_url='dashboard:login')
def api_category_create(request):
    name = request.POST.get('name')
    category_type = request.POST.get('category_type')
    if not name or not category_type:
        return JsonResponse({'success': False, 'message': 'Missing data'})
    cat, created = Category.objects.get_or_create(name=name, category_type=category_type)
    return JsonResponse({'success': True, 'id': cat.id, 'name': cat.name})

@require_POST
@login_required(login_url='dashboard:login')
def api_technology_create(request):
    name = request.POST.get('name')
    if not name:
        return JsonResponse({'success': False, 'message': 'Missing data'})
    tech, created = Technology.objects.get_or_create(name=name)
    return JsonResponse({'success': True, 'id': tech.id, 'name': tech.name})

@login_required(login_url='dashboard:login')
def categories_list(request):
    categories = Category.objects.order_by('category_type', 'name')
    return render(request, 'dashboard/taxonomy/categories_list.html', {
        'categories': categories, 'active_nav': 'categories',
    })


@login_required(login_url='dashboard:login')
def category_create(request):
    form = CategoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cat = form.save()
        messages.success(request, f'Category "{cat.name}" created.')
        return redirect('dashboard:categories_list')
    return render(request, 'dashboard/taxonomy/category_form.html', {
        'form': form, 'active_nav': 'categories',
    })


@login_required(login_url='dashboard:login')
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Category "{category.name}" updated.')
        return redirect('dashboard:categories_list')
    return render(request, 'dashboard/taxonomy/category_form.html', {
        'form': form, 'category': category, 'active_nav': 'categories',
    })


@login_required(login_url='dashboard:login')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('dashboard:categories_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'Category', 'object_label': category.name,
        'cancel_url': reverse('dashboard:categories_list'),
        'active_nav': 'categories',
    })


@login_required(login_url='dashboard:login')
def technologies_list(request):
    technologies = Technology.objects.select_related('category').order_by('name')
    return render(request, 'dashboard/taxonomy/technologies_list.html', {
        'technologies': technologies, 'active_nav': 'technologies',
    })


@login_required(login_url='dashboard:login')
def technology_create(request):
    form = TechnologyForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        tech = form.save()
        messages.success(request, f'Technology "{tech.name}" created.')
        return redirect('dashboard:technologies_list')
    return render(request, 'dashboard/taxonomy/technology_form.html', {
        'form': form, 'active_nav': 'technologies',
    })


@login_required(login_url='dashboard:login')
def technology_edit(request, pk):
    technology = get_object_or_404(Technology, pk=pk)
    form = TechnologyForm(request.POST or None, request.FILES or None, instance=technology)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Technology "{technology.name}" updated.')
        return redirect('dashboard:technologies_list')
    return render(request, 'dashboard/taxonomy/technology_form.html', {
        'form': form, 'technology': technology, 'active_nav': 'technologies',
    })


@login_required(login_url='dashboard:login')
def technology_delete(request, pk):
    technology = get_object_or_404(Technology, pk=pk)
    if request.method == 'POST':
        technology.delete()
        messages.success(request, 'Technology deleted.')
        return redirect('dashboard:technologies_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'Technology', 'object_label': technology.name,
        'cancel_url': reverse('dashboard:technologies_list'),
        'active_nav': 'technologies',
    })


# ═══════════════════════════════════════════════════════════════
# CONTACTS & MESSAGES
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='dashboard:login')
def contacts_list(request):
    unread_count = ContactSubmission.objects.filter(is_read=False).count()
    contacts = ContactSubmission.objects.order_by('-submitted_date')
    return render(request, 'dashboard/contacts/list.html', {
        'contacts': contacts, 'unread_count': unread_count, 'active_nav': 'contacts',
    })


@login_required(login_url='dashboard:login')
def contact_detail(request, pk):
    contact = get_object_or_404(ContactSubmission, pk=pk)
    if not contact.is_read:
        contact.is_read = True
        contact.save(update_fields=['is_read'])
    return render(request, 'dashboard/contacts/detail.html', {
        'contact': contact, 'active_nav': 'contacts',
    })


@login_required(login_url='dashboard:login')
def contact_delete(request, pk):
    contact = get_object_or_404(ContactSubmission, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Message deleted.')
        return redirect('dashboard:contacts_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'Message',
        'object_label': f'from {contact.name}',
        'cancel_url': reverse('dashboard:contacts_list'),
        'active_nav': 'contacts',
    })


@require_POST
@login_required(login_url='dashboard:login')
def contact_mark_read(request, pk):
    contact = get_object_or_404(ContactSubmission, pk=pk)
    contact.is_read = not contact.is_read
    contact.save(update_fields=['is_read'])
    return redirect('dashboard:contact_detail', pk=pk)


@login_required(login_url='dashboard:login')
def newsletter_list(request):
    subscribers = NewsletterSubscriber.objects.order_by('-subscribed_date')
    return render(request, 'dashboard/contacts/newsletter.html', {
        'subscribers': subscribers, 'active_nav': 'newsletter',
    })


@login_required(login_url='dashboard:login')
def newsletter_delete(request, pk):
    subscriber = get_object_or_404(NewsletterSubscriber, pk=pk)
    if request.method == 'POST':
        email = subscriber.email
        subscriber.delete()
        messages.success(request, f'Subscriber "{email}" removed.')
        return redirect('dashboard:newsletter_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'Subscriber', 'object_label': subscriber.email,
        'cancel_url': reverse('dashboard:newsletter_list'),
        'active_nav': 'newsletter',
    })


# ═══════════════════════════════════════════════════════════════
# AI
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='dashboard:login')
def ai_queries_list(request):
    queries = AIQuery.objects.order_by('-created_at')
    return render(request, 'dashboard/ai/queries.html', {
        'queries': queries, 'active_nav': 'ai',
    })


@login_required(login_url='dashboard:login')
def ai_query_delete(request, pk):
    query = get_object_or_404(AIQuery, pk=pk)
    if request.method == 'POST':
        query.delete()
        messages.success(request, 'AI query deleted.')
        return redirect('dashboard:ai_queries_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'AI Query', 'object_label': query.question[:80],
        'cancel_url': reverse('dashboard:ai_queries_list'),
        'active_nav': 'ai',
    })


@login_required(login_url='dashboard:login')
def ai_context_list(request):
    contexts = AIContext.objects.order_by('title')
    return render(request, 'dashboard/ai/context_list.html', {
        'contexts': contexts, 'active_nav': 'ai_context',
    })


@login_required(login_url='dashboard:login')
def ai_context_create(request):
    form = AIContextForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        ctx = form.save()
        messages.success(request, f'AI context "{ctx.title}" created.')
        return redirect('dashboard:ai_context_list')
    return render(request, 'dashboard/ai/context_form.html', {
        'form': form, 'active_nav': 'ai_context',
    })


@login_required(login_url='dashboard:login')
def ai_context_edit(request, pk):
    context = get_object_or_404(AIContext, pk=pk)
    form = AIContextForm(request.POST or None, instance=context)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'AI context "{context.title}" updated.')
        return redirect('dashboard:ai_context_list')
    return render(request, 'dashboard/ai/context_form.html', {
        'form': form, 'context': context, 'active_nav': 'ai_context',
    })


@login_required(login_url='dashboard:login')
def ai_context_delete(request, pk):
    context = get_object_or_404(AIContext, pk=pk)
    if request.method == 'POST':
        context.delete()
        messages.success(request, 'AI context deleted.')
        return redirect('dashboard:ai_context_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'AI Context', 'object_label': context.title,
        'cancel_url': reverse('dashboard:ai_context_list'),
        'active_nav': 'ai_context',
    })


@require_POST
@login_required(login_url='dashboard:login')
def ai_context_toggle_active(request, pk):
    context = get_object_or_404(AIContext, pk=pk)
    context.is_active = not context.is_active
    context.save(update_fields=['is_active'])
    return JsonResponse({'status': 'ok', 'is_active': context.is_active})


# ═══════════════════════════════════════════════════════════════
# SETTINGS
# ═══════════════════════════════════════════════════════════════

@login_required(login_url='dashboard:login')
def settings_site(request):
    instance = SiteConfiguration.get_instance()
    form = SiteConfigurationForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Site configuration saved.')
        return redirect('dashboard:settings_site')
    return render(request, 'dashboard/settings/site.html', {
        'form': form, 'active_nav': 'settings_site',
    })


@login_required(login_url='dashboard:login')
def settings_about(request):
    instance, _ = AboutMeConfiguration.objects.get_or_create(pk=1)
    form = AboutMeForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'About Me configuration saved.')
        return redirect('dashboard:settings_about')
    return render(request, 'dashboard/settings/about.html', {
        'form': form, 'active_nav': 'settings_about',
    })


@login_required(login_url='dashboard:login')
def settings_resume(request):
    resume = Resume.objects.first()
    video_resume = VideoResume.objects.first()
    resume_form = ResumeForm(
        request.POST or None, request.FILES or None,
        instance=resume, prefix='resume',
    )
    video_form = VideoResumeForm(
        request.POST or None, request.FILES or None,
        instance=video_resume, prefix='video',
    )
    if request.method == 'POST':
        if resume_form.is_valid() and video_form.is_valid():
            resume_form.save()
            video_form.save()
            messages.success(request, 'Resume settings saved.')
            return redirect('dashboard:settings_resume')
    return render(request, 'dashboard/settings/resume.html', {
        'resume_form': resume_form, 'video_form': video_form,
        'resume': resume, 'video_resume': video_resume,
        'active_nav': 'settings_resume',
    })


@login_required(login_url='dashboard:login')
def settings_notifications(request):
    instance = NotificationSettings.get_settings()
    form = NotificationSettingsForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Notification settings saved.')
        return redirect('dashboard:settings_notifications')
    return render(request, 'dashboard/settings/notifications.html', {
        'form': form, 'active_nav': 'settings_notifications',
    })


@login_required(login_url='dashboard:login')
def settings_resources_config(request):
    instance = ResourcesConfiguration.objects.first()
    form = ResourcesConfigForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Resources page configuration saved.')
        return redirect('dashboard:settings_resources_config')
    return render(request, 'dashboard/settings/resources_config.html', {
        'form': form, 'active_nav': 'settings_resources',
    })


@login_required(login_url='dashboard:login')
def email_templates_list(request):
    templates = EmailTemplate.objects.order_by('template_type', 'name')
    return render(request, 'dashboard/settings/email_templates.html', {
        'templates': templates, 'active_nav': 'email_templates',
    })


@login_required(login_url='dashboard:login')
def email_template_create(request):
    form = EmailTemplateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        tmpl = form.save()
        messages.success(request, f'Template "{tmpl.name}" created.')
        return redirect('dashboard:email_templates_list')
    return render(request, 'dashboard/settings/email_template_form.html', {
        'form': form, 'active_nav': 'email_templates',
    })


@login_required(login_url='dashboard:login')
def email_template_edit(request, pk):
    template = get_object_or_404(EmailTemplate, pk=pk)
    form = EmailTemplateForm(request.POST or None, instance=template)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Template "{template.name}" updated.')
        return redirect('dashboard:email_templates_list')
    return render(request, 'dashboard/settings/email_template_form.html', {
        'form': form, 'template': template, 'active_nav': 'email_templates',
    })


@login_required(login_url='dashboard:login')
def email_template_delete(request, pk):
    template = get_object_or_404(EmailTemplate, pk=pk)
    if request.method == 'POST':
        template.delete()
        messages.success(request, 'Template deleted.')
        return redirect('dashboard:email_templates_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': 'Email Template', 'object_label': template.name,
        'cancel_url': reverse('dashboard:email_templates_list'),
        'active_nav': 'email_templates',
    })
