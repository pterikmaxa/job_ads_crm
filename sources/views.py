from django.shortcuts import render

from .models import JobSite


def jobsite_list(request):
    job_sites = (
        JobSite.objects
        .select_related("country")
        .order_by("priority", "name")
    )
    return render(request, "sources/jobsite_list.html", {"job_sites": job_sites})
