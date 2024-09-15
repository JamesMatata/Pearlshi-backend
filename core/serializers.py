from rest_framework import serializers
from .models import Booking, Review


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['booking_id', 'first_name', 'last_name', 'phone_number', 'email', 'package', 'event_name', 'guests',
                  'event_date', 'event_time', 'location', 'description', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)  # Include booking details in the response
    booking_id = serializers.CharField(write_only=True)  # Use this field to link the review to a booking

    class Meta:
        model = Review
        fields = ['booking', 'booking_id', 'review_text', 'rating', 'created_at']

    # Custom validation to check if the booking exists
    def validate_booking_id(self, value):
        if not Booking.objects.filter(booking_id=value).exists():
            raise serializers.ValidationError("Booking ID is not valid.")
        return value

    # Override the create method to assign the correct booking instance
    def create(self, validated_data):
        booking_id = validated_data.pop('booking_id')
        booking = Booking.objects.get(booking_id=booking_id)
        review = Review.objects.create(booking=booking, **validated_data)
        return review
