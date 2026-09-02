"""URL configuration for the project."""

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import path


def health_check(_: HttpRequest) -> HttpResponse:
    """Return a lightweight response confirming Django is running."""
    return HttpResponse("Project Feedback is running.")


urlpatterns = [
    path("", health_check, name="health-check"),
    path("admin/", admin.site.urls),
]
