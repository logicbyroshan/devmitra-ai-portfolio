from .models import SiteConfiguration, Resume, VideoResume

def site_context(request):
    """
    Context processor to make site configuration available to all templates.
    This ensures footer social links and other global data work across all pages.
    """
    return {
        'config': SiteConfiguration.objects.first(),
        'resume': Resume.objects.first(),
        'video_resume': VideoResume.objects.first(),
    }
