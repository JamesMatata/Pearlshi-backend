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
    It first checks if the provided booking ID is valid, then allows the user to submit a review.
    """
    serializer = ReviewSerializer(data=request.data)

    if serializer.is_valid():
        booking_id = serializer.validated_data['booking_id']
        # Check if a review already exists for this booking
        if Review.objects.filter(booking__booking_id=booking_id).exists():
            return Response(
                {"error": "A review already exists for this booking."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If no review exists, proceed to create one
        serializer.save()  # The custom `create` method in the serializer will handle linking the booking
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
