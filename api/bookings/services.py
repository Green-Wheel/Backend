from datetime import datetime

from api.bookings.models import Bookings
from api.bookings.serializers import BookingsEditSerializer
from api.publications.models import OccupationRanges
from api.publications.services import create_occupation, create_booking_occupation
from api.users.models import Trophies
from api.users.services import send_notification


def get_user_bookings(user_id, order, bookings_type='not_finished'):
    if bookings_type == 'not_finished':
        bookings = Bookings.objects.filter(user_id=user_id, end_date__gt=datetime.now(),
                                       status_id=1) | Bookings.objects.filter(user_id=user_id,
                                                                              end_date__gt=datetime.now(),
                                                                              status_id=2)
    elif bookings_type == 'historial':
        bookings = Bookings.objects.filter(user_id=user_id, end_date__lt=datetime.now(),
                                           status_id=2) | Bookings.objects.filter(user_id=user_id,
                                                                                  status_id__gte=3)
    else:
        bookings = Bookings.objects.filter(user_id=user_id)
    if order == 'date':
        bookings = bookings.order_by('start_date')
    elif order == 'town':
        bookings = bookings.order_by('publication__town')
    else:
        bookings = bookings.order_by('id')

    return bookings


def get_owner_bookings(owner_id, booking_type):
    bookings = Bookings.objects.filter(publication__owner_id=owner_id)
    if booking_type == 'pending':
        bookings = bookings.filter(publication__owner_id=owner_id, status_id=1).order_by('start_date')
    elif booking_type == 'not_finished':
        bookings = bookings.filter(publication__owner_id=owner_id, end_date__gt=datetime.now(),
                                   status=1) | Bookings.objects.filter(publication__owner_id=owner_id,
                                                                       end_date__gt=datetime.now(), status_id=2)
    elif booking_type == 'finished':
        bookings = bookings.filter(publication__owner_id=owner_id, end_date__lte=datetime.now(), status_id=2)
    elif booking_type == 'cancelled':
        bookings = bookings.filter(publication__owner_id=owner_id, status_id=3)

    elif booking_type == 'historial':
        bookings = bookings.filter(publication__owner_id=owner_id, end_date__lt=datetime.now(),
                                   status_id=2) | Bookings.objects.filter(publication__owner_id=owner_id,
                                                                          status_id__gte=3)
    bookings = bookings.order_by('start_date')
    return bookings


def get_booking(booking_id):
    return Bookings.objects.get(id=booking_id)

def send_booking_owner_notification(booking):
    user = booking.publication.owner.id
    title = 'Tienes una nueva reserva!'
    body = 'Tienes una nueva reserva para tu publicación ' + booking.publication.title + ' del ' + booking.start_date.strftime(
        '%d/%m/%Y') + ' al ' + booking.end_date.strftime('%d/%m/%Y')

    send_notification(user, title, body)

def send_booking_owner_cancelled_notification(booking):
    user = booking.publication.owner.id
    title = 'Una reserva ha sido cancelada'
    body = 'Tu reserva para la publicación ' + booking.publication.title + ' del ' + booking.start_date.strftime(
        '%d/%m/%Y') + ' al ' + booking.end_date.strftime('%d/%m/%Y') + ' ha sido cancelada'

    send_notification(user, title, body)

def send_booking_user_confirmation_notification(booking):
    user = booking.user.id
    if booking.status_id == 2:
        title = 'Tu reserva ha sido confirmada'
        body = 'Tu reserva para la publicación ' + booking.publication.title + ' del ' + booking.start_date.strftime(
            '%d/%m/%Y') + ' al ' + booking.end_date.strftime('%d/%m/%Y') + ' ha sido confirmada'
    else:
        title = 'Tu reserva ha sido rechazada'
        body = 'Tu reserva para la publicación ' + booking.publication.title + ' del ' + booking.start_date.strftime(
            '%d/%m/%Y') + ' al ' + booking.end_date.strftime('%d/%m/%Y') + ' ha sido rechazada'

    send_notification(user, title, body)


def set_bookings_trophies(user):
    num_bookings = Bookings.objects.filter(user_id=user.id).count()
    if num_bookings == 1:
        trophie = Trophies.objects.get(id=7)
        user.trophies.add(trophie)
    elif num_bookings == 5:
        trophie = Trophies.objects.get(id=8)
        user.trophies.add(trophie)
    elif num_bookings == 10:
        trophie = Trophies.objects.get(id=9)
        user.trophies.add(trophie)


def create_booking(booking):
    booking_instance = BookingsEditSerializer(data=booking)
    if booking_instance.is_valid():
        booking_instance.save()
        booking = Bookings.objects.latest('id')
        data = {
            "start_date": booking_instance.data["start_date"],
            "end_date": booking_instance.data["end_date"],
            "booking": booking.id
        }
        send_booking_owner_notification(booking)
        create_booking_occupation(data, booking.publication.id)
        set_bookings_trophies(booking.user)
        return booking
    raise Exception(booking_instance.errors)


def cancel_booking(booking_id):
    booking_instance = Bookings.objects.get(id=booking_id)
    if booking_instance.status_id == 3:
        raise Exception('Booking already cancelled')
    booking_instance.status_id = 3
    booking_instance.save()
    send_booking_owner_cancelled_notification(booking_instance)
    OccupationRanges.objects.filter(booking_id=booking_id).delete()
    return booking_instance


def confirm_booking(booking_id, confirmed):
    booking_instance = Bookings.objects.get(id=booking_id)
    if booking_instance.status_id != 1:
        raise Exception('Booking already confirmed, cancelled or denied')
    if confirmed:
        booking_instance.status_id = 2
    else:
        booking_instance.status_id = 4
        OccupationRanges.objects.filter(booking_id=booking_id).delete()
    booking_instance.save()
    send_booking_user_confirmation_notification(booking_instance)
    return booking_instance
