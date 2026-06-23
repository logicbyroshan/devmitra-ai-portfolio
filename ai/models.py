# ai/models.py
from django.db import models

class AIQuery(models.Model):
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query from {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name_plural = "AI Queries"
        ordering = ['-created_at']

class AIContext(models.Model):
    """
    Model to store supporting context information about Roshan Damor for AI responses
    """
    title = models.CharField(max_length=200, help_text="Title for this context piece")
    content = models.TextField(help_text="Supporting content about Roshan Damor - personal, background, approach, etc.")
    is_active = models.BooleanField(default=True, help_text="Whether to include this in AI responses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "AI Context"
        ordering = ['title']