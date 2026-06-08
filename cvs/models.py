from django.db import models


class CVProfile(models.Model):
    title = models.CharField(max_length=150)
    country = models.ForeignKey(
        "sources.Country",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="cv_profiles",
    )
    specialization = models.CharField(max_length=150, blank=True)
    short_description = models.TextField(blank=True)
    file_path = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
