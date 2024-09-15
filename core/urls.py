from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('bookings/', views.list_bookings, name='list-bookings'),  # Get all bookings
    path('bookings/create/', views.create_booking, name='create-booking'),  # Create a new booking
    path('reviews/', views.list_reviews, name='list-reviews'),  # Get all reviews
    path('reviews/top/', views.top_reviews, name='top-reviews'),  # This is the new route
    path('reviews/create/', views.create_review, name='create-review'),  # Create a new review
]
