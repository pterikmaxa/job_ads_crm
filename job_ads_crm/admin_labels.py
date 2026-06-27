from cvs.models import CVProfile
from sources.models import Country, JobSite, SearchSignature
from vacancies.models import JobPost


Country._meta.verbose_name = "Страна"
Country._meta.verbose_name_plural = "Страны"

JobSite._meta.verbose_name = "Сайт вакансий"
JobSite._meta.verbose_name_plural = "Сайты вакансий"

SearchSignature._meta.verbose_name = "Поисковый запрос"
SearchSignature._meta.verbose_name_plural = "Поисковые запросы"

CVProfile._meta.verbose_name = "Профиль резюме"
CVProfile._meta.verbose_name_plural = "Профили резюме"

JobPost._meta.verbose_name = "Вакансия"
JobPost._meta.verbose_name_plural = "Вакансии"
