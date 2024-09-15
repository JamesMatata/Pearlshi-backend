
# Booking and Review System Overview

This application allows users to create bookings for events and provide feedback through reviews after their events are marked as "achieved." The system uses Django for the backend, with REST API endpoints for managing bookings and reviews.

## How the Review System Works

1. **Review Creation**:
   - Reviews are directly associated with a booking. A `Review` can only be created if a valid `booking_id` is provided, ensuring each booking can have at most one review.
   - When a booking is marked as "achieved" (`is_achieved` is set to `True`), an automated email is sent to the user asking for feedback. This email contains a unique link with the booking ID that directs the user to a review form.
   - The user can follow the link to provide their feedback. The link includes a query parameter `booking_id` to identify which booking the review is for, allowing the form to automatically populate the booking ID.

2. **Review Submission**:
   - Users submit their reviews through the review form, which sends a POST request to the `/api/reviews/create/` endpoint.
   - The `create_review` view validates the review data, checks if a review already exists for the booking, and if not, saves the review.
   - If the review submission is successful, it is saved in the database and can be displayed on the frontend.
   
3. **Fetching Reviews**:
   - The top 3 reviews are fetched from the backend and displayed on the home page. This is handled by the `top_reviews` endpoint, which returns the top three reviews based on their ratings.
   - Only verified reviews (`is_verified=True`) are displayed.

## What Happens During Booking

1. **Booking Creation**:
   - Users can create a booking by submitting a form, which sends a POST request to the `/api/bookings/create/` endpoint.
   - The `create_booking` view handles the request by validating and saving the booking data using the `BookingSerializer`.
   - When a booking is created, an 8-character alphanumeric `booking_id` is automatically generated using the `generate_booking_id` function.

2. **Booking Confirmation**:
   - When a booking is confirmed (i.e., `is_confirmed` is set to `True`), an automated email is sent to the user confirming the booking. This is managed in the `save` method of the `Booking` model.
   - The `send_booking_email` function constructs and sends an email with details like the event name, event date, and the booking ID.

3. **Booking Achieved**:
   - When the event associated with a booking is marked as "achieved" (i.e., `is_achieved` is set to `True`), the `send_review_email` function is triggered.
   - This function sends an email to the user, asking for their feedback. The email includes a link to the review form, with the booking ID passed as a query parameter to facilitate the review process.

## Reason for the Approach

Given the nature of catering and event planning services, it's assumed that a user may only need to make a booking once or on rare occasions. Hence, the system does not require account creation to maintain anonymity and simplicity while still allowing users to provide feedback. This approach balances privacy and user engagement by making the review process accessible without requiring a persistent user account.

## Model Relationships

- **Booking**: Represents a booking for an event, storing information such as the user's name, contact details, event details, and statuses (`is_confirmed` and `is_achieved`).
- **Review**: Represents feedback provided by the user about their event. It is linked to a `Booking` using a one-to-one relationship, ensuring each booking can have at most one review.

## API Endpoints

- **Booking Endpoints**:
  - `POST /api/bookings/create/`: Create a new booking.
  - `GET /api/bookings/`: Retrieve a list of all bookings.
  
- **Review Endpoints**:
  - `POST /api/reviews/create/`: Submit a new review.
  - `GET /api/reviews/`: Retrieve a list of verified reviews.
  - `GET /api/reviews/top/`: Retrieve the top 3 reviews by rating.

## Email Notifications

- **Booking Confirmation**: Triggered when `is_confirmed` is set to `True`. Sends an email to the user confirming their booking.
- **Review Request**: Triggered when `is_achieved` is set to `True`. Sends an email to the user asking for their feedback and providing a link to the review form.

## Setup and Usage

1. **Create a Booking**:
   - Submit a booking form with the required details.
   - The backend will generate a `booking_id` and save the booking in the database.
   - An email will be sent to the user upon booking confirmation.

2. **Leave a Review**:
   - After the event is marked as "achieved," the user receives an email with a link to leave a review.
   - The user follows the link, submits their review through the form, and the review is stored in the database.
