"""
Dashboard context processor — injects common variables into every
template that is rendered while the user is logged in as staff.
Only runs DB queries for authenticated staff users, so it adds no
overhead to the public-facing portfolio pages.
"""
from portfolio.models import ContactSubmission
from roshan.models import AboutMeConfiguration


def dashboard_context(request):
    if not hasattr(request, 'user') or not (request.user.is_authenticated and request.user.is_staff):
        return {}

    unread = ContactSubmission.objects.filter(is_read=False).count()

    try:
        about = AboutMeConfiguration.objects.first()
        user_avatar = about.profile_image if about and about.profile_image else None
    except Exception:
        user_avatar = None

    return {
        'unread_messages_count': unread,
        'user_avatar': user_avatar,
    }
