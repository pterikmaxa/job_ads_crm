from django.contrib import admin
from django.urls import path

from job_ads_crm import admin_labels  # noqa: F401
from jobs import views as jobs_views
from sources import views as sources_views
from vacancies import views as vacancies_views


admin.site.site_header = "Администрирование Django"
admin.site.site_title = "Job Ads CRM"
admin.site.index_title = "Панель управления"


urlpatterns = [
    path("", jobs_views.home, name="home"),
    path("sites/", sources_views.jobsite_list, name="jobsite_list"),
    path("vacancies/", vacancies_views.jobpost_list, name="jobpost_list"),
    path("vacancies/<int:pk>/", vacancies_views.jobpost_detail, name="jobpost_detail"),
    path("admin/", admin.site.urls),
]
