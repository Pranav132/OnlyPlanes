from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

# django urls page to create routes


urlpatterns = [
    path('', views.index, name='index'),
    path("home/", views.index, name="index"),
    path("index/", views.index, name="index"),
    path("search/", views.search, name='search'),
    path("contact/", views.contact, name="contact"),
    path("user/", views.user, name="user"),
    path('accounts/', include('allauth.urls')),
    path('hotels/', views.hotels, name="hotels"),
    path('flight_booking/', views.flight_booking, name="flight_booking"),
    path('hotel_booking/<int:hotel_id>/<int:room_id>/<str:room_name>',
         views.hotel_booking, name="hotel_booking"),
    path('hotel_search/', views.hotel_search, name="hotel_search"),
    path('hotel/<int:hotel_id>', views.eachhotel, name="eachhotel"),
    path('newreview/<int:hotel_id>', views.newreview, name="newreview"),
    path("deleteReview/<int:reviewsRatings_id>",
         views.deleteReview, name="deleteReview"),
    path('checkout/', views.checkout, name="checkout"),
    path('cancelHotelBooking/<int:hotel_id>', views.cancelHotelBooking,
         name="cancelHotelBooking"),
    path('cancelFlightBooking/<int:flightbook_id>', views.cancelFlightBooking,
         name="cancelFlightBooking"),
    path('logout', LogoutView.as_view(), name="logout"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # static media url and root to serve images uploaded through imagefield
