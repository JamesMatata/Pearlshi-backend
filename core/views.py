from .models import Review, Booking
from .serializers import BookingSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.conf import settings
from django.middleware.csrf import get_token
from django.http import JsonResponse


@api_view(['POST'])
def create_booking(request):
    """
    This view handles the creation of a new booking.
    """
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        # Save the booking
        serializer.save()

        # Return the response with the created booking data
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Log the validation errors to help with debugging
    print("Validation errors:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_review(request):
    """
    This view handles the submission of a review.
    It first checks if the booking is achieved and then allows the user to submit a review if it doesn't already exist.
    """
    serializer = ReviewSerializer(data=request.data)

    if serializer.is_valid():
        booking_id = serializer.validated_data['booking_id']

        # Check if the booking exists and is marked as achieved
        try:
            booking = Booking.objects.get(booking_id=booking_id)
            if not booking.is_achieved:
                return Response(
                    {"error": "The booking is not marked as achieved."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if a review already exists for this booking
        if Review.objects.filter(booking=booking).exists():
            return Response(
                {"error": "A review already exists for this booking."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If no review exists and the booking is achieved, proceed to create one
        serializer.save()  # No need to pass booking; the serializer's create method handles it
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_bookings(request):
    """
    This view returns a list of all bookings.
    """
    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def list_reviews(request):
    """
    This view returns a list of all reviews.
    """
    reviews = Review.objects.filter(is_verified=True)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def top_reviews(request):
    """
    Fetch the top 3 reviews by rating.
    """
    top_three_reviews = Review.objects.filter(is_verified=True).order_by('-rating')[:3]
    serializer = ReviewSerializer(top_three_reviews, many=True)
    return Response(serializer.data)


# CSRF Token View (Optional, if you need to fetch CSRF tokens from the API)
def get_csrf_token(request):
    """
    Return a CSRF token to be used in subsequent POST requests.
    """
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})
