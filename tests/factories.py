"""
Test factories for creating test data.
Using factory_boy to create realistic test objects.
"""

import factory
from django.contrib.auth.models import User
from django.utils.text import slugify
from faker import Faker
from portfolio.models import (
    SiteConfiguration,
    Project,
    Category,
    Technology,
    Experience,
    Achievement,
    ContactSubmission,
    ProjectImage,
)
from blog.models import Blog
from roshan.models import AboutMeConfiguration, Resource, ResourceCategory

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating User instances."""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_staff = False
    is_active = True


class SiteConfigurationFactory(factory.django.DjangoModelFactory):
    """Factory for creating SiteConfiguration instances."""

    class Meta:
        model = SiteConfiguration
        django_get_or_create = ("hero_name",)

    hero_name = "Test Portfolio Owner"
    hero_leetcode_rating = "1800+"
    hero_opensource_contributions = "50+"
    hero_hackathons_count = "12+"
    twitter_url = "https://twitter.com/testuser"
    github_url = "https://github.com/testuser"
    linkedin_url = "https://linkedin.com/in/testuser"


class CategoryFactory(factory.django.DjangoModelFactory):
    """Factory for creating Category instances."""

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    category_type = factory.Iterator(
        Category.CategoryType.choices, getter=lambda x: x[0]
    )


class TechnologyFactory(factory.django.DjangoModelFactory):
    """Factory for creating Technology instances."""

    class Meta:
        model = Technology

    name = factory.Sequence(lambda n: f"Technology {n}")


class ProjectFactory(factory.django.DjangoModelFactory):
    """Factory for creating Project instances."""

    class Meta:
        model = Project

    title = factory.Sequence(lambda n: f"Test Project {n}")
    summary = factory.Faker("text", max_nb_chars=200)
    content = factory.Faker("text", max_nb_chars=500)
    cover_image = factory.django.FileField(filename="project_cover.jpg")
    github_url = factory.Sequence(lambda n: f"https://github.com/testuser/project-{n}")
    live_url = factory.Sequence(lambda n: f"https://project-{n}.example.com")

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)
        else:
            project_categories = CategoryFactory.create_batch(
                2, category_type=Category.CategoryType.PROJECT
            )
            for category in project_categories:
                self.categories.add(category)

    @factory.post_generation
    def technologies(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tech in extracted:
                self.technologies.add(tech)


class ProjectImageFactory(factory.django.DjangoModelFactory):
    """Factory for creating ProjectImage instances."""

    class Meta:
        model = ProjectImage

    project = factory.SubFactory(ProjectFactory)
    image = factory.django.FileField(filename="project_image.jpg")
    caption = factory.Faker("sentence", nb_words=5)


class ExperienceFactory(factory.django.DjangoModelFactory):
    """Factory for creating Experience instances."""

    class Meta:
        model = Experience

    company_name = factory.Faker("company")
    role = factory.Faker("job")
    company_url = factory.Faker("url")
    summary = factory.Faker("text", max_nb_chars=300)
    responsibilities = factory.Faker("text", max_nb_chars=500)
    achievements = factory.Faker("text", max_nb_chars=300)
    start_date = factory.Faker("date_between", start_date="-3y", end_date="today")
    end_date = factory.LazyAttribute(
        lambda obj: (
            fake.date_between(start_date=obj.start_date, end_date="today")
            if fake.boolean(chance_of_getting_true=50)
            else None
        )
    )
    experience_type = factory.SubFactory(
        "tests.factories.CategoryFactory",
        category_type=Category.CategoryType.EXPERIENCE,
    )


class AchievementFactory(factory.django.DjangoModelFactory):
    """Factory for creating Achievement instances."""

    class Meta:
        model = Achievement

    title = factory.Faker("sentence", nb_words=4)
    issuing_organization = factory.Faker("company")
    summary = factory.Faker("text", max_nb_chars=300)
    date_issued = factory.Faker("date_between", start_date="-2y", end_date="today")
    image = factory.django.FileField(filename="certificate.jpg")
    credential_url = factory.Faker("url")
    category = factory.SubFactory(
        "tests.factories.CategoryFactory",
        category_type=Category.CategoryType.ACHIEVEMENT,
    )


class ContactSubmissionFactory(factory.django.DjangoModelFactory):
    """Factory for creating ContactSubmission instances."""

    class Meta:
        model = ContactSubmission

    name = factory.Faker("name")
    email = factory.Faker("email")
    subject = factory.Faker("sentence", nb_words=5)
    message = factory.Faker("text", max_nb_chars=500)
    is_read = factory.Faker("boolean", chance_of_getting_true=30)


class BlogFactory(factory.django.DjangoModelFactory):
    """Factory for creating Blog instances."""

    class Meta:
        model = Blog

    title = factory.Sequence(lambda n: f"Test Blog Post {n}")
    summary = factory.Faker("text", max_nb_chars=200)
    content = factory.Faker("text", max_nb_chars=1000)
    cover_image = factory.django.FileField(filename="blog_cover.jpg")

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)
        else:
            blog_categories = CategoryFactory.create_batch(
                2, category_type=Category.CategoryType.BLOG
            )
            for category in blog_categories:
                self.categories.add(category)


class AboutMeConfigurationFactory(factory.django.DjangoModelFactory):
    """Factory for creating AboutMeConfiguration instances."""

    class Meta:
        model = AboutMeConfiguration
        django_get_or_create = ("intro_paragraph",)

    intro_paragraph = factory.Faker("text", max_nb_chars=300)
    location = factory.Faker("city")
    open_to_work = True
    profile_image = factory.django.FileField(filename="profile.jpg")


class ResourceCategoryFactory(factory.django.DjangoModelFactory):
    """Factory for creating ResourceCategory instances."""

    class Meta:
        model = ResourceCategory

    name = factory.Sequence(lambda n: f"ResourceCategory {n}")
    description = factory.Faker("text", max_nb_chars=200)
    icon = "fa-solid fa-folder"
    order = factory.Sequence(lambda n: n)


class ResourceFactory(factory.django.DjangoModelFactory):
    """Factory for creating Resource instances."""

    class Meta:
        model = Resource

    title = factory.Sequence(lambda n: f"Test Resource {n}")
    description = factory.Faker("text", max_nb_chars=300)
    resource_type = factory.Iterator(
        Resource.ResourceType.choices, getter=lambda x: x[0]
    )
    link = factory.Faker("url")
    is_featured = factory.Faker("boolean", chance_of_getting_true=30)
    is_active = True
    order = factory.Sequence(lambda n: n)


# Convenience functions for creating complete test scenarios


def create_complete_portfolio():
    """Create a complete portfolio setup for testing."""
    # Site configuration
    site_config = SiteConfigurationFactory()

    # Categories
    project_categories = CategoryFactory.create_batch(
        3, category_type=Category.CategoryType.PROJECT
    )
    blog_categories = CategoryFactory.create_batch(
        2, category_type=Category.CategoryType.BLOG
    )

    # Technologies
    technologies = TechnologyFactory.create_batch(8)

    # Projects with images
    projects = []
    for i in range(5):
        project = ProjectFactory(
            categories=project_categories[:2], technologies=technologies[:3]
        )
        # Add project images
        ProjectImageFactory.create_batch(3, project=project)
        projects.append(project)

    # Experience
    experiences = ExperienceFactory.create_batch(3)

    # Achievements
    achievements = AchievementFactory.create_batch(4)

    # Blog posts
    blogs = BlogFactory.create_batch(3, categories=blog_categories)

    # About me configuration
    about_me = AboutMeConfigurationFactory()

    # Resource categories and resources
    resource_categories = ResourceCategoryFactory.create_batch(2)
    resources = ResourceFactory.create_batch(len(resource_categories) * 3)

    # Contact submissions
    contacts = ContactSubmissionFactory.create_batch(5)

    return {
        "site_config": site_config,
        "categories": {
            "project": project_categories,
            "blog": blog_categories,
        },
        "technologies": technologies,
        "projects": projects,
        "experiences": experiences,
        "achievements": achievements,
        "blogs": blogs,
        "about_me": about_me,
        "resource_categories": resource_categories,
        "resources": resources,
        "contacts": contacts,
    }
