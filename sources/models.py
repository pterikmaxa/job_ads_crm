from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "countries"

    def __str__(self):
        return self.name


class JobSite(models.Model):
    class Status(models.TextChoices):
        PROBLEM = "problem", "Problem"
        ATTENTION = "attention", "Attention"
        OK = "ok", "OK"
        INACTIVE = "inactive", "Inactive"
        BROKEN = "broken", "Broken"

    name = models.CharField(max_length=150)
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="job_sites",
    )
    url = models.URLField(max_length=500)
    priority = models.PositiveSmallIntegerField(default=3)
    daily_plan = models.PositiveIntegerField(default=0)
    processed_today = models.PositiveIntegerField(default=0)
    color_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.INACTIVE,
    )
    comment = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["priority", "name"]

    def __str__(self):
        return self.name

    def calculate_color_status(self):
        if self.color_status == self.Status.BROKEN:
            return self.Status.BROKEN
        if self.daily_plan == 0:
            return self.Status.INACTIVE
        if self.processed_today == 0:
            return self.Status.PROBLEM
        if self.processed_today < self.daily_plan:
            return self.Status.ATTENTION
        return self.Status.OK

    def save(self, *args, **kwargs):
        self.color_status = self.calculate_color_status()
        super().save(*args, **kwargs)


class SearchSignature(models.Model):
    job_site = models.ForeignKey(
        JobSite,
        on_delete=models.CASCADE,
        related_name="search_signatures",
    )
    search_text = models.CharField(max_length=300)
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="search_signatures",
    )
    technology = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["job_site__name", "search_text"]

    def __str__(self):
        return f"{self.job_site}: {self.search_text}"
