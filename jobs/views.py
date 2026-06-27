from django.shortcuts import render

from cvs.models import CVProfile
from sources.models import Country, JobSite, SearchSignature
from vacancies.models import JobPost


def home(request):
    latest_job_posts = (
        JobPost.objects
        .select_related("job_site", "cv_profile", "country")
        .order_by("-added_at")[:10]
    )

    context = {
        "countries_count": Country.objects.count(),
        "job_sites_count": JobSite.objects.count(),
        "search_signatures_count": SearchSignature.objects.count(),
        "cv_profiles_count": CVProfile.objects.count(),
        "job_posts_count": JobPost.objects.count(),
        "latest_job_posts": latest_job_posts,
    }
    return render(request, "home.html", context)
