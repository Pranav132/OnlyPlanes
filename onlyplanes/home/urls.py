from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

# django urls page to create routes


urlpatterns = [
    path('', views.index, name='index'),
    path("home/", views.index, name="index"),
    path("index/", views.index, name="index"),
    path("flight_search", views.flight_search)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # static media url and root to serve images uploaded through imagefield
