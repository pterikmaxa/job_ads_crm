from django.db import models


class Country(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    code = models.CharField("Код", max_length=2, unique=True)
    is_active = models.BooleanField("Активна", default=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class JobSite(models.Model):
    class Status(models.TextChoices):
        PROBLEM = "problem", "Проблема"
        ATTENTION = "attention", "Внимание"
        OK = "ok", "OK"
        INACTIVE = "inactive", "Неактивен"
        BROKEN = "broken", "Сломан"

    name = models.CharField("Название", max_length=150)
    country = models.ForeignKey(
        Country,
        verbose_name="Страна",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="job_sites",
    )
    url = models.URLField("Сайт", max_length=500)
    priority = models.PositiveSmallIntegerField("Приоритет", default=3)
    daily_plan = models.PositiveIntegerField("План в день", default=0)
    processed_today = models.PositiveIntegerField("Обработано сегодня", default=0)
    color_status = models.CharField(
        "Статус",
        max_length=20,
        choices=Status.choices,
        default=Status.INACTIVE,
    )
    comment = models.TextField("Комментарий", blank=True)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        ordering = ["priority", "name"]
        verbose_name = "Сайт вакансий"
        verbose_name_plural = "Сайты вакансий"

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


class SearchTechnology(models.Model):
    code = models.CharField("Код", max_length=50, unique=True)
    name = models.CharField("Название", max_length=100)
    sort_order = models.PositiveSmallIntegerField("Порядок", unique=True)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Технология"
        verbose_name_plural = "Технологии"

    def __str__(self):
        return self.name


class SearchSignature(models.Model):
    job_site = models.ForeignKey(
        JobSite,
        verbose_name="Сайт вакансий",
        on_delete=models.CASCADE,
        related_name="search_signatures",
    )
    search_text = models.CharField("Поисковый запрос", max_length=300)
    country = models.ForeignKey(
        Country,
        verbose_name="Страна",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="search_signatures",
    )
    technology = models.CharField("Технология", max_length=150, blank=True)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        ordering = ["job_site__name", "search_text"]
        verbose_name = "Поисковый запрос"
        verbose_name_plural = "Поисковые запросы"

    def __str__(self):
        return f"{self.job_site}: {self.search_text}"
