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


class Company(models.Model):
    name = models.CharField("Название", max_length=250, unique=True)
    website = models.URLField("Сайт", max_length=1000, blank=True)
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name


class Lead(models.Model):
    class Language(models.TextChoices):
        UA = "UA", "Украинский"
        RU = "RU", "Русский"
        EN = "EN", "Английский"
        DE = "DE", "Немецкий"

    class Status(models.TextChoices):
        NEW = "new", "Новый"
        NEED_ACTION = "need_action", "Нужно обработать"
        CONTACTED = "contacted", "Контакт отправлен"
        WAITING = "waiting", "Жду ответа"
        RESPONSE_RECEIVED = "response_received", "Получен ответ"
        INTERVIEW = "interview", "Интервью"
        REJECTED = "rejected", "Отказ"
        CLOSED = "closed", "Закрыто"
        DUPLICATE = "duplicate", "Дубль"

    class Priority(models.IntegerChoices):
        LOW = 10, "Низкий"
        NORMAL = 20, "Обычный"
        HIGH = 30, "Высокий"
        HOT = 40, "Горячий"
        URGENT = 90, "Срочный"

    title = models.CharField("Название вакансии", max_length=250)
    company = models.ForeignKey(
        Company,
        verbose_name="Компания",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="leads",
    )
    url = models.URLField("URL объявления", max_length=1000, blank=True)
    description_text = models.TextField("Полный текст объявления", blank=True)
    language = models.CharField(
        "Язык вакансии",
        max_length=2,
        choices=Language.choices,
        blank=True,
    )
    location_text = models.CharField(
        "Место / регион / remote",
        max_length=300,
        blank=True,
    )
    priority = models.PositiveSmallIntegerField(
        "Приоритет",
        choices=Priority.choices,
        default=Priority.NORMAL,
    )
    status = models.CharField(
        "Статус",
        max_length=30,
        choices=Status.choices,
        default=Status.NEW,
    )
    technologies = models.ManyToManyField(
        "sources.SearchTechnology",
        verbose_name="Технологии",
        blank=True,
        related_name="leads",
    )
    technology_text = models.TextField(
        "Дополнительный текст по технологиям",
        blank=True,
    )
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Дата найдено", auto_now_add=True)
    updated_at = models.DateTimeField("Дата последнего действия", auto_now=True)

    class Meta:
        ordering = ["-created_at", "-priority", "title"]
        verbose_name = "Лид"
        verbose_name_plural = "Лиды"

    def __str__(self):
        return self.title


class LeadAction(models.Model):
    class ActionType(models.TextChoices):
        EMAIL = "email", "Email"
        WEBSITE = "website", "Форма на сайте"
        WHATSAPP = "whatsapp", "WhatsApp"
        VIBER = "viber", "Viber"
        PHONE = "phone", "Телефон"
        LINKEDIN = "linkedin", "LinkedIn"
        OTHER = "other", "Другое"

    class Status(models.TextChoices):
        PLANNED = "planned", "Запланировано"
        DONE = "done", "Сделано"
        FAILED = "failed", "Ошибка"
        CANCELLED = "cancelled", "Отменено"

    lead = models.ForeignKey(
        Lead,
        verbose_name="Лид",
        on_delete=models.CASCADE,
        related_name="actions",
    )
    action_type = models.CharField(
        "Тип действия",
        max_length=30,
        choices=ActionType.choices,
        default=ActionType.EMAIL,
    )
    status = models.CharField(
        "Статус действия",
        max_length=30,
        choices=Status.choices,
        default=Status.PLANNED,
    )
    planned_date = models.DateTimeField(
        "Плановая дата",
        null=True,
        blank=True,
    )
    action_date = models.DateTimeField(
        "Дата действия",
        null=True,
        blank=True,
    )
    contact_value = models.CharField(
        "Контакт / ссылка / телефон",
        max_length=500,
        blank=True,
    )
    cv_text = models.CharField(
        "Отправленное CV / профиль",
        max_length=250,
        blank=True,
    )
    message_text = models.TextField(
        "Текст сообщения / что отправлено",
        blank=True,
    )
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ["-planned_date", "-action_date", "-created_at"]
        verbose_name = "Действие по лиду"
        verbose_name_plural = "Действия по лидам"

    def __str__(self):
        return f"{self.lead} — {self.get_action_type_display()}"


class LeadResponse(models.Model):
    class Channel(models.TextChoices):
        EMAIL = "email", "Email"
        WHATSAPP = "whatsapp", "WhatsApp"
        VIBER = "viber", "Viber"
        PHONE = "phone", "Телефон"
        WEBSITE = "website", "Сайт"
        LINKEDIN = "linkedin", "LinkedIn"
        OTHER = "other", "Другое"

    class ResponseType(models.TextChoices):
        AUTO_REPLY = "auto_reply", "Автоответ"
        POSITIVE = "positive", "Положительный ответ"
        NEGATIVE = "negative", "Отказ"
        NEED_INFO = "need_info", "Запрос информации"
        INTERVIEW = "interview", "Интервью"
        NO_RESPONSE = "no_response", "Нет ответа"
        OTHER = "other", "Другое"

    lead = models.ForeignKey(
        Lead,
        verbose_name="Лид",
        on_delete=models.CASCADE,
        related_name="responses",
    )
    response_type = models.CharField(
        "Тип ответа",
        max_length=30,
        choices=ResponseType.choices,
        default=ResponseType.OTHER,
    )
    response_channel = models.CharField(
        "Канал ответа",
        max_length=30,
        choices=Channel.choices,
        default=Channel.EMAIL,
    )
    response_date = models.DateTimeField(
        "Дата ответа",
        null=True,
        blank=True,
    )
    from_value = models.CharField(
        "От кого / контакт",
        max_length=500,
        blank=True,
    )
    response_text = models.TextField("Текст ответа", blank=True)
    next_action = models.TextField("Следующее действие", blank=True)
    next_action_date = models.DateTimeField(
        "Дата следующего действия",
        null=True,
        blank=True,
    )
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ["-response_date", "-created_at"]
        verbose_name = "Ответ по лиду"
        verbose_name_plural = "Ответы по лидам"

    def __str__(self):
        return f"{self.lead} — {self.get_response_type_display()}"
