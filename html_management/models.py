from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PostListTemplate(models.Model):
    name = models.CharField(max_length=100)
    template = models.TextField()
    is_active = models.BooleanField(default=False)
    activated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self) -> str:
        return self.name
