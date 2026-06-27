from django.shortcuts import get_object_or_404, render

from .models import JobPost


def jobpost_list(request):
    job_posts = (
        JobPost.objects
        .select_related("job_site", "cv_profile", "country")
        .order_by("-added_at", "title")
    )
    return render(request, "vacancies/jobpost_list.html", {"job_posts": job_posts})


def jobpost_detail(request, pk):
    job = get_object_or_404(
        JobPost.objects.select_related("job_site", "cv_profile", "country"),
        pk=pk,
    )
    return render(request, "vacancies/jobpost_detail.html", {"job": job})
