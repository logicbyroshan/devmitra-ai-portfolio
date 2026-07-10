"""
Dashboard forms for all portfolio models.
"""
from django import forms
from django.forms import inlineformset_factory
from tinymce.widgets import TinyMCE

from portfolio.models import (
    Project, ProjectImage, Experience, Achievement,
    Category, Technology, SiteConfiguration, Resume, VideoResume,
    FAQ, ContactSubmission,
)
from blog.models import Blog
from roshan.models import (
    AboutMeConfiguration, Resource, ResourceCategory, ResourcesConfiguration,
)
from ai.models import AIContext
from notifications.models import NotificationSettings, EmailTemplate
from django.utils.safestring import mark_safe

class TechnologyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        icon_url = obj.get_icon_url
        if icon_url:
            return mark_safe(f'<span style="display:inline-flex; align-items:center; gap:8px;"><img src="{icon_url}" style="width:20px; height:20px; object-fit:contain; border-radius:4px;" alt=""> {obj.name}</span>')
        return obj.name


# ─────────────────────────────────────────────
# Project Forms
# ─────────────────────────────────────────────
class ProjectForm(forms.ModelForm):
    technologies = TechnologyModelMultipleChoiceField(
        queryset=Technology.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Project
        fields = [
            'title', 'summary', 'content', 'cover_image',
            'youtube_embed_code', 'technologies', 'categories',
            'github_url', 'live_url', 'is_published',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Project title'}),
            'summary': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Short summary'}),
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'youtube_embed_code': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'YouTube iframe or URL'}),
            'github_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://github.com/...'}),
            'live_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'technologies': forms.CheckboxSelectMultiple(),
            'categories': forms.CheckboxSelectMultiple(),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Image caption (optional)'}),
        }


ProjectImageFormSet = inlineformset_factory(
    Project, ProjectImage,
    form=ProjectImageForm,
    extra=2,
    can_delete=True,
)


# ─────────────────────────────────────────────
# Blog Forms
# ─────────────────────────────────────────────
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            'title', 'summary', 'content', 'cover_image',
            'categories', 'is_published',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Blog post title'}),
            'summary': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Short excerpt'}),
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'categories': forms.CheckboxSelectMultiple(),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


# ─────────────────────────────────────────────
# Experience Forms
# ─────────────────────────────────────────────
class ExperienceForm(forms.ModelForm):
    technologies = TechnologyModelMultipleChoiceField(
        queryset=Technology.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Experience
        fields = [
            'company_name', 'company_url', 'role',
            'start_date', 'end_date', 'summary',
            'responsibilities', 'achievements',
            'technologies', 'experience_type', 'is_visible',
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-input'}),
            'company_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'role': forms.TextInput(attrs={'class': 'form-input'}),
            'start_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'summary': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'responsibilities': TinyMCE(attrs={'cols': 80, 'rows': 20}),
            'achievements': TinyMCE(attrs={'cols': 80, 'rows': 20}),
            'technologies': forms.CheckboxSelectMultiple(),
            'experience_type': forms.Select(attrs={'class': 'form-select'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


# ─────────────────────────────────────────────
# Skill Forms (backed by Technology model)
# ─────────────────────────────────────────────
class SkillForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = ['name', 'icon', 'icon_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Skill name'}),
            'icon_url': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Optional: Paste external icon URL or Markdown'}),
        }


class TechnologyForm(forms.ModelForm):
    """Used by the Taxonomy > Technologies CRUD views."""
    class Meta:
        model = Technology
        fields = ['name', 'icon', 'icon_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Technology name'}),
            'icon_url': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Optional: Paste external icon URL or Markdown'}),
        }


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'order']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-input'}),
            'answer': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
        }


# ─────────────────────────────────────────────
# Achievement Forms
# ─────────────────────────────────────────────
class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = [
            'title', 'issuing_organization', 'summary',
            'date_issued', 'credential_url', 'image',
            'category', 'is_visible',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'issuing_organization': forms.TextInput(attrs={'class': 'form-input'}),
            'summary': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'date_issued': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'credential_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


# ─────────────────────────────────────────────
# Resource Forms
# ─────────────────────────────────────────────
class ResourceForm(forms.ModelForm):
    technologies = TechnologyModelMultipleChoiceField(
        queryset=Technology.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Resource
        fields = [
            'title', 'description', 'resource_type', 'link',
            'file_upload', 'youtube_embed_id', 'vimeo_embed_id',
            'custom_embed_code', 'thumbnail', 'preview_image',
            'categories', 'technologies', 'author',
            'publication_date', 'is_featured', 'is_active',
            'order', 'personal_rating',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': TinyMCE(attrs={'cols': 80, 'rows': 15}),
            'resource_type': forms.Select(attrs={'class': 'form-select'}),
            'link': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'youtube_embed_id': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'dQw4w9WgXcQ'}),
            'vimeo_embed_id': forms.TextInput(attrs={'class': 'form-input'}),
            'custom_embed_code': TinyMCE(attrs={'cols': 80, 'rows': 8}),
            'author': forms.TextInput(attrs={'class': 'form-input'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'categories': forms.CheckboxSelectMultiple(),
            'technologies': forms.CheckboxSelectMultiple(),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'personal_rating': forms.Select(attrs={'class': 'form-select'}),
        }


class ResourceCategoryForm(forms.ModelForm):
    class Meta:
        model = ResourceCategory
        fields = ['name', 'description', 'icon', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': TinyMCE(attrs={'cols': 80, 'rows': 8}),
            'icon': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'fa-solid fa-folder'}),
            'order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
        }


# ─────────────────────────────────────────────
# Taxonomy Forms
# ─────────────────────────────────────────────
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'category_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'category_type': forms.Select(attrs={'class': 'form-select'}),
        }


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Category name'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.category_type = 'BLG'
        if commit:
            instance.save()
        return instance


# ─────────────────────────────────────────────
# AI Forms
# ─────────────────────────────────────────────
class AIContextForm(forms.ModelForm):
    class Meta:
        model = AIContext
        fields = ['title', 'content', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 8}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


# ─────────────────────────────────────────────
# Settings Forms
# ─────────────────────────────────────────────
class SiteConfigurationForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        exclude = []
        widgets = {
            f: forms.TextInput(attrs={'class': 'form-input'})
            for f in [
                'hero_name', 'hero_leetcode_rating', 'hero_opensource_contributions',
                'hero_hackathons_count', 'email', 'phone', 'location',
            ]
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.FileInput)):
                if not field.widget.attrs.get('class'):
                    field.widget.attrs['class'] = 'form-input'


class AboutMeForm(forms.ModelForm):
    class Meta:
        model = AboutMeConfiguration
        fields = [
            'page_title', 'intro_paragraph', 'profile_image',
            'detailed_description', 'birthday', 'location',
            'open_to_work', 'github_url', 'linkedin_url',
            'twitter_url', 'youtube_url', 'instagram_url',
            'website_url', 'email',
        ]
        widgets = {
            'page_title': forms.TextInput(attrs={'class': 'form-input'}),
            'intro_paragraph': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'detailed_description': TinyMCE(attrs={'cols': 80, 'rows': 15}),
            'birthday': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'open_to_work': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'github_url': forms.URLInput(attrs={'class': 'form-input'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-input'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-input'}),
            'youtube_url': forms.URLInput(attrs={'class': 'form-input'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-input'}),
            'website_url': forms.URLInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'preview_image', 'downloadable_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
        }


class VideoResumeForm(forms.ModelForm):
    class Meta:
        model = VideoResume
        fields = ['embed_code']
        widgets = {
            'embed_code': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'YouTube iframe or URL'}),
        }


class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = NotificationSettings
        exclude = ['created_at', 'updated_at']
        widgets = {
            'admin_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'from_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'reply_to_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'admin_notification_delay': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'thankyou_notification_delay': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'admin_notification_enabled': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'thankyou_notification_enabled': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'auto_mark_as_read': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['name', 'template_type', 'subject', 'html_content', 'text_content', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'template_type': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-input'}),
            'html_content': TinyMCE(attrs={'cols': 80, 'rows': 20}),
            'text_content': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 8}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class ResourcesConfigForm(forms.ModelForm):
    class Meta:
        model = ResourcesConfiguration
        fields = ['page_title', 'intro_paragraph', 'resources_description', 'resources_per_page']
        widgets = {
            'page_title': TinyMCE(attrs={'cols': 80, 'rows': 5}),
            'intro_paragraph': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'resources_description': TinyMCE(attrs={'cols': 80, 'rows': 10}),
            'resources_per_page': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
        }


# ─────────────────────────────────────────────
# Dashboard Login Form
# ─────────────────────────────────────────────
class DashboardLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'})
    )
