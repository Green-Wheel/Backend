from datetime import datetime

from api.bookings.models import Bookings
from api.bookings.serializers import BookingsEditSerializer


def get_user_bookings(user_id, order):
    bookings = Bookings.objects.filter(user_id=user_id, end_date__gt=datetime.now(), cancelled=False)
    if order == 'date':
        bookings= bookings.order_by('start_date')
    elif order == 'town':
        bookings= bookings.order_by('publication__town')
    else:
        bookings = bookings.order_by('id')

    return bookings


def get_owner_bookings(owner_id, booking_type):
    bookings = Bookings.objects.filter(publication__owner_id=owner_id)
    if booking_type == 'pending':
        bookings = bookings.filter(publication__owner_id=owner_id, confirmed=False, cancelled=False)
    elif booking_type == 'not_finished':
        bookings = bookings.filter(publication__owner_id=owner_id, end_date__gt=datetime.now(), cancelled=False)
    elif booking_type == 'finished':
        bookings = bookings.filter(publication__owner_id=owner_id, end_date__lte=datetime.now(), cancelled=False)
    elif booking_type == 'cancelled':
        bookings = bookings.filter(publication__owner_id=owner_id, cancelled=True)
    bookings = bookings.order_by('start_date')
    return bookings


def get_booking(booking_id):
    return Bookings.objects.get(id=booking_id)

def create_booking(booking):
    booking_instance = BookingsEditSerializer(data=booking)
    if booking_instance.is_valid():
        booking_instance.save()
        return Bookings.objects.latest('id')
    raise Exception(booking_instance.errors)

def cancel_booking(booking_id):
    booking_instance = Bookings.objects.get(id=booking_id)
    if booking_instance.cancelled:
        raise Exception('Booking already cancelled')
    booking_instance.cancelled = True
    booking_instance.save()
    return booking_instance

def confirm_booking(booking_id):
    booking_instance = Bookings.objects.get(id=booking_id)
    if booking_instance.confirmed:
        raise Exception('Booking already confirmed')
    if booking_instance.cancelled:
        raise Exception('Booking is cancelled, cannot confirm')
    booking_instance.confirmed = True
    booking_instance.save()
    return booking_instance