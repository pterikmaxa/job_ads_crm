from django.db import models


class JobPostStatus(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    sort_order = models.PositiveSmallIntegerField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Статус вакансии"
        verbose_name_plural = "Статусы вакансий"

    def __str__(self):
        return self.name


class JobPost(models.Model):
    job_site = models.ForeignKey(
        "sources.JobSite",
        on_delete=models.PROTECT,
        related_name="job_posts",
    )
    cv_profile = models.ForeignKey(
        "cvs.CVProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="job_posts",
    )
    url = models.URLField(max_length=1000, unique=True)
    title = models.CharField(max_length=250)
    company = models.CharField(max_length=200, blank=True)
    country = models.ForeignKey(
        "sources.Country",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="job_posts",
    )
    city = models.CharField(max_length=100, blank=True)
    source_name = models.CharField(max_length=150, blank=True)
    provider_name = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=50, default="new")
    added_at = models.DateTimeField(auto_now_add=True)
    applied_at = models.DateTimeField(null=True, blank=True)
    response_received = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-added_at", "title"]
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.title

    @property
    def status_name(self):
        status = JobPostStatus.objects.filter(code=self.status).first()
        if status:
            return status.name
        return self.status
