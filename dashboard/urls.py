from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # ── Auth ──────────────────────────────────────────────────
    path('login/', views.dashboard_login, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),

    # ── Dashboard Home ────────────────────────────────────────
    path('', views.dashboard_index, name='index'),

    # ── Projects ──────────────────────────────────────────────
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/new/', views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('projects/<int:pk>/toggle-published/', views.project_toggle_published, name='project_toggle_published'),

    # ── Blog ──────────────────────────────────────────────────
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/new/', views.blog_create, name='blog_create'),
    path('blog/<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('blog/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    path('blog/<int:pk>/toggle-published/', views.blog_toggle_published, name='blog_toggle_published'),
    path('blog/categories/', views.blog_categories_list, name='blog_categories_list'),
    path('blog/categories/new/', views.blog_category_create, name='blog_category_create'),
    path('blog/categories/<int:pk>/edit/', views.blog_category_edit, name='blog_category_edit'),
    path('blog/categories/<int:pk>/delete/', views.blog_category_delete, name='blog_category_delete'),
    # ── Experience ────────────────────────────────────────────
    path('experience/', views.experience_list, name='experience_list'),
    path('experience/new/', views.experience_create, name='experience_create'),
    path('experience/<int:pk>/edit/', views.experience_edit, name='experience_edit'),
    path('experience/<int:pk>/delete/', views.experience_delete, name='experience_delete'),
    path('experience/<int:pk>/toggle-visible/', views.experience_toggle_visible, name='experience_toggle_visible'),

    # ── Skills ────────────────────────────────────────────────
    path('skills/', views.skills_list, name='skills_list'),
    path('skills/new/', views.skill_create, name='skill_create'),
    path('skills/<int:pk>/edit/', views.skill_edit, name='skill_edit'),
    path('skills/<int:pk>/delete/', views.skill_delete, name='skill_delete'),


    # ── FAQs ──────────────────────────────────────────────────
    path('faqs/', views.faq_list, name='faq_list'),
    path('faqs/new/', views.faq_create, name='faq_create'),
    path('faqs/<int:pk>/edit/', views.faq_edit, name='faq_edit'),
    path('faqs/<int:pk>/delete/', views.faq_delete, name='faq_delete'),

    # ── Achievements ──────────────────────────────────────────
    path('achievements/', views.achievements_list, name='achievements_list'),
    path('achievements/new/', views.achievement_create, name='achievement_create'),
    path('achievements/<int:pk>/edit/', views.achievement_edit, name='achievement_edit'),
    path('achievements/<int:pk>/delete/', views.achievement_delete, name='achievement_delete'),
    path('achievements/<int:pk>/toggle-visible/', views.achievement_toggle_visible, name='achievement_toggle_visible'),

    # ── Resources ─────────────────────────────────────────────
    path('resources/', views.resources_list, name='resources_list'),
    path('resources/new/', views.resource_create, name='resource_create'),
    path('resources/<int:pk>/edit/', views.resource_edit, name='resource_edit'),
    path('resources/<int:pk>/delete/', views.resource_delete, name='resource_delete'),
    path('resources/<int:pk>/toggle-active/', views.resource_toggle_active, name='resource_toggle_active'),
    path('resources/<int:pk>/toggle-featured/', views.resource_toggle_featured, name='resource_toggle_featured'),
    path('resources/categories/', views.resource_categories_list, name='resource_categories_list'),
    path('resources/categories/new/', views.resource_category_create, name='resource_category_create'),
    path('resources/categories/<int:pk>/edit/', views.resource_category_edit, name='resource_category_edit'),
    path('resources/categories/<int:pk>/delete/', views.resource_category_delete, name='resource_category_delete'),

    # ── Taxonomy ──────────────────────────────────────────────
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/new/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('api/categories/create/', views.api_category_create, name='api_category_create'),
    path('technologies/', views.technologies_list, name='technologies_list'),
    path('technologies/new/', views.technology_create, name='technology_create'),
    path('technologies/<int:pk>/edit/', views.technology_edit, name='technology_edit'),
    path('technologies/<int:pk>/delete/', views.technology_delete, name='technology_delete'),
    path('api/technologies/create/', views.api_technology_create, name='api_technology_create'),

    # ── Contacts ──────────────────────────────────────────────
    path('contacts/', views.contacts_list, name='contacts_list'),
    path('contacts/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    path('contacts/<int:pk>/mark-read/', views.contact_mark_read, name='contact_mark_read'),
    path('newsletter/', views.newsletter_list, name='newsletter_list'),
    path('newsletter/<int:pk>/delete/', views.newsletter_delete, name='newsletter_delete'),

    # ── AI ────────────────────────────────────────────────────
    path('ai/queries/', views.ai_queries_list, name='ai_queries_list'),
    path('ai/queries/<int:pk>/delete/', views.ai_query_delete, name='ai_query_delete'),
    path('ai/context/', views.ai_context_list, name='ai_context_list'),
    path('ai/context/new/', views.ai_context_create, name='ai_context_create'),
    path('ai/context/<int:pk>/edit/', views.ai_context_edit, name='ai_context_edit'),
    path('ai/context/<int:pk>/delete/', views.ai_context_delete, name='ai_context_delete'),
    path('ai/context/<int:pk>/toggle-active/', views.ai_context_toggle_active, name='ai_context_toggle_active'),

    # ── Settings ──────────────────────────────────────────────
    path('settings/site/', views.settings_site, name='settings_site'),
    path('settings/about/', views.settings_about, name='settings_about'),
    path('settings/resume/', views.settings_resume, name='settings_resume'),
    path('settings/notifications/', views.settings_notifications, name='settings_notifications'),
    path('settings/resources-config/', views.settings_resources_config, name='settings_resources_config'),
    path('settings/email-templates/', views.email_templates_list, name='email_templates_list'),
    path('settings/email-templates/new/', views.email_template_create, name='email_template_create'),
    path('settings/email-templates/<int:pk>/edit/', views.email_template_edit, name='email_template_edit'),
    path('settings/email-templates/<int:pk>/delete/', views.email_template_delete, name='email_template_delete'),
]
