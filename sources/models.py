from django.db import models


class JobSite(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=50, blank=True)
    url = models.URLField(max_length=500)
    priority = models.PositiveSmallIntegerField(default=3)
    daily_plan = models.PositiveIntegerField(default=0)
    processed_today = models.PositiveIntegerField(default=0)
    color_status = models.CharField(max_length=20, default="gray")
    comment = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["priority", "name"]

    def __str__(self):
        return self.name


class SearchSignature(models.Model):
    job_site = models.ForeignKey(
        JobSite,
        on_delete=models.CASCADE,
        related_name="search_signatures",
    )
    search_text = models.CharField(max_length=300)
    country = models.CharField(max_length=50, blank=True)
    technology = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["job_site__name", "search_text"]

    def __str__(self):
        return f"{self.job_site}: {self.search_text}"
