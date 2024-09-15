from django.db import models
import random
import string
from django.core.mail import send_mail
from django.conf import settings


def generate_booking_id():
    """Generates a random 8-character alphanumeric booking ID"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


class Booking(models.Model):
    booking_id = models.CharField(max_length=8, unique=True, default=generate_booking_id, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    package = models.CharField(max_length=50)
    event_name = models.CharField(max_length=100)
    guests = models.IntegerField()
    event_date = models.DateField()
    event_time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    is_achieved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.booking_id} - {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Check if the instance already exists in the database
        if self.pk:
            original = Booking.objects.get(pk=self.pk)

            # Check if is_confirmed is changing from False to True
            if not original.is_confirmed and self.is_confirmed:
                send_booking_email(self)

            # Check if is_achieved is changing from False to True
            if not original.is_achieved and self.is_achieved:
                send_review_email(self)

        # Call the original save method
        super().save(*args, **kwargs)


def send_booking_email(booking):
    """
    Send an email to the user after a booking is confirmed.
    """
    subject = 'Booking Confirmation'
    message = f"""
    Hi {booking.first_name},

    Your booking for {booking.event_name} on {booking.event_date} has been confirmed.
    Booking ID: {booking.booking_id}

    Thank you for choosing us!

    Best regards,
    Your Event Team
    """
    recipient_email = booking.email

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # From email
            [recipient_email],  # To email
            fail_silently=False,
        )
        print("Booking confirmation email sent successfully")
    except Exception as e:
        print(f"Failed to send confirmation email: {e}")


def send_review_email(booking):
    """
    Send an email to the user after the booking is marked as achieved, asking for a review and rating.
    """
    # Construct the review link with booking_id for the local server
    review_link = f"http://localhost:3000/review?booking_id={booking.booking_id}"

    subject = 'Thank you for using our services - Please leave a review!'
    message = f"""
    Hi {booking.first_name},

    We hope you enjoyed your event '{booking.event_name}' on {booking.event_date} at {booking.location}!

    We would love to hear your feedback on our services. Please take a moment to leave a review and rate your experience. Your feedback helps us improve and continue providing the best service possible.

    You can review us by clicking the link below:
    {review_link}

    Booking ID: {booking.booking_id}
    Event Name: {booking.event_name}
    Location: {booking.location}

    Thank you again for choosing us!

    Best regards,
    Your Event Team
    """
    recipient_email = booking.email

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # From email
            [recipient_email],  # To email
            fail_silently=False,
        )
        print("Review request email sent successfully")
    except Exception as e:
        print(f"Failed to send review request email: {e}")


class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)  # Link the review to a booking
    review_text = models.TextField()
    rating = models.PositiveIntegerField(default=1)  # Rating from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Review for Booking {self.booking.booking_id} - {self.rating} stars"
